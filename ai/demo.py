# Gradio 웹 데모 - 사용자 친화적 인터페이스
import gradio as gr
import requests
import json
import os
from typing import Optional, Tuple

API_BASE_URL = "http://localhost:4700/api/v1"

def process_document(file, company_name: Optional[str] = None) -> Tuple[str, str, str]:
    """완전 자동화 파이프라인 처리"""
    if file is None:
        return "파일을 업로드해주세요.", "", ""
    
    try:
        # Gradio 파일 객체는 이미 파일 경로를 제공함
        file_path = file.name if hasattr(file, 'name') else file
        
        with open(file_path, "rb") as f:
            # API 엔드포인트와 매개변수명 맞춤 (file -> file)
            files = {"file": (os.path.basename(file_path), f, "application/octet-stream")}
            data = {"company_name": company_name} if company_name else {}
            
            response = requests.post(
                f"{API_BASE_URL}/questions/process-complete",
                files=files,
                data=data,
                timeout=60.0
            )
        
        if response.status_code == 200:
            result = response.json()
            
            # 결과 포맷팅
            keywords_text = ", ".join(result.get("keywords", []))
            
            questions_text = ""
            for q in result.get("questions", []):
                questions_text += f"**{q['type'].upper()}**: {q['text']}\n"
                questions_text += f"*평가 포인트*: {q['explanation']}\n\n"
            
            # 문서 내용 안전하게 처리
            doc_content = result.get("document_content", "")
            if len(doc_content) > 500:
                doc_preview = doc_content[:500] + "..."
            else:
                doc_preview = doc_content
            
            return (
                f"✅ 처리 완료!\n키워드: {keywords_text}",
                doc_preview,
                questions_text
            )
        else:
            error_detail = ""
            try:
                error_detail = response.json().get("detail", response.text)
            except:
                error_detail = response.text
            return f"❌ 오류 발생: {response.status_code} - {error_detail}", "", ""
            
    except Exception as e:
        return f"❌ 처리 실패: {str(e)}", "", ""

# Gradio 인터페이스 구성
with gr.Blocks(title="AI 포트폴리오 분석기") as demo:
    gr.Markdown("# 🤖 AI 포트폴리오 분석기")
    gr.Markdown("포트폴리오를 업로드하면 AI가 키워드를 추출하고 면접 질문을 생성합니다.")
    
    with gr.Row():
        with gr.Column():
            file_input = gr.File(
                label="포트폴리오 파일 업로드",
                file_types=[".pdf", ".docx", ".txt"]
            )
            company_input = gr.Textbox(
                label="지원 회사명 (선택사항)",
                placeholder="예: 네이버, 카카오, 삼성전자"
            )
            process_btn = gr.Button("분석 시작", variant="primary")
        
        with gr.Column():
            status_output = gr.Textbox(
                label="처리 상태",
                lines=3
            )
    
    with gr.Row():
        document_output = gr.Textbox(
            label="추출된 문서 내용 (미리보기)",
            lines=5
        )
        questions_output = gr.Textbox(
            label="생성된 면접 질문",
            lines=10
        )
    
    process_btn.click(
        fn=process_document,
        inputs=[file_input, company_input],
        outputs=[status_output, document_output, questions_output]
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
