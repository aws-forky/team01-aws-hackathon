import React, { useEffect, useCallback } from 'react'
import { useSpeechRecognition } from '../hooks/useSpeechRecognition'

interface VoiceRecorderProps {
  onTranscript: (text: string) => void
  onError?: (error: string) => void
  isActive: boolean
  className?: string
  language?: string
}

const VoiceRecorder: React.FC<VoiceRecorderProps> = ({
  onTranscript,
  onError,
  isActive,
  className = '',
  language = 'ko-KR'
}) => {
  const {
    isSupported,
    isListening,
    transcript,
    confidence,
    error,
    startListening,
    stopListening,
    resetTranscript
  } = useSpeechRecognition({
    language,
    continuous: false,
    interimResults: true,
    maxRetries: 2
  })

  // 트랜스크립트 변화 감지하여 부모에게 전달
  useEffect(() => {
    if (transcript) {
      onTranscript(transcript)
      resetTranscript() // 전달 후 리셋
    }
  }, [transcript, onTranscript, resetTranscript])

  // 에러 발생 시 부모에게 전달
  useEffect(() => {
    if (error && onError) {
      onError(error)
    }
  }, [error, onError])

  // isActive 상태에 따른 음성 인식 제어
  useEffect(() => {
    if (isActive && isSupported) {
      startListening()
    } else {
      stopListening()
    }
  }, [isActive, isSupported, startListening, stopListening])

  // 수동 제어 함수
  const handleToggle = useCallback(() => {
    if (isListening) {
      stopListening()
    } else {
      startListening()
    }
  }, [isListening, startListening, stopListening])

  // 브라우저 지원하지 않는 경우
  if (!isSupported) {
    return (
      <div className={`voice-recorder-error ${className}`}>
        <div className="flex flex-col items-center space-y-2 text-red-600 p-4 bg-red-50 rounded-lg border border-red-200">
          <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <div className="text-center">
            <div className="text-sm font-medium">음성 인식이 지원되지 않는 브라우저입니다</div>
            <div className="text-xs text-red-500 mt-1">
              Chrome, Edge, Safari 등의 최신 브라우저를 사용해주세요.
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className={`voice-recorder ${className}`}>
      <div className="flex items-center space-x-3">
        {/* 마이크 버튼 */}
        <button
          type="button"
          onClick={handleToggle}
          disabled={!!error}
          className={`
            relative p-3 rounded-full transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2
            ${isListening 
              ? 'bg-red-500 text-white focus:ring-red-500 animate-pulse' 
              : 'bg-blue-500 text-white hover:bg-blue-600 focus:ring-blue-500'
            }
            ${error ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
          `}
          title={isListening ? '음성 인식 중지' : '음성 인식 시작'}
        >
          {isListening ? (
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 10a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1v-4z" />
            </svg>
          ) : (
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
            </svg>
          )}
          
          {/* 녹음 중 애니메이션 */}
          {isListening && (
            <div className="absolute inset-0 rounded-full border-2 border-white animate-ping"></div>
          )}
        </button>

        {/* 상태 표시 */}
        <div className="flex flex-col">
          <span className={`text-sm font-medium ${isListening ? 'text-red-600' : 'text-gray-600'}`}>
            {isListening ? '음성 인식 중...' : '음성 입력 대기'}
          </span>
          
          {confidence > 0 && (
            <span className="text-xs text-gray-500">
              정확도: {Math.round(confidence * 100)}%
            </span>
          )}
        </div>

        {/* 음성 파형 시각화 (간단한 애니메이션) */}
        {isListening && (
          <div className="flex items-center space-x-1">
            {[...Array(5)].map((_, i) => (
              <div
                key={i}
                className="w-1 bg-blue-500 rounded-full animate-pulse"
                style={{
                  height: `${Math.random() * 20 + 10}px`,
                  animationDelay: `${i * 0.1}s`,
                  animationDuration: '0.5s'
                }}
              />
            ))}
          </div>
        )}
      </div>

      {/* 에러 메시지 */}
      {error && (
        <div className="mt-3 p-3 bg-red-50 border border-red-200 rounded-lg">
          <div className="flex items-start space-x-2">
            <svg className="w-5 h-5 text-red-500 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <div className="flex-1">
              <div className="text-sm text-red-700 font-medium mb-1">음성 인식 오류</div>
              <div className="text-sm text-red-600 mb-2">{error}</div>
              
              {/* 해결 방법 안내 */}
              <div className="text-xs text-red-500 space-y-1">
                {error.includes('권한') && (
                  <div>• 브라우저 주소창 왼쪽의 마이크 아이콘을 클릭하여 권한을 허용해주세요</div>
                )}
                {error.includes('HTTPS') && (
                  <div>• 보안 연결(HTTPS)이 필요합니다</div>
                )}
                {error.includes('마이크') && (
                  <div>• 마이크가 제대로 연결되어 있는지 확인해주세요</div>
                )}
                <div>• 텍스트 입력으로 대체할 수 있습니다</div>
              </div>
              
              <div className="flex space-x-2 mt-2">
                <button
                  onClick={startListening}
                  className="text-xs bg-red-100 text-red-700 px-2 py-1 rounded hover:bg-red-200 transition-colors"
                >
                  다시 시도
                </button>
                <button
                  onClick={() => window.location.reload()}
                  className="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded hover:bg-gray-200 transition-colors"
                >
                  페이지 새로고침
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* 사용법 안내 */}
      {!isListening && !error && (
        <div className="mt-3 p-2 bg-blue-50 border border-blue-200 rounded-lg">
          <div className="text-xs text-blue-700 space-y-1">
            <div className="font-medium">🎤 음성 입력 안내</div>
            <div>• 마이크 버튼을 클릭하고 또박또박 말씨해주세요</div>
            <div>• 음성 인식이 완료되면 자동으로 텍스트로 변환됩니다</div>
            <div>• 처음 사용 시 마이크 권한 허용이 필요합니다</div>
          </div>
        </div>
      )}
    </div>
  )
}

export default VoiceRecorder