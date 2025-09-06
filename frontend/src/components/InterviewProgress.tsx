import React from 'react'
import { MainQuestion, FollowUpQuestionNew, InterviewSession } from '../types'

interface InterviewProgressProps {
  session: InterviewSession
  className?: string
}

const InterviewProgress: React.FC<InterviewProgressProps> = ({
  session,
  className = ''
}) => {
  const {
    mainQuestions,
    currentMainQuestionId,
    completedMainQuestions,
    currentStep,
    currentFollowUpIndex,
    startTime
  } = session

  // 현재 선택된 메인 질문
  const currentMainQuestion = mainQuestions.find(q => q.id === currentMainQuestionId)

  // 전체 진행률 계산
  const totalProgress = (completedMainQuestions.length / mainQuestions.length) * 100

  // 현재 질문 내 진행률 계산 (메인 + 꼬리 질문)
  const getCurrentQuestionProgress = () => {
    if (currentStep === 'selection') return 0
    if (currentStep === 'main-answer') return 25
    if (currentStep === 'followup') {
      return 25 + ((currentFollowUpIndex + 1) / 3) * 75
    }
    return 100
  }

  // 경과 시간 계산
  const getElapsedTime = () => {
    const now = new Date()
    const elapsed = Math.floor((now.getTime() - startTime.getTime()) / 1000)
    const minutes = Math.floor(elapsed / 60)
    const seconds = elapsed % 60
    return `${minutes}:${seconds.toString().padStart(2, '0')}`
  }

  // 예상 남은 시간 계산
  const getEstimatedRemainingTime = () => {
    const remainingQuestions = mainQuestions.length - completedMainQuestions.length
    const avgTimePerQuestion = 5 // 메인 질문당 평균 5분 (메인 + 꼬리 질문 포함)
    const estimatedMinutes = remainingQuestions * avgTimePerQuestion
    
    if (currentStep !== 'selection' && currentMainQuestion) {
      // 현재 질문의 남은 시간 추가
      const currentQuestionRemaining = currentMainQuestion.estimatedTime * (1 - getCurrentQuestionProgress() / 100)
      return Math.ceil(estimatedMinutes + currentQuestionRemaining)
    }
    
    return estimatedMinutes
  }

  return (
    <div className={`interview-progress bg-white border-b border-gray-200 ${className}`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        {/* 상단 정보 바 */}
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-6">
            {/* 전체 진행률 */}
            <div className="flex items-center space-x-2">
              <span className="text-sm font-medium text-gray-700">전체 진행률:</span>
              <div className="flex items-center space-x-2">
                <div className="w-24 bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${totalProgress}%` }}
                  />
                </div>
                <span className="text-sm text-gray-600 min-w-[3rem]">
                  {Math.round(totalProgress)}%
                </span>
              </div>
            </div>

            {/* 완료된 질문 수 */}
            <div className="flex items-center space-x-2">
              <svg className="w-4 h-4 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span className="text-sm text-gray-700">
                {completedMainQuestions.length}/{mainQuestions.length} 완료
              </span>
            </div>
          </div>

          {/* 시간 정보 */}
          <div className="flex items-center space-x-6">
            <div className="flex items-center space-x-2">
              <svg className="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span className="text-sm text-gray-600">
                경과: {getElapsedTime()}
              </span>
            </div>
            <div className="flex items-center space-x-2">
              <svg className="w-4 h-4 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              <span className="text-sm text-blue-600">
                예상 남은 시간: {getEstimatedRemainingTime()}분
              </span>
            </div>
          </div>
        </div>

        {/* 현재 단계 표시 */}
        {currentStep !== 'selection' && currentMainQuestion && (
          <div className="bg-blue-50 rounded-lg p-4 border border-blue-200">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center space-x-3">
                <div className="flex items-center space-x-2">
                  <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white text-sm font-medium">
                    {completedMainQuestions.length + 1}
                  </div>
                  <div>
                    <h3 className="font-medium text-gray-900">{currentMainQuestion.title}</h3>
                    <p className="text-sm text-gray-600">{currentMainQuestion.category} • {currentMainQuestion.difficulty}</p>
                  </div>
                </div>
              </div>

              {/* 현재 질문 진행률 */}
              <div className="flex items-center space-x-2">
                <span className="text-sm text-gray-600">질문 진행률:</span>
                <div className="w-20 bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${getCurrentQuestionProgress()}%` }}
                  />
                </div>
                <span className="text-sm text-gray-600 min-w-[3rem]">
                  {Math.round(getCurrentQuestionProgress())}%
                </span>
              </div>
            </div>

            {/* 단계별 진행 상황 */}
            <div className="flex items-center space-x-4">
              {/* 메인 질문 */}
              <div className={`flex items-center space-x-2 ${
                currentStep === 'main-answer' ? 'text-blue-600' : 
                currentStep === 'followup' || currentStep === 'completed' ? 'text-green-600' : 'text-gray-400'
              }`}>
                <div className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-medium ${
                  currentStep === 'main-answer' ? 'bg-blue-600 text-white' :
                  currentStep === 'followup' || currentStep === 'completed' ? 'bg-green-600 text-white' : 'bg-gray-300 text-gray-600'
                }`}>
                  {currentStep === 'followup' || currentStep === 'completed' ? '✓' : '1'}
                </div>
                <span className="text-sm font-medium">메인 질문</span>
              </div>

              {/* 연결선 */}
              <div className={`flex-1 h-0.5 ${
                currentStep === 'followup' || currentStep === 'completed' ? 'bg-green-600' : 'bg-gray-300'
              }`} />

              {/* 꼬리 질문들 */}
              {[1, 2, 3].map((num) => (
                <React.Fragment key={num}>
                  <div className={`flex items-center space-x-2 ${
                    currentStep === 'followup' && currentFollowUpIndex + 1 === num ? 'text-blue-600' :
                    currentStep === 'followup' && currentFollowUpIndex + 1 > num ? 'text-green-600' :
                    currentStep === 'completed' ? 'text-green-600' : 'text-gray-400'
                  }`}>
                    <div className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-medium ${
                      currentStep === 'followup' && currentFollowUpIndex + 1 === num ? 'bg-blue-600 text-white' :
                      (currentStep === 'followup' && currentFollowUpIndex + 1 > num) || currentStep === 'completed' ? 'bg-green-600 text-white' : 'bg-gray-300 text-gray-600'
                    }`}>
                      {((currentStep === 'followup' && currentFollowUpIndex + 1 > num) || currentStep === 'completed') ? '✓' : num + 1}
                    </div>
                    <span className="text-sm font-medium">꼬리 {num}</span>
                  </div>
                  {num < 3 && (
                    <div className={`flex-1 h-0.5 ${
                      (currentStep === 'followup' && currentFollowUpIndex + 1 > num) || currentStep === 'completed' ? 'bg-green-600' : 'bg-gray-300'
                    }`} />
                  )}
                </React.Fragment>
              ))}
            </div>

            {/* 현재 단계 설명 */}
            <div className="mt-3 text-sm text-gray-600">
              {currentStep === 'main-answer' && '메인 질문에 답변해주세요.'}
              {currentStep === 'followup' && `꼬리 질문 ${currentFollowUpIndex + 1}/3에 답변해주세요.`}
              {currentStep === 'completed' && '이 질문의 모든 답변이 완료되었습니다.'}
            </div>
          </div>
        )}

        {/* 선택 단계일 때의 안내 */}
        {currentStep === 'selection' && (
          <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
            <div className="flex items-center space-x-3">
              <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
              <div>
                <h3 className="font-medium text-gray-900">질문을 선택해주세요</h3>
                <p className="text-sm text-gray-600">
                  아래에서 면접 질문을 선택하면 메인 질문과 3개의 꼬리 질문으로 구성된 면접이 시작됩니다.
                </p>
              </div>
            </div>
          </div>
        )}

        {/* 완료 단계일 때의 축하 메시지 */}
        {currentStep === 'completed' && completedMainQuestions.length === mainQuestions.length && (
          <div className="bg-green-50 rounded-lg p-4 border border-green-200">
            <div className="flex items-center space-x-3">
              <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <div>
                <h3 className="font-medium text-green-900">🎉 면접이 완료되었습니다!</h3>
                <p className="text-sm text-green-800">
                  모든 질문에 답변을 완료했습니다. 결과 페이지에서 상세한 피드백을 확인하세요.
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default InterviewProgress