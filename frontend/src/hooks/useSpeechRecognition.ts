import { useState, useRef, useCallback, useEffect } from 'react'

interface UseSpeechRecognitionOptions {
  language?: string
  continuous?: boolean
  interimResults?: boolean
  maxRetries?: number
}

interface SpeechRecognitionHook {
  isSupported: boolean
  isListening: boolean
  transcript: string
  confidence: number
  error: string | null
  startListening: () => void
  stopListening: () => void
  resetTranscript: () => void
}

export const useSpeechRecognition = (
  options: UseSpeechRecognitionOptions = {}
): SpeechRecognitionHook => {
  const {
    language = 'ko-KR',
    continuous = false,
    interimResults = true,
    maxRetries = 3
  } = options

  const [isSupported, setIsSupported] = useState(false)
  const [isListening, setIsListening] = useState(false)
  const [transcript, setTranscript] = useState('')
  const [confidence, setConfidence] = useState(0)
  const [error, setError] = useState<string | null>(null)

  const recognitionRef = useRef<SpeechRecognition | null>(null)
  const isStartingRef = useRef(false)
  const errorCountRef = useRef(0)
  const timeoutRef = useRef<NodeJS.Timeout | null>(null)

  // 브라우저 지원 확인
  const checkSupport = useCallback(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
    return !!SpeechRecognition
  }, [])

  // 음성 인식 초기화
  const initRecognition = useCallback(() => {
    if (!checkSupport()) return null

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
    const recognition = new SpeechRecognition()

    recognition.continuous = continuous
    recognition.interimResults = interimResults
    recognition.lang = language

    recognition.onstart = () => {
      isStartingRef.current = false
      errorCountRef.current = 0
      setIsListening(true)
      setError(null)
    }

    recognition.onresult = (event) => {
      let finalTranscript = ''
      let interimTranscript = ''

      for (let i = event.resultIndex; i < event.results.length; i++) {
        const result = event.results[i]
        const text = result[0].transcript

        if (result.isFinal) {
          finalTranscript += text
          setConfidence(result[0].confidence)
        } else {
          interimTranscript += text
        }
      }

      if (finalTranscript) {
        setTranscript(prev => prev + finalTranscript)
      }
    }

    recognition.onerror = (event) => {
      // aborted는 의도적 중단이므로 무시
      if (event.error === 'aborted') {
        return
      }
      
      isStartingRef.current = false
      errorCountRef.current++

      let errorMessage = '음성 인식 중 오류가 발생했습니다.'
      let shouldRetry = false

      switch (event.error) {
        case 'no-speech':
          // no-speech는 에러가 아니라 자동 재시도
          if (errorCountRef.current < maxRetries) {
            setTimeout(() => {
              if (!isListening) {
                startListening()
              }
            }, 500)
          }
          return
        case 'audio-capture':
          errorMessage = '마이크에 접근할 수 없습니다.'
          break
        case 'not-allowed':
          errorMessage = '마이크 사용 권한이 거부되었습니다.'
          break
        case 'network':
          errorMessage = '네트워크 오류가 발생했습니다.'
          shouldRetry = errorCountRef.current < maxRetries
          break
        default:
          return
      }

      setIsListening(false)
      
      if (!shouldRetry) {
        setError(errorMessage)
      } else {
        setTimeout(() => startListening(), 1000)
      }
    }

    recognition.onend = () => {
      isStartingRef.current = false
      setIsListening(false)
    }

    return recognition
  }, [language, continuous, interimResults, maxRetries])

  // 음성 인식 시작
  const startListening = useCallback(async () => {
    if (isStartingRef.current || isListening) return

    // 기존 인식 중지
    if (recognitionRef.current) {
      try {
        recognitionRef.current.abort()
      } catch (e) {}
    }

    // HTTPS 체크
    if (location.protocol !== 'https:' && location.hostname !== 'localhost') {
      setError('음성 인식은 HTTPS 환경에서만 사용할 수 있습니다.')
      return
    }

    // 마이크 권한 요청
    try {
      await navigator.mediaDevices.getUserMedia({ audio: true })
    } catch (permissionError) {
      setError('마이크 사용 권한이 필요합니다. 브라우저 설정에서 마이크 권한을 허용해주세요.')
      return
    }

    // 새로운 인식 객체 생성
    recognitionRef.current = initRecognition()

    if (!recognitionRef.current) {
      setError('음성 인식이 지원되지 않는 브라우저입니다.')
      return
    }

    try {
      isStartingRef.current = true
      errorCountRef.current = 0
      setError(null)
      
      // 짧은 지연 후 시작
      setTimeout(() => {
        if (recognitionRef.current && isStartingRef.current) {
          recognitionRef.current.start()
        }
      }, 100)
    } catch (err) {
      isStartingRef.current = false
      setError('음성 인식을 시작할 수 없습니다. 다시 시도해주세요.')
    }
  }, [initRecognition, isListening])

  // 음성 인식 중지
  const stopListening = useCallback(() => {
    isStartingRef.current = false
    
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current)
      timeoutRef.current = null
    }

    if (recognitionRef.current) {
      try {
        recognitionRef.current.stop()
        recognitionRef.current.abort()
      } catch (err) {}
      recognitionRef.current = null
    }

    setIsListening(false)
    setError(null)
  }, [])

  // 트랜스크립트 리셋
  const resetTranscript = useCallback(() => {
    setTranscript('')
    setConfidence(0)
    setError(null)
  }, [])

  // 초기화
  useEffect(() => {
    setIsSupported(checkSupport())

    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current)
      }
      if (recognitionRef.current) {
        try {
          recognitionRef.current.abort()
        } catch (err) {
          console.warn('음성 인식 정리 실패:', err)
        }
        recognitionRef.current = null
      }
    }
  }, [checkSupport])

  return {
    isSupported,
    isListening,
    transcript,
    confidence,
    error,
    startListening,
    stopListening,
    resetTranscript
  }
}