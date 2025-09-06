import httpx
import json
from typing import List, Tuple, Optional
from config import config
from prompts.keyword_extraction import KEYWORD_EXTRACTION_PROMPT
from prompts.question_generation import QUESTION_GENERATION_PROMPT
from prompts.following_question import FOLLOWING_QUESTION_PROMPT
from prompts.question_evaluate import QUESTION_EVALUATE_PROMPT
from prompts.all_evaluate import ALL_EVALUATE_PROMPT
from prompts.portfolio_evaluate import PORTFOLIO_EVALUATE_PROMPT

class LLMProcessor:
    def __init__(self):
        self.api_key = config.UPSTAGE_API_KEY
        self.chat_url = config.UPSTAGE_CHAT_URL
    
    async def _call_llm_structured(self, prompt: str, schema: dict) -> dict:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "solar-pro2",
            "messages": [{"role": "user", "content": prompt}],
            "response_format": {
                "type": "json_schema",
                "json_schema": schema
            },
            "stream": False
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.chat_url,
                headers=headers,
                json=data,
                timeout=30.0
            )
            
            if response.status_code != 200:
                raise Exception(f"LLM call failed: {response.text}")
            
            result = response.json()
            return json.loads(result["choices"][0]["message"]["content"])
    
    async def _call_llm(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "solar-1-mini-chat",
            "messages": [{"role": "user", "content": prompt}],
            "stream": False
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.chat_url,
                headers=headers,
                json=data,
                timeout=30.0
            )
            
            if response.status_code != 200:
                raise Exception(f"LLM call failed: {response.text}")
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
    
    async def extract_keywords(self, html_content: str) -> List[str]:
        schema = {
            "name": "keyword_extraction",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "keywords": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                },
                "required": ["keywords"]
            }
        }
        
        prompt = KEYWORD_EXTRACTION_PROMPT.format(html_content=html_content)
        result = await self._call_llm_structured(prompt, schema)
        return result.get("keywords", [])
    
    async def generate_questions(self, html_content: str, count: int) -> List[dict]:
        schema = {
            "name": "question_generation",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "questions": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "question": {"type": "string"},
                                "tip": {"type": "string"}
                            },
                            "required": ["question", "tip"]
                        }
                    }
                },
                "required": ["questions"]
            }
        }
        
        prompt = QUESTION_GENERATION_PROMPT.format(
            html_content=html_content, 
            question_count=count
        )
        result = await self._call_llm_structured(prompt, schema)
        return result.get("questions", [])
    
    async def generate_following_question(self, question: str, answer: str) -> str:
        schema = {
            "name": "following_question",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "following_question": {"type": "string"}
                },
                "required": ["following_question"]
            }
        }
        
        prompt = FOLLOWING_QUESTION_PROMPT.format(
            question=question, 
            answer=answer
        )
        result = await self._call_llm_structured(prompt, schema)
        return result.get("following_question", "")
    
    async def evaluate_answer(self, question: str, answer: str) -> Tuple[str, Optional[int]]:
        schema = {
            "name": "answer_evaluation",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "feedback": {"type": "string"},
                    "score": {"type": "number"}
                },
                "required": ["feedback", "score"]
            }
        }
        
        prompt = QUESTION_EVALUATE_PROMPT.format(
            question=question, 
            answer=answer
        )
        result = await self._call_llm_structured(prompt, schema)
        return result.get("feedback", ""), result.get("score")
    
    async def evaluate_all_answers(self, qa_pairs: List[dict]) -> Tuple[str, Optional[int]]:
        schema = {
            "name": "overall_evaluation",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "overall_feedback": {"type": "string"},
                    "total_score": {"type": "number"}
                },
                "required": ["overall_feedback", "total_score"]
            }
        }
        
        qa_text = "\n".join([f"Q: {qa['question']}\nA: {qa['answer']}\n" for qa in qa_pairs])
        prompt = ALL_EVALUATE_PROMPT.format(qa_pairs=qa_text)
        result = await self._call_llm_structured(prompt, schema)
        return result.get("overall_feedback", ""), result.get("total_score")
    
    async def evaluate_portfolio(self, html_content: str) -> Tuple[str, Optional[int]]:
        schema = {
            "name": "portfolio_evaluation",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "portfolio_feedback": {"type": "string"},
                    "completeness_score": {"type": "number"}
                },
                "required": ["portfolio_feedback", "completeness_score"]
            }
        }
        
        prompt = PORTFOLIO_EVALUATE_PROMPT.format(html_content=html_content)
        result = await self._call_llm_structured(prompt, schema)
        return result.get("portfolio_feedback", ""), result.get("completeness_score")
