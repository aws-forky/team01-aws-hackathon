// Enhanced Interview page with structured question system
import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import EnhancedInterviewSimulator from '../components/EnhancedInterviewSimulator'
import InterviewResult from '../components/InterviewResult'
import { useApp } from '../context/AppContext'
import { questionAPI } from '../services/api'
import { MainQuestion, InterviewSession as StructuredInterviewSession } from '../types'

export default function InterviewPage() {
  const navigate = useNavigate()
  const { state } = useApp()
  
  const [mainQuestions, setMainQuestions] = useState<MainQuestion[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [interviewCompleted, setInterviewCompleted] = useState(false)
  const [completedSession, setCompletedSession] = useState<StructuredInterviewSession | null>(null)

  // 구조화된 질문 생성
  useEffect(() => {
    generateStructuredQuestions()
  }, [])

  const generateStructuredQuestions = async () => {
    if (!state.extractedText) {
      setError('포트폴리오 텍스트가 없습니다. 업로드 페이지로 돌아가주세요.')
      setIsLoading(false)
      return
    }

    try {
      setIsLoading(true)
      setError(null)
      
      const response = await questionAPI.generateMain(
        state.extractedText,
        state.selectedCompany,
        '백엔드 개발자',
        10
      )

      if (response.success && response.questions) {
        const questions: MainQuestion[] = response.questions.map((q: any) => ({
          id: q.id,
          title: q.title,
          content: q.content,
          category: q.category,
          difficulty: q.difficulty as 'Easy' | 'Medium' | 'Hard',
          estimatedTime: q.estimated_time,
          isCompleted: false
        }))
        
        setMainQuestions(questions)
      } else {
        throw new Error(response.message || '질문 생성에 실패했습니다')
      }
    } catch (error) {
      console.error('구조화된 질문 생성 실패:', error)
      setError('질문 생성 중 오류가 발생했습니다. 다시 시도해주세요.')
    } finally {
      setIsLoading(false)
    }
  }

  const handleSessionComplete = (session: StructuredInterviewSession) => {
    setCompletedSession(session)
    setInterviewCompleted(true)
  }

  const handleNewInterview = () => {
    setInterviewCompleted(false)
    setCompletedSession(null)
    setMainQuestions([])
    generateStructuredQuestions()
  }

  // 로딩 상태
  if (isLoading) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">AI가 맞춤형 면접 질문을 생성하고 있습니다</h3>
          <p className="text-gray-600">포트폴리오를 분석하여 개인화된 질문을 만들고 있어요...</p>
        </div>
      </div>
    )
  }

  // 에러 상태
  if (error) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="text-center py-12">
          <div className="bg-red-50 border border-red-200 rounded-lg p-6">
            <h3 className="text-lg font-medium text-red-900 mb-2">오류가 발생했습니다</h3>
            <p className="text-red-700 mb-4">{error}</p>
            <div className="space-x-4">
              <button
                onClick={generateStructuredQuestions}
                className="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700"
              >
                다시 시도
              </button>
              <button
                onClick={() => navigate('/upload')}
                className="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700"
              >
                업로드 페이지로
              </button>
            </div>
          </div>
        </div>
      </div>
    )
  }

  // 면접 완료 상태
  if (interviewCompleted && completedSession) {
    return (
      <InterviewResult
        session={completedSession}
        onNewInterview={handleNewInterview}
      />
    )
  }

  // 질문이 없는 경우
  if (mainQuestions.length === 0) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="text-center py-12">
          <p className="text-gray-500">질문이 생성되지 않았습니다.</p>
          <button
            onClick={() => navigate('/company')}
            className="mt-4 text-blue-600 hover:text-blue-800"
          >
            ← 회사 선택으로 돌아가기
          </button>
        </div>
      </div>
    )
  }

  // 메인 면접 시뮬레이터 렌더링
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* 헤더 */}
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          🎯 {state.selectedCompany} AI 면접 시뮬레이션
        </h1>
        <p className="text-gray-600 max-w-2xl mx-auto">
          포트폴리오 기반으로 생성된 맞춤형 질문에 답변하고, 실시간 피드백을 받아보세요.
          음성 또는 텍스트로 답변할 수 있습니다.
        </p>
      </div>

      {/* 향상된 면접 시뮬레이터 */}
      <EnhancedInterviewSimulator
        mainQuestions={mainQuestions}
        onSessionComplete={handleSessionComplete}
      />

      {/* 하단 네비게이션 */}
      <div className="mt-12 flex justify-between items-center">
        <button
          onClick={() => navigate('/company')}
          className="flex items-center space-x-2 text-gray-500 hover:text-gray-700 transition-colors"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          <span>회사 선택으로 돌아가기</span>
        </button>
        
        <div className="text-sm text-gray-500">
          💡 ESC 키를 눌러 질문 선택으로 돌아갈 수 있습니다
        </div>
      </div>
    </div>
  )
}
