import React, { useState, useEffect, useRef } from 'react'
import VoiceRecorder from './VoiceRecorder'

interface EnhancedAnswerInputProps {
  value: string
  onChange: (value: string) => void
  onSubmit: () => void
  placeholder?: string
  disabled?: boolean
  maxLength?: number
  showWordCount?: boolean
  className?: string
}

type InputMode = 'text' | 'voice'

const EnhancedAnswerInput: React.FC<EnhancedAnswerInputProps> = ({
  value,
  onChange,
  onSubmit,
  placeholder = '답변을 입력하세요...',
  disabled = false,
  maxLength = 2000,
  showWordCount = true,
  className = ''
}) => {
  const [inputMode, setInputMode] = useState<InputMode>('text')
  const [isVoiceActive, setIsVoiceActive] = useState(false)
  const [voiceTranscript, setVoiceTranscript] = useState('')
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  // 텍스트 영역 자동 높이 조절
  const adjustTextareaHeight = () => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`
    }
  }

  // 값 변경 시 높이 조절
  useEffect(() => {
    adjustTextareaHeight()
  }, [value])

  // 음성 인식 결과 처리
  const handleVoiceTranscript = (transcript: string) => {
    const newValue = value + (value ? ' ' : '') + transcript
    setVoiceTranscript(transcript)
    onChange(newValue)
    
    // 음성 입력 후 텍스트 모드로 전환하여 편집 가능하게 함
    setTimeout(() => {
      setInputMode('text')
      setIsVoiceActive(false)
      if (textareaRef.current) {
        textareaRef.current.focus()
        // 커서를 끝으로 이동
        textareaRef.current.setSelectionRange(newValue.length, newValue.length)
      }
    }, 500)
  }

  // 음성 인식 에러 처리
  const handleVoiceError = (error: string) => {
    console.error('음성 인식 오류:', error)
    // 에러 발생 시 텍스트 모드로 복귀
    setInputMode('text')
    setIsVoiceActive(false)
  }

  // 모드 전환
  const toggleInputMode = () => {
    if (inputMode === 'text') {
      setInputMode('voice')
      setIsVoiceActive(true)
    } else {
      setInputMode('text')
      setIsVoiceActive(false)
    }
  }

  // 키보드 이벤트 처리
  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
      e.preventDefault()
      onSubmit()
    }
  }

  // 단어 수 계산
  const wordCount = value.trim() ? value.trim().split(/\s+/).length : 0
  const charCount = value.length

  return (
    <div className={`enhanced-answer-input ${className}`}>
      {/* 입력 모드 선택 */}
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center space-x-2">
          <span className="text-sm font-medium text-gray-700">입력 방식:</span>
          <div className="flex bg-gray-100 rounded-lg p-1">
            <button
              type="button"
              onClick={() => {
                setInputMode('text')
                setIsVoiceActive(false)
              }}
              className={`
                px-3 py-1 text-sm rounded-md transition-all duration-200 flex items-center space-x-1
                ${inputMode === 'text' 
                  ? 'bg-white text-blue-600 shadow-sm' 
                  : 'text-gray-600 hover:text-gray-800'
                }
              `}
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
              </svg>
              <span>텍스트</span>
            </button>
            <button
              type="button"
              onClick={toggleInputMode}
              disabled={disabled}
              className={`
                px-3 py-1 text-sm rounded-md transition-all duration-200 flex items-center space-x-1
                ${inputMode === 'voice' 
                  ? 'bg-white text-red-600 shadow-sm' 
                  : 'text-gray-600 hover:text-gray-800'
                }
                ${disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
              `}
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
              </svg>
              <span>음성</span>
            </button>
          </div>
        </div>

        {/* 글자 수 / 단어 수 표시 */}
        {showWordCount && (
          <div className="text-sm text-gray-500">
            <span className={charCount > maxLength * 0.9 ? 'text-orange-500' : ''}>
              {charCount}/{maxLength}
            </span>
            {wordCount > 0 && (
              <span className="ml-2">
                {wordCount}단어
              </span>
            )}
          </div>
        )}
      </div>

      {/* 입력 영역 */}
      <div className="relative">
        {inputMode === 'text' ? (
          // 텍스트 입력 모드
          <div className="relative">
            <textarea
              ref={textareaRef}
              value={value}
              onChange={(e) => onChange(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder={placeholder}
              disabled={disabled}
              maxLength={maxLength}
              className={`
                w-full min-h-[120px] max-h-[400px] p-4 border border-gray-300 rounded-lg
                focus:ring-2 focus:ring-blue-500 focus:border-transparent
                resize-none transition-all duration-200
                ${disabled ? 'bg-gray-50 cursor-not-allowed' : 'bg-white'}
                ${charCount > maxLength * 0.9 ? 'border-orange-300' : ''}
              `}
              style={{ 
                fontSize: '16px', // iOS에서 줌 방지
                lineHeight: '1.5'
              }}
            />
            
            {/* 텍스트 입력 도움말 */}
            <div className="absolute bottom-2 right-2 text-xs text-gray-400">
              Ctrl+Enter로 제출
            </div>
          </div>
        ) : (
          // 음성 입력 모드
          <div className="min-h-[120px] p-4 border-2 border-dashed border-blue-300 rounded-lg bg-blue-50 flex flex-col items-center justify-center">
            <VoiceRecorder
              onTranscript={handleVoiceTranscript}
              onError={handleVoiceError}
              isActive={isVoiceActive}
              className="mb-4"
            />
            
            {/* 음성 입력 안내 */}
            <div className="text-center">
              <p className="text-sm text-gray-600 mb-2">
                마이크 버튼을 클릭하고 답변을 말씀해주세요
              </p>
              <p className="text-xs text-gray-500">
                음성 인식이 완료되면 자동으로 텍스트 모드로 전환되어 편집할 수 있습니다
              </p>
            </div>

            {/* 현재 입력된 텍스트 미리보기 */}
            {value && (
              <div className="mt-4 w-full p-3 bg-white rounded border border-gray-200">
                <div className="text-xs text-gray-500 mb-1">현재 입력된 내용:</div>
                <div className="text-sm text-gray-800 max-h-20 overflow-y-auto">
                  {value}
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* 최근 음성 인식 결과 표시 */}
      {voiceTranscript && inputMode === 'text' && (
        <div className="mt-2 p-2 bg-green-50 border border-green-200 rounded-md">
          <div className="flex items-center space-x-2">
            <svg className="w-4 h-4 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span className="text-sm text-green-700">
              음성 인식 완료: "{voiceTranscript}"
            </span>
          </div>
        </div>
      )}

      {/* 제출 버튼 */}
      <div className="flex justify-between items-center mt-4">
        <div className="text-sm text-gray-500">
          {inputMode === 'voice' ? (
            <span>음성 입력 후 자동으로 텍스트 편집 모드로 전환됩니다</span>
          ) : (
            <span>답변을 완료한 후 제출 버튼을 클릭하세요</span>
          )}
        </div>
        
        <button
          type="button"
          onClick={onSubmit}
          disabled={disabled || !value.trim()}
          className={`
            px-6 py-2 rounded-lg font-medium transition-all duration-200
            ${disabled || !value.trim()
              ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
              : 'bg-blue-600 text-white hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2'
            }
          `}
        >
          답변 제출
        </button>
      </div>

      {/* 입력 가이드 */}
      <div className="mt-3 p-3 bg-gray-50 rounded-lg">
        <div className="text-xs text-gray-600">
          <div className="font-medium mb-1">💡 입력 팁:</div>
          <ul className="space-y-1">
            <li>• 구체적인 예시와 경험을 포함해서 답변하세요</li>
            <li>• 기술적 용어는 정확하게 사용하세요</li>
            <li>• 음성 입력 시 또박또박 말씀해주세요</li>
            <li>• 답변 후 내용을 검토하고 수정할 수 있습니다</li>
          </ul>
        </div>
      </div>
    </div>
  )
}

export default EnhancedAnswerInput