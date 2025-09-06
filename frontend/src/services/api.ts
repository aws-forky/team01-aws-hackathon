// Assumption: Using axios for HTTP requests with error handling
import axios from 'axios'
import { 
  UploadResponse, KeywordResponse, QuestionResponse, CompanyListResponse,
  InterviewFeedbackResponse, CompanyProfile, PortfolioAnalysis, PortfolioImprovement,
  FeedbackAnalysis, FollowUpQuestion, MainQuestion, FollowUpQuestionNew, Answer, InterviewSession
} from '../types'

const api = axios.create({
  baseURL: `${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}`,
  timeout: 60000, // 60초로 증가
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
})

// 요청/응답 인터셉터 추가
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`)
    return config
  },
  (error) => Promise.reject(error)
)

api.interceptors.response.use(
  (response) => {
    console.log(`API Response: ${response.status} ${response.config.url}`)
    return response
  },
  (error) => {
    console.error(`API Error: ${error.response?.status} ${error.config?.url}`, error.response?.data)
    return Promise.reject(error)
  }
)

export const apiService = {
  // =============================================================================
  // 문서 처리 API
  // =============================================================================
  async parseDocument(file: File): Promise<any> {
    try {
      const formData = new FormData()
      formData.append('file', file)
      
      const response = await api.post('/api/v2/documents/parse', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        timeout: 60000  // 60초 타임아웃
      })
      
      if (response.data.success) {
        return response.data
      } else {
        throw new Error(response.data.message || 'PDF 처리에 실패했습니다.')
      }
    } catch (error: any) {
      console.error('PDF parsing error:', error)
      // 에러를 그대로 전달하여 사용자가 재시도할 수 있도록 함
      throw new Error(error.response?.data?.message || error.message || 'PDF 처리 중 오류가 발생했습니다. 다시 시도해주세요.')
    }
  },

  // 레거시 지원
  async uploadFile(file: File): Promise<UploadResponse> {
    return this.parseDocument(file)
  },

  // =============================================================================
  // 키워드 추출 API
  // =============================================================================
  async extractKeywords(text: string, documentId?: string): Promise<any> {
    try {
      const response = await api.post('/api/v2/keywords/extract', { 
        text, 
        document_id: documentId || '' 
      })
      
      if (response.data.success) {
        return response.data
      } else {
        throw new Error(response.data.message || '키워드 추출에 실패했습니다.')
      }
    } catch (error: any) {
      console.error('Keyword extraction error:', error)
      
      // 네트워크 오류 처리
      if (error.code === 'ECONNREFUSED' || error.code === 'ENOTFOUND') {
        throw new Error('네트워크 연결 오류가 발생했습니다. 인터넷 연결을 확인해주세요.')
      }
      
      // 서버 오류 처리
      if (error.response?.status >= 500) {
        throw new Error('서버 내부 오류가 발생했습니다. 잠시 후 다시 시도해주세요.')
      }
      
      // 기타 오류
      throw new Error(error.response?.data?.message || error.message || '키워드 추출 중 오류가 발생했습니다. 다시 시도해주세요.')
    }
  },

  // =============================================================================
  // 질문 생성 API
  // =============================================================================
  async generateMainQuestions(portfolioText: string, companyInfo: string = '', jobPosition: string = '백엔드 개발자', questionCount: number = 5): Promise<any> {
    try {
      console.log('Generating questions with:', { portfolioTextLength: portfolioText.length, companyInfo, jobPosition })
      
      const response = await api.post('/api/v2/questions/generate', {
        portfolio_text: portfolioText,
        company_info: companyInfo,
        job_position: jobPosition,
        question_count: questionCount
      })
      
      console.log('Question generation response:', response.data)
      
      if (response.data && response.data.success) {
        return response.data
      } else {
        const errorMsg = response.data?.message || response.data?.error || '질문 생성에 실패했습니다.'
        throw new Error(errorMsg)
      }
    } catch (error: any) {
      console.error('Question generation error:', error)
      
      // 응답이 있지만 에러인 경우
      if (error.response) {
        const status = error.response.status
        const data = error.response.data
        
        if (status >= 500) {
          throw new Error('서버 내부 오류가 발생했습니다. 잠시 후 다시 시도해주세요.')
        } else if (status >= 400) {
          throw new Error(data?.message || data?.error || '요청 처리 중 오류가 발생했습니다.')
        }
      }
      
      // 네트워크 에러
      if (error.code === 'ECONNABORTED' || error.message.includes('timeout')) {
        throw new Error('서비스 응답 시간이 초과되었습니다. 잠시 후 다시 시도해주세요.')
      }
      
      if (error.code === 'ECONNREFUSED' || error.code === 'ENOTFOUND') {
        throw new Error('서버에 연결할 수 없습니다. 네트워크 연결을 확인해주세요.')
      }
      
      // 기타 에러
      throw new Error(error.message || '질문 생성 중 예상치 못한 오류가 발생했습니다.')
    }
  },

  async generateFollowingQuestions(mainQuestionId: string, mainQuestionContent: string, userAnswer: string, context: any = {}, followupCount: number = 3): Promise<any> {
    const response = await api.post('/api/v2/questions/following', {
      main_question_id: mainQuestionId,
      main_question_content: mainQuestionContent,
      user_answer: userAnswer,
      context,
      followup_count: followupCount
    })
    return response.data
  },

  // 레거시 지원
  async generateQuestions(keywords: string[], company: string, text: string = ''): Promise<QuestionResponse> {
    return this.generateMainQuestions(text, company)
  },

  // =============================================================================
  // 평가 API
  // =============================================================================
  async evaluateAnswer(questionId: string, questionContent: string, answerContent: string, questionType: string = 'main', answerMethod: string = 'text', context: any = {}): Promise<any> {
    const response = await api.post('/api/v2/questions/evaluate', {
      question_id: questionId,
      question_content: questionContent,
      answer_content: answerContent,
      question_type: questionType,
      answer_method: answerMethod,
      context
    })
    return response.data
  },

  async evaluateCompleteInterview(sessionId: string, interviewData: any, answers: any[], questions: any[], sessionInfo: any = {}): Promise<any> {
    const response = await api.post('/api/v2/evaluate/all', {
      session_id: sessionId,
      interview_data: interviewData,
      answers,
      questions,
      session_info: sessionInfo
    })
    return response.data
  },

  async evaluatePortfolio(portfolioText: string, targetCompany: string = '', targetPosition: string = '', evaluationCriteria: string[] = []): Promise<any> {
    const response = await api.post('/api/v2/evaluate/portfolio', {
      portfolio_text: portfolioText,
      target_company: targetCompany,
      target_position: targetPosition,
      evaluation_criteria: evaluationCriteria
    })
    return response.data
  },

  // =============================================================================
  // 시스템 API
  // =============================================================================
  async checkSystemHealth(): Promise<any> {
    const response = await api.get('/api/v2/health')
    return response.data
  },

  async getCompanies(): Promise<CompanyListResponse> {
    // 임시 데이터 반환 (추후 별도 API로 분리 예정)
    return {
      success: true,
      companies: [
        { name: '네이버', description: '국내 최대 포털 및 IT 서비스 기업', tech_stack: ['Java', 'Spring', 'React'] },
        { name: '카카오', description: '모바일 메신저 및 플랫폼 서비스 기업', tech_stack: ['Kotlin', 'Swift', 'React'] },
        { name: '삼성전자', description: '글로벌 전자제품 및 반도체 기업', tech_stack: ['C++', 'Python', 'Android'] },
        { name: 'AWS', description: '클라우드 컴퓨팅 서비스를 제공하는 글로벌 IT 기업', tech_stack: ['Python', 'Java', 'AWS Lambda', 'DynamoDB', 'S3'] }
      ]
    }
  },

  // =============================================================================
  // 새로운 기능 API 메서드들
  // =============================================================================

  async startInterviewSession(company: string, position: string = '백엔드 개발자', 
                             interviewer_persona: string = '친근한_시니어'): Promise<any> {
    const response = await api.post('/interview/start', {
      company,
      position,
      interviewer_persona
    })
    return response.data
  },

  async processInterviewInteraction(session_id: string, user_answer: string, context: any): Promise<InterviewFeedbackResponse> {
    const response = await api.post<InterviewFeedbackResponse>('/interview/process', {
      session_id,
      user_answer,
      context
    })
    return response.data
  },

  async analyzeFeedback(question: string, answer: string, user_level: string = 'intermediate'): Promise<{ success: boolean; feedback: FeedbackAnalysis }> {
    const response = await api.post('/feedback/analyze', {
      question,
      answer,
      user_level
    })
    return response.data
  },

  async generateFollowUpQuestions(question: string, answer: string, 
                                 interviewer_persona: string = '친근한_시니어',
                                 max_questions: number = 2,
                                 portfolio_text: string = ''): Promise<{ success: boolean; follow_up_questions: FollowUpQuestion[] }> {
    const response = await api.post('/follow-up/generate', {
      question,
      answer,
      interviewer_persona,
      max_questions,
      portfolio_text
    })
    return response.data
  },

  async getCompanyProfile(company_name: string): Promise<{ success: boolean; profile: CompanyProfile }> {
    const response = await api.get(`/companies/${encodeURIComponent(company_name)}/profile`)
    return response.data
  },

  async generateCompanyCustomizedQuestions(company: string, user_keywords: string[]): Promise<any> {
    const response = await api.post('/companies/questions/customized', {
      company,
      user_keywords
    })
    return response.data
  },

  async analyzePortfolio(portfolio_text: string, target_company: string = '', 
                        target_position: string = ''): Promise<{ success: boolean; analysis: PortfolioAnalysis; improvements: PortfolioImprovement[] }> {
    const response = await api.post('/portfolio/analyze', {
      portfolio_text,
      target_company,
      target_position
    })
    return response.data
  },

  async optimizePortfolioForCompany(portfolioText: string, targetCompany: string): Promise<any> {
    return this.evaluatePortfolio(portfolioText, targetCompany)
  },

  // =============================================================================
  // 레거시 API 지원 (호환성 유지)
  // =============================================================================
  async generateStructuredQuestions(portfolioText: string, companyInfo: string = '', jobPosition: string = '백엔드 개발자'): Promise<any> {
    return this.generateMainQuestions(portfolioText, companyInfo, jobPosition)
  },

  async generateFollowupQuestions(mainQuestionId: string, mainQuestionContent: string, userAnswer: string, followupCount: number = 3): Promise<any> {
    return this.generateFollowingQuestions(mainQuestionId, mainQuestionContent, userAnswer, {}, followupCount)
  },

  async generateFinalReport(sessionId: string, answers: any[], mainQuestions: any[]): Promise<any> {
    return this.evaluateCompleteInterview(sessionId, {}, answers, mainQuestions)
  },

  async speechToText(audioData: any): Promise<any> {
    // 현재는 프론트엔드에서 Web Speech API 사용
    // 필요시 외부 STT 서비스 연동용
    return {
      success: false,
      message: '현재 프론트엔드에서 Web Speech API를 사용합니다'
    }
  }
}

// =============================================================================
// 전용 API 그룹화
// =============================================================================

// 문서 처리 API
export const documentAPI = {
  parse: apiService.parseDocument,
  // 레거시
  upload: apiService.uploadFile
}

// 키워드 API
export const keywordAPI = {
  extract: apiService.extractKeywords
}

// 질문 API
export const questionAPI = {
  generateMain: apiService.generateMainQuestions,
  generateFollowing: apiService.generateFollowingQuestions,
  // 레거시
  generate: apiService.generateQuestions
}

// 평가 API
export const evaluationAPI = {
  evaluateAnswer: apiService.evaluateAnswer,
  evaluateInterview: apiService.evaluateCompleteInterview,
  evaluatePortfolio: apiService.evaluatePortfolio
}

// 시스템 API
export const systemAPI = {
  health: apiService.checkSystemHealth
}

// 구조화된 질문 시스템 전용 API (호환성 유지)
export const structuredInterviewAPI = {
  generateMainQuestions: apiService.generateMainQuestions,
  generateFollowUpQuestions: apiService.generateFollowingQuestions,
  evaluateAnswer: apiService.evaluateAnswer,
  generateFinalReport: apiService.generateFinalReport
}

// 기존 API와의 호환성을 위한 별칭
export const generateFollowUpQuestions = apiService.generateFollowingQuestions
export const evaluateAnswer = apiService.evaluateAnswer
