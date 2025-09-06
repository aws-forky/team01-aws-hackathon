// Assumption: Matching backend models for type safety
export interface Keyword {
  name: string
  category: 'language' | 'framework' | 'tool' | 'database' | 'cloud'
  importance: number
}

export interface Question {
  question: string
  answer: string
  type: 'technical' | 'behavioral' | 'situational'
  difficulty: 'beginner' | 'intermediate' | 'advanced'
}

export interface Company {
  name: string
  description: string
  tech_stack: string[]
}

export interface UploadResponse {
  success: boolean
  file_id: string
  extracted_text: string
  message: string
}

export interface KeywordResponse {
  success: boolean
  keywords: Keyword[]
  is_fallback: boolean
  message: string
}

export interface QuestionResponse {
  success: boolean
  questions: Question[]
  is_fallback: boolean
  fallback_reason?: string
  message: string
}

export interface CompanyListResponse {
  success: boolean
  companies: Company[]
}

export interface AppState {
  extractedText: string
  keywords: Keyword[]
  selectedCompany: string
  questions: Question[]
  currentStep: number
}

// 향상된 기능들을 위한 새로운 타입 정의

// 구조화된 질문 시스템
export interface MainQuestion {
  id: string
  title: string
  content: string
  category: string
  difficulty: 'Easy' | 'Medium' | 'Hard'
  estimatedTime: number // 예상 답변 시간 (분)
  isCompleted: boolean
}

export interface FollowUpQuestionNew {
  id: string
  parentQuestionId: string
  content: string
  order: number // 1, 2, 3 순서
  basedOnAnswer?: string // 이전 답변 기반 생성된 경우
  aiGenerated?: boolean // AI 기반 개인화 질문인지
  reasoning?: string // AI 생성 근거
}

export interface Answer {
  id: string
  questionId: string
  questionType: 'main' | 'followup'
  content: string
  inputMethod: 'text' | 'voice'
  timestamp: Date
  duration: number // 답변 시간 (초)
  feedback?: FeedbackAnalysis
}

export interface InterviewSession {
  id: string
  mainQuestions: MainQuestion[]
  currentMainQuestionId: string | null
  followUpQuestions: FollowUpQuestionNew[]
  completedMainQuestions: string[]
  answers: Answer[]
  startTime: Date
  currentStep: 'selection' | 'main-answer' | 'followup' | 'completed'
  currentFollowUpIndex: number // 현재 꼬리 질문 인덱스 (0, 1, 2)
}

// 음성 인식 관련
export interface VoiceRecognitionState {
  isSupported: boolean
  isListening: boolean
  transcript: string
  confidence: number
  error: string | null
}

export interface SpeechRecognitionResult {
  transcript: string
  confidence: number
  isFinal: boolean
}

// PDF 생성 관련
export interface InterviewReport {
  sessionId: string
  completedAt: Date
  totalDuration: number
  totalQuestions: number
  averageScore: number
  categoryScores: Record<string, number>
  strengths: string[]
  weaknesses: string[]
  recommendations: string[]
  detailedResults: Array<{
    mainQuestion: MainQuestion
    mainAnswer: Answer
    followUpResults: Array<{
      question: FollowUpQuestionNew
      answer: Answer
    }>
  }>
}

// 기존 타입 정의
export interface FeedbackAnalysis {
  overall_score: number
  star_analysis: {
    situation: { present: boolean; quality: string; suggestion: string | null }
    task: { present: boolean; quality: string; suggestion: string | null }
    action: { present: boolean; quality: string; suggestion: string | null }
    result: { present: boolean; quality: string; suggestion: string | null }
  }
  technical_accuracy: {
    score: number
    correct_concepts: string[]
    missing_details: string[]
  }
  improvement_suggestions: string[]
  strengths: string[]
  next_steps: string[]
}

export interface FollowUpQuestion {
  question: string
  type: 'deepening' | 'alternative' | 'problem' | 'scaling' | 'business'
  intent: string
  difficulty: 'beginner' | 'intermediate' | 'advanced'
  expected_keywords: string[]
}

export interface InterviewFeedbackResponse {
  success: boolean
  feedback: FeedbackAnalysis
  follow_up_questions: FollowUpQuestion[]
  portfolio_insight?: {
    category: string
    suggestion: string
    priority: 'high' | 'medium' | 'low'
  }
  interviewer_response: string
  next_action: 'continue' | 'deep_dive' | 'new_topic'
}

export interface CompanyProfile {
  name: string
  industry: string
  size: string
  tech_stack: string[]
  culture_keywords: string[]
  interview_style: {
    approach: string
    duration: string
    difficulty: string
    evaluation_weight: {
      technical_depth: number
      problem_solving: number
      communication: number
      culture_fit: number
    }
  }
  typical_questions: Array<{
    category: string
    question: string
    intent: string
    difficulty: string
  }>
  success_tips: string[]
  red_flags: string[]
}

export interface PortfolioAnalysis {
  overall_score: number
  target_score: number
  market_fit: number
  detailed_analysis: {
    technical_skills: {
      present_skills: string[]
      missing_skills: string[]
      skill_depth_score: number
    }
    project_descriptions: {
      clarity_score: number
      quantification_score: number
      star_usage: number
    }
  }
  company_specific_advice: string
}

export interface PortfolioImprovement {
  category: string
  priority: 'high' | 'medium' | 'low'
  suggestion: string
  example: string
  impact: 'high' | 'medium' | 'low'
  effort: 'high' | 'medium' | 'low'
  timeline: string
}

export interface InterviewSession {
  session_id: string
  company: string
  position: string
  interviewer_persona: string
  current_question_depth: number
  max_depth: number
  questions_asked: Array<{
    question: string
    answer: string
    feedback: FeedbackAnalysis
    follow_ups: FollowUpQuestion[]
  }>
  session_status: 'active' | 'paused' | 'completed'
}

export interface EnhancedQuestion extends Question {
  follow_ups?: FollowUpQuestion[]
  feedback?: FeedbackAnalysis
  company_relevance?: string
}
