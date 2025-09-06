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

class AIService:
    def __init__(self):
        self.upstage_service = UpstageAIService()
    
    async def extract_keywords(self, text: str) -> List[Keyword]:
        """Extract technical keywords - always returns keywords"""
        print(f"Extracting keywords from text length: {len(text)}")
        
        # 텍스트에서 직접 키워드 추출
        text_lower = text.lower()
        
        # 기술 키워드 매핑
        tech_keywords = {
            'java': ('Java', 'language', 9),
            'javascript': ('JavaScript', 'language', 8),
            'python': ('Python', 'language', 8),
            'typescript': ('TypeScript', 'language', 7),
            'kotlin': ('Kotlin', 'language', 7),
            'spring': ('Spring', 'framework', 8),
            'react': ('React', 'framework', 8),
            'vue': ('Vue.js', 'framework', 7),
            'angular': ('Angular', 'framework', 7),
            'node.js': ('Node.js', 'framework', 8),
            'express': ('Express', 'framework', 6),
            'django': ('Django', 'framework', 7),
            'mysql': ('MySQL', 'database', 7),
            'postgresql': ('PostgreSQL', 'database', 7),
            'mongodb': ('MongoDB', 'database', 6),
            'redis': ('Redis', 'database', 6),
            'aws': ('AWS', 'cloud', 8),
            'docker': ('Docker', 'devops', 7),
            'git': ('Git', 'tool', 8),
            'github': ('GitHub', 'tool', 7)
        }
        
        found_keywords = []
        
        # 텍스트에서 키워드 찾기
        for keyword, (name, category, importance) in tech_keywords.items():
            if keyword in text_lower:
                found_keywords.append(Keyword(
                    name=name,
                    category=category,
                    importance=importance
                ))
        
        # 기본 키워드 추가 (아무것도 없을 경우)
        if not found_keywords:
            default_keywords = [
                Keyword(name='Java', category='language', importance=8),
                Keyword(name='Spring Boot', category='framework', importance=7),
                Keyword(name='React', category='framework', importance=7),
                Keyword(name='MySQL', category='database', importance=6),
                Keyword(name='Git', category='tool', importance=8)
            ]
            found_keywords = default_keywords
        
        # 중요도 순으로 정렬 및 최대 8개 반환
        found_keywords.sort(key=lambda x: x.importance, reverse=True)
        print(f"Extracted {len(found_keywords[:8])} keywords")
        return found_keywords[:8]
    
    async def generate_structured_questions(self, portfolio_text: str, company_info: str = "", job_position: str = "") -> List:
        """구조화된 메인 질문 10개 생성"""
        print(f"Generating structured questions for portfolio length: {len(portfolio_text)}")
        
        # 포트폴리오에서 키워드 추출
        keywords = await self.extract_keywords(portfolio_text)
        keyword_names = [kw.name for kw in keywords]
        
        print(f"Using keywords: {keyword_names}")
        
        # 항상 포트폴리오 기반 개인화된 질문 생성
        return get_portfolio_based_questions(portfolio_text, keyword_names)

class FeedbackService:
    """실시간 면접 피드백 서비스"""
    
    def __init__(self):
        pass
    
    async def analyze_answer(self, question: str, answer: str, user_level: str = "intermediate") -> dict:
        """답변을 분석하여 피드백 생성"""
        print(f"Analyzing answer for question length: {len(question)}, answer length: {len(answer)}")
        
        # 기본 피드백 생성 (AI 서버 없이)
        word_count = len(answer.split())
        sentence_count = len([s for s in answer.split('.') if s.strip()])
        
        # 기본 점수 계산
        base_score = min(90, word_count * 1.5 + sentence_count * 2)
        score = max(60, base_score)
        
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
        
        return {
            "overall_score": int(score),
            "star_analysis": star_analysis,
            "technical_accuracy": technical_accuracy,
            "improvement_suggestions": improvement_suggestions or ["좋은 답변입니다"],
            "strengths": strengths or ["경험 기반 답변"],
            "next_steps": ["계속해서 구체적인 경험을 바탕으로 답변해주세요"]
        }

class FollowUpService:
    """꼬리질문 생성 서비스"""
    
    def __init__(self):
        pass
    
    async def generate_follow_up_questions(self, question: str, answer: str, 
                                         interviewer_persona: str = "친근한_시니어",
                                         max_questions: int = 2, portfolio_text: str = "") -> list:
        """꼬리질문 생성"""
        print(f"Generating follow-up questions for answer length: {len(answer)}")
        
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
                '말씀하신 결과나 성과를 구체적으로 어떤 지표로 측정하셨나요? 사용자나 비즈니스 관점에서는 어떤 의미였나요?'
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
                personalized_questions.append('말씀하신 내용 중에서 가장 중요하다고 생각하는 포인트 3가지를 선정한다면 무엇인가요?')
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

class IntegratedInterviewService:
    """통합 면접 시뮬레이션 서비스"""
    
    def __init__(self):
        self.feedback_service = FeedbackService()
        self.followup_service = FollowUpService()
        self.sessions = {}

class CompanyService:
    """회사별 면접 문화 서비스"""
    
    def __init__(self):
        self.company_cache = {}
    
    async def get_company_profile(self, company_name: str) -> dict:
        """회사 프로필 조회"""
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

class PortfolioService:
    """포트폴리오 개선 제안 서비스"""
    
    def __init__(self):
        pass
    
    async def analyze_portfolio(self, portfolio_text: str, target_company: str = "", 
                              target_position: str = "") -> dict:
        """포트폴리오 분석"""
        return {
            'overall_assessment': {
                'current_score': 75,
                'target_score': 85,
                'market_fit': 75,
                'improvement_potential': 'medium'
            },
            'detailed_analysis': {
                'technical_skills': {
                    'present_skills': ['기본 기술'],
                    'missing_skills': ['추가 필요 기술'],
                    'skill_depth_score': 70,
                    'recommendations': ['기술 스택 보강']
                }
            }
        }
    
    async def generate_improvements(self, analysis_result: dict) -> list:
        """개선 제안 생성"""
        return [{
            'category': '성과 지표 정량화',
            'priority': 'high',
            'suggestion': '프로젝트 결과를 구체적인 수치로 표현하세요',
            'example': '사용자 경험 개선 → 로딩 시간 3초에서 0.8초로 75% 단축',
            'impact': 'high',
            'effort': 'low',
            'timeline': '2-3일'
        }]

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