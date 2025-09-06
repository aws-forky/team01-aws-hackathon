import React from 'react'
import { FollowUpQuestion } from '../types'

interface FollowUpQuestionsProps {
  questions: FollowUpQuestion[]
  onQuestionSelect: (question: FollowUpQuestion) => void
  interviewer_persona?: string
  className?: string
}

export default function FollowUpQuestions({ 
  questions, 
  onQuestionSelect, 
  interviewer_persona = '친근한_시니어',
  className = '' 
}: FollowUpQuestionsProps) {
  if (questions.length === 0) {
    return null;
  }

  const getQuestionTypeIcon = (type: string) => {
    const icons = {
      deepening: '🔍',
      alternative: '🔄', 
      problem: '⚠️',
      scaling: '📈',
      business: '💼',
      '깊이_파기': '🔍',
      '대안_탐색': '🔄',
      '문제_상황': '⚠️',
      '확장_시나리오': '📈',
      '비즈니스_연결': '💼'
    };
    return icons[type as keyof typeof icons] || '💬';
  };

  const getDifficultyColor = (difficulty: string) => {
    const colors = {
      beginner: 'bg-green-100 text-green-800',
      intermediate: 'bg-yellow-100 text-yellow-800',
      advanced: 'bg-red-100 text-red-800'
    };
    return colors[difficulty as keyof typeof colors] || 'bg-gray-100 text-gray-800';
  };

  return (
    <div className={`bg-white rounded-lg shadow-md p-6 ${className}`}>
      <h3 className="text-lg font-semibold text-gray-900 mb-4">
        🔄 꼬리 질문 ({questions.length}개)
      </h3>
      <div className="space-y-3">
        {questions.map((question, index) => (
          <div
            key={index}
            className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer"
            onClick={() => onQuestionSelect(question)}
          >
            <div className="flex items-start justify-between mb-2">
              <div className="flex items-center space-x-2">
                <span className="text-lg">{getQuestionTypeIcon(question.type)}</span>
                <span className={`px-2 py-1 rounded text-xs ${getDifficultyColor(question.difficulty)}`}>
                  {question.difficulty}
                </span>
              </div>
            </div>
            
            <p className="text-gray-800 mb-2">{question.question}</p>
            
            {question.intent && (
              <p className="text-sm text-gray-500 italic">
                🎯 {question.intent}
              </p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}