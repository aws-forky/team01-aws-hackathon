import React, { useState, useEffect, useCallback } from 'react'
import { MainQuestion, FollowUpQuestionNew, Answer, InterviewSession, FeedbackAnalysis } from '../types'
import QuestionSelector from './QuestionSelector'
import InterviewProgress from './InterviewProgress'
import EnhancedAnswerInput from './EnhancedAnswerInput'
import RealTimeFeedback from './RealTimeFeedback'
import { questionAPI, evaluationAPI } from '../services/api'

interface EnhancedInterviewSimulatorProps {
  mainQuestions: MainQuestion[]
  onSessionComplete: (session: InterviewSession) => void
  className?: string
}

const EnhancedInterviewSimulator: React.FC<EnhancedInterviewSimulatorProps> = ({
  mainQuestions,
  onSessionComplete,
  className = ''
}) => {
  // 면접 세션 상태
  const [session, setSession] = useState<InterviewSession>({
    id: `session_${Date.now()}`,
    mainQuestions,
    currentMainQuestionId: null,
    followUpQuestions: [],
    completedMainQuestions: [],
    answers: [],
    startTime: new Date(),
    currentStep: 'selection',
    currentFollowUpIndex: 0
  })

  // 현재 답변 상태
  const [currentAnswer, setCurrentAnswer] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [currentFeedback, setCurrentFeedback] = useState<FeedbackAnalysis | null>(null)
  const [answerStartTime, setAnswerStartTime] = useState<Date | null>(null)

  // 현재 질문 정보
  const currentMainQuestion = session.mainQuestions.find(q => q.id === session.currentMainQuestionId)
  const currentFollowUpQuestion = session.followUpQuestions[session.currentFollowUpIndex]

  // 현재 표시할 질문 결정
  const getCurrentQuestion = () => {
    if (session.currentStep === 'main-answer' && currentMainQuestion) {
      return {
        type: 'main' as const,
        content: currentMainQuestion.content,
        title: currentMainQuestion.title
      }
    }
    if (session.currentStep === 'followup' && currentFollowUpQuestion) {
      return {
        type: 'followup' as const,
        content: currentFollowUpQuestion.content,
        title: `꼬리 질문 ${session.currentFollowUpIndex + 1}/3`
      }
    }
    return null
  }

  // 메인 질문 선택 처리
  const handleQuestionSelect = useCallback(async (question: MainQuestion) => {
    setAnswerStartTime(new Date())
    setCurrentAnswer('')
    setCurrentFeedback(null)
    
    setSession(prev => ({
      ...prev,
      currentMainQuestionId: question.id,
      currentStep: 'main-answer',
      followUpQuestions: [],
      currentFollowUpIndex: 0
    }))
  }, [])

  // 답변 제출 처리
  const handleAnswerSubmit = useCallback(async () => {
    if (!currentAnswer.trim() || isSubmitting) return

    setIsSubmitting(true)
    const answerEndTime = new Date()
    const duration = answerStartTime ? Math.floor((answerEndTime.getTime() - answerStartTime.getTime()) / 1000) : 0

    try {
      const currentQuestion = getCurrentQuestion()
      if (!currentQuestion) return

      // 답변 객체 생성
      const newAnswer: Answer = {
        id: `answer_${Date.now()}`,
        questionId: session.currentStep === 'main-answer' ? session.currentMainQuestionId! : currentFollowUpQuestion.id,
        questionType: session.currentStep === 'main-answer' ? 'main' : 'followup',
        content: currentAnswer.trim(),
        inputMethod: 'text', // TODO: 음성 입력 감지 로직 추가
        timestamp: answerEndTime,
        duration
      }

      // 답변 평가 요청
      const feedbackResponse = await evaluationAPI.evaluateAnswer(
        newAnswer.questionId,
        currentQuestion.content,
        currentAnswer.trim(),
        session.currentStep === 'main-answer' ? 'main' : 'followup',
        'text', // TODO: 음성 입력 감지 로직 추가
        {
          mainQuestion: currentMainQuestion?.content || '',
          previousAnswers: session.answers.filter(a => 
            a.questionId === session.currentMainQuestionId || 
            session.followUpQuestions.some(fq => fq.id === a.questionId && fq.parentQuestionId === session.currentMainQuestionId)
          ).map(a => a.content),
          answer_duration: duration,
          timestamp: answerEndTime.toISOString()
        }
      )

      if (feedbackResponse.success) {
        newAnswer.feedback = {
          overall_score: feedbackResponse.evaluation.overall_score,
          star_analysis: feedbackResponse.evaluation.star_analysis,
          technical_accuracy: feedbackResponse.evaluation.technical_analysis,
          improvement_suggestions: feedbackResponse.evaluation.weaknesses,
          strengths: feedbackResponse.evaluation.strengths,
          next_steps: feedbackResponse.evaluation.recommendations
        }
        setCurrentFeedback(newAnswer.feedback)
      }

      // 세션 상태 업데이트
      setSession(prev => ({
        ...prev,
        answers: [...prev.answers, newAnswer]
      }))

      // 다음 단계 결정
      if (session.currentStep === 'main-answer') {
        // 메인 질문 완료 후 꼬리 질문 생성
        await generateAndSetFollowUpQuestions(currentAnswer.trim())
      } else if (session.currentStep === 'followup') {
        // 꼬리 질문 처리
        if (session.currentFollowUpIndex < 2) {
          // 다음 꼬리 질문으로 이동
          setSession(prev => ({
            ...prev,
            currentFollowUpIndex: prev.currentFollowUpIndex + 1
          }))
          setAnswerStartTime(new Date())
        } else {
          // 모든 꼬리 질문 완료 - 메인 질문을 완료 목록에 추가
          setSession(prev => ({
            ...prev,
            completedMainQuestions: [...prev.completedMainQuestions, prev.currentMainQuestionId!],
            currentMainQuestionId: null,
            currentStep: 'selection',
            followUpQuestions: [],
            currentFollowUpIndex: 0
          }))
        }
      }

      setCurrentAnswer('')
      
    } catch (error) {
      console.error('답변 제출 중 오류:', error)
      // 에러 처리 - 사용자에게 알림
    } finally {
      setIsSubmitting(false)
    }
  }, [currentAnswer, isSubmitting, answerStartTime, session, currentMainQuestion, currentFollowUpQuestion])

  // AI 기반 개인화 꼬리 질문 생성
  const generateAndSetFollowUpQuestions = async (mainAnswer: string) => {
    try {
      if (!currentMainQuestion) return

      // 로딩 상태 표시를 위한 임시 설정
      setSession(prev => ({
        ...prev,
        currentStep: 'generating-followup',
        loadingMessage: '🤖 AI가 답변을 분석하여 개인화된 심화 질문을 생성하고 있습니다...'
      }))

      const followUpResponse = await questionAPI.generateFollowing(
        currentMainQuestion.id,
        currentMainQuestion.content,
        mainAnswer,
        {
          portfolio_text: '',  // TODO: 포트폴리오 텍스트 전달
          company_info: ''     // TODO: 회사 정보 전달
        },
        3
      )

      if (followUpResponse.success && followUpResponse.following_questions) {
        const followUpQuestions: FollowUpQuestionNew[] = followUpResponse.following_questions.map((fq: any) => ({
          id: fq.id,
          parentQuestionId: fq.parent_question_id,
          content: fq.content,
          order: fq.order,
          basedOnAnswer: fq.based_on_answer,
          aiGenerated: true  // AI 생성 표시
        }))

        setSession(prev => ({
          ...prev,
          followUpQuestions,
          currentStep: 'followup',
          currentFollowUpIndex: 0,
          loadingMessage: undefined
        }))
        
        setAnswerStartTime(new Date())
      } else {
        throw new Error('AI 서버에서 유효한 꼬리 질문을 생성하지 못했습니다.')
      }
    } catch (error) {
      console.error('AI 꼬리 질문 생성 중 오류:', error)
      
      // 사용자에게 명확한 오류 메시지 표시
      setSession(prev => ({
        ...prev,
        currentStep: 'error',
        errorMessage: `AI 기반 심화 질문 생성에 실패했습니다: ${error instanceof Error ? error.message : '알 수 없는 오류'}. 메인 질문으로 돌아가서 다시 시도해주세요.`,
        loadingMessage: undefined
      }))
    }
  }

  // 면접 완료 체크
  useEffect(() => {
    if (session.completedMainQuestions.length === session.mainQuestions.length && 
        session.mainQuestions.length > 0 && 
        session.currentStep === 'selection') {
      // 모든 질문 완료 - 결과 페이지로 이동
      onSessionComplete(session)
    }
  }, [session.completedMainQuestions.length, session.mainQuestions.length, session.currentStep, session, onSessionComplete])

  // 키보드 단축키 처리
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && session.currentStep !== 'selection') {
        // ESC 키로 질문 선택으로 돌아가기 (확인 후)
        if (window.confirm('현재 진행 중인 질문을 중단하고 질문 선택으로 돌아가시겠습니까?')) {
          setSession(prev => ({
            ...prev,
            currentStep: 'selection',
            currentMainQuestionId: null,
            followUpQuestions: [],
            currentFollowUpIndex: 0
          }))
          setCurrentAnswer('')
          setCurrentFeedback(null)
        }
      }
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [session.currentStep])

  const currentQuestion = getCurrentQuestion()

  return (
    <div className={`enhanced-interview-simulator ${className}`}>
      {/* 진행 상황 표시 */}
      <InterviewProgress session={session} className="mb-6" />

      {/* 메인 컨텐츠 */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {session.currentStep === 'selection' ? (
          // 질문 선택 화면
          <QuestionSelector
            questions={session.mainQuestions}
            completedQuestions={session.completedMainQuestions}
            onQuestionSelect={handleQuestionSelect}
          />
        ) : session.currentStep === 'generating-followup' ? (
          // AI 꼬리 질문 생성 중
          <div className="text-center py-12">
            <div className="flex flex-col items-center space-y-4">
              <div className="relative">
                <div className="w-16 h-16 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin"></div>
                <div className="absolute inset-0 flex items-center justify-center">
                  <span className="text-2xl">🤖</span>
                </div>
              </div>
              <div className="max-w-md text-center">
                <h3 className="text-lg font-semibold text-gray-900 mb-2">AI가 심화 질문을 생성하고 있습니다</h3>
                <p className="text-gray-600 mb-4">{(session as any).loadingMessage || '답변 내용을 바탕으로 개인화된 꼬리 질문을 만들고 있습니다...'}</p>
                <div className="text-sm text-blue-600">
                  💡 잠시만 기다려주세요. AI가 최적의 심화 질문을 선별하고 있습니다.
                </div>
              </div>
            </div>
          </div>
        ) : session.currentStep === 'error' ? (
          // 오류 화면
          <div className="text-center py-12">
            <div className="flex flex-col items-center space-y-4">
              <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center">
                <span className="text-2xl">⚠️</span>
              </div>
              <div className="max-w-md text-center">
                <h3 className="text-lg font-semibold text-red-900 mb-2">AI 서비스 오류</h3>
                <p className="text-red-700 mb-4">{(session as any).errorMessage || 'AI 기반 기능에서 오류가 발생했습니다.'}</p>
                <div className="space-x-3">
                  <button
                    onClick={() => setSession(prev => ({
                      ...prev,
                      currentStep: 'selection',
                      currentMainQuestionId: null,
                      followUpQuestions: [],
                      currentFollowUpIndex: 0,
                      errorMessage: undefined
                    }))}
                    className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
                  >
                    질문 선택으로 돌아가기
                  </button>
                  <button
                    onClick={() => window.location.reload()}
                    className="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700 transition-colors"
                  >
                    페이지 새로고침
                  </button>
                </div>
              </div>
            </div>
          </div>
        ) : (
          // 질문 답변 화면
          <div className="space-y-6">
            {/* 현재 질문 표시 */}
            {currentQuestion && (
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-2">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                        currentQuestion.type === 'main' 
                          ? 'bg-blue-100 text-blue-800' 
                          : 'bg-purple-100 text-purple-800'
                      }`}>
                        {currentQuestion.type === 'main' ? '메인 질문' : currentQuestion.title}
                      </span>
                      {currentQuestion.type === 'followup' && (currentFollowUpQuestion as any)?.aiGenerated && (
                        <span className="px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                          🤖 AI 개인화
                        </span>
                      )}
                      {currentMainQuestion && (
                        <span className="px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-700">
                          {currentMainQuestion.category}
                        </span>
                      )}
                    </div>
                    <h2 className="text-xl font-semibold text-gray-900 mb-2">
                      {currentQuestion.content}
                    </h2>
                    {currentQuestion.type === 'followup' && (currentFollowUpQuestion as any)?.aiGenerated && (
                      <div className="text-sm text-green-700 bg-green-50 rounded-md p-2 mb-2">
                        💡 이 질문은 AI가 당신의 답변을 분석하여 생성한 개인화된 심화 질문입니다.
                      </div>
                    )}
                    {currentQuestion.type === 'main' && currentMainQuestion && (
                      <p className="text-sm text-gray-600">
                        예상 답변 시간: {currentMainQuestion.estimatedTime}분 • 난이도: {currentMainQuestion.difficulty}
                      </p>
                    )}
                  </div>
                  
                  {/* 질문 선택으로 돌아가기 버튼 */}
                  <button
                    type="button"
                    onClick={() => {
                      if (window.confirm('현재 진행 중인 질문을 중단하고 질문 선택으로 돌아가시겠습니까?')) {
                        setSession(prev => ({
                          ...prev,
                          currentStep: 'selection',
                          currentMainQuestionId: null,
                          followUpQuestions: [],
                          currentFollowUpIndex: 0
                        }))
                        setCurrentAnswer('')
                        setCurrentFeedback(null)
                      }
                    }}
                    className="px-3 py-1 text-sm text-gray-600 hover:text-gray-800 border border-gray-300 rounded-md hover:bg-gray-50 transition-colors duration-200"
                  >
                    질문 선택으로 돌아가기
                  </button>
                </div>

                {/* 답변 입력 */}
                <EnhancedAnswerInput
                  value={currentAnswer}
                  onChange={setCurrentAnswer}
                  onSubmit={handleAnswerSubmit}
                  disabled={isSubmitting}
                  placeholder={`${currentQuestion.type === 'main' ? '메인' : '꼬리'} 질문에 대한 답변을 입력하세요...`}
                  className="mb-4"
                />

                {/* 제출 상태 표시 */}
                {isSubmitting && (
                  <div className="flex items-center justify-center py-4">
                    <div className="flex items-center space-x-2 text-blue-600">
                      <svg className="animate-spin w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                      </svg>
                      <span>답변을 분석하고 있습니다...</span>
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* 실시간 피드백 표시 */}
            {currentFeedback && (
              <RealTimeFeedback 
                feedback={currentFeedback}
                className="mb-6"
              />
            )}

            {/* 이전 답변들 요약 (꼬리 질문 진행 중일 때) */}
            {session.currentStep === 'followup' && session.currentFollowUpIndex > 0 && (
              <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
                <h3 className="font-medium text-gray-900 mb-3">이전 답변 요약</h3>
                <div className="space-y-2">
                  {session.answers
                    .filter(a => 
                      a.questionId === session.currentMainQuestionId || 
                      session.followUpQuestions.some(fq => fq.id === a.questionId && fq.parentQuestionId === session.currentMainQuestionId)
                    )
                    .slice(-2) // 최근 2개 답변만 표시
                    .map((answer, index) => (
                      <div key={answer.id} className="text-sm">
                        <span className="font-medium text-gray-700">
                          {answer.questionType === 'main' ? '메인 답변' : `꼬리 답변 ${index}`}:
                        </span>
                        <span className="text-gray-600 ml-2">
                          {answer.content.length > 100 ? `${answer.content.substring(0, 100)}...` : answer.content}
                        </span>
                      </div>
                    ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* 도움말 및 단축키 안내 */}
      <div className="fixed bottom-4 right-4 bg-white rounded-lg shadow-lg border border-gray-200 p-3 max-w-xs">
        <div className="text-xs text-gray-600">
          <div className="font-medium mb-1">💡 도움말</div>
          <ul className="space-y-1">
            <li>• Ctrl+Enter: 답변 제출</li>
            <li>• ESC: 질문 선택으로 돌아가기</li>
            <li>• 음성/텍스트 입력 전환 가능</li>
          </ul>
        </div>
      </div>
    </div>
  )
}

export default EnhancedInterviewSimulator