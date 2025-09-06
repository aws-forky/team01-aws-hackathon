import React, { useState, useEffect, useRef, useCallback } from 'react'
import { VoiceRecognitionState, SpeechRecognitionResult } from '../types'

interface VoiceRecorderProps {
  onTranscript: (text: string) => void
  onError?: (error: string) => void
  isActive: boolean
  className?: string
  language?: string
}

// Web Speech API 타입 확장
declare global {
  interface Window {
    SpeechRecognition: typeof SpeechRecognition
    webkitSpeechRecognition: typeof SpeechRecognition
  }
}

interface SpeechRecognition extends EventTarget {
  continuous: boolean
  interimResults: boolean
  lang: string
  start(): void
  stop(): void
  abort(): void
}

interface SpeechRecognitionEvent extends Event {
  results: SpeechRecognitionResultList
  resultIndex: number
}

const VoiceRecorder: React.FC<VoiceRecorderProps> = ({
  onTranscript,
  onError,
  isActive,
  className = '',
  language = 'ko-KR'
}) => {
  const [voiceState, setVoiceState] = useState<VoiceRecognitionState>({
    isSupported: false,
    isListening: false,
    transcript: '',
    confidence: 0,
    error: null
  })

  const recognitionRef = useRef<SpeechRecognition | null>(null)
  const timeoutRef = useRef<NodeJS.Timeout | null>(null)

  // 브라우저 호환성 체크
  const checkBrowserSupport = useCallback((): boolean => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
    return !!SpeechRecognition
  }, [])

  // 음성 인식 초기화
  const initializeSpeechRecognition = useCallback(() => {
    if (!checkBrowserSupport()) {
      setVoiceState(prev => ({
        ...prev,
        isSupported: false,
        error: '이 브라우저는 음성 인식을 지원하지 않습니다. Chrome, Edge, Safari를 사용해주세요.'
      }))
      return null
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
    const recognition = new SpeechRecognition()

    // 음성 인식 설정
    recognition.continuous = true
    recognition.interimResults = true
    recognition.lang = language

    // 이벤트 핸들러 설정
    recognition.onstart = () => {
      setVoiceState(prev => ({
        ...prev,
        isListening: true,
        error: null
      }))
    }

    recognition.onresult = (event: SpeechRecognitionEvent) => {
      let finalTranscript = ''
      let interimTranscript = ''

      for (let i = event.resultIndex; i < event.results.length; i++) {
        const result = event.results[i]
        const transcript = result[0].transcript

        if (result.isFinal) {
          finalTranscript += transcript
          setVoiceState(prev => ({
            ...prev,
            confidence: result[0].confidence,
            transcript: finalTranscript
          }))
        } else {
          interimTranscript += transcript
        }
      }

      // 최종 결과가 있으면 부모 컴포넌트에 전달
      if (finalTranscript) {
        onTranscript(finalTranscript.trim())
      }
    }

    recognition.onerror = (event: any) => {
      let errorMessage = '음성 인식 중 오류가 발생했습니다.'
      
      switch (event.error) {
        case 'no-speech':
          errorMessage = '음성이 감지되지 않았습니다. 다시 시도해주세요.'
          break
        case 'audio-capture':
          errorMessage = '마이크에 접근할 수 없습니다. 마이크 권한을 확인해주세요.'
          break
        case 'not-allowed':
          errorMessage = '마이크 사용 권한이 거부되었습니다. 브라우저 설정에서 마이크 권한을 허용해주세요.'
          break
        case 'network':
          errorMessage = '네트워크 오류로 음성 인식에 실패했습니다.'
          break
        case 'service-not-allowed':
          errorMessage = '음성 인식 서비스를 사용할 수 없습니다.'
          break
      }

      setVoiceState(prev => ({
        ...prev,
        isListening: false,
        error: errorMessage
      }))

      if (onError) {
        onError(errorMessage)
      }
    }

    recognition.onend = () => {
      setVoiceState(prev => ({
        ...prev,
        isListening: false
      }))

      // 자동 재시작 (활성 상태이고 에러가 없는 경우)
      if (isActive && !voiceState.error) {
        setTimeout(() => {
          if (recognitionRef.current && isActive) {
            try {
              recognitionRef.current.start()
            } catch (error) {
              console.warn('음성 인식 재시작 실패:', error)
            }
          }
        }, 100)
      }
    }

    return recognition
  }, [language, onTranscript, onError, isActive, voiceState.error])

  // 음성 인식 시작
  const startListening = useCallback(() => {
    if (!recognitionRef.current) {
      recognitionRef.current = initializeSpeechRecognition()
    }

    if (recognitionRef.current && !voiceState.isListening) {
      try {
        recognitionRef.current.start()
      } catch (error) {
        console.error('음성 인식 시작 실패:', error)
        setVoiceState(prev => ({
          ...prev,
          error: '음성 인식을 시작할 수 없습니다.'
        }))
      }
    }
  }, [initializeSpeechRecognition, voiceState.isListening])

  // 음성 인식 중지
  const stopListening = useCallback(() => {
    if (recognitionRef.current && voiceState.isListening) {
      recognitionRef.current.stop()
    }
  }, [voiceState.isListening])

  // 컴포넌트 초기화
  useEffect(() => {
    setVoiceState(prev => ({
      ...prev,
      isSupported: checkBrowserSupport()
    }))

    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.abort()
      }
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current)
      }
    }
  }, [checkBrowserSupport])

  // isActive 상태 변화에 따른 음성 인식 제어
  useEffect(() => {
    if (isActive && voiceState.isSupported && !voiceState.error) {
      startListening()
    } else {
      stopListening()
    }
  }, [isActive, voiceState.isSupported, voiceState.error, startListening, stopListening])

  // 브라우저 지원하지 않는 경우
  if (!voiceState.isSupported) {
    return (
      <div className={`voice-recorder-error ${className}`}>
        <div className="flex items-center space-x-2 text-red-600">
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span className="text-sm">음성 인식이 지원되지 않는 브라우저입니다</span>
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
          onClick={isActive ? stopListening : startListening}
          disabled={!!voiceState.error}
          className={`
            relative p-3 rounded-full transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2
            ${voiceState.isListening 
              ? 'bg-red-500 text-white focus:ring-red-500 animate-pulse' 
              : 'bg-blue-500 text-white hover:bg-blue-600 focus:ring-blue-500'
            }
            ${voiceState.error ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
          `}
          title={voiceState.isListening ? '음성 인식 중지' : '음성 인식 시작'}
        >
          {voiceState.isListening ? (
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
          {voiceState.isListening && (
            <div className="absolute inset-0 rounded-full border-2 border-white animate-ping"></div>
          )}
        </button>

        {/* 상태 표시 */}
        <div className="flex flex-col">
          <span className={`text-sm font-medium ${voiceState.isListening ? 'text-red-600' : 'text-gray-600'}`}>
            {voiceState.isListening ? '음성 인식 중...' : '음성 입력 대기'}
          </span>
          
          {voiceState.confidence > 0 && (
            <span className="text-xs text-gray-500">
              정확도: {Math.round(voiceState.confidence * 100)}%
            </span>
          )}
        </div>

        {/* 음성 파형 시각화 (간단한 애니메이션) */}
        {voiceState.isListening && (
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
      {voiceState.error && (
        <div className="mt-2 p-2 bg-red-50 border border-red-200 rounded-md">
          <div className="flex items-center space-x-2 text-red-700">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span className="text-sm">{voiceState.error}</span>
          </div>
        </div>
      )}

      {/* 사용법 안내 */}
      {!voiceState.isListening && !voiceState.error && (
        <div className="mt-2 text-xs text-gray-500">
          마이크 버튼을 클릭하여 음성으로 답변하세요
        </div>
      )}
    </div>
  )
}

export default VoiceRecorder