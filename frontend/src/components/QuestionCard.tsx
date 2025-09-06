// Assumption: Expandable question card with answer toggle
import React, { useState } from 'react'
import { Question } from '../types'

interface QuestionCardProps {
  question: Question
  index: number
}

export default function QuestionCard({ question, index }: QuestionCardProps) {
  const [showAnswer, setShowAnswer] = useState(false)

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'technical': return 'bg-blue-100 text-blue-800'
      case 'behavioral': return 'bg-green-100 text-green-800'
      case 'situational': return 'bg-purple-100 text-purple-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'beginner': return 'bg-green-100 text-green-800'
      case 'intermediate': return 'bg-yellow-100 text-yellow-800'
      case 'advanced': return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6 mb-4">
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-2">
            <span className="font-bold text-lg">Q{index + 1}.</span>
            <span className={`px-2 py-1 rounded-full text-xs font-medium ${getTypeColor(question.type)}`}>
              {question.type}
            </span>
            <span className={`px-2 py-1 rounded-full text-xs font-medium ${getDifficultyColor(question.difficulty)}`}>
              {question.difficulty}
            </span>
          </div>
          <p className="text-gray-900 text-lg leading-relaxed">{question.question}</p>
        </div>
      </div>

      <button
        onClick={() => setShowAnswer(!showAnswer)}
        className="w-full mt-4 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
      >
        {showAnswer ? '답안 숨기기' : '모범답안 보기'}
      </button>

      {showAnswer && (
        <div className="mt-4 p-4 bg-gray-50 rounded-lg">
          <h4 className="font-medium text-gray-900 mb-2">💡 모범답안</h4>
          <p className="text-gray-700 leading-relaxed">{question.answer}</p>
        </div>
      )}
    </div>
  )
}
