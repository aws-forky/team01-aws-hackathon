"""
Upstage API를 활용한 AI 서비스
실시간 피드백, 꼬리질문 생성, 포트폴리오 분석 등 핵심 기능 구현
"""
import httpx
import json
from typing import List, Dict, Any
from app.config.config import settings

class UpstageAIService:
    """Upstage Solar LLM을 활용한 AI 서비스"""
    
    def __init__(self):
        self.api_key = settings.UPSTAGE_API_KEY
        self.base_url = settings.UPSTAGE_BASE_URL
        self.model = settings.UPSTAGE_MODEL
        
    async def _call_upstage_api(self, prompt: str, max_tokens: int = 800) -> str:
        """Upstage API 호출"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "당신은 10년차 IT 기술면접관이자 채용 전문가입니다."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": max_tokens,
                "temperature": 0.7
            }
            
            response = await client.post(
                f"{self.base_url}/v1/chat/completions",
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                raise Exception(f"Upstage API error: {response.status_code}")

    async def analyze_answer_feedback(self, question: str, answer: str, user_level: str = "intermediate") -> Dict[str, Any]:
        """답변 분석 및 피드백 생성"""
        prompt = f"""
당신은 10년차 IT 기술면접관입니다. 사용자의 답변을 다음 기준으로 분석하세요:

[분석 항목]
1. STAR 기법 완성도 (Situation, Task, Action, Result)
2. 기술적 정확성 (언급된 기술의 올바른 이해도)
3. 구체성 수준 (정량적 지표, 구체적 사례)
4. 논리적 구조 (답변의 일관성 및 흐름)

[출력 형식 - 반드시 JSON으로 응답]
{{
  "overall_score": 85,
  "star_analysis": {{
    "situation": {{"present": true, "quality": "good", "suggestion": "더 구체적인 상황 설명"}},
    "task": {{"present": true, "quality": "excellent", "suggestion": null}},
    "action": {{"present": true, "quality": "good", "suggestion": "기술적 선택 이유 추가"}},
    "result": {{"present": false, "quality": null, "suggestion": "정량적 결과 지표 필수"}}
  }},
  "technical_accuracy": {{
    "score": 90,
    "correct_concepts": ["Redis 캐싱", "API 최적화"],
    "missing_details": ["캐시 무효화 전략"]
  }},
  "improvement_suggestions": [
    "결과 부분에 구체적 수치 추가",
    "기술 선택 근거 설명 보완"
  ],
  "strengths": [
    "기술적 이해도가 높음",
    "실제 경험 기반 답변"
  ]
}}

질문: {question}
답변: {answer}
사용자 레벨: {user_level}
"""
        
        try:
            response = await self._call_upstage_api(prompt, 600)
            # JSON 파싱 시도
            return json.loads(response)
        except json.JSONDecodeError:
            # JSON 파싱 실패시 기본 응답
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
                "strengths": ["경험 기반 답변"]
            }

    async def generate_follow_up_questions(self, question: str, answer: str, 
                                         interviewer_persona: str = "친근한_시니어", 
                                         max_questions: int = 2) -> List[Dict[str, Any]]:
        """꼬리질문 생성"""
        persona_prompts = {
            "친근한_시니어": "당신은 친근하고 경험 많은 시니어 개발자입니다. 사용자를 격려하면서도 기술적 깊이를 파악하려고 합니다.",
            "까다로운_테크리드": "당신은 기술적으로 까다로운 테크리드입니다. 정확성과 깊이 있는 이해를 중시하며 압박감 있는 질문을 합니다.",
            "비즈니스_중심_매니저": "당신은 비즈니스 가치를 중시하는 개발 매니저입니다. 기술적 구현보다 비즈니스 임팩트와 ROI에 관심이 많습니다."
        }
        
        prompt = f"""
{persona_prompts.get(interviewer_persona, persona_prompts["친근한_시니어"])}

사용자의 답변을 분석하여 적절한 꼬리질문을 생성하세요.

[꼬리질문 패턴]
1. 깊이_파기: 구체적인 구현 세부사항 질문
2. 대안_탐색: 다른 기술 선택지와 비교
3. 문제_상황: 어려움이나 예상치 못한 문제
4. 확장_시나리오: 확장 상황에서의 대응
5. 비즈니스_연결: 비즈니스 임팩트 연결

[출력 형식 - 반드시 JSON으로 응답]
{{
  "follow_up_questions": [
    {{
      "question": "구체적인 꼬리질문",
      "type": "깊이_파기",
      "intent": "이 질문의 의도",
      "difficulty": "intermediate",
      "expected_keywords": ["예상 키워드"]
    }}
  ]
}}

원래 질문: {question}
사용자 답변: {answer}
최대 질문 수: {max_questions}
"""
        
        try:
            response = await self._call_upstage_api(prompt, 400)
            result = json.loads(response)
            return result.get("follow_up_questions", [])
        except json.JSONDecodeError:
            # 기본 꼬리질문 반환
            return [{
                "question": "조금 더 구체적으로 설명해주실 수 있나요?",
                "type": "깊이_파기",
                "intent": "더 자세한 설명 요청",
                "difficulty": "intermediate",
                "expected_keywords": []
            }]

    async def analyze_portfolio(self, portfolio_text: str, target_company: str = "", 
                              target_position: str = "") -> Dict[str, Any]:
        """포트폴리오 분석"""
        prompt = f"""
당신은 10년차 IT 채용 전문가입니다. 포트폴리오를 분석하여 개선점을 제안하세요.

[분석 기준]
1. 기술 스택 시장 적합성
2. 프로젝트 설명의 명확성
3. 성과 지표의 구체성
4. STAR 기법 적용도
5. 스토리텔링 완성도

[출력 형식 - 반드시 JSON으로 응답]
{{
  "overall_assessment": {{
    "current_score": 68,
    "target_score": 85,
    "market_fit": 75,
    "improvement_potential": "high"
  }},
  "detailed_analysis": {{
    "technical_skills": {{
      "present_skills": ["현재 보유 기술"],
      "missing_skills": ["부족한 기술"],
      "skill_depth_score": 75,
      "recommendations": ["기술 보완 방안"]
    }},
    "project_descriptions": {{
      "clarity_score": 65,
      "quantification_score": 30,
      "star_usage": 40,
      "improvements": ["구체적 개선 방안"]
    }}
  }},
  "priority_improvements": [
    {{
      "category": "성과 지표 정량화",
      "current_issue": "현재 문제점",
      "suggestion": "구체적 개선 방안",
      "example": "개선 예시",
      "impact": "high",
      "effort": "low",
      "timeline": "2-3일"
    }}
  ]
}}

목표 회사: {target_company}
목표 직무: {target_position}
포트폴리오 내용:
{portfolio_text[:1500]}
"""
        
        try:
            response = await self._call_upstage_api(prompt, 800)
            return json.loads(response)
        except json.JSONDecodeError:
            # 기본 분석 결과 반환
            return {
                "overall_assessment": {
                    "current_score": 70,
                    "target_score": 85,
                    "market_fit": 75,
                    "improvement_potential": "medium"
                },
                "detailed_analysis": {
                    "technical_skills": {
                        "present_skills": ["기본 기술"],
                        "missing_skills": ["추가 필요 기술"],
                        "skill_depth_score": 70,
                        "recommendations": ["기술 스택 보완"]
                    },
                    "project_descriptions": {
                        "clarity_score": 70,
                        "quantification_score": 50,
                        "star_usage": 60,
                        "improvements": ["구체적 수치 추가"]
                    }
                },
                "priority_improvements": [{
                    "category": "성과 지표 정량화",
                    "current_issue": "정량적 지표 부족",
                    "suggestion": "구체적 수치로 성과 표현",
                    "example": "사용자 만족도 향상 → 사용자 만족도 4.2에서 4.7로 12% 향상",
                    "impact": "high",
                    "effort": "low",
                    "timeline": "2-3일"
                }]
            }

    async def generate_company_questions(self, company_name: str, user_keywords: List[str]) -> List[Dict[str, Any]]:
        """회사별 맞춤 질문 생성"""
        prompt = f"""
당신은 {company_name}의 시니어 개발자이자 면접관입니다.

[회사별 특성 반영]
- 네이버: 대규모 트래픽, 검색/광고 기술, Java/Spring 중심
- 카카오: 모바일 플랫폼, 메신저 서비스, Kotlin/React 중심  
- 삼성전자: 하드웨어 연동, 임베디드, C++/Android 중심
- 쿠팡: 이커머스, 물류 최적화, Java/AWS 중심

[출력 형식 - 반드시 JSON으로 응답]
{{
  "customized_questions": [
    {{
      "question": "회사 특성을 반영한 구체적 질문",
      "category": "기술",
      "company_relevance": "이 질문이 우리 회사에 중요한 이유",
      "expected_answer_direction": "기대하는 답변 방향",
      "difficulty": "intermediate"
    }}
  ]
}}

회사: {company_name}
사용자 기술 키워드: {user_keywords}
"""
        
        try:
            response = await self._call_upstage_api(prompt, 600)
            result = json.loads(response)
            return result.get("customized_questions", [])
        except json.JSONDecodeError:
            # 기본 질문 반환
            return [{
                "question": f"{company_name}에 지원한 이유와 기여할 수 있는 부분을 설명해주세요.",
                "category": "문화",
                "company_relevance": "회사 적합성 확인",
                "expected_answer_direction": "회사 이해도와 기여 의지",
                "difficulty": "intermediate"
            }]

    async def extract_keywords(self, text: str) -> List[Dict[str, Any]]:
        """기술 키워드 추출"""
        prompt = f"""
다음 포트폴리오 텍스트에서 기술 관련 키워드를 추출하세요.

[키워드 카테고리]
- language: 프로그래밍 언어 (Java, Python, JavaScript 등)
- framework: 프레임워크 (Spring, React, Django 등)
- database: 데이터베이스 (MySQL, Redis, MongoDB 등)
- cloud: 클라우드 서비스 (AWS, GCP, Azure 등)
- tool: 개발 도구 (Docker, Git, Jenkins 등)

[출력 형식 - 반드시 JSON으로 응답]
{{
  "keywords": [
    {{
      "name": "키워드명",
      "category": "language",
      "importance": 9
    }}
  ]
}}

텍스트:
{text[:1000]}
"""
        
        try:
            response = await self._call_upstage_api(prompt, 400)
            result = json.loads(response)
            return result.get("keywords", [])
        except json.JSONDecodeError:
            # 기본 키워드 반환
            return [
                {"name": "Java", "category": "language", "importance": 8},
                {"name": "Spring", "category": "framework", "importance": 7},
                {"name": "MySQL", "category": "database", "importance": 6}
            ]

    async def generate_questions(self, keywords: List[str], company: str, text: str = "") -> List[Dict[str, Any]]:
        """면접 질문 생성"""
        prompt = f"""
다음 키워드와 회사 정보를 바탕으로 기술면접 질문을 생성하세요.

[출력 형식 - 반드시 JSON으로 응답]
{{
  "questions": [
    {{
      "question": "구체적인 면접 질문",
      "answer": "모범 답변 가이드",
      "type": "technical",
      "difficulty": "intermediate"
    }}
  ]
}}

키워드: {keywords}
회사: {company}
"""
        
        try:
            response = await self._call_upstage_api(prompt, 600)
            result = json.loads(response)
            return result.get("questions", [])
        except json.JSONDecodeError:
            # 기본 질문 반환
            return [{
                "question": "가장 기억에 남는 프로젝트에 대해 설명해주세요.",
                "answer": "STAR 기법을 활용하여 상황, 과제, 행동, 결과 순으로 설명하세요.",
                "type": "technical",
                "difficulty": "intermediate"
            }]