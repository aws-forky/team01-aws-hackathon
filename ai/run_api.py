#!/usr/bin/env python3
"""
API Server Runner - 개발 환경용 서버 실행 스크립트
"""

import uvicorn
from main import app

if __name__ == "__main__":
    print("Starting AI Document Processing API...")
    print("API Documentation: http://localhost:4700/docs")
    print("Health Check: http://localhost:4700/api/v1/health")
    print("Press Ctrl+C to stop")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=4700,
        reload=True,
        log_level="info"
    )
