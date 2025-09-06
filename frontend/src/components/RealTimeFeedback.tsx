import React, { useState } from 'react';
import { FeedbackAnalysis } from '../types';

interface RealTimeFeedbackProps {
  feedback: FeedbackAnalysis;
  onClose?: () => void;
}

const RealTimeFeedback: React.FC<RealTimeFeedbackProps> = ({ feedback, onClose }) => {
  const [activeTab, setActiveTab] = useState<'overview' | 'star' | 'technical'>('overview');

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getQualityBadge = (quality: string) => {
    const colors = {
      excellent: 'bg-green-100 text-green-800',
      good: 'bg-blue-100 text-blue-800',
      fair: 'bg-yellow-100 text-yellow-800',
      poor: 'bg-red-100 text-red-800'
    };
    return colors[quality as keyof typeof colors] || 'bg-gray-100 text-gray-800';
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 max-w-4xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-800">실시간 답변 피드백</h2>
        {onClose && (
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700"
          >
            ✕
          </button>
        )}
      </div>

      {/* 전체 점수 */}
      <div className="mb-6 p-4 bg-gray-50 rounded-lg">
        <div className="flex items-center justify-between">
          <span className="text-lg font-medium">전체 점수</span>
          <span className={`text-3xl font-bold ${getScoreColor(feedback.overall_score)}`}>
            {feedback.overall_score}/100
          </span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
          <div
            className={`h-2 rounded-full ${
              feedback.overall_score >= 80 ? 'bg-green-500' :
              feedback.overall_score >= 60 ? 'bg-yellow-500' : 'bg-red-500'
            }`}
            style={{ width: `${feedback.overall_score}%` }}
          />
        </div>
      </div>

      {/* 탭 네비게이션 */}
      <div className="flex border-b border-gray-200 mb-6">
        {[
          { key: 'overview', label: '개요' },
          { key: 'star', label: 'STAR 분석' },
          { key: 'technical', label: '기술적 정확성' }
        ].map(tab => (
          <button
            key={tab.key}
            onClick={() => setActiveTab(tab.key as any)}
            className={`px-4 py-2 font-medium ${
              activeTab === tab.key
                ? 'text-blue-600 border-b-2 border-blue-600'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* 탭 컨텐츠 */}
      {activeTab === 'overview' && (
        <div className="space-y-6">
          {/* 강점 */}
          <div>
            <h3 className="text-lg font-semibold text-green-700 mb-3">👍 잘한 점</h3>
            <ul className="space-y-2">
              {feedback.strengths.map((strength, index) => (
                <li key={index} className="flex items-start">
                  <span className="text-green-500 mr-2">•</span>
                  <span>{strength}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* 개선 제안 */}
          <div>
            <h3 className="text-lg font-semibold text-orange-700 mb-3">💡 개선 제안</h3>
            <ul className="space-y-2">
              {feedback.improvement_suggestions.map((suggestion, index) => (
                <li key={index} className="flex items-start">
                  <span className="text-orange-500 mr-2">•</span>
                  <span>{suggestion}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}

      {activeTab === 'star' && (
        <div className="space-y-4">
          <h3 className="text-lg font-semibold mb-4">STAR 기법 분석</h3>
          {Object.entries(feedback.star_analysis).map(([key, analysis]) => (
            <div key={key} className="border rounded-lg p-4">
              <div className="flex items-center justify-between mb-2">
                <span className="font-medium capitalize">
                  {key === 'situation' ? '상황 (Situation)' :
                   key === 'task' ? '과제 (Task)' :
                   key === 'action' ? '행동 (Action)' :
                   '결과 (Result)'}
                </span>
                <div className="flex items-center space-x-2">
                  <span className={`px-2 py-1 rounded text-sm ${
                    analysis.present ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                  }`}>
                    {analysis.present ? '포함됨' : '누락'}
                  </span>
                  {analysis.quality && (
                    <span className={`px-2 py-1 rounded text-sm ${getQualityBadge(analysis.quality)}`}>
                      {analysis.quality}
                    </span>
                  )}
                </div>
              </div>
              {analysis.suggestion && (
                <p className="text-sm text-gray-600 mt-2">
                  💡 {analysis.suggestion}
                </p>
              )}
            </div>
          ))}
        </div>
      )}

      {activeTab === 'technical' && (
        <div className="space-y-4">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold">기술적 정확성</h3>
            <span className={`text-2xl font-bold ${getScoreColor(feedback.technical_accuracy.score)}`}>
              {feedback.technical_accuracy.score}/100
            </span>
          </div>

          {feedback.technical_accuracy.correct_concepts.length > 0 && (
            <div>
              <h4 className="font-medium text-green-700 mb-2">✅ 올바른 개념</h4>
              <div className="flex flex-wrap gap-2">
                {feedback.technical_accuracy.correct_concepts.map((concept, index) => (
                  <span key={index} className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm">
                    {concept}
                  </span>
                ))}
              </div>
            </div>
          )}

          {feedback.technical_accuracy.missing_details.length > 0 && (
            <div>
              <h4 className="font-medium text-orange-700 mb-2">⚠️ 보완 필요</h4>
              <div className="flex flex-wrap gap-2">
                {feedback.technical_accuracy.missing_details.map((detail, index) => (
                  <span key={index} className="px-3 py-1 bg-orange-100 text-orange-800 rounded-full text-sm">
                    {detail}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default RealTimeFeedback;