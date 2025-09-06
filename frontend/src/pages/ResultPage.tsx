// Assumption: Results page with PDF download and restart functionality
import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useApp } from '../context/AppContext'
import { pdfService } from '../services/pdf'

export default function ResultPage() {
  const navigate = useNavigate()
  const { state, resetApp } = useApp()
  const [downloading, setDownloading] = useState(false)

  const handleDownloadPDF = async () => {
    setDownloading(true)
    try {
      await pdfService.generatePDF(state.questions, state.selectedCompany)
    } catch (error) {
      alert('PDF 다운로드 중 오류가 발생했습니다.')
    } finally {
      setDownloading(false)
    }
  }

  const handleRestart = () => {
    resetApp()
    navigate('/')
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="text-center mb-8">
        <div className="text-6xl mb-4">🎉</div>
        <h2 className="text-3xl font-bold text-gray-900 mb-4">
          면접 준비 완료!
        </h2>
        <p className="text-gray-600">
          {state.selectedCompany} 면접을 위한 {state.questions.length}개의 질문이 준비되었습니다.
        </p>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6 mb-8">
        <h3 className="text-xl font-bold text-gray-900 mb-4">📊 분석 결과</h3>
        
        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <h4 className="font-semibold text-gray-700 mb-2">추출된 기술 키워드</h4>
            <div className="flex flex-wrap gap-2">
              {state.keywords.map((keyword, index) => (
                <span
                  key={index}
                  className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm"
                >
                  {keyword.name}
                </span>
              ))}
            </div>
          </div>
          
          <div>
            <h4 className="font-semibold text-gray-700 mb-2">질문 유형 분포</h4>
            <div className="space-y-2">
              {['technical', 'behavioral', 'situational'].map(type => {
                const count = state.questions.filter(q => q.type === type).length
                return (
                  <div key={type} className="flex justify-between">
                    <span className="capitalize">{type}</span>
                    <span className="font-medium">{count}개</span>
                  </div>
                )
              })}
            </div>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6 mb-8">
        <h3 className="text-xl font-bold text-gray-900 mb-4">📝 질문 미리보기</h3>
        <div className="space-y-3">
          {state.questions.slice(0, 3).map((question, index) => (
            <div key={index} className="border-l-4 border-primary pl-4">
              <p className="font-medium">Q{index + 1}. {question.question}</p>
            </div>
          ))}
          {state.questions.length > 3 && (
            <p className="text-gray-500 text-sm">... 외 {state.questions.length - 3}개 질문</p>
          )}
        </div>
      </div>

      <div className="flex flex-col sm:flex-row gap-4 justify-center">
        <button
          onClick={handleDownloadPDF}
          disabled={downloading}
          className="bg-primary text-white px-6 py-3 rounded-lg hover:bg-blue-600 transition-colors disabled:opacity-50"
        >
          {downloading ? '다운로드 중...' : '📄 PDF 다운로드'}
        </button>
        
        <button
          onClick={handleRestart}
          className="bg-secondary text-white px-6 py-3 rounded-lg hover:bg-green-600 transition-colors"
        >
          🔄 다시 시작하기
        </button>
      </div>

      <div className="mt-8 text-center">
        <button
          onClick={() => navigate('/interview')}
          className="text-gray-500 hover:text-gray-700 transition-colors"
        >
          ← 질문 다시 보기
        </button>
      </div>
    </div>
  )
}
