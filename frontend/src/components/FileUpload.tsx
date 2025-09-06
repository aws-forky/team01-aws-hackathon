// Assumption: Drag and drop file upload with validation
import React, { useCallback, useState } from 'react'

interface FileUploadProps {
  onFileSelect: (file: File) => void
  loading?: boolean
}

export default function FileUpload({ onFileSelect, loading = false }: FileUploadProps) {
  const [dragActive, setDragActive] = useState(false)

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }, [])

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0]
      if (file.type === 'application/pdf') {
        onFileSelect(file)
      } else {
        alert('PDF 파일만 업로드 가능합니다.')
      }
    }
  }, [onFileSelect])

  const handleChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault()
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0]
      if (file.type === 'application/pdf') {
        onFileSelect(file)
      } else {
        alert('PDF 파일만 업로드 가능합니다.')
      }
    }
  }, [onFileSelect])

  return (
    <div className="w-full">
      <div
        className={`relative border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
          dragActive ? 'border-primary bg-blue-50' : 'border-gray-300'
        } ${loading ? 'opacity-50 pointer-events-none' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <input
          type="file"
          accept=".pdf"
          onChange={handleChange}
          disabled={loading}
          className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
        />
        
        <div className="space-y-4">
          <div className="text-6xl">📄</div>
          <div>
            <p className="text-lg font-medium text-gray-900">
              포트폴리오 PDF를 업로드하세요
            </p>
            <p className="text-sm text-gray-500 mt-2">
              파일을 드래그하거나 클릭하여 선택하세요
            </p>
          </div>
          <div className="text-xs text-gray-400">
            최대 10MB, PDF 형식만 지원
          </div>
        </div>
      </div>
    </div>
  )
}
