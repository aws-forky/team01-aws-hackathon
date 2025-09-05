# Solar LLM 처리 - 키워드 추출 및 질문 생성
import json
import logging
import asyncio
import httpx
import os
from typing import Dict, List, Optional, Any
from config import settings

logger = logging.getLogger(__name__)

class LLMProcessor:
    def __init__(self):
        self.api_url = f"{settings.upstage_base_url}/v1/solar/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {settings.upstage_api_key}",
            "Content-Type": "application/json"
        }
        self.last_call_time = 0.0
        # 프롬프트 파일 절대 경로 설정
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.prompts_dir = os.path.join(self.base_dir, "prompts")

    async def _wait_rate_limit(self) -> None:
        """API 호출 간격 제어"""
        current_time = asyncio.get_event_loop().time()
        elapsed = current_time - self.last_call_time
        if elapsed < settings.rate_limit_interval:
            await asyncio.sleep(settings.rate_limit_interval - elapsed)
        self.last_call_time = asyncio.get_event_loop().time()

    async def _call_llm(self, system_prompt: str, user_prompt: str, max_tokens: int = 500) -> Optional[str]:
        """Solar LLM API 호출 (ChatGPT 호환 형식)"""
        try:
            await self._wait_rate_limit()
            
            payload = {
                "model": settings.upstage_model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.3,
                "max_tokens": max_tokens,
                "stream": False
            }

            async with httpx.AsyncClient(timeout=settings.api_timeout) as client:
                response = await client.post(self.api_url, headers=self.headers, json=payload)

            if response.status_code == 200:
                data = response.json()
                if "choices" in data and data["choices"]:
                    return data["choices"][0]["message"]["content"].strip()
            
            return None
            
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            return None

    def _extract_json(self, text: str) -> Optional[Dict[str, Any]]:
        """LLM 응답에서 JSON 형식 데이터 추출"""
        try:
            # 코드 블록 제거
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
            
            # JSON 경계 찾기
            start = text.find("{")
            end = text.rfind("}")
            
            if start != -1 and end != -1:
                json_str = text[start:end + 1]
                return json.loads(json_str)
            
            return None
            
        except json.JSONDecodeError:
            return None

    def _truncate_text(self, text: str, max_length: int) -> str:
        """텍스트 길이 제한"""
        return text[:max_length] + "..." if len(text) > max_length else text

    async def extract_keywords(self, text: str) -> Dict[str, Any]:
        """포트폴리오 텍스트에서 기술 키워드 5-10개 추출"""
        if not settings.upstage_api_key:
            return self._get_fallback_keywords("API key not configured")

        try:
            prompts = self._load_keyword_prompts()
            user_prompt = prompts["user_prompt_template"].format(
                portfolio_text=self._truncate_text(text, settings.max_text_length)
            )
            
            response = await self._call_llm(prompts["system_prompt"], user_prompt, 500)
            
            if response:
                result = self._extract_json(response)
                if result and isinstance(result.get("keywords"), list):
                    return {
                        "keywords": result["keywords"][:10],
                        "detailed_keywords": result.get("detailed_keywords", []),
                        "is_fallback": False,
                        "fallback_reason": None
                    }
            
            return self._get_fallback_keywords("AI keyword extraction failed")
            
        except Exception as e:
            logger.error(f"Keyword extraction error: {e}")
            return self._get_fallback_keywords(f"System error: {e}")

    async def generate_questions(self, text: str, keywords: List[str], company_name: Optional[str] = None) -> Dict[str, Any]:
        """키워드 기반 맞춤형 면접 질문 생성 (기술3개 + 행동2개)"""
        if not settings.upstage_api_key:
            return self._get_fallback_questions(company_name, "API key not configured")

        try:
            prompts = self._load_question_prompts()
            company_info = f"지원 회사: {company_name}" if company_name else "지원 회사: 미지정"
            
            user_prompt = prompts["user_prompt_template"].format(
                portfolio_text=self._truncate_text(text, settings.max_text_length),
                keywords=", ".join(keywords),
                company_info=company_info
            )
            
            response = await self._call_llm(prompts["system_prompt"], user_prompt, settings.max_output_tokens)
            
            if response:
                result = self._extract_json(response)
                if result and isinstance(result.get("questions"), list):
                    return {
                        "questions": result["questions"],
                        "is_fallback": False,
                        "fallback_reason": None
                    }
            
            return self._get_fallback_questions(company_name, "AI question generation failed")
            
        except Exception as e:
            logger.error(f"Question generation error: {e}")
            return self._get_fallback_questions(company_name, f"System error: {e}")

    def _load_keyword_prompts(self) -> Dict[str, str]:
        """키워드 추출 프롬프트 로드"""
        try:
            prompt_file = os.path.join(self.prompts_dir, "keyword_extraction.json")
            with open(prompt_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load keyword prompts: {e}")
            return {
                "system_prompt": "Extract technical keywords from portfolio text.",
                "user_prompt_template": "Extract keywords from: {portfolio_text}"
            }

    def _load_question_prompts(self) -> Dict[str, str]:
        """질문 생성 프롬프트 로드"""
        try:
            prompt_file = os.path.join(self.prompts_dir, "question_generation.json")
            with open(prompt_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load question prompts: {e}")
            return {
                "system_prompt": "Generate interview questions based on portfolio.",
                "user_prompt_template": "Generate questions for: {portfolio_text}\nKeywords: {keywords}\n{company_info}"
            }

    def _get_fallback_keywords(self, reason: str) -> Dict[str, Any]:
        """폴백 키워드 제공"""
        return {
            "keywords": ["JavaScript", "Python", "React", "Node.js", "Git"],
            "detailed_keywords": [],
            "is_fallback": True,
            "fallback_reason": reason
        }

    def _get_fallback_questions(self, company_name: Optional[str], reason: str) -> Dict[str, Any]:
        """폴백 질문 제공"""
        company_text = company_name if company_name else "목표하는 회사"
        
        questions = [
            {
                "id": "fallback_tech_1",
                "type": "technical",
                "text": "프로젝트에서 사용한 주요 기술 스택에 대해 설명해주세요.",
                "explanation": "사용한 기술의 특징과 선택 이유를 설명할 수 있어야 합니다."
            },
            {
                "id": "fallback_tech_2", 
                "type": "technical",
                "text": "개발 과정에서 직면한 가장 어려운 기술적 문제는 무엇이었고, 어떻게 해결했나요?",
                "explanation": "문제 해결 능력과 기술적 사고 과정을 보여줄 수 있어야 합니다."
            },
            {
                "id": "fallback_tech_3",
                "type": "technical", 
                "text": "팀 프로젝트에서 버전 관리는 어떻게 했나요?",
                "explanation": "Git 브랜치 전략, 협업 경험 등을 설명할 수 있어야 합니다."
            },
            {
                "id": "fallback_behavioral_1",
                "type": "behavioral",
                "text": "팀 프로젝트에서 의견 충돌이 발생했을 때 어떻게 해결했나요?",
                "explanation": "협업 능력과 갈등 해결 능력을 보여줄 수 있어야 합니다."
            },
            {
                "id": "fallback_behavioral_2",
                "type": "behavioral", 
                "text": f"{company_text}에서 어떤 기여를 하고 싶나요?",
                "explanation": "회사에 대한 이해와 기여 의지를 보여줄 수 있어야 합니다."
            }
        ]
        
        return {
            "questions": questions,
            "is_fallback": True,
            "fallback_reason": reason
        }
