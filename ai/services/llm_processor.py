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
    
    def _parse_json_response(self, response: str) -> dict:
        try:
            # Remove code blocks if present
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                response = response.split("```")[1].split("```")[0]
            
            return json.loads(response.strip())
        except:
            return {}
    
    async def extract_keywords(self, html_content: str) -> List[str]:
        prompt = KEYWORD_EXTRACTION_PROMPT.format(html_content=html_content)
        response = await self._call_llm(prompt)
        
        parsed = self._parse_json_response(response)
        return parsed.get("keywords", [])
    
    async def generate_questions(self, html_content: str, count: int) -> List[str]:
        prompt = QUESTION_GENERATION_PROMPT.format(
            html_content=html_content, 
            question_count=count
        )
        response = await self._call_llm(prompt)
        
        parsed = self._parse_json_response(response)
        return parsed.get("questions", [])
    
    async def generate_following_question(self, question: str, answer: str) -> str:
        prompt = FOLLOWING_QUESTION_PROMPT.format(
            question=question, 
            answer=answer
        )
        response = await self._call_llm(prompt)
        
        parsed = self._parse_json_response(response)
        return parsed.get("following_question", "")
    
    async def evaluate_answer(self, question: str, answer: str) -> Tuple[str, Optional[int]]:
        prompt = QUESTION_EVALUATE_PROMPT.format(
            question=question, 
            answer=answer
        )
        response = await self._call_llm(prompt)
        
        parsed = self._parse_json_response(response)
        return parsed.get("feedback", ""), parsed.get("score")
    
    async def evaluate_all_answers(self, qa_pairs: List[dict]) -> Tuple[str, Optional[int]]:
        qa_text = "\n".join([f"Q: {qa['question']}\nA: {qa['answer']}\n" for qa in qa_pairs])
        prompt = ALL_EVALUATE_PROMPT.format(qa_pairs=qa_text)
        response = await self._call_llm(prompt)
        
        parsed = self._parse_json_response(response)
        return parsed.get("overall_feedback", ""), parsed.get("total_score")
    
    async def evaluate_portfolio(self, html_content: str) -> Tuple[str, Optional[int]]:
        prompt = PORTFOLIO_EVALUATE_PROMPT.format(html_content=html_content)
        response = await self._call_llm(prompt)
        
        parsed = self._parse_json_response(response)
        return parsed.get("portfolio_feedback", ""), parsed.get("completeness_score")
