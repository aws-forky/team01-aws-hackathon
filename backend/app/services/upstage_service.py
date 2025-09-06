# Dummy Upstage service to avoid import errors
class UpstageAIService:
    def __init__(self):
        pass
    
    async def extract_keywords(self, text: str):
        return []
    
    async def analyze_answer(self, question: str, answer: str, user_level: str):
        return {}
    
    async def generate_follow_up_questions(self, question: str, answer: str, persona: str, count: int, portfolio: str):
        return []
    
    async def analyze_portfolio(self, text: str, company: str):
        return {}