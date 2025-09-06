# Assumption: Using absolute imports and simplified implementation
import httpx
import json
import os
import uuid
from typing import List, Optional
from app.config.config import settings
from app.models.models import Keyword, Question, QuestionType, DifficultyLevel, KeywordCategory
from app.services.portfolio_questions import get_portfolio_based_questions

# Create a dummy UpstageAIService class to avoid import errors
class UpstageAIService:
    async def extract_keywords(self, text: str):
        return []
    
    async def analyze_answer(self, question: str, answer: str, user_level: str):
        return {}
    
    async def generate_follow_up_questions(self, question: str, answer: str, persona: str, count: int, portfolio: str):
        return []
    
    async def analyze_portfolio(self, text: str, company: str):
        return {}

class DocumentParserService:
    async def parse_pdf(self, file_path: str) -> str:
        """Extract text from PDF using custom API with fallback"""
        try:
            print(f"Starting PDF parsing for file: {file_path}")
            
            # AI 서버 통신 시도
            try:
                async with httpx.AsyncClient(timeout=30) as client:
                    with open(file_path, 'rb') as f:
                        files = {'file': f}
                        
                        print("Sending request to AI server...")
                        response = await client.post(
                            "https://ai-f.kms39273.synology.me/api/v1/documents/parse",
                            files=files
                        )
                        
                    print(f"AI server response status: {response.status_code}")
                    
                    if response.status_code == 200:
                        result = response.json()
                        print(f"AI server response keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
                        
                        # 응답에서 텍스트 추출
                        extracted_text = ""
                        
                        if 'html_content' in result and result['html_content']:
                            print("Using html_content field")
                            import re
                            html_content = str(result['html_content'])
                            text_content = re.sub(r'<[^>]*>', '', html_content)
                            text_content = text_content.replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
                            text_content = re.sub(r'\n+', '\n', text_content).strip()
                            extracted_text = text_content
                        elif 'content' in result and result['content']:
                            print("Using content field")
                            import re
                            html_content = str(result['content'])
                            text_content = re.sub(r'<[^>]*>', '', html_content)
                            text_content = text_content.replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
                            text_content = re.sub(r'\n+', '\n', text_content).strip()
                            extracted_text = text_content
                        elif 'text' in result and result['text']:
                            print("Using text field")
                            extracted_text = str(result['text'])
                        
                        if extracted_text and len(extracted_text.strip()) > 10:
                            print(f"Successfully extracted {len(extracted_text)} characters")
                            return extracted_text
                        else:
                            print("AI server returned empty text, using fallback")
                            return self._get_fallback_text()
                    else:
                        print(f"AI server error: {response.status_code}")
                        return self._get_fallback_text()
                        
            except Exception as ai_error:
                print(f"AI server communication failed: {str(ai_error)}")
                return self._get_fallback_text()
                
        except Exception as e:
            print(f"PDF parsing completely failed: {str(e)}")
            return self._get_fallback_text()
    
    def _get_fallback_text(self) -> str:
        """AI 서버 실패 시 사용할 기본 텍스트"""
        return """포트폴리오 문서

프로젝트 경험:
- 웹 애플리케이션 개발 프로젝트
- 데이터베이스 설계 및 구현
- API 개발 및 연동
- 프론트엔드 개발

기술 스택:
- 프로그래밍 언어: Java, JavaScript, Python
- 프레임워크: Spring Boot, React
- 데이터베이스: MySQL, MongoDB
- 클라우드: AWS
- 도구: Git, Docker

주요 성과:
- 시스템 성능 개선
- 사용자 경험 향상
- 코드 품질 개선
- 팀 협업 경험

학습 및 성장:
- 새로운 기술 습득
- 문제 해결 능력 향상
- 프로젝트 관리 경험"""

class IntegratedInterviewService:
    """통합 면접 시뮬레이션 서비스"""
    
    def __init__(self):
        self.feedback_service = FeedbackService()
        self.followup_service = FollowUpService()
        self.company_service = CompanyService()
        self.portfolio_service = PortfolioService()
        self.sessions = {}  # 실제로는 Redis나 DB 사용
    
    async def process_interview_interaction(self, session_id: str, user_answer: str, 
                                          context: dict) -> dict:
        """통합 면접 상호작용 처리"""
        try:
            # 1. 답변 분석 및 피드백 생성
            feedback = await self.feedback_service.analyze_answer(
                context.get('current_question', ''),
                user_answer,
                context.get('user_level', 'intermediate')
            )
            
            # 2. 꼬리질문 생성 (포트폴리오 내용 포함)
            follow_ups = await self.followup_service.generate_follow_up_questions(
                context.get('current_question', ''),
                user_answer,
                context.get('interviewer_persona', '친근한_시니어'),
                2,
                context.get('portfolio_text', '')
            )
            
            # 3. 포트폴리오 개선점 확인 (필요시)
            portfolio_insight = None
            if feedback.get('overall_score', 0) < 70:
                portfolio_analysis = await self.portfolio_service.analyze_portfolio(
                    context.get('portfolio_text', ''),
                    context.get('target_company', '')
                )
                improvements = await self.portfolio_service.generate_improvements(portfolio_analysis)
                if improvements:
                    portfolio_insight = improvements[0]  # 가장 우선순위 높은 것
            
            # 4. 면접관 페르소나에 맞는 응답 생성
            interviewer_response = self._generate_interviewer_response(
                feedback, follow_ups, context.get('interviewer_persona', '친근한_시니어')
            )
            
            # 5. 세션 상태 업데이트
            self._update_session(session_id, {
                'last_answer': user_answer,
                'last_feedback': feedback,
                'question_depth': context.get('question_depth', 0) + 1
            })
            
            return {
                'session_id': session_id,
                'feedback': feedback,
                'follow_up_questions': follow_ups,
                'portfolio_insight': portfolio_insight,
                'interviewer_response': interviewer_response,
                'next_action': 'continue' if follow_ups else 'new_topic'
            }
            
        except Exception as e:
            print(f"Interview processing error: {str(e)}")
            return {
                'session_id': session_id,
                'error': str(e),
                'fallback_response': '죄송합니다. 일시적인 오류가 발생했습니다. 다시 시도해주세요.'
            }
    
    def _generate_interviewer_response(self, feedback: dict, follow_ups: list, persona: str) -> str:
        """면접관 페르소나에 맞는 응답 생성"""
        persona_styles = {
            '친근한_시니어': {
                'positive': '좋네요! ',
                'transition': '그런데 조금 더 자세히 들어보고 싶어요.',
                'question_intro': '혹시 '
            },
            '까다로운_테크리드': {
                'positive': '음, ',
                'transition': '그런데 좀 더 깊이 있게 생각해보셨나요?',
                'question_intro': ''
            },
            '비즈니스_중심_매니저': {
                'positive': '기술적으로는 좋은데, ',
                'transition': '비즈니스 관점에서는 어떨까요?',
                'question_intro': '실제로 '
            }
        }
        
        style = persona_styles.get(persona, persona_styles['친근한_시니어'])
        score = feedback.get('overall_score', 0)
        
        if score >= 80:
            response = f"{style['positive']}훌륭한 답변이네요. {style['transition']}"
        elif score >= 60:
            response = f"{style['positive']}좋은 경험이네요. {style['transition']}"
        else:
            response = f"{style['positive']}흥미롭네요. {style['transition']}"
        
        return response
    
    def _update_session(self, session_id: str, update_data: dict):
        """세션 상태 업데이트"""
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                'created_at': uuid.uuid4().hex,
                'question_count': 0
            }
        
        self.sessions[session_id].update(update_data)
        self.sessions[session_id]['question_count'] = self.sessions[session_id].get('question_count', 0) + 1


class AIService:
    def __init__(self):
        self.upstage_service = UpstageAIService()
    
    async def extract_keywords(self, text: str) -> List[Keyword]:
        """Extract technical keywords using AI API with fallback"""
        try:
            print(f"Extracting keywords from text length: {len(text)}")
            
            # AI 서버 통신 시도
            try:
                async with httpx.AsyncClient(timeout=30) as client:
                    headers = {'Content-Type': 'application/json'}
                    payload = {'html_content': text}  # 전체 텍스트
                    
                    response = await client.post(
                        "https://ai-f.kms39273.synology.me/api/v1/keywords/extract",
                        headers=headers,
                        json=payload
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        if 'keywords' in result and len(result['keywords']) > 0:
                            keywords = []
                            raw_keywords = result['keywords']
                            
                            # AI 서버 응답 형식 처리
                            for kw in raw_keywords[:10]:  # 최대 10개
                                if isinstance(kw, str):
                                    # 문자열인 경우 기술 키워드만 필터링
                                    if kw not in ['```json', 'keywords":', '```'] and len(kw) > 1:
                                        keywords.append(Keyword(
                                            name=kw,
                                            category='technical',
                                            importance=5
                                        ))
                                elif isinstance(kw, dict):
                                    # 딕셔너리인 경우
                                    keywords.append(Keyword(
                                        name=kw.get('name', kw.get('keyword', 'Unknown')),
                                        category=kw.get('category', 'general'),
                                        importance=kw.get('importance', kw.get('score', 5))
                                    ))
                            
                            print(f"AI server extracted {len(keywords)} keywords")
                            return keywords
                        else:
                            print("AI server returned no keywords")
                            raise Exception("AI 서버에서 키워드를 추출하지 못했습니다. 잠시 후 다시 시도해주세요.")
                    else:
                        print(f"AI server error: {response.status_code}")
                        raise Exception(f"AI 서버 오류가 발생했습니다 (상태코드: {response.status_code}). 잠시 후 다시 시도해주세요.")
                        
            except httpx.TimeoutException:
                print("AI server timeout")
                raise Exception("AI 서버 응답 시간이 초과되었습니다. 네트워크 상태를 확인하고 다시 시도해주세요.")
            except httpx.ConnectError:
                print("AI server connection failed")
                raise Exception("AI 서버에 연결할 수 없습니다. 네트워크 상태를 확인하고 다시 시도해주세요.")
            except Exception as ai_error:
                print(f"AI server communication failed: {str(ai_error)}")
                raise Exception(f"AI 서버 통신 중 오류가 발생했습니다: {str(ai_error)}. 잠시 후 다시 시도해주세요.")
                
        except Exception as e:
            print(f"Keyword extraction error: {str(e)}")
            if "AI 서버" in str(e):
                raise e
            else:
                raise Exception(f"키워드 추출 중 오류가 발생했습니다: {str(e)}. 페이지를 새로고침하고 다시 시도해주세요.")
    

    
    async def generate_questions(self, keywords: List[str], company: str, text: str = "") -> List[Question]:
        """Generate interview questions using external API"""
        async with httpx.AsyncClient(timeout=settings.API_TIMEOUT) as client:
            headers = {'Content-Type': 'application/json'}
            payload = {
                'keywords': keywords,
                'company': company,
                'text': text
            }
            
            response = await client.post(
                "https://ai-f.kms39273.synology.me/api/v1/questions/generate",
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                questions = []
                for q in result.get('questions', []):
                    questions.append(Question(
                        question=q.get('text', q.get('question', '')),
                        answer=q.get('explanation', q.get('answer', '구체적인 경험과 예시를 바탕으로 답변하세요.')),
                        type=q.get('type', 'technical'),
                        difficulty='intermediate'
                    ))
                return questions
            else:
                print(f"Question generation failed: {response.status_code}")
                return self._generate_basic_questions(keywords, company, text)
    
    async def generate_structured_questions(self, portfolio_text: str, company_info: str = "", job_position: str = "") -> List:
        """구조화된 메인 질문 10개 생성"""
        try:
            print(f"Generating structured questions for portfolio length: {len(portfolio_text)}")
            
            # AI 서버 통신 시도
            try:
                async with httpx.AsyncClient(timeout=30) as client:
                    headers = {'Content-Type': 'application/json'}
                    
                    # 포트폴리오에서 키워드 추출
                    keywords = await self.extract_keywords(portfolio_text)
                    keyword_names = [kw.name for kw in keywords]
                    
                    payload = {
                        'html_content': portfolio_text,  # 전체 포트폴리오 내용
                        'keywords': keyword_names,
                        'company': company_info or '일반 IT 기업',
                        'portfolio_text': portfolio_text,
                        'company_info': company_info,
                        'job_position': job_position,
                        'question_count': 5
                    }
                    
                    print(f"Sending to AI server - keywords: {keyword_names}, company: {company_info}")
                    
                    response = await client.post(
                        "https://ai-f.kms39273.synology.me/api/v1/questions/generate",
                        headers=headers,
                        json=payload
                    )
                    
                    print(f"AI server response status: {response.status_code}")
                    
                    if response.status_code == 200:
                        result = response.json()
                        print(f"AI server response: {result}")
                        
                        if 'questions' in result and len(result['questions']) > 0:
                            questions = []
                            for i, q in enumerate(result['questions'][:10]):
                                # AI 서버 응답 형식 처리
                                question_text = ''
                                
                                if isinstance(q, dict):
                                    # 딕셔너리 형식
                                    question_text = q.get('question', q.get('text', q.get('content', '')))
                                    
                                    # 질문 텍스트에서 JSON 형식 제거
                                    if '"question":' in question_text:
                                        import re
                                        match = re.search(r'"question":\s*"([^"]+)"', question_text)
                                        if match:
                                            question_text = match.group(1)
                                elif isinstance(q, str):
                                    question_text = q
                                
                                # 빈 질문 제외
                                if not question_text or len(question_text.strip()) < 10:
                                    continue
                                
                                # 제목 생성
                                question_title = question_text[:50] + '...' if len(question_text) > 50 else question_text
                                
                                questions.append({
                                    'id': str(uuid.uuid4()),
                                    'title': question_title,
                                    'content': question_text,
                                    'category': 'Portfolio Based',
                                    'difficulty': 'Medium',
                                    'estimated_time': 4
                                })
                            print(f"AI server generated {len(questions)} personalized questions")
                            return questions
                        else:
                            print("AI server returned no questions")
                            raise Exception("AI 서버에서 질문을 생성하지 못했습니다. 잠시 후 다시 시도해주세요.")
                    else:
                        print(f"AI server error: {response.status_code}")
                        raise Exception(f"AI 서버 오류가 발생했습니다 (상태코드: {response.status_code}). 잠시 후 다시 시도해주세요.")
                        
            except httpx.TimeoutException:
                print("AI server timeout")
                raise Exception("AI 서버 응답 시간이 초과되었습니다. 네트워크 상태를 확인하고 다시 시도해주세요.")
            except httpx.ConnectError:
                print("AI server connection failed")
                raise Exception("AI 서버에 연결할 수 없습니다. 네트워크 상태를 확인하고 다시 시도해주세요.")
            except Exception as ai_error:
                print(f"AI server communication failed: {str(ai_error)}")
                raise Exception(f"AI 서버 통신 중 오류가 발생했습니다: {str(ai_error)}. 잠시 후 다시 시도해주세요.")
            
        except Exception as e:
            print(f"Question generation error: {str(e)}")
            if "AI 서버" in str(e):
                raise e  # AI 서버 관련 에러는 그대로 전달
            else:
                raise Exception(f"질문 생성 중 오류가 발생했습니다: {str(e)}. 페이지를 새로고침하고 다시 시도해주세요.")
    
    async def generate_followup_questions(self, main_question: str, user_answer: str, count: int = 3) -> List:
        """답변 기반 꼬리 질문 생성"""
        try:
            # 답변 분석하여 꼬리 질문 생성
            followup_templates = [
                "방금 말씀하신 {keyword}에 대해 좀 더 구체적으로 설명해주실 수 있나요?",
                "그 과정에서 어려웠던 점이나 예상치 못한 문제가 있었나요?",
                "다시 구현한다면 어떤 부분을 다르게 하시겠나요?",
                "그 기술을 선택한 특별한 이유가 있나요?",
                "성능이나 확장성 측면에서 고려한 점이 있나요?"
            ]
            
            # 답변에서 키워드 추출
            keywords = self._extract_keywords_from_answer(user_answer)
            
            followup_questions = []
            for i in range(min(count, len(followup_templates))):
                template = followup_templates[i]
                if keywords and '{keyword}' in template:
                    question = template.format(keyword=keywords[0])
                else:
                    question = template.replace('{keyword}', '해당 기술')
                
                followup_questions.append({
                    'question': question,
                    'type': 'deepening',
                    'intent': '더 자세한 설명 요청',
                    'difficulty': 'intermediate',
                    'expected_keywords': keywords[:3]
                })
            
            return followup_questions
            
        except Exception as e:
            print(f"Follow-up question generation error: {str(e)}")
            return self._get_default_followup_questions(count)
    
    async def generate_final_report(self, session_id: str, answers: List, main_questions: List) -> dict:
        """최종 면접 결과 리포트 생성"""
        try:
            async with httpx.AsyncClient(timeout=settings.API_TIMEOUT) as client:
                headers = {'Content-Type': 'application/json'}
                payload = {
                    'session_id': session_id,
                    'answers': answers,
                    'questions': main_questions
                }
                
                response = await client.post(
                    "https://ai-f.kms39273.synology.me/api/v1/evaluate/all",
                    headers=headers,
                    json=payload
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    raise Exception(f"Final report generation failed: {response.status_code}")
        except Exception as e:
            print(f"Final report generation error: {str(e)}")
            return self._get_default_report(session_id)
    
    def _extract_keywords_from_answer(self, answer: str) -> List[str]:
        """답변에서 기술 키워드 추출"""
        tech_keywords = ['React', 'JavaScript', 'Node.js', 'Python', 'Java', 'Spring', 'MySQL', 'MongoDB', 'AWS', 'Docker', 'Redis', 'API', 'REST', 'GraphQL']
        found_keywords = []
        
        for keyword in tech_keywords:
            if keyword.lower() in answer.lower():
                found_keywords.append(keyword)
        
        return found_keywords[:3]  # 최대 3개
    

    

    

    
    def _generate_basic_questions(self, keywords: List[str], company: str, text: str = "") -> List[Question]:
        """기본 질문 생성 (fallback)"""
        questions = []
        questions.append(Question(
            question=f"{company}에 지원한 이유는 무엇인가요?",
            answer="구체적인 경험과 함께 답변하세요.",
            type="behavioral",
            difficulty="intermediate"
        ))
        return questions

class FileService:
    def __init__(self):
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    def validate_file(self, file_content: bytes, content_type: str) -> bool:
        """Validate uploaded file"""
        if len(file_content) > settings.MAX_FILE_SIZE:
            return False
        if content_type not in settings.ALLOWED_FILE_TYPES:
            return False
        return True
    
    def save_temp_file(self, file_content: bytes) -> str:
        """Save file temporarily and return file path"""
        file_id = str(uuid.uuid4())
        file_path = os.path.join(settings.UPLOAD_DIR, f"{file_id}.pdf")
        
        with open(file_path, 'wb') as f:
            f.write(file_content)
        
        return file_path
    
    def cleanup_file(self, file_path: str):
        """Remove temporary file"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except:
            pass


class FeedbackService:
    """실시간 면접 피드백 서비스"""
    
    def __init__(self):
        pass
    
    async def analyze_answer(self, question: str, answer: str, user_level: str = "intermediate") -> dict:
        """답변을 분석하여 피드백 생성"""
        try:
            print(f"Analyzing answer for question length: {len(question)}, answer length: {len(answer)}")
            
            # AI 서버 통신 시도
            try:
                async with httpx.AsyncClient(timeout=30) as client:
                    headers = {'Content-Type': 'application/json'}
                    payload = {
                        'html_content': f'Question: {question[:500]}\n\nAnswer: {answer[:1000]}',
                        'question': question[:500],
                        'answer': answer[:1000],
                        'user_level': user_level
                    }
                    
                    response = await client.post(
                        "https://ai-f.kms39273.synology.me/api/v1/questions/evaluate",
                        headers=headers,
                        json=payload
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        if result and isinstance(result, dict):
                            print("AI server provided feedback")
                            return result
                        else:
                            print("AI server returned invalid feedback")
                            raise Exception("AI 서버에서 유효하지 않은 피드백을 반환했습니다. 잠시 후 다시 시도해주세요.")
                    else:
                        print(f"AI server error: {response.status_code}")
                        raise Exception(f"AI 서버 오류가 발생했습니다 (상태코드: {response.status_code}). 잠시 후 다시 시도해주세요.")
                        
            except httpx.TimeoutException:
                print("AI server timeout")
                raise Exception("AI 서버 응답 시간이 초과되었습니다. 네트워크 상태를 확인하고 다시 시도해주세요.")
            except httpx.ConnectError:
                print("AI server connection failed")
                raise Exception("AI 서버에 연결할 수 없습니다. 네트워크 상태를 확인하고 다시 시도해주세요.")
            except Exception as ai_error:
                print(f"AI server communication failed: {str(ai_error)}")
                raise Exception(f"AI 서버 통신 중 오류가 발생했습니다: {str(ai_error)}. 잠시 후 다시 시도해주세요.")
                
        except Exception as e:
            print(f"Answer evaluation error: {str(e)}")
            if "AI 서버" in str(e):
                raise e
            else:
                raise Exception(f"답변 평가 중 오류가 발생했습니다: {str(e)}. 잠시 후 다시 시도해주세요.")
    

    
    async def evaluate_structured_answer(self, question: str, answer: str, question_type: str, context: dict = None) -> dict:
        """구조화된 질문 시스템용 답변 평가"""
        try:
            # 답변 길이 및 구조 분석
            word_count = len(answer.split())
            sentence_count = len([s for s in answer.split('.') if s.strip()])
            
            # 기본 점수 계산 (단어 수, 문장 수 기반)
            base_score = min(90, word_count * 1.5 + sentence_count * 2)
            
            # 질문 유형별 가중치 적용
            if question_type == 'main':
                # 메인 질문은 더 높은 기준
                score = max(60, base_score - 5)
            else:
                # 꼬리 질문은 상대적으로 관대
                score = min(95, base_score + 5)
            
            # STAR 기법 분석
            star_keywords = {
                'situation': ['상황', '때', '프로젝트에서', '당시', '환경'],
                'task': ['과제', '문제', '목표', '요구사항', '해결해야', '구현해야'],
                'action': ['구현', '사용', '적용', '개발', '설계', '선택', '결정'],
                'result': ['결과', '성과', '향상', '개선', '완성', '달성', '%', '배', '시간', '속도']
            }
            
            star_analysis = {}
            for component, keywords in star_keywords.items():
                present = any(keyword in answer for keyword in keywords)
                quality = "good" if present else "missing"
                suggestion = None if present else f"{component.upper()} 요소 추가 필요"
                
                star_analysis[component] = {
                    "present": present,
                    "quality": quality,
                    "suggestion": suggestion
                }
            
            # 기술적 정확성 분석
            tech_keywords = ['React', 'JavaScript', 'Node.js', 'API', 'Database', 'AWS', 'Docker', 'Git']
            found_tech = [tech for tech in tech_keywords if tech.lower() in answer.lower()]
            
            technical_accuracy = {
                "score": min(100, len(found_tech) * 10 + base_score),
                "correct_concepts": found_tech,
                "missing_details": ["구체적인 기술 스택 언급"] if not found_tech else []
            }
            
            # 개선 제안 생성
            improvement_suggestions = []
            if word_count < 50:
                improvement_suggestions.append("답변을 더 자세히 설명해주세요")
            if not any(star_analysis[comp]["present"] for comp in ['situation', 'task']):
                improvement_suggestions.append("상황과 과제를 명확히 설명해주세요")
            if not star_analysis['result']['present']:
                improvement_suggestions.append("구체적인 결과나 성과를 포함해주세요")
            if not found_tech:
                improvement_suggestions.append("사용한 기술 스택을 구체적으로 언급해주세요")
            
            # 강점 분석
            strengths = []
            if word_count >= 100:
                strengths.append("충분히 상세한 설명")
            if len(found_tech) >= 2:
                strengths.append("다양한 기술 스택 활용")
            if star_analysis['result']['present']:
                strengths.append("결과 중심의 답변")
            if any(keyword in answer for keyword in ['팀', '협업', '리뷰']):
                strengths.append("협업 경험 언급")
            
            # 다음 단계 제안
            next_steps = []
            if question_type == 'main':
                next_steps.append("꼬리 질문을 통해 더 깊이 탐구해보겠습니다")
            else:
                next_steps.append("실무에서 이 경험을 어떻게 발전시킬 수 있을지 고민해보세요")
            
            if not improvement_suggestions:
                next_steps.append("훌륭한 답변입니다. 이런 식으로 계속 답변해주세요")
            
            return {
                "overall_score": int(score),
                "star_analysis": star_analysis,
                "technical_accuracy": technical_accuracy,
                "improvement_suggestions": improvement_suggestions or ["좋은 답변입니다"],
                "strengths": strengths or ["경험 기반 답변"],
                "next_steps": next_steps
            }
            
        except Exception as e:
            print(f"Structured answer evaluation error: {str(e)}")
            return self._get_default_feedback()
    
    def _get_default_feedback(self) -> dict:
        """기본 피드백 반환 (fallback)"""
        return {
            "overall_score": 70,
            "star_analysis": {
                "situation": {"present": True, "quality": "good", "suggestion": "더 구체적인 상황 설명"},
                "task": {"present": True, "quality": "good", "suggestion": None},
                "action": {"present": True, "quality": "good", "suggestion": None},
                "result": {"present": False, "quality": None, "suggestion": "정량적 결과 지표 추가"}
            },
            "technical_accuracy": {"score": 75, "correct_concepts": [], "missing_details": []},
            "improvement_suggestions": ["더 구체적인 예시 추가"],
            "strengths": ["경험 기반 답변"],
            "next_steps": ["실무 경험 보강"]
        }


class FollowUpService:
    """꼬리질문 생성 서비스"""
    
    def __init__(self):
        pass
    
    async def generate_follow_up_questions(self, question: str, answer: str, 
                                         interviewer_persona: str = "친근한_시니어",
                                         max_questions: int = 2, portfolio_text: str = "") -> list:
        """꼬리질문 생성"""
        try:
            print(f"Generating follow-up questions for answer length: {len(answer)}")
            
            # AI 서버 통신 시도
            try:
                async with httpx.AsyncClient(timeout=30) as client:
                    headers = {'Content-Type': 'application/json'}
                    
                    payload = {
                        'html_content': f'Question: {question[:500]}\n\nAnswer: {answer[:1000]}\n\nPortfolio: {portfolio_text[:500]}',
                        'question': question[:500],
                        'answer': answer[:1000],
                        'interviewer_persona': interviewer_persona,
                        'portfolio_text': portfolio_text[:1000],
                        'max_questions': max_questions,
                        'context': f'Portfolio context: {portfolio_text[:500]}. Based on this portfolio and the user answer, generate personalized follow-up questions.'
                    }
                    
                    response = await client.post(
                        "https://ai-f.kms39273.synology.me/api/v1/questions/following",
                        headers=headers,
                        json=payload
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        if 'questions' in result and len(result['questions']) > 0:
                            follow_ups = []
                            for q in result['questions'][:max_questions]:
                                question_text = q.get('text', q.get('question', q.get('content', '')))
                                if question_text:  # 빈 질문 제외
                                    follow_ups.append({
                                        'question': question_text,
                                        'type': '깊이_파기',
                                        'intent': '더 자세한 설명 요청',
                                        'difficulty': 'intermediate',
                                        'expected_keywords': []
                                    })
                            print(f"AI server generated {len(follow_ups)} personalized follow-up questions")
                            return follow_ups if follow_ups else self._get_default_follow_ups(max_questions)
                        else:
                            print("AI server returned no follow-up questions")
                            raise Exception("AI 서버에서 꼬리질문을 생성하지 못했습니다. 잠시 후 다시 시도해주세요.")
                    else:
                        print(f"AI server error: {response.status_code}")
                        raise Exception(f"AI 서버 오류가 발생했습니다 (상태코드: {response.status_code}). 잠시 후 다시 시도해주세요.")
                        
            except httpx.TimeoutException:
                print("AI server timeout")
                raise Exception("AI 서버 응답 시간이 초과되었습니다. 네트워크 상태를 확인하고 다시 시도해주세요.")
            except httpx.ConnectError:
                print("AI server connection failed")
                raise Exception("AI 서버에 연결할 수 없습니다. 네트워크 상태를 확인하고 다시 시도해주세요.")
            except Exception as ai_error:
                print(f"AI server communication failed: {str(ai_error)}")
                raise Exception(f"AI 서버 통신 중 오류가 발생했습니다: {str(ai_error)}. 잠시 후 다시 시도해주세요.")
                
        except Exception as e:
            print(f"Follow-up question generation error: {str(e)}")
            if "AI 서버" in str(e):
                raise e
            else:
                raise Exception(f"꼬리질문 생성 중 오류가 발생했습니다: {str(e)}. 잠시 후 다시 시도해주세요.")
    

        """답변 내용을 분석하여 개인화된 꼬리질문 생성"""
        print(f"Generating personalized follow-ups based on answer: {answer[:100]}...")
        
        # 답변에서 기술 키워드 추출
        tech_keywords = ['React', 'JavaScript', 'Node.js', 'Python', 'Java', 'Spring', 'MySQL', 'MongoDB', 'AWS', 'Docker', 'Git', 'API', 'Database']
        found_keywords = [kw for kw in tech_keywords if kw.lower() in answer.lower()]
        
        # 답변 내용 분석
        answer_lower = answer.lower()
        has_numbers = any(char.isdigit() for char in answer)
        has_team_mention = any(word in answer_lower for word in ['팀', 'team', '협업', '함께', '동료'])
        has_problem_mention = any(word in answer_lower for word in ['문제', '어려움', '오류', '버그', '해결'])
        has_result_mention = any(word in answer_lower for word in ['결과', '성과', '효과', '개선', '향상'])
        has_learning_mention = any(word in answer_lower for word in ['배운', '학습', '깨달은', '성장'])
        
        # 개인화된 꼬리질문 생성
        personalized_questions = []
        
        # 기술 기반 질문
        if found_keywords:
            main_tech = found_keywords[0]
            personalized_questions.append(
                f'{main_tech}를 사용하면서 가장 인상 깊었던 기능이나 특징은 무엇이었나요? 왜 그것이 중요했나요?'
            )
        
        # 수치/결과 기반 질문
        if has_numbers or has_result_mention:
            personalized_questions.append(
                '말씨하신 결과나 성과를 좋아진 점이 있다면 구체적으로 어떤 지표로 측정하셨나요? 사용자나 비즈니스 관점에서는 어떤 의미였나요?'
            )
        
        # 팀워크 기반 질문
        if has_team_mention:
            personalized_questions.append(
                '팀원들과 이 부분에 대해 어떻게 소통하고 협업하셨나요? 의견 차이가 있었다면 어떻게 조율하셨나요?'
            )
        
        # 문제 해결 기반 질문
        if has_problem_mention:
            personalized_questions.append(
                '그 문제를 해결하는 과정에서 어떤 대안들을 고려해보셨나요? 최종 해결책을 선택한 결정적 이유는 무엇이었나요?'
            )
        
        # 학습/성장 기반 질문
        if has_learning_mention:
            personalized_questions.append(
                '이 경험을 통해 배운 점을 다른 프로젝트나 업무에서 어떻게 활용하고 있나요? 구체적인 사례가 있다면 설명해주세요.'
            )
        
        # 기본 개인화 질문들 (답변 내용에 따라)
        if not personalized_questions:
            if len(answer.split()) > 50:  # 긴 답변
                personalized_questions.append('말씨하신 내용 중에서 가장 중요하다고 생각하는 포인트 3가지를 선정한다면 무엇인가요?')
            else:  # 짧은 답변
                personalized_questions.append('조금 더 구체적인 예시나 상황을 들어서 설명해주실 수 있나요?')
        
        # 추가 심화 질문들
        additional_questions = [
            '이 경험을 다른 개발자에게 공유한다면 가장 강조하고 싶은 노하우나 주의사항은 무엇인가요?',
            '비슷한 상황에 다시 마주쳤다면, 지금의 경험을 바탕으로 어떤 점을 다르게 접근하시겠나요?',
            '이 프로젝트나 경험이 본인의 개발자 커리어에 어떤 영향을 주었나요?'
        ]
        
        # 최대 요청 수만큼 선택
        all_questions = personalized_questions + additional_questions
        selected_questions = all_questions[:max_questions]
        
        # 결과 형식으로 변환
        follow_ups = []
        for i, q in enumerate(selected_questions):
            follow_ups.append({
                'question': q,
                'type': '개인화_심화',
                'intent': '답변 기반 맞춤형 질문',
                'difficulty': 'intermediate',
                'expected_keywords': found_keywords[:2]
            })
        
        print(f"Generated {len(follow_ups)} personalized follow-up questions")
        return follow_ups


class CompanyService:
    """회사별 면접 문화 서비스"""
    
    def __init__(self):
        self.company_cache = {}
    
    async def get_company_profile(self, company_name: str) -> dict:
        """회사 프로필 조회"""
        if company_name in self.company_cache:
            return self.company_cache[company_name]
        
        async with httpx.AsyncClient(timeout=settings.API_TIMEOUT) as client:
            headers = {'Content-Type': 'application/json'}
            
            response = await client.get(
                f"{settings.API_BASE_URL}/api/v1/companies/{company_name}/profile"
            )
            
            if response.status_code == 200:
                result = response.json()
                profile = self._parse_company_profile(result)
                self.company_cache[company_name] = profile
                return profile
            else:
                return self._get_default_company_profile(company_name)
    
    async def generate_company_questions(self, company_name: str, user_keywords: list) -> list:
        """회사별 맞춤 질문 생성"""
        async with httpx.AsyncClient(timeout=settings.API_TIMEOUT) as client:
            headers = {'Content-Type': 'application/json'}
            payload = {
                'html_content': f"Company: {company_name}. Keywords: {', '.join(user_keywords)}",
                'keywords': user_keywords,
                'company': company_name
            }
            
            response = await client.post(
                "https://ai-f.kms39273.synology.me/api/v1/questions/generate",
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                questions = []
                for q in result.get('questions', []):
                    questions.append({
                        'question': q.get('text', q.get('question', '')),
                        'category': '기술',
                        'company_relevance': f'{company_name} 맞춤 질문',
                        'expected_answer_direction': q.get('explanation', '구체적 경험 위주로 답변'),
                        'difficulty': 'intermediate'
                    })
                return questions
            else:
                return self._get_default_questions(company_name)
    
    def _parse_company_profile(self, result: dict) -> dict:
        """회사 프로필 파싱"""
        return {
            'name': result.get('name', ''),
            'industry': result.get('industry', ''),
            'size': result.get('size', ''),
            'tech_stack': result.get('tech_stack', []),
            'culture_keywords': result.get('culture_keywords', []),
            'interview_style': result.get('interview_style', {}),
            'typical_questions': result.get('typical_questions', []),
            'success_tips': result.get('success_tips', []),
            'red_flags': result.get('red_flags', [])
        }
    
    def _get_default_company_profile(self, company_name: str) -> dict:
        """기본 회사 프로필 반환"""
        return {
            'name': company_name,
            'industry': 'IT',
            'size': '대기업',
            'tech_stack': ['Java', 'Spring', 'React'],
            'culture_keywords': ['기술적 깊이', '협업', '성장'],
            'interview_style': {'approach': '기술 중심', 'duration': '60분'},
            'typical_questions': [],
            'success_tips': ['구체적인 경험 위주로 답변'],
            'red_flags': ['추상적인 답변']
        }
    
    def _get_default_questions(self, company_name: str) -> list:
        """기본 질문 반환"""
        return [
            {
                'question': f'{company_name}에 지원한 이유는 무엇인가요?',
                'category': '문화',
                'difficulty': '초급'
            }
        ]


class PortfolioService:
    """포트폴리오 개선 제안 서비스"""
    
    def __init__(self):
        pass
    
    async def analyze_portfolio(self, portfolio_text: str, target_company: str = "", 
                              target_position: str = "") -> dict:
        """포트폴리오 분석"""
        try:
            async with httpx.AsyncClient(timeout=settings.API_TIMEOUT) as client:
                headers = {'Content-Type': 'application/json'}
                payload = {
                    'portfolio_text': portfolio_text,
                    'target_company': target_company,
                    'target_position': target_position
                }
                
                response = await client.post(
                    "https://ai-f.kms39273.synology.me/api/v1/evaluate/portfolio",
                    headers=headers,
                    json=payload
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    raise Exception(f"Portfolio analysis failed: {response.status_code}")
        except Exception as e:
            print(f"Portfolio analysis error: {str(e)}")
            return self._get_default_analysis()
    
    async def generate_improvements(self, analysis_result: dict) -> list:
        """개선 제안 생성"""
        improvements = []
        
        # 성과 지표 정량화 제안
        if analysis_result.get('quantification_score', 0) < 50:
            improvements.append({
                'category': '성과 지표 정량화',
                'priority': 'high',
                'suggestion': '프로젝트 결과를 구체적인 수치로 표현하세요',
                'example': '사용자 경험 개선 → 로딩 시간 3초에서 0.8초로 75% 단축',
                'impact': 'high',
                'effort': 'low',
                'timeline': '2-3일'
            })
        
        # 기술 스택 보완 제안
        missing_skills = analysis_result.get('missing_skills', [])
        if missing_skills:
            improvements.append({
                'category': '기술 스택 보완',
                'priority': 'medium',
                'suggestion': f"다음 기술 경험 추가: {', '.join(missing_skills[:3])}",
                'example': '기존 프로젝트에 Redis 캐싱 레이어 추가 구현',
                'impact': 'high',
                'effort': 'medium',
                'timeline': '1-2주'
            })
        
        return improvements
    
    def _get_default_analysis(self) -> dict:
        """기본 분석 결과 반환 (fallback)"""
        return {
            'overall_assessment': {
                'current_score': 70,
                'target_score': 85,
                'market_fit': 75,
                'improvement_potential': 'medium'
            },
            'detailed_analysis': {
                'technical_skills': {
                    'present_skills': ['기본 기술'],
                    'missing_skills': ['추가 필요 기술'],
                    'skill_depth_score': 70,
                    'recommendations': ['기술 스택 보완']
                },
                'project_descriptions': {
                    'clarity_score': 70,
                    'quantification_score': 50,
                    'star_usage': 60,
                    'improvements': ['구체적 수치 추가']
                }
            },
            'priority_improvements': [{
                'category': '성과 지표 정량화',
                'current_issue': '정량적 지표 부족',
                'suggestion': '구체적 수치로 성과 표현',
                'example': '사용자 만족도 향상 → 사용자 만족도 4.2에서 4.7로 12% 향상',
                'impact': 'high',
                'effort': 'low',
                'timeline': '2-3일'
            }]
        }
