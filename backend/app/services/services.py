# Assumption: Using absolute imports and simplified implementation
import httpx
import json
import os
import uuid
from typing import List, Optional
from app.config.config import settings
from app.models.models import Keyword, Question, QuestionType, DifficultyLevel, KeywordCategory
from app.services.upstage_service import UpstageAIService

class DocumentParserService:
    async def parse_pdf(self, file_path: str) -> str:
        """Extract text from PDF using custom API"""
        try:
            async with httpx.AsyncClient(timeout=settings.API_TIMEOUT) as client:
                with open(file_path, 'rb') as f:
                    files = {'file': f}
                    
                    response = await client.post(
                        settings.DOCUMENT_PARSER_URL,
                        files=files
                    )
                    
                if response.status_code == 200:
                    result = response.json()
                    print(f"Document parser response: {result}")
                    
                    # API 응답에서 텍스트 추출
                    if 'content' in result:
                        import re
                        html_content = result['content']
                        # HTML 태그 제거
                        text_content = re.sub(r'<[^>]*>', '', html_content)
                        # HTML 엔티티 디코딩
                        text_content = text_content.replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
                        # 여러 줄바꿈을 하나로 정리
                        text_content = re.sub(r'\n+', '\n', text_content).strip()
                        return text_content
                    elif 'text' in result:
                        return result['text']
                    else:
                        print(f"No text found in response: {result}")
                        return ''
                else:
                    error_text = response.text
                    print(f"Document parsing failed: {response.status_code}, {error_text}")
                    raise Exception(f"Document parsing failed: {response.status_code}")
                    
        except Exception as e:
            print(f"Document parsing exception: {str(e)}")
            raise Exception(f"Document parsing error: {str(e)}")

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
        """Extract technical keywords using Upstage API"""
        try:
            keywords_data = await self.upstage_service.extract_keywords(text)
            keywords = []
            for kw in keywords_data:
                keywords.append(Keyword(
                    name=kw['name'],
                    category=kw['category'],
                    importance=kw['importance']
                ))
            return keywords
        except Exception as e:
            print(f"Keyword extraction error: {str(e)}")
            # Fallback to basic keyword extraction
            return self._extract_basic_keywords(text)
    
    def _extract_basic_keywords(self, text: str) -> List[Keyword]:
        """기본 키워드 추출 (fallback)"""
        basic_keywords = [
            ('Java', 'language', 8),
            ('Spring', 'framework', 7),
            ('MySQL', 'database', 6),
            ('React', 'framework', 7),
            ('AWS', 'cloud', 6)
        ]
        
        keywords = []
        for name, category, importance in basic_keywords:
            if name.lower() in text.lower():
                keywords.append(Keyword(name=name, category=category, importance=importance))
        
        return keywords[:5]  # 최대 5개
    
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
                "https://forky-ai.kms39273.synology.me/api/v1/questions/generate",
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
            # 포트폴리오에서 기술 스택 추출
            keywords = await self.extract_keywords(portfolio_text)
            tech_stack = [kw.name for kw in keywords]
            
            # 카테고리별 질문 분배 (총 10개)
            categories = {
                'React': ['프론트엔드', 'React'],
                'JavaScript': ['프론트엔드', 'JavaScript'], 
                'TypeScript': ['프론트엔드', 'TypeScript'],
                'Node.js': ['백엔드', 'Node.js'],
                'Java': ['백엔드', 'Java'],
                'Spring': ['백엔드', 'Spring'],
                'Python': ['백엔드', 'Python'],
                'Database': ['데이터베이스', 'MySQL'],
                'AWS': ['클라우드', 'AWS'],
                'Algorithm': ['알고리즘', '자료구조']
            }
            
            main_questions = []
            question_templates = {
                'React': {
                    'title': 'React 상태 관리 경험',
                    'content': '프로젝트에서 React의 상태 관리를 어떻게 구현하셨나요? useState, useReducer, 또는 외부 라이브러리를 사용한 경험을 구체적으로 설명해주세요.',
                    'difficulty': 'Medium',
                    'time': 4
                },
                'JavaScript': {
                    'title': 'JavaScript 비동기 처리',
                    'content': 'JavaScript에서 비동기 처리를 다룬 경험에 대해 설명해주세요. Promise, async/await를 사용한 구체적인 사례를 포함해주세요.',
                    'difficulty': 'Medium', 
                    'time': 3
                },
                'Node.js': {
                    'title': 'Node.js API 개발 경험',
                    'content': 'Node.js로 REST API를 개발한 경험에 대해 설명해주세요. 어떤 프레임워크를 사용했고, 어떤 기능을 구현했나요?',
                    'difficulty': 'Medium',
                    'time': 4
                },
                'Database': {
                    'title': '데이터베이스 설계 및 최적화',
                    'content': '프로젝트에서 데이터베이스를 설계하고 쿼리를 최적화한 경험이 있나요? 구체적인 사례를 설명해주세요.',
                    'difficulty': 'Hard',
                    'time': 5
                },
                'AWS': {
                    'title': '클라우드 서비스 활용 경험',
                    'content': 'AWS나 다른 클라우드 서비스를 사용해본 경험이 있나요? 어떤 서비스를 사용했고, 어떤 문제를 해결했나요?',
                    'difficulty': 'Medium',
                    'time': 4
                }
            }
            
            # 포트폴리오 기반 질문 생성
            used_categories = set()
            for tech in tech_stack[:5]:  # 상위 5개 기술
                if tech in question_templates and tech not in used_categories:
                    template = question_templates[tech]
                    main_questions.append({
                        'id': str(uuid.uuid4()),
                        'title': template['title'],
                        'content': template['content'],
                        'category': tech,
                        'difficulty': template['difficulty'],
                        'estimated_time': template['time']
                    })
                    used_categories.add(tech)
            
            # 기본 질문으로 10개 채우기
            default_questions = [
                {
                    'title': '프로젝트 아키텍처 설계',
                    'content': '가장 복잡했던 프로젝트의 아키텍처를 어떻게 설계했나요? 기술 선택의 이유와 함께 설명해주세요.',
                    'category': 'System Design',
                    'difficulty': 'Hard',
                    'time': 6
                },
                {
                    'title': '성능 최적화 경험',
                    'content': '애플리케이션의 성능을 개선한 경험이 있나요? 어떤 문제를 발견했고, 어떻게 해결했나요?',
                    'category': 'Performance',
                    'difficulty': 'Medium',
                    'time': 4
                },
                {
                    'title': '팀 협업 및 코드 리뷰',
                    'content': '팀 프로젝트에서 코드 리뷰나 협업 도구를 사용한 경험에 대해 설명해주세요.',
                    'category': 'Collaboration',
                    'difficulty': 'Easy',
                    'time': 3
                },
                {
                    'title': '문제 해결 과정',
                    'content': '개발 중 가장 어려웠던 기술적 문제는 무엇이었고, 어떻게 해결했나요?',
                    'category': 'Problem Solving',
                    'difficulty': 'Medium',
                    'time': 5
                },
                {
                    'title': '테스트 및 품질 관리',
                    'content': '코드의 품질을 보장하기 위해 어떤 테스트 전략을 사용하나요? 단위 테스트, 통합 테스트 경험을 설명해주세요.',
                    'category': 'Testing',
                    'difficulty': 'Medium',
                    'time': 4
                }
            ]
            
            # 10개가 될 때까지 기본 질문 추가
            for default_q in default_questions:
                if len(main_questions) >= 10:
                    break
                main_questions.append({
                    'id': str(uuid.uuid4()),
                    'title': default_q['title'],
                    'content': default_q['content'],
                    'category': default_q['category'],
                    'difficulty': default_q['difficulty'],
                    'estimated_time': default_q['time']
                })
            
            return main_questions[:10]  # 정확히 10개만 반환
            
        except Exception as e:
            print(f"Structured question generation error: {str(e)}")
            return self._get_default_structured_questions()
    
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
            # 답변 분석
            total_score = 0
            category_scores = {}
            strengths = []
            weaknesses = []
            recommendations = []
            
            for answer in answers:
                if answer.get('feedback'):
                    score = answer['feedback'].get('overall_score', 0)
                    total_score += score
                    
                    # 카테고리별 점수 집계
                    question = next((q for q in main_questions if q['id'] == answer['question_id']), None)
                    if question:
                        category = question['category']
                        if category not in category_scores:
                            category_scores[category] = []
                        category_scores[category].append(score)
                    
                    # 강점과 약점 수집
                    strengths.extend(answer['feedback'].get('strengths', []))
                    weaknesses.extend(answer['feedback'].get('improvement_suggestions', []))
                    recommendations.extend(answer['feedback'].get('next_steps', []))
            
            # 평균 점수 계산
            avg_score = total_score / len(answers) if answers else 0
            
            # 카테고리별 평균 점수
            final_category_scores = {}
            for category, scores in category_scores.items():
                final_category_scores[category] = sum(scores) / len(scores)
            
            # 중복 제거 및 상위 항목 선별
            unique_strengths = list(set(strengths))[:5]
            unique_weaknesses = list(set(weaknesses))[:5] 
            unique_recommendations = list(set(recommendations))[:5]
            
            return {
                'session_id': session_id,
                'overall_score': round(avg_score),
                'category_scores': final_category_scores,
                'total_questions': len(answers),
                'strengths': unique_strengths,
                'weaknesses': unique_weaknesses,
                'recommendations': unique_recommendations,
                'completion_rate': 100,
                'summary': f"총 {len(answers)}개 질문에 답변하여 평균 {round(avg_score)}점을 획득했습니다."
            }
            
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
    
    def _get_default_structured_questions(self) -> List:
        """기본 구조화된 질문 반환 (fallback)"""
        return [
            {
                'id': str(uuid.uuid4()),
                'title': '프로젝트 경험 소개',
                'content': '가장 기억에 남는 프로젝트에 대해 설명해주세요.',
                'category': 'General',
                'difficulty': 'Easy',
                'estimated_time': 3
            }
        ] * 10  # 10개 생성
    
    def _get_default_followup_questions(self, count: int) -> List:
        """기본 꼬리 질문 반환 (fallback)"""
        default_questions = [
            '조금 더 구체적으로 설명해주실 수 있나요?',
            '그 과정에서 어려웠던 점은 무엇인가요?',
            '다른 방법도 고려해보셨나요?'
        ]
        
        return [{
            'question': q,
            'type': 'deepening',
            'intent': '더 자세한 설명 요청',
            'difficulty': 'intermediate',
            'expected_keywords': []
        } for q in default_questions[:count]]
    
    def _get_default_report(self, session_id: str) -> dict:
        """기본 리포트 반환 (fallback)"""
        return {
            'session_id': session_id,
            'overall_score': 70,
            'category_scores': {'General': 70},
            'total_questions': 1,
            'strengths': ['기본적인 답변 제공'],
            'weaknesses': ['더 구체적인 설명 필요'],
            'recommendations': ['실무 경험 보강'],
            'completion_rate': 100,
            'summary': '면접이 완료되었습니다.'
        }lt.get('questions', []):
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
    
    def _generate_basic_questions(self, keywords: List[str], company: str, text: str = "") -> List[Question]:
        """기본 질문 생성 (fallback)"""
        # 포트폴리오 텍스트에서 기술 키워드 추출
        tech_keywords = []
        if text:
            common_techs = ['Java', 'Python', 'JavaScript', 'React', 'Spring', 'Node.js', 'MySQL', 'MongoDB', 'AWS', 'Docker']
            for tech in common_techs:
                if tech.lower() in text.lower():
                    tech_keywords.append(tech)
        
        questions = []
        
        # 포트폴리오 기반 질문 생성
        if tech_keywords:
            questions.append(Question(
                question=f"{', '.join(tech_keywords[:2])} 기술을 사용한 프로젝트 경험에 대해 설명해주세요.",
                answer="STAR 기법을 활용하여 답변하세요.",
                type="technical",
                difficulty="intermediate"
            ))
        
        # 기본 질문 추가
        questions.extend([
            Question(
                question=f"{company}에 지원한 이유는 무엇인가요?",
                answer="구체적인 경험과 함께 답변하세요.",
                type="behavioral",
                difficulty="intermediate"
            ),
            Question(
                question="가장 기억에 남는 프로젝트에 대해 설명해주세요.",
                answer="STAR 기법을 활용하여 답변하세요.",
                type="technical",
                difficulty="intermediate"
            )
        ])
        
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
    
    async def analyze_answer(self, question: str, answer: str, user_level: str = "intermediate") -> dict:
        """답변을 분석하여 피드백 생성"""
        # 기본 피드백 생성 (간단한 분석)
        score = min(85, len(answer.split()) * 2)  # 단어 수 기반 점수
        
        return {
            "overall_score": score,
            "star_analysis": {
                "situation": {"present": "상황" in answer or "때" in answer, "quality": "good", "suggestion": "더 구체적인 상황 설명"},
                "task": {"present": "과제" in answer or "문제" in answer, "quality": "good", "suggestion": None},
                "action": {"present": "구현" in answer or "사용" in answer, "quality": "good", "suggestion": None},
                "result": {"present": "결과" in answer or "향상" in answer, "quality": None, "suggestion": "정량적 결과 지표 추가"}
            },
            "technical_accuracy": {"score": score, "correct_concepts": [], "missing_details": []},
            "improvement_suggestions": ["더 구체적인 예시 추가"],
            "strengths": ["경험 기반 답변"],
            "next_steps": ["실무 경험 보강"]
        }
    
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
    
    async def generate_follow_up_questions(self, question: str, answer: str, 
                                         interviewer_persona: str = "친근한_시니어",
                                         max_questions: int = 2, portfolio_text: str = "") -> list:
        """꼬리질문 생성"""
        async with httpx.AsyncClient(timeout=settings.API_TIMEOUT) as client:
            headers = {'Content-Type': 'application/json'}
            
            # 포트폴리오 내용을 포함하여 더 구체적인 꼬리질문 생성
            context_text = f"Portfolio: {portfolio_text[:500]}\n\nOriginal Question: {question}\nUser Answer: {answer}\n\nBased on the user's portfolio and answer, generate specific follow-up questions."
            
            payload = {
                'keywords': [question, answer, 'follow-up', 'detailed'],
                'company': interviewer_persona,
                'text': context_text
            }
            
            response = await client.post(
                "https://forky-ai.kms39273.synology.me/api/v1/questions/generate",
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                follow_ups = []
                for q in result.get('questions', [])[:max_questions]:
                    follow_ups.append({
                        'question': q.get('text', q.get('question', '')),
                        'type': '깊이_파기',
                        'intent': '더 자세한 설명 요청',
                        'difficulty': 'intermediate',
                        'expected_keywords': []
                    })
                return follow_ups
            else:
                return self._get_default_follow_ups()
    
    def _get_default_follow_ups(self) -> list:
        """기본 꼬리질문 반환 (fallback)"""
        return [{
            'question': '조금 더 구체적으로 설명해주실 수 있나요?',
            'type': '깊이_파기',
            'intent': '더 자세한 설명 요청',
            'difficulty': 'intermediate',
            'expected_keywords': []
        }]


class CompanyService:
    """회사별 면접 문화 서비스"""
    
    def __init__(self):
        self.company_cache = {}
        self.upstage_service = UpstageAIService()
    
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
                'keywords': user_keywords,
                'company': company_name,
                'text': f"Company: {company_name}"
            }
            
            response = await client.post(
                "https://forky-ai.kms39273.synology.me/api/v1/questions/generate",
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
        self.upstage_service = UpstageAIService()
    
    async def analyze_portfolio(self, portfolio_text: str, target_company: str = "", 
                              target_position: str = "") -> dict:
        """포트폴리오 분석"""
        # 간단한 포트폴리오 분석
        word_count = len(portfolio_text.split())
        score = min(85, word_count // 10)  # 단어 수 기반 점수
        
        return {
            'overall_assessment': {
                'current_score': score,
                'target_score': 85,
                'market_fit': score + 5,
                'improvement_potential': 'high' if score < 70 else 'medium'
            },
            'detailed_analysis': {
                'technical_skills': {
                    'present_skills': ['기본 기술'],
                    'missing_skills': ['추가 필요 기술'],
                    'skill_depth_score': score,
                    'recommendations': ['기술 스택 보완']
                },
                'project_descriptions': {
                    'clarity_score': score,
                    'quantification_score': max(30, score - 20),
                    'star_usage': max(40, score - 10),
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
