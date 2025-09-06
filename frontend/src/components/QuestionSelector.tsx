import React from 'react'
import { MainQuestion } from '../types'

interface QuestionSelectorProps {
  questions: MainQuestion[]
  completedQuestions: string[]
  onQuestionSelect: (question: MainQuestion) => void
  className?: string
}

const QuestionSelector: React.FC<QuestionSelectorProps> = ({
  questions,
  completedQuestions,
  onQuestionSelect,
  className = ''
}) => {
  // 카테고리별 색상 매핑
  const getCategoryColor = (category: string): string => {
    const colors: Record<string, string> = {
      'React': 'bg-blue-100 text-blue-800 border-blue-200',
      'JavaScript': 'bg-yellow-100 text-yellow-800 border-yellow-200',
      'TypeScript': 'bg-indigo-100 text-indigo-800 border-indigo-200',
      'Node.js': 'bg-green-100 text-green-800 border-green-200',
      'Database': 'bg-purple-100 text-purple-800 border-purple-200',
      'Algorithm': 'bg-red-100 text-red-800 border-red-200',
      'System Design': 'bg-gray-100 text-gray-800 border-gray-200',
      'DevOps': 'bg-orange-100 text-orange-800 border-orange-200',
      'Testing': 'bg-pink-100 text-pink-800 border-pink-200',
      'Performance': 'bg-teal-100 text-teal-800 border-teal-200'
    }
    return colors[category] || 'bg-gray-100 text-gray-800 border-gray-200'
  }

  // 난이도별 아이콘 및 색상
  const getDifficultyInfo = (difficulty: 'Easy' | 'Medium' | 'Hard') => {
    switch (difficulty) {
      case 'Easy':
        return {
          icon: '⭐',
          color: 'text-green-600',
          bgColor: 'bg-green-50',
          label: '쉬움'
        }
      case 'Medium':
        return {
          icon: '⭐⭐',
          color: 'text-yellow-600',
          bgColor: 'bg-yellow-50',
          label: '보통'
        }
      case 'Hard':
        return {
          icon: '⭐⭐⭐',
          color: 'text-red-600',
          bgColor: 'bg-red-50',
          label: '어려움'
        }
    }
  }

  // 진행률 계산
  const progressPercentage = (completedQuestions.length / questions.length) * 100

  return (
    <div className={`question-selector ${className}`}>
      {/* 헤더 및 진행률 */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-2xl font-bold text-gray-900">
            면접 질문 선택
          </h2>
          <div className="text-sm text-gray-600">
            {completedQuestions.length}/{questions.length} 완료
          </div>
        </div>

        {/* 진행률 바 */}
        <div className="w-full bg-gray-200 rounded-full h-2 mb-2">
          <div 
            className="bg-blue-600 h-2 rounded-full transition-all duration-300"
            style={{ width: `${progressPercentage}%` }}
          />
        </div>
        <p className="text-sm text-gray-600">
          원하는 질문을 선택하여 면접을 진행하세요. 각 질문마다 3개의 꼬리 질문이 이어집니다.
        </p>
      </div>

      {/* 질문 카드 그리드 */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {questions.map((question) => {
          const isCompleted = completedQuestions.includes(question.id)
          const difficultyInfo = getDifficultyInfo(question.difficulty)
          const categoryColor = getCategoryColor(question.category)

          return (
            <div
              key={question.id}
              className={`
                relative p-4 rounded-lg border-2 transition-all duration-200 cursor-pointer
                ${isCompleted 
                  ? 'bg-gray-50 border-gray-300 opacity-75' 
                  : 'bg-white border-gray-200 hover:border-blue-300 hover:shadow-md transform hover:-translate-y-1'
                }
                ${!isCompleted ? 'hover:bg-blue-50' : ''}
              `}
              onClick={() => !isCompleted && onQuestionSelect(question)}
              style={{ minHeight: '180px' }}
            >
              {/* 완료 체크마크 */}
              {isCompleted && (
                <div className="absolute top-2 right-2 w-6 h-6 bg-green-500 rounded-full flex items-center justify-center">
                  <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                </div>
              )}

              {/* 카테고리 배지 */}
              <div className={`inline-block px-2 py-1 rounded-full text-xs font-medium border mb-3 ${categoryColor}`}>
                {question.category}
              </div>

              {/* 질문 제목 */}
              <h3 className={`font-semibold text-sm mb-2 line-clamp-2 ${isCompleted ? 'text-gray-500' : 'text-gray-900'}`}>
                {question.title}
              </h3>

              {/* 질문 내용 미리보기 */}
              <p className={`text-xs mb-3 line-clamp-3 ${isCompleted ? 'text-gray-400' : 'text-gray-600'}`}>
                {question.content}
              </p>

              {/* 하단 정보 */}
              <div className="absolute bottom-4 left-4 right-4">
                <div className="flex items-center justify-between">
                  {/* 난이도 */}
                  <div className={`flex items-center space-x-1 px-2 py-1 rounded-full text-xs ${difficultyInfo.bgColor}`}>
                    <span>{difficultyInfo.icon}</span>
                    <span className={difficultyInfo.color}>{difficultyInfo.label}</span>
                  </div>

                  {/* 예상 시간 */}
                  <div className="flex items-center space-x-1 text-xs text-gray-500">
                    <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <span>{question.estimatedTime}분</span>
                  </div>
                </div>
              </div>

              {/* 호버 효과 오버레이 */}
              {!isCompleted && (
                <div className="absolute inset-0 bg-blue-500 bg-opacity-0 hover:bg-opacity-5 rounded-lg transition-all duration-200 flex items-center justify-center">
                  <div className="opacity-0 hover:opacity-100 transition-opacity duration-200">
                    <div className="bg-blue-600 text-white px-3 py-1 rounded-full text-sm font-medium">
                      선택하기
                    </div>
                  </div>
                </div>
              )}
            </div>
          )
        })}

        {/* 빈 슬롯 (10개 미만인 경우) */}
        {questions.length < 10 && [...Array(10 - questions.length)].map((_, index) => (
          <div
            key={`empty-${index}`}
            className="p-4 rounded-lg border-2 border-dashed border-gray-200 bg-gray-50 flex items-center justify-center"
            style={{ minHeight: '180px' }}
          >
            <div className="text-center text-gray-400">
              <svg className="w-8 h-8 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              <p className="text-sm">추가 질문</p>
            </div>
          </div>
        ))}
      </div>

      {/* 하단 안내 */}
      <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
        <div className="flex items-start space-x-3">
          <svg className="w-5 h-5 text-blue-600 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <div>
            <h4 className="font-medium text-blue-900 mb-1">면접 진행 방식</h4>
            <ul className="text-sm text-blue-800 space-y-1">
              <li>• 질문을 선택하면 메인 질문에 먼저 답변합니다</li>
              <li>• 답변 후 해당 질문과 관련된 3개의 꼬리 질문이 이어집니다</li>
              <li>• 모든 꼬리 질문 완료 후 다시 메인 질문을 선택할 수 있습니다</li>
              <li>• 텍스트 또는 음성으로 답변할 수 있습니다</li>
            </ul>
          </div>
        </div>
      </div>

      {/* 완료 상태일 때 결과 보기 버튼 */}
      {completedQuestions.length === questions.length && questions.length > 0 && (
        <div className="mt-6 text-center">
          <div className="mb-4 p-4 bg-green-50 rounded-lg border border-green-200">
            <div className="flex items-center justify-center space-x-2 text-green-800">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span className="font-medium">모든 면접 질문을 완료했습니다!</span>
            </div>
          </div>
          <button
            type="button"
            className="px-8 py-3 bg-green-600 text-white rounded-lg font-medium hover:bg-green-700 transition-colors duration-200"
            onClick={() => {
              // 결과 페이지로 이동하는 로직은 부모 컴포넌트에서 처리
              window.location.href = '/result'
            }}
          >
            면접 결과 보기
          </button>
        </div>
      )}
    </div>
  )
}

export default QuestionSelector