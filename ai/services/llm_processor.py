import json
import boto3
import time
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
        print(f"AWS_ACCESS_KEY_ID: {getattr(config, 'AWS_ACCESS_KEY_ID', 'NOT SET')}")
        print(f"AWS_SECRET_ACCESS_KEY: {getattr(config, 'AWS_SECRET_ACCESS_KEY', 'NOT SET')}")
        
        # AWS 자격증명을 직접 전달
        aws_config = {}
        if hasattr(config, 'AWS_ACCESS_KEY_ID') and config.AWS_ACCESS_KEY_ID:
            aws_config = {
                'aws_access_key_id': config.AWS_ACCESS_KEY_ID,
                'aws_secret_access_key': config.AWS_SECRET_ACCESS_KEY,
                'region_name': 'us-east-1'
            }
        else:
            aws_config = {'region_name': 'us-east-1'}
            
        self.bedrock = boto3.client('bedrock', **aws_config)
        self.bedrock_runtime = boto3.client('bedrock-runtime', **aws_config)
        self.model_id = self._get_or_create_profile()
    
    def _get_or_create_profile(self):
        # Claude Sonnet 4 시스템 정의된 Profile 사용
        return 'arn:aws:bedrock:us-east-1:992382469643:inference-profile/us.anthropic.claude-sonnet-4-20250514-v1:0'
    
    async def _call_bedrock_simple(self, prompt: str) -> str:
        try:
            # Converse API 사용
            response = self.bedrock_runtime.converse(
                modelId=self.model_id,
                messages=[
                    {
                        "role": "user",
                        "content": [{"text": prompt}]
                    }
                ],
                inferenceConfig={
                    "maxTokens": 4000,
                    "temperature": 0.7
                }
            )
            
            # 응답에서 텍스트 추출
            if 'output' in response and 'message' in response['output']:
                content = response['output']['message']['content']
                if content and len(content) > 0 and 'text' in content[0]:
                    return content[0]['text'].strip()
            
            print(f"Unexpected response structure: {response}")
            return ""
            
        except Exception as e:
            print(f"Bedrock converse failed: {e}")
            # ThrottlingException의 경우 기본값 반환
            if "ThrottlingException" in str(e):
                return "요청이 많아 잠시 후 다시 시도해주세요."
            # 다른 오류의 경우 예외 발생
            raise Exception(f"Opus 4.1 호출 실패: {e}")
    
    async def _fallback_invoke_model(self, prompt: str) -> str:
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 4000,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7
        })
        
        try:
            response = self.bedrock_runtime.invoke_model(
                modelId=self.model_id,
                body=body
            )
            
            response_body = json.loads(response['body'].read())
            content = response_body['content'][0]['text']
            return content.strip()
        except Exception as e:
            print(f"Fallback invoke_model failed: {e}")
            return ""
    
    async def _call_bedrock_structured(self, prompt: str, schema: dict) -> dict:
        # 텍스트 생성 후 기본값 반환
        result_text = await self._call_bedrock_simple(prompt)
        
        # JSON 파싱 시도
        try:
            if result_text.startswith('{') or result_text.startswith('['):
                parsed = json.loads(result_text)
                return parsed
        except:
            pass
        
        # 기본 응답 구조 생성
        if schema["name"] == "keyword_extraction":
            # 텍스트에서 키워드 추출 시도
            words = result_text.replace(',', ' ').replace('.', ' ').split()
            keywords = [word.strip() for word in words if len(word) > 2][:10]
            return {"keywords": keywords}
        elif schema["name"] == "question_generation":
            # 텍스트를 줄 단위로 분할하여 질문 추출
            lines = [line.strip() for line in result_text.split('\n') if line.strip() and '?' in line]
            return {"questions": lines[:5]}
        elif schema["name"] == "answer_evaluation":
            return {"feedback": result_text, "score": 85}
        elif schema["name"] == "overall_evaluation":
            return {"overall_feedback": result_text, "total_score": 85}
        elif schema["name"] == "portfolio_evaluation":
            return {"portfolio_feedback": result_text, "completeness_score": 85}
        
        return {}
    
    async def extract_keywords(self, html_content: str) -> List[str]:
        prompt = KEYWORD_EXTRACTION_PROMPT.format(html_content=html_content)
        result_text = await self._call_bedrock_simple(prompt)
        
        # JSON 파싱 시도
        try:
            if result_text.startswith('{') or result_text.startswith('['):
                parsed = json.loads(result_text)
                if isinstance(parsed, dict) and "keywords" in parsed:
                    return parsed["keywords"]
                elif isinstance(parsed, list):
                    return parsed
        except:
            pass
        
        # 텍스트에서 키워드 추출
        words = result_text.replace(',', ' ').replace('.', ' ').replace('\n', ' ').split()
        keywords = [word.strip('[]"\'') for word in words if len(word.strip('[]"\'')) > 2][:10]
        return keywords
    
    async def generate_questions(self, html_content: str, count: int) -> List[dict]:
        prompt = QUESTION_GENERATION_PROMPT.format(
            html_content=html_content, 
            question_count=count
        )
        result_text = await self._call_bedrock_simple(prompt)
        
        # JSON 파싱 시도
        try:
            if result_text.startswith('{') or result_text.startswith('['):
                parsed = json.loads(result_text)
                if isinstance(parsed, dict) and "questions" in parsed:
                    return parsed["questions"]
                elif isinstance(parsed, list):
                    return parsed
        except:
            pass
        
        # 텍스트에서 질문 추출하여 기본 구조로 변환
        lines = [line.strip() for line in result_text.split('\n') if line.strip()]
        questions = []
        for line in lines:
            if '?' in line or line.startswith(('Q:', 'q:', '질문', '문제')):
                clean_question = line.strip('1234567890.- ').strip()
                if clean_question:
                    questions.append({
                        "question": clean_question,
                        "tip": "답변시 구체적인 예시를 포함해주세요."
                    })
        
        return questions[:count] if questions else [{"question": result_text, "tip": "자세히 설명해주세요."}]
    
    async def generate_following_question(self, question: str, answer: str) -> str:
        prompt = FOLLOWING_QUESTION_PROMPT.format(
            question=question, 
            answer=answer
        )
        result = await self._call_bedrock_simple(prompt)
        
        # JSON 응답에서 following_question 추출
        try:
            if result.startswith('{') and result.endswith('}'):
                import json
                parsed = json.loads(result)
                return parsed.get("following_question", result)
        except:
            pass
        
        return result
    
    async def evaluate_answer(self, question: str, answer: str) -> str:
        prompt = QUESTION_EVALUATE_PROMPT.format(
            question=question, 
            answer=answer
        )
        result_text = await self._call_bedrock_simple(prompt)
        
        # JSON 파싱 시도
        try:
            if result_text.startswith('{'):
                parsed = json.loads(result_text)
                return parsed.get("feedback", result_text)
        except:
            pass
        
        return result_text
    
    async def evaluate_all_answers(self, qa_pairs: List[dict]) -> str:
        qa_text = "\n".join([f"Q: {qa['question']}\nA: {qa['answer']}\n" for qa in qa_pairs])
        prompt = ALL_EVALUATE_PROMPT.format(qa_pairs=qa_text)
        result_text = await self._call_bedrock_simple(prompt)
        
        # JSON 파싱 시도
        try:
            if result_text.startswith('{'):
                parsed = json.loads(result_text)
                return parsed.get("overall_feedback", result_text)
        except:
            pass
        
        return result_text
    
    async def evaluate_portfolio(self, html_content: str) -> str:
        prompt = PORTFOLIO_EVALUATE_PROMPT.format(html_content=html_content)
        result_text = await self._call_bedrock_simple(prompt)
        
        # JSON 파싱 시도
        try:
            if result_text.startswith('{'):
                parsed = json.loads(result_text)
                return parsed.get("portfolio_feedback", result_text)
        except:
            pass
        
        return result_text
