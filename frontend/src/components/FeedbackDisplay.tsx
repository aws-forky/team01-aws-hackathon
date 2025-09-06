import React from 'react'
import { FeedbackAnalysis } from '../types'

interface FeedbackDisplayProps {
  feedback: FeedbackAnalysis
  className?: string
}

export default function FeedbackDisplay({ feedback, className = '' }: FeedbackDisplayProps) {
  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600'
    if (score >= 60) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getQualityBadge = (quality: string) => {
    const colors = {
      excellent: 'bg-green-100 text-green-800',
      good: 'bg-blue-100 text-blue-800',
      fair: 'bg-yellow-100 text-yellow-800',
      poor: 'bg-red-100 text-red-800'
    }
    return colors[quality as keyof typeof colors] || 'bg-gray-100 text-gray-800'
  }

  return (
    <div className={`bg-white rounded-lg shadow-md p-6 ${className}`}>
      {/* 전체 점수 */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-lg font-semibold text-gray-900">답변 분석 결과</h3>
          <div className={`text-2xl font-bold ${getScoreColor(feedback.overall_score)}`}>
            {feedback.overall_score}/100
          </div>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div 
            className={`h-2 rounded-full ${
              feedback.overall_score >= 80 ? 'bg-green-500' :
              feedback.overall_score >= 60 ? 'bg-yellow-500' : 'bg-red-500'
            }`}
            style={{ width: `${feedback.overall_score}%` }}
          />
        </div>
      </div>

      {/* STAR 분석 */}
      <div className="mb-6">
        <h4 className="font-medium text-gray-900 mb-3">📊 STAR 기법 분석</h4>
        <div className="grid grid-cols-2 gap-4">
          {Object.entries(feedback.star_analysis).map(([key, value]) => (
            <div key={key} className="border rounded-lg p-3">
              <div className="flex items-center justify-between mb-1">
                <span className="text-sm font-medium capitalize">{key}</span>
                {value.present ? (
                  <span className={`px-2 py-1 rounded-full text-xs ${getQualityBadge(value.quality)}`}>
                    {value.quality}
                  </span>
                ) : (
                  <span className="px-2 py-1 rounded-full text-xs bg-gray-100 text-gray-600">
                    누락
                  </span>
                )}
              </div>
              {value.suggestion && (
                <p className="text-xs text-gray-600 mt-1">{value.suggestion}</p>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* 기술적 정확성 */}
      <div className="mb-6">
        <h4 className="font-medium text-gray-900 mb-3">🔧 기술적 정확성</h4>
        <div className="bg-gray-50 rounded-lg p-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-gray-600">정확도</span>
            <span className={`font-semibold ${getScoreColor(feedback.technical_accuracy.score)}`}>
              {feedback.technical_accuracy.score}%
            </span>
          </div>
          
          {feedback.technical_accuracy.correct_concepts && feedback.technical_accuracy.correct_concepts.length > 0 && (
            <div className="mb-2">
              <span className="text-xs text-gray-500">올바른 개념:</span>
              <div className="flex flex-wrap gap-1 mt-1">
                {feedback.technical_accuracy.correct_concepts.map((concept, index) => (
                  <span key={index} className="px-2 py-1 bg-green-100 text-green-700 rounded text-xs">
                    {concept}
                  </span>
                ))}
              </div>
            </div>
          )}
          
          {feedback.technical_accuracy.missing_details && feedback.technical_accuracy.missing_details.length > 0 && (
            <div>
              <span className="text-xs text-gray-500">보완 필요:</span>
              <div className="flex flex-wrap gap-1 mt-1">
                {feedback.technical_accuracy.missing_details.map((detail, index) => (
                  <span key={index} className="px-2 py-1 bg-yellow-100 text-yellow-700 rounded text-xs">
                    {detail}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* 잘한 점 */}
      {feedback.strengths && feedback.strengths.length > 0 && (
        <div className="mb-6">
          <h4 className="font-medium text-gray-900 mb-3">✅ 잘한 점</h4>
          <ul className="space-y-2">
            {feedback.strengths.map((strength, index) => (
              <li key={index} className="flex items-start">
                <span className="text-green-500 mr-2">•</span>
                <span className="text-sm text-gray-700">{strength}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* 개선 제안 */}
      {feedback.improvement_suggestions && feedback.improvement_suggestions.length > 0 && (
        <div className="mb-6">
          <h4 className="font-medium text-gray-900 mb-3">🔧 개선할 점</h4>
          <ul className="space-y-2">
            {feedback.improvement_suggestions.map((suggestion, index) => (
              <li key={index} className="flex items-start">
                <span className="text-blue-500 mr-2">•</span>
                <span className="text-sm text-gray-700">{suggestion}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* 다음 단계 */}
      {feedback.next_steps && feedback.next_steps.length > 0 && (
        <div>
          <h4 className="font-medium text-gray-900 mb-3">📚 추천 학습</h4>
          <ul className="space-y-2">
            {feedback.next_steps.map((step, index) => (
              <li key={index} className="flex items-start">
                <span className="text-purple-500 mr-2">•</span>
                <span className="text-sm text-gray-700">{step}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}