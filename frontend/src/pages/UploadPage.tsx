// Assumption: File upload page with progress tracking
import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import FileUpload from '../components/FileUpload'
import LoadingSpinner from '../components/LoadingSpinner'
import { useApp } from '../context/AppContext'
import { apiService } from '../services/api'

export default function UploadPage() {
  const navigate = useNavigate()
  const { setExtractedText, setKeywords, nextStep } = useApp()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleFileSelect = async (file: File) => {
    setLoading(true)
    setError('')

    try {
      // Upload file and extract text
      const uploadResult = await apiService.uploadFile(file)
      
      if (!uploadResult.success) {
        throw new Error(uploadResult.message)
      }

      // Check if text extraction was successful
      const extractedText = String(uploadResult.extracted_text || '')
      
      setExtractedText(extractedText)
      if (!extractedText || extractedText.trim().length === 0) {
        throw new Error('PDF에서 텍스트를 추출할 수 없습니다. 다른 파일을 시도해보세요.')
      }

      // Extract keywords
      const keywordResult = await apiService.extractKeywords(extractedText)
      
      if (keywordResult.success) {
        setKeywords(keywordResult.keywords)
        nextStep()
        navigate('/company')
      } else {
        throw new Error(keywordResult.message)
      }

    } catch (err) {
      setError(err instanceof Error ? err.message : '파일 처리 중 오류가 발생했습니다.')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="text-center">
        <LoadingSpinner message="포트폴리오를 분석하고 있습니다..." />
        <div className="mt-4 space-y-2 text-sm text-gray-600">
          <p>📄 PDF 파일을 읽고 있습니다...</p>
          <p>🤖 AI가 기술 스택을 분석하고 있습니다...</p>
          <p>⏱️ 잠시만 기다려주세요 (약 30초)</p>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-2xl mx-auto">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-gray-900 mb-4">
          포트폴리오 업로드
        </h2>
        <p className="text-gray-600">
          PDF 형식의 포트폴리오를 업로드하면 AI가 자동으로 분석합니다.
        </p>
      </div>

      <FileUpload onFileSelect={handleFileSelect} loading={loading} />

      {error && (
        <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-red-800">❌ {error}</p>
        </div>
      )}

      <div className="mt-8 text-center">
        <button
          onClick={() => navigate('/')}
          className="text-gray-500 hover:text-gray-700 transition-colors"
        >
          ← 이전으로
        </button>
      </div>
    </div>
  )
}
