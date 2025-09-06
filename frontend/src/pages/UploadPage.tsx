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
        throw new Error(uploadResult.message || 'PDF 업로드에 실패했습니다.')
      }

      // Check if text extraction was successful
      const extractedText = String(uploadResult.text_content || uploadResult.html_content || uploadResult.extracted_text || '')
      
      console.log('Extracted text length:', extractedText.length)
      console.log('Full text extracted successfully')
      
      setExtractedText(extractedText)
      
      // 텍스트가 비어있으면 에러 발생
      if (!extractedText || extractedText.trim().length < 10) {
        console.warn('Extracted text is too short or empty')
        throw new Error('PDF에서 충분한 텍스트를 추출할 수 없습니다. 다른 PDF 파일을 시도해보세요.')
      }

      // Extract keywords - 실패해도 계속 진행
      try {
        console.log('Starting keyword extraction...')
        const keywordResult = await apiService.extractKeywords(extractedText)
        
        if (keywordResult.success && keywordResult.keywords && keywordResult.keywords.length > 0) {
          console.log('Keywords extracted successfully:', keywordResult.keywords)
          setKeywords(keywordResult.keywords)
        } else {
          console.warn('키워드 추출 실패 또는 빈 결과, 기본 키워드 사용:', keywordResult)
          setKeywords([]) // 빈 배열로 설정
        }
      } catch (keywordError) {
        console.warn('키워드 추출 중 오류 발생, 기본 키워드 사용:', keywordError)
        setKeywords([]) // 빈 배열로 설정
        
        // 사용자에게 알림 (선택사항)
        if (keywordError.message && keywordError.message.includes('AI 서버')) {
          console.info('키워드 추출에 실패했지만 면접 진행에는 문제없습니다.')
        }
      }
      
      // 키워드 추출 성공 여부와 관계없이 다음 단계로 진행
      console.log('PDF processing completed successfully, moving to next step')
      nextStep()
      navigate('/company')

    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : '파일 처리 중 알 수 없는 오류가 발생했습니다.'
      console.error('File processing error:', err)
      
      // PDF 파싱은 성공했지만 키워드 추출에서 실패한 경우 처리
      if (errorMessage.includes('키워드') && extractedText) {
        console.log('키워드 추출 실패했지만 PDF 파싱은 성공, 계속 진행')
        setKeywords([])
        nextStep()
        navigate('/company')
        return
      }
      
      setError(errorMessage)
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
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <p className="text-red-800 font-medium">❌ 오류가 발생했습니다</p>
              <p className="text-red-600 text-sm mt-1">{error}</p>
            </div>
            <button
              onClick={() => {
                setError('')
                // 파일 선택을 다시 할 수 있도록 유도
              }}
              className="ml-4 px-3 py-1 bg-red-100 hover:bg-red-200 text-red-700 text-sm rounded transition-colors"
            >
              다시 시도
            </button>
          </div>
          <div className="mt-3 text-xs text-red-600">
            팁: 네트워크 연결을 확인하고 PDF 파일이 손상되지 않았는지 확인해주세요.
          </div>
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
