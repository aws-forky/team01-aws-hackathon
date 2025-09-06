import React, { useState } from 'react'
import { PortfolioAnalysis, PortfolioImprovement } from '../types'

interface PortfolioImprovementProps {
  analysis: PortfolioAnalysis
  improvements: PortfolioImprovement[]
  onImprovementComplete?: (improvementId: string) => void
  className?: string
}

export default function PortfolioImprovementComponent({ 
  analysis, 
  improvements, 
  onImprovementComplete,
  className = '' 
}: PortfolioImprovementProps) {
  const [completedImprovements, setCompletedImprovements] = useState<Set<string>>(new Set())
  const [expandedItems, setExpandedItems] = useState<Set<number>>(new Set())

  const getPriorityColor = (priority: string) => {
    const colors = {
      high: 'bg-red-100 text-red-800 border-red-200',
      medium: 'bg-yellow-100 text-yellow-800 border-yellow-200', 
      low: 'bg-green-100 text-green-800 border-green-200'
    }
    return colors[priority as keyof typeof colors] || 'bg-gray-100 text-gray-800 border-gray-200'
  }

  const getPriorityIcon = (priority: string) => {
    const icons = {
      high: '🚨',
      medium: '⚠️',
      low: '💡'
    }
    return icons[priority as keyof typeof icons] || '📝'
  }

  const getImpactIcon = (impact: string) => {
    const icons = {
      high: '🎯',
      medium: '📊', 
      low: '📈'
    }
    return icons[impact as keyof typeof icons] || '📋'
  }

  const toggleExpanded = (index: number) => {
    const newExpanded = new Set(expandedItems)
    if (newExpanded.has(index)) {
      newExpanded.delete(index)
    } else {
      newExpanded.add(index)
    }
    setExpandedItems(newExpanded)
  }

  const markAsCompleted = (index: number, category: string) => {
    const newCompleted = new Set(completedImprovements)
    newCompleted.add(category)
    setCompletedImprovements(newCompleted)
    
    if (onImprovementComplete) {
      onImprovementComplete(category)
    }
  }

  return (
    <div className={`bg-white rounded-lg shadow-md p-6 ${className}`}>
      {/* 전체 분석 결과 */}
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">📊 포트폴리오 분석 결과</h3>
        
        <div className="grid grid-cols-3 gap-4 mb-4">
          <div className="text-center p-3 bg-gray-50 rounded-lg">
            <div className="text-2xl font-bold text-gray-900">{analysis.overall_score}</div>
            <div className="text-sm text-gray-600">현재 점수</div>
          </div>
          <div className="text-center p-3 bg-blue-50 rounded-lg">
            <div className="text-2xl font-bold text-blue-600">{analysis.target_score}</div>
            <div className="text-sm text-gray-600">목표 점수</div>
          </div>
          <div className="text-center p-3 bg-green-50 rounded-lg">
            <div className="text-2xl font-bold text-green-600">{analysis.market_fit}%</div>
            <div className="text-sm text-gray-600">시장 적합도</div>
          </div>
        </div>

        {/* 진행률 바 */}
        <div className="mb-4">
          <div className="flex justify-between text-sm text-gray-600 mb-1">
            <span>개선 진행률</span>
            <span>{improvements && improvements.length > 0 ? Math.round((completedImprovements.size / improvements.length) * 100) : 0}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div 
              className="bg-green-500 h-2 rounded-full transition-all duration-300"
              style={{ width: `${improvements && improvements.length > 0 ? (completedImprovements.size / improvements.length) * 100 : 0}%` }}
            />
          </div>
        </div>
      </div>

      {/* 개선 제안 목록 */}
      <div className="space-y-4">
        <h4 className="font-semibold text-gray-900">🔧 개선 제안 ({improvements ? improvements.length : 0}개)</h4>
        
        {improvements && improvements.map((improvement, index) => {
          const isCompleted = completedImprovements.has(improvement.category)
          const isExpanded = expandedItems.has(index)
          
          return (
            <div 
              key={index}
              className={`border rounded-lg transition-all duration-200 ${
                isCompleted ? 'bg-green-50 border-green-200 opacity-75' : 'bg-white border-gray-200'
              }`}
            >
              <div 
                className="p-4 cursor-pointer"
                onClick={() => toggleExpanded(index)}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center mb-2">
                      <span className="mr-2">{getPriorityIcon(improvement.priority)}</span>
                      <h5 className={`font-medium ${isCompleted ? 'line-through text-gray-500' : 'text-gray-900'}`}>
                        {improvement.category}
                      </h5>
                      <span className={`ml-2 px-2 py-1 rounded-full text-xs border ${getPriorityColor(improvement.priority)}`}>
                        {improvement.priority}
                      </span>
                      {isCompleted && (
                        <span className="ml-2 px-2 py-1 bg-green-100 text-green-800 rounded-full text-xs">
                          ✅ 완료
                        </span>
                      )}
                    </div>
                    
                    <p className={`text-sm ${isCompleted ? 'text-gray-500' : 'text-gray-700'}`}>
                      {improvement.suggestion}
                    </p>
                    
                    <div className="flex items-center mt-2 space-x-4 text-xs text-gray-500">
                      <span>{getImpactIcon(improvement.impact)} 임팩트: {improvement.impact}</span>
                      <span>⏱️ 소요시간: {improvement.timeline}</span>
                      <span>🔧 난이도: {improvement.effort}</span>
                    </div>
                  </div>
                  
                  <button className="ml-4 text-gray-400 hover:text-gray-600">
                    {isExpanded ? '▲' : '▼'}
                  </button>
                </div>
              </div>

              {/* 확장된 내용 */}
              {isExpanded && (
                <div className="px-4 pb-4 border-t border-gray-100">
                  <div className="pt-4 space-y-3">
                    <div>
                      <h6 className="text-sm font-medium text-gray-900 mb-1">📝 개선 예시</h6>
                      <div className="bg-gray-50 p-3 rounded text-sm text-gray-700">
                        {improvement.example}
                      </div>
                    </div>
                    
                    <div className="flex items-center justify-between">
                      <div className="text-xs text-gray-500">
                        예상 효과: 점수 +{Math.round((analysis.target_score - analysis.overall_score) * 0.3)}점
                      </div>
                      
                      {!isCompleted && (
                        <button
                          onClick={(e) => {
                            e.stopPropagation()
                            markAsCompleted(index, improvement.category)
                          }}
                          className="px-3 py-1 bg-blue-600 text-white rounded text-sm hover:bg-blue-700 transition-colors"
                        >
                          완료 표시
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              )}
            </div>
          )
        })}
      </div>

      {/* 회사별 맞춤 조언 */}
      {analysis.company_specific_advice && (
        <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <h4 className="font-semibold text-blue-900 mb-2">🏢 회사별 맞춤 조언</h4>
          <p className="text-blue-800 text-sm leading-relaxed">
            {analysis.company_specific_advice}
          </p>
        </div>
      )}

      {/* 전체 완료 시 축하 메시지 */}
      {improvements && completedImprovements.size === improvements.length && improvements.length > 0 && (
        <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-lg text-center">
          <div className="text-2xl mb-2">🎉</div>
          <h4 className="font-semibold text-green-900 mb-1">모든 개선 사항 완료!</h4>
          <p className="text-green-800 text-sm">
            예상 점수: {analysis.overall_score}점 → {analysis.target_score}점 (+{analysis.target_score - analysis.overall_score}점)
          </p>
        </div>
      )}
    </div>
  )
}