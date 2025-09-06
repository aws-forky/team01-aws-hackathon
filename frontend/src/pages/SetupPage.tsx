// Assumption: Welcome page with service introduction
import React from 'react'
import { useNavigate } from 'react-router-dom'

export default function SetupPage() {
  const navigate = useNavigate()

  return (
    <div className="text-center">
      <div className="mb-8">
        <div className="text-8xl mb-4">🍴</div>
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Forky에 오신 것을 환영합니다!
        </h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          AI가 당신의 포트폴리오를 분석하여 맞춤형 기술면접 질문을 생성해드립니다.
        </p>
      </div>

      <div className="grid md:grid-cols-3 gap-8 mb-12">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <div className="text-4xl mb-4">📄</div>
          <h3 className="text-lg font-semibold mb-2">포트폴리오 분석</h3>
          <p className="text-gray-600">
            PDF 포트폴리오를 업로드하면 AI가 자동으로 기술 스택을 분석합니다.
          </p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md">
          <div className="text-4xl mb-4">🏢</div>
          <h3 className="text-lg font-semibold mb-2">회사별 맞춤화</h3>
          <p className="text-gray-600">
            지원하는 회사에 특화된 질문을 생성하여 실전 면접을 대비합니다.
          </p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md">
          <div className="text-4xl mb-4">💡</div>
          <h3 className="text-lg font-semibold mb-2">모범답안 제공</h3>
          <p className="text-gray-600">
            각 질문에 대한 상세한 모범답안으로 면접 준비를 완벽하게 합니다.
          </p>
        </div>
      </div>

      <button
        onClick={() => navigate('/upload')}
        className="bg-primary text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-blue-600 transition-colors"
      >
        시작하기 🚀
      </button>
    </div>
  )
}
