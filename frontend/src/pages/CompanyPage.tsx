// Assumption: Company selection page with preset companies
import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import LoadingSpinner from '../components/LoadingSpinner'
import { useApp } from '../context/AppContext'
import { apiService } from '../services/api'
import { Company } from '../types'

export default function CompanyPage() {
  const navigate = useNavigate()
  const { state, setSelectedCompany, setQuestions, nextStep } = useApp()
  const [companies, setCompanies] = useState<Company[]>([])
  const [loading, setLoading] = useState(true)
  const [generating, setGenerating] = useState(false)
  const [selectedCompanyName, setSelectedCompanyName] = useState('')

  useEffect(() => {
    loadCompanies()
  }, [])

  const loadCompanies = async () => {
    try {
      const result = await apiService.getCompanies()
      if (result.success) {
        setCompanies(result.companies)
      }
    } catch (error) {
      console.error('Failed to load companies:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleCompanySelect = async (companyName: string) => {
    setGenerating(true)
    setSelectedCompanyName(companyName)

    try {
      const keywords = state.keywords.map(k => k.name)
      const result = await apiService.generateQuestions(keywords, companyName, state.extractedText)
      
      if (result.success) {
        setSelectedCompany(companyName)
        setQuestions(result.questions)
        nextStep()
        navigate('/interview')
      } else {
        throw new Error(result.message)
      }
    } catch (error) {
      alert('질문 생성 중 오류가 발생했습니다.')
    } finally {
      setGenerating(false)
    }
  }

  if (loading) {
    return <LoadingSpinner message="회사 목록을 불러오고 있습니다..." />
  }

  if (generating) {
    return (
      <div className="text-center">
        <LoadingSpinner message={`${selectedCompanyName} 맞춤 질문을 생성하고 있습니다...`} />
        <div className="mt-4 space-y-2 text-sm text-gray-600">
          <p>🤖 AI가 회사별 특화 질문을 만들고 있습니다...</p>
          <p>📝 기술 질문과 행동 질문을 준비하고 있습니다...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-gray-900 mb-4">
          지원 회사 선택
        </h2>
        <p className="text-gray-600">
          면접을 준비할 회사를 선택하면 맞춤형 질문을 생성해드립니다.
        </p>
      </div>

      <div className="mb-6 p-4 bg-blue-50 rounded-lg">
        <h3 className="font-semibold text-blue-900 mb-2">분석된 기술 키워드</h3>
        <div className="flex flex-wrap gap-2">
          {state.keywords.map((keyword, index) => (
            <span
              key={index}
              className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm"
            >
              {keyword.name} ({keyword.importance}/10)
            </span>
          ))}
        </div>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {companies.map((company, index) => (
          <div
            key={index}
            className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow cursor-pointer"
            onClick={() => handleCompanySelect(company.name)}
          >
            <h3 className="text-xl font-bold text-gray-900 mb-2">
              {company.name}
            </h3>
            <p className="text-gray-600 mb-4 text-sm">
              {company.description}
            </p>
            <div className="space-y-2">
              <h4 className="font-medium text-gray-700">주요 기술 스택</h4>
              <div className="flex flex-wrap gap-1">
                {company.tech_stack.map((tech, techIndex) => (
                  <span
                    key={techIndex}
                    className="px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs"
                  >
                    {tech}
                  </span>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-8 text-center">
        <button
          onClick={() => navigate('/upload')}
          className="text-gray-500 hover:text-gray-700 transition-colors"
        >
          ← 이전으로
        </button>
      </div>
    </div>
  )
}
