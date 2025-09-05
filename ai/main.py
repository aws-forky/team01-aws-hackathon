# FastAPI 애플리케이션 진입점 - 라우터 통합 및 CORS 설정
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import documents, keywords, questions, health

app = FastAPI(
    title="AI Document Processing API",
    description="API for document parsing and AI-based keyword/question generation",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(documents.router, prefix="/api/v1", tags=["documents"])
app.include_router(keywords.router, prefix="/api/v1", tags=["keywords"])
app.include_router(questions.router, prefix="/api/v1", tags=["questions"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
