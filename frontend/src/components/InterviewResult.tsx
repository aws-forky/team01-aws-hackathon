import React, { useState, useEffect } from 'react'
import { InterviewSession, InterviewReport, MainQuestion, Answer } from '../types'
import PDFGenerator from './PDFGenerator'

interface InterviewResultProps {
  session: InterviewSession
  onNewInterview: () => void
  className?: string
}

const InterviewResult: React.FC<InterviewResultProps> = ({
  session,
  onNewInterview,
  className = ''
}) => {
  const [report, setReport] = useState<InterviewReport | null>(null)
  const [expandedQuestions, setExpandedQuestions] = useState<Set<string>>(new Set())
  const [isGeneratingPDF, setIsGeneratingPDF] = useState(false)

  // 결과 분석 및 리포트 생성
  useEffect(() => {
    generateReport()
  }, [session])

  const generateReport = () => {
    const now = new Date()
    const totalDuration = Math.floor((now.getTime() - session.startTime.getTime()) / 1000 / 60) // 분 단위

    // 카테고리별 점수 계산
    const categoryScores: Record<string, { total: number; count: number }> = {}
    let totalScore = 0
    let scoreCount = 0

    session.answers.forEach(answer => {
      if (answer.feedback?.overall_score) {
        const question = session.mainQuestions.find(q => q.id === answer.questionId) ||
                        session.followUpQuestions.find(q => q.id === answer.questionId)
        
        if (question && 'category' in question) {
          const category = question.category
          if (!categoryScores[category]) {
            categoryScores[category] = { total: 0, count: 0 }
          }
          categoryScores[category].total += answer.feedback.overall_score
          categoryScores[category].count += 1
        }

        totalScore += answer.feedback.overall_score
        scoreCount += 1
      }
    })

    const averageScore = scoreCount > 0 ? Math.round(totalScore / scoreCount) : 0
    const finalCategoryScores: Record<string, number> = {}
    
    Object.entries(categoryScores).forEach(([category, data]) => {
      finalCategoryScores[category] = Math.round(data.total / data.count)
    })

    // 강점과 약점 분석
    const allStrengths: string[] = []
    const allWeaknesses: string[] = []
    const allRecommendations: string[] = []

    session.answers.forEach(answer => {
      if (answer.feedback) {
        allStrengths.push(...answer.feedback.strengths)
        allWeaknesses.push(...answer.feedback.improvement_suggestions)
        allRecommendations.push(...answer.feedback.next_steps)
      }
    })

    // 중복 제거 및 상위 항목 선별
    const uniqueStrengths = [...new Set(allStrengths)].slice(0, 5)
    const uniqueWeaknesses = [...new Set(allWeaknesses)].slice(0, 5)
    const uniqueRecommendations = [...new Set(allRecommendations)].slice(0, 5)

    // 상세 결과 구성
    const detailedResults = session.mainQuestions
      .filter(mq => session.completedMainQuestions.includes(mq.id))
      .map(mainQuestion => {
        const mainAnswer = session.answers.find(a => a.questionId === mainQuestion.id && a.questionType === 'main')
        const followUpResults = session.followUpQuestions
          .filter(fq => fq.parentQuestionId === mainQuestion.id)
          .map(followUpQuestion => {
            const answer = session.answers.find(a => a.questionId === followUpQuestion.id && a.questionType === 'followup')
            return {
              question: followUpQuestion,
              answer: answer!
            }
          })
          .filter(result => result.answer)

        return {
          mainQuestion,
          mainAnswer: mainAnswer!,
          followUpResults
        }
      })
      .filter(result => result.mainAnswer)

    const newReport: InterviewReport = {
      sessionId: session.id,
      completedAt: now,
      totalDuration,
      totalQuestions: session.answers.length,
      averageScore,
      categoryScores: finalCategoryScores,
      strengths: uniqueStrengths,
      weaknesses: uniqueWeaknesses,
      recommendations: uniqueRecommendations,
      detailedResults
    }

    setReport(newReport)
  }

  // 질문 상세 내용 토글
  const toggleQuestionExpansion = (questionId: string) => {
    setExpandedQuestions(prev => {
      const newSet = new Set(prev)
      if (newSet.has(questionId)) {
        newSet.delete(questionId)
      } else {
        newSet.add(questionId)
      }
      return newSet
    })
  }

  // 점수에 따른 색상 반환
  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600'
    if (score >= 60) return 'text-yellow-600'
    return 'text-red-600'
  }

  // 점수에 따른 배경색 반환
  const getScoreBgColor = (score: number) => {
    if (score >= 80) return 'bg-green-100'
    if (score >= 60) return 'bg-yellow-100'
    return 'bg-red-100'
  }

  if (!report) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full mx-auto mb-4"></div>
          <p className="text-gray-600">결과를 분석하고 있습니다...</p>
        </div>
      </div>
    )
  }

  return (
    <div className={`interview-result ${className}`}>
      {/* 헤더 */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white py-8">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-3xl font-bold mb-2">🎉 면접 완료!</h1>
            <p className="text-blue-100">
              총 {report.totalQuestions}개 질문에 답변하셨습니다. 수고하셨습니다!
            </p>
          </div>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* 전체 요약 카드 */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">📊 면접 요약</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            {/* 전체 점수 */}
            <div className="text-center">
              <div className={`text-3xl font-bold mb-2 ${getScoreColor(report.averageScore)}`}>
                {report.averageScore}점
              </div>
              <div className="text-sm text-gray-600">전체 평균 점수</div>
            </div>

            {/* 소요 시간 */}
            <div className="text-center">
              <div className="text-3xl font-bold text-blue-600 mb-2">
                {report.totalDuration}분
              </div>
              <div className="text-sm text-gray-600">총 소요 시간</div>
            </div>

            {/* 답변 질문 수 */}
            <div className="text-center">
              <div className="text-3xl font-bold text-purple-600 mb-2">
                {report.totalQuestions}개
              </div>
              <div className="text-sm text-gray-600">답변한 질문</div>
            </div>

            {/* 평균 답변 시간 */}
            <div className="text-center">
              <div className="text-3xl font-bold text-green-600 mb-2">
                {Math.round(report.totalDuration / report.totalQuestions * 10) / 10}분
              </div>
              <div className="text-sm text-gray-600">질문당 평균 시간</div>
            </div>
          </div>
        </div>

        {/* 카테고리별 점수 */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">📈 카테고리별 성과</h2>
          
          <div className="space-y-4">
            {Object.entries(report.categoryScores).map(([category, score]) => (
              <div key={category} className="flex items-center justify-between">
                <span className="font-medium text-gray-700">{category}</span>
                <div className="flex items-center space-x-3">
                  <div className="w-32 bg-gray-200 rounded-full h-2">
                    <div 
                      className={`h-2 rounded-full ${score >= 80 ? 'bg-green-500' : score >= 60 ? 'bg-yellow-500' : 'bg-red-500'}`}
                      style={{ width: `${score}%` }}
                    />
                  </div>
                  <span className={`font-semibold ${getScoreColor(score)}`}>
                    {score}점
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* 강점 및 약점 분석 */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* 강점 */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-green-700 mb-4 flex items-center">
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              잘한 점
            </h3>
            <ul className="space-y-2">
              {report.strengths.map((strength, index) => (
                <li key={index} className="flex items-start space-x-2">
                  <span className="text-green-500 mt-1">•</span>
                  <span className="text-gray-700 text-sm">{strength}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* 개선점 */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-orange-700 mb-4 flex items-center">
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
              개선이 필요한 점
            </h3>
            <ul className="space-y-2">
              {report.weaknesses.map((weakness, index) => (
                <li key={index} className="flex items-start space-x-2">
                  <span className="text-orange-500 mt-1">•</span>
                  <span className="text-gray-700 text-sm">{weakness}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* 추천 학습 방향 */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
          <h3 className="text-lg font-semibold text-blue-700 mb-4 flex items-center">
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
            추천 학습 방향
          </h3>
          <ul className="space-y-2">
            {report.recommendations.map((recommendation, index) => (
              <li key={index} className="flex items-start space-x-2">
                <span className="text-blue-500 mt-1">•</span>
                <span className="text-gray-700 text-sm">{recommendation}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* 상세 질문별 결과 */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">📝 상세 질문별 결과</h2>
          
          <div className="space-y-4">
            {report.detailedResults.map((result, index) => (
              <div key={result.mainQuestion.id} className="border border-gray-200 rounded-lg">
                {/* 메인 질문 헤더 */}
                <button
                  type="button"
                  onClick={() => toggleQuestionExpansion(result.mainQuestion.id)}
                  className="w-full px-4 py-3 text-left hover:bg-gray-50 transition-colors duration-200"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <span className="flex-shrink-0 w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-medium">
                        {index + 1}
                      </span>
                      <div>
                        <h3 className="font-medium text-gray-900">{result.mainQuestion.title}</h3>
                        <p className="text-sm text-gray-600">{result.mainQuestion.category} • {result.mainQuestion.difficulty}</p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      {result.mainAnswer.feedback && (
                        <span className={`px-2 py-1 rounded-full text-sm font-medium ${getScoreBgColor(result.mainAnswer.feedback.overall_score)} ${getScoreColor(result.mainAnswer.feedback.overall_score)}`}>
                          {result.mainAnswer.feedback.overall_score}점
                        </span>
                      )}
                      <svg 
                        className={`w-5 h-5 text-gray-400 transition-transform duration-200 ${expandedQuestions.has(result.mainQuestion.id) ? 'rotate-180' : ''}`} 
                        fill="none" 
                        stroke="currentColor" 
                        viewBox="0 0 24 24"
                      >
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                      </svg>
                    </div>
                  </div>
                </button>

                {/* 상세 내용 */}
                {expandedQuestions.has(result.mainQuestion.id) && (
                  <div className="px-4 pb-4 border-t border-gray-200">
                    {/* 메인 질문 및 답변 */}
                    <div className="mb-4">
                      <h4 className="font-medium text-gray-900 mb-2">질문</h4>
                      <p className="text-gray-700 text-sm mb-3">{result.mainQuestion.content}</p>
                      
                      <h4 className="font-medium text-gray-900 mb-2">답변</h4>
                      <p className="text-gray-700 text-sm mb-3 bg-gray-50 p-3 rounded">{result.mainAnswer.content}</p>
                      
                      {result.mainAnswer.feedback && (
                        <div className="mb-4">
                          <h4 className="font-medium text-gray-900 mb-2">피드백</h4>
                          <div className="bg-blue-50 p-3 rounded text-sm">
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                              <div>
                                <span className="font-medium text-blue-900">강점:</span>
                                <ul className="mt-1 space-y-1">
                                  {result.mainAnswer.feedback.strengths.slice(0, 3).map((strength, i) => (
                                    <li key={i} className="text-blue-800">• {strength}</li>
                                  ))}
                                </ul>
                              </div>
                              <div>
                                <span className="font-medium text-blue-900">개선점:</span>
                                <ul className="mt-1 space-y-1">
                                  {result.mainAnswer.feedback.improvement_suggestions.slice(0, 3).map((suggestion, i) => (
                                    <li key={i} className="text-blue-800">• {suggestion}</li>
                                  ))}
                                </ul>
                              </div>
                            </div>
                          </div>
                        </div>
                      )}
                    </div>

                    {/* 꼬리 질문들 */}
                    {result.followUpResults.length > 0 && (
                      <div>
                        <h4 className="font-medium text-gray-900 mb-3">꼬리 질문들</h4>
                        <div className="space-y-3">
                          {result.followUpResults.map((followUp, followUpIndex) => (
                            <div key={followUp.question.id} className="bg-gray-50 p-3 rounded">
                              <div className="flex items-start space-x-2 mb-2">
                                <span className="flex-shrink-0 w-6 h-6 bg-purple-600 text-white rounded-full flex items-center justify-center text-xs font-medium">
                                  {followUpIndex + 1}
                                </span>
                                <div className="flex-1">
                                  <p className="text-sm text-gray-900 font-medium mb-1">{followUp.question.content}</p>
                                  <p className="text-sm text-gray-700 mb-2">{followUp.answer.content}</p>
                                  {followUp.answer.feedback && (
                                    <div className="flex items-center space-x-2">
                                      <span className={`px-2 py-1 rounded text-xs font-medium ${getScoreBgColor(followUp.answer.feedback.overall_score)} ${getScoreColor(followUp.answer.feedback.overall_score)}`}>
                                        {followUp.answer.feedback.overall_score}점
                                      </span>
                                      <span className="text-xs text-gray-500">
                                        답변 시간: {followUp.answer.duration}초
                                      </span>
                                    </div>
                                  )}
                                </div>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* 액션 버튼들 */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <PDFGenerator
            report={report}
            onGenerateStart={() => setIsGeneratingPDF(true)}
            onGenerateComplete={() => setIsGeneratingPDF(false)}
            disabled={isGeneratingPDF}
          />
          
          <button
            type="button"
            onClick={onNewInterview}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors duration-200 flex items-center justify-center space-x-2"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            <span>새로운 면접 시작</span>
          </button>

          <button
            type="button"
            onClick={() => window.print()}
            className="px-6 py-3 bg-gray-600 text-white rounded-lg font-medium hover:bg-gray-700 transition-colors duration-200 flex items-center justify-center space-x-2"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
            </svg>
            <span>인쇄하기</span>
          </button>
        </div>
      </div>
    </div>
  )
}

export default InterviewResult