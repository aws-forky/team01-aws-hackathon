from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import documents, keywords, questions, evaluate, health

app = FastAPI(
    title="AI Interview System API",
    description="포트폴리오 기반 AI 면접 시스템",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents.router, prefix="/api/v1")
app.include_router(keywords.router, prefix="/api/v1")
app.include_router(questions.router, prefix="/api/v1")
app.include_router(evaluate.router, prefix="/api/v1")
app.include_router(health.router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=4700)
