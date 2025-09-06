import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';
import { InterviewSession, FeedbackAnalysis, FollowUpQuestion, CompanyProfile } from '../types';
import RealTimeFeedback from './RealTimeFeedback';
import FollowUpQuestions from './FollowUpQuestions';

interface InterviewSimulatorProps {
  company: string;
  portfolioText: string;
  keywords: string[];
}

const InterviewSimulator: React.FC<InterviewSimulatorProps> = ({ 
  company, 
  portfolioText, 
  keywords 
}) => {
  const [session, setSession] = useState<InterviewSession | null>(null);
  const [companyProfile, setCompanyProfile] = useState<CompanyProfile | null>(null);
  const [currentQuestion, setCurrentQuestion] = useState<string>('');
  const [userAnswer, setUserAnswer] = useState<string>('');
  const [feedback, setFeedback] = useState<FeedbackAnalysis | null>(null);
  const [followUpQuestions, setFollowUpQuestions] = useState<FollowUpQuestion[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [interviewerPersona, setInterviewerPersona] = useState<string>('친근한_시니어');
  const [showFeedback, setShowFeedback] = useState<boolean>(false);
  const [interviewerComment, setInterviewerComment] = useState<string>('');

  const personas = [
    { value: '친근한_시니어', label: '친근한 시니어 개발자', description: '격려하며 깊이 파는 스타일' },
    { value: '까다로운_테크리드', label: '까다로운 테크리드', description: '기술적 정확성 중시' },
    { value: '비즈니스_중심_매니저', label: '비즈니스 중심 매니저', description: '비즈니스 임팩트 중시' }
  ];

  useEffect(() => {
    initializeInterview();
  }, [company]);

  const initializeInterview = async () => {
    try {
      setIsLoading(true);
      
      // 면접 세션 시작
      const sessionResponse = await apiService.startInterviewSession(company, '백엔드 개발자', interviewerPersona);
      setSession(sessionResponse.session_id);
      setCompanyProfile(sessionResponse.company_profile);
      
      // 회사별 맞춤 질문 생성
      const questionsResponse = await apiService.generateCompanyCustomizedQuestions(company, keywords);
      if (questionsResponse.success && questionsResponse.customized_questions.length > 0) {
        setCurrentQuestion(questionsResponse.customized_questions[0].question);
      }
      
    } catch (error) {
      console.error('면접 초기화 실패:', error);
      setCurrentQuestion('자기소개를 해주세요.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleAnswerSubmit = async () => {
    if (!userAnswer.trim() || !session) return;

    try {
      setIsLoading(true);
      
      const context = {
        current_question: currentQuestion,
        user_level: 'intermediate',
        interviewer_persona: interviewerPersona,
        portfolio_text: portfolioText,
        target_company: company,
        question_depth: 1
      };

      // 통합 면접 상호작용 처리
      const response = await apiService.processInterviewInteraction(session, userAnswer, context);
      
      if (response.success) {
        setFeedback(response.feedback);
        setFollowUpQuestions(response.follow_up_questions || []);
        setInterviewerComment(response.interviewer_response || '');
        setShowFeedback(true);
      }
      
    } catch (error) {
      console.error('답변 처리 실패:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFollowUpSelect = (question: FollowUpQuestion) => {
    setCurrentQuestion(question.question);
    setUserAnswer('');
    setShowFeedback(false);
    setFeedback(null);
    setFollowUpQuestions([]);
  };

  const handleNewQuestion = async () => {
    try {
      setIsLoading(true);
      const questionsResponse = await apiService.generateCompanyCustomizedQuestions(company, keywords);
      if (questionsResponse.success && questionsResponse.customized_questions.length > 0) {
        const randomIndex = Math.floor(Math.random() * questionsResponse.customized_questions.length);
        setCurrentQuestion(questionsResponse.customized_questions[randomIndex].question);
        setUserAnswer('');
        setShowFeedback(false);
        setFeedback(null);
        setFollowUpQuestions([]);
      }
    } catch (error) {
      console.error('새 질문 생성 실패:', error);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading && !currentQuestion) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">면접을 준비하고 있습니다...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto p-6 space-y-6">
      {/* 헤더 */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex justify-between items-start mb-4">
          <div>
            <h1 className="text-3xl font-bold text-gray-800">{company} 기술면접 시뮬레이션</h1>
            <p className="text-gray-600 mt-2">AI 면접관과 실제 면접을 연습해보세요</p>
          </div>
          <div className="text-right">
            <label className="block text-sm font-medium text-gray-700 mb-2">면접관 스타일</label>
            <select
              value={interviewerPersona}
              onChange={(e) => setInterviewerPersona(e.target.value)}
              className="border border-gray-300 rounded-md px-3 py-2 text-sm"
            >
              {personas.map(persona => (
                <option key={persona.value} value={persona.value}>
                  {persona.label}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* 회사 정보 */}
        {companyProfile && (
          <div className="bg-blue-50 rounded-lg p-4 mb-4">
            <h3 className="font-semibold text-blue-800 mb-2">면접 정보</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
              <div>
                <span className="font-medium">면접 스타일:</span> {companyProfile.interview_style.approach}
              </div>
              <div>
                <span className="font-medium">예상 시간:</span> {companyProfile.interview_style.duration}
              </div>
              <div>
                <span className="font-medium">주요 기술:</span> {companyProfile.tech_stack.slice(0, 3).join(', ')}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* 현재 질문 */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex justify-between items-start mb-4">
          <h2 className="text-xl font-semibold text-gray-800">면접 질문</h2>
          <button
            onClick={handleNewQuestion}
            disabled={isLoading}
            className="px-4 py-2 bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200 disabled:opacity-50"
          >
            새 질문
          </button>
        </div>
        
        <div className="bg-blue-50 rounded-lg p-4 mb-6">
          <p className="text-lg text-gray-800">{currentQuestion}</p>
        </div>

        {/* 면접관 코멘트 */}
        {interviewerComment && (
          <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-6">
            <div className="flex">
              <div className="ml-3">
                <p className="text-sm text-yellow-700">
                  <strong>면접관:</strong> {interviewerComment}
                </p>
              </div>
            </div>
          </div>
        )}

        {/* 답변 입력 */}
        <div className="space-y-4">
          <label className="block text-sm font-medium text-gray-700">
            답변을 입력하세요 (STAR 기법 권장: 상황 → 과제 → 행동 → 결과)
          </label>
          <textarea
            value={userAnswer}
            onChange={(e) => setUserAnswer(e.target.value)}
            placeholder="구체적인 경험과 예시를 바탕으로 답변해주세요..."
            className="w-full h-32 p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            disabled={isLoading}
          />
          <button
            onClick={handleAnswerSubmit}
            disabled={isLoading || !userAnswer.trim()}
            className="w-full bg-blue-600 text-white py-3 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? '분석 중...' : '답변 제출'}
          </button>
        </div>
      </div>

      {/* 실시간 피드백 */}
      {showFeedback && feedback && (
        <RealTimeFeedback 
          feedback={feedback} 
          onClose={() => setShowFeedback(false)}
        />
      )}

      {/* 꼬리질문 */}
      {followUpQuestions.length > 0 && (
        <FollowUpQuestions
          questions={followUpQuestions}
          onQuestionSelect={handleFollowUpSelect}
        />
      )}

      {/* 면접 팁 */}
      {companyProfile && companyProfile.success_tips.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">💡 {company} 면접 성공 팁</h3>
          <ul className="space-y-2">
            {companyProfile.success_tips.map((tip, index) => (
              <li key={index} className="flex items-start">
                <span className="text-green-500 mr-2">•</span>
                <span className="text-gray-700">{tip}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default InterviewSimulator;