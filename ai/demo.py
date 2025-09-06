import gradio as gr
import httpx
import asyncio
import json
from typing import List, Dict, Any

# API 기본 URL
API_BASE_URL = "http://localhost:4700/api/v1"

class InterviewDemo:
    def __init__(self):
        self.client = None
        self.html_content = ""
        self.keywords = []
        self.questions = []
        self.qa_pairs = []
        self.current_question_idx = 0
    
    async def get_client(self):
        """클라이언트 연결 확인 및 재생성"""
        if self.client is None or self.client.is_closed:
            self.client = httpx.AsyncClient(timeout=60.0)
        return self.client
        
    async def parse_pdf(self, pdf_file):
        """PDF 파일을 HTML로 변환"""
        if pdf_file is None:
            return "❌ PDF 파일을 업로드해주세요.", "", ""
        
        try:
            client = await self.get_client()
            # 파일을 바이너리로 읽기
            with open(pdf_file.name, "rb") as f:
                files = {"file": (pdf_file.name, f, "application/pdf")}
                response = await client.post(f"{API_BASE_URL}/documents/parse", files=files)
            
            if response.status_code == 200:
                result = response.json()
                self.html_content = result["html_content"]
                # HTML 전체 내용 표시
                if self.html_content and len(self.html_content.strip()) > 0:
                    return "✅ PDF 파싱 완료!", self.html_content, gr.update(interactive=True)
                else:
                    return "⚠️ PDF 파싱 완료되었지만 내용이 비어있습니다.", "내용 없음", gr.update(interactive=True)
            else:
                return f"❌ PDF 파싱 실패: {response.text}", "", gr.update(interactive=False)
                
        except Exception as e:
            return f"❌ 오류 발생: {str(e)}", "", gr.update(interactive=False)
    
    async def extract_keywords(self):
        """키워드 추출"""
        if not self.html_content:
            return "❌ 먼저 PDF를 파싱해주세요.", ""
        
        try:
            client = await self.get_client()
            response = await client.post(
                f"{API_BASE_URL}/keywords/extract",
                json={"html_content": self.html_content}
            )
            
            if response.status_code == 200:
                result = response.json()
                self.keywords = result["keywords"]
                keywords_text = " | ".join([f"#{kw}" for kw in self.keywords])
                return "✅ 키워드 추출 완료!", keywords_text
            else:
                return f"❌ 키워드 추출 실패: {response.text}", ""
                
        except Exception as e:
            return f"❌ 오류 발생: {str(e)}", ""
    
    async def generate_questions(self, count):
        """면접 질문 생성"""
        if not self.html_content:
            return "❌ 먼저 PDF를 파싱해주세요.", "", gr.update(visible=False)
        
        try:
            client = await self.get_client()
            response = await client.post(
                f"{API_BASE_URL}/questions/generate",
                json={"html_content": self.html_content, "count": count}
            )
            
            if response.status_code == 200:
                result = response.json()
                self.questions = result["questions"]
                self.qa_pairs = []
                self.current_question_idx = 0
                
                questions_text = ""
                for i, q in enumerate(self.questions, 1):
                    questions_text += f"{i}. {q['question']}\n   💡 {q['tip']}\n\n"
                
                return "✅ 질문 생성 완료!", questions_text, gr.update(visible=True)
            else:
                return f"❌ 질문 생성 실패: {response.text}", "", gr.update(visible=False)
                
        except Exception as e:
            return f"❌ 오류 발생: {str(e)}", "", gr.update(visible=False)
    
    def get_current_question(self):
        """현재 질문 반환"""
        if self.current_question_idx < len(self.questions):
            q = self.questions[self.current_question_idx]
            return f"**질문 {self.current_question_idx + 1}/{len(self.questions)}**\n\n{q['question']}\n\n💡 {q['tip']}"
        return "모든 질문이 완료되었습니다!"
    
    async def submit_answer(self, answer):
        """답변 제출 및 평가"""
        if not answer.strip():
            return "❌ 답변을 입력해주세요.", "", "", gr.update(visible=False)
        
        if self.current_question_idx >= len(self.questions):
            return "❌ 모든 질문이 완료되었습니다.", "", "", gr.update(visible=False)
        
        current_q = self.questions[self.current_question_idx]
        
        try:
            client = await self.get_client()
            
            # 답변 평가
            response = await client.post(
                f"{API_BASE_URL}/questions/evaluate",
                json={"question": current_q["question"], "answer": answer}
            )
            
            feedback = ""
            if response.status_code == 200:
                result = response.json()
                feedback = result["feedback"]
            else:
                feedback = f"평가 실패: {response.text}"
            
            # QA 쌍 저장
            self.qa_pairs.append({
                "question": current_q["question"],
                "answer": answer
            })
            
            # 꼬리질문 생성
            follow_response = await client.post(
                f"{API_BASE_URL}/questions/following",
                json={"question": current_q["question"], "answer": answer}
            )
            
            following_question = ""
            if follow_response.status_code == 200:
                follow_result = follow_response.json()
                following_question = follow_result["following_question"]
            
            # 다음 질문으로 이동
            self.current_question_idx += 1
            
            # 모든 질문 완료 시 최종 평가 버튼 표시
            show_final = self.current_question_idx >= len(self.questions)
            
            return feedback, following_question, self.get_current_question(), gr.update(visible=show_final)
            
        except Exception as e:
            return f"❌ 오류 발생: {str(e)}", "", "", gr.update(visible=False)
    
    async def final_evaluation(self):
        """최종 평가"""
        if not self.qa_pairs:
            return "❌ 답변한 질문이 없습니다.", ""
        
        try:
            client = await self.get_client()
            
            # 전체 면접 평가
            response = await client.post(
                f"{API_BASE_URL}/evaluate/all",
                json={"qa_pairs": self.qa_pairs}
            )
            
            overall_feedback = ""
            if response.status_code == 200:
                result = response.json()
                overall_feedback = result["overall_feedback"]
            else:
                overall_feedback = f"전체 평가 실패: {response.text}"
            
            # 포트폴리오 평가
            portfolio_response = await client.post(
                f"{API_BASE_URL}/evaluate/portfolio",
                json={"html_content": self.html_content}
            )
            
            portfolio_feedback = ""
            if portfolio_response.status_code == 200:
                portfolio_result = portfolio_response.json()
                portfolio_feedback = portfolio_result["portfolio_feedback"]
            else:
                portfolio_feedback = f"포트폴리오 평가 실패: {portfolio_response.text}"
            
            return overall_feedback, portfolio_feedback
            
        except Exception as e:
            return f"❌ 오류 발생: {str(e)}", ""

# 전역 인스턴스
demo_instance = InterviewDemo()

# Gradio 인터페이스
def create_interface():
    with gr.Blocks(title="AI 면접 시스템", theme=gr.themes.Soft()) as interface:
        gr.Markdown("# 🎯 AI 면접 시스템")
        gr.Markdown("포트폴리오 PDF를 업로드하여 AI 면접을 진행해보세요!")
        
        with gr.Tab("📄 문서 업로드"):
            pdf_input = gr.File(label="포트폴리오 PDF 업로드", file_types=[".pdf"])
            parse_btn = gr.Button("PDF 파싱", variant="primary")
            parse_status = gr.Textbox(label="파싱 상태", interactive=False)
            html_preview = gr.Textbox(label="HTML 전체 내용", lines=20, interactive=False, max_lines=50)
            
        with gr.Tab("🔍 키워드 추출"):
            extract_btn = gr.Button("키워드 추출", variant="primary", interactive=False)
            keyword_status = gr.Textbox(label="추출 상태", interactive=False)
            keywords_display = gr.Textbox(label="추출된 키워드", interactive=False)
            
        with gr.Tab("❓ 질문 생성"):
            question_count = gr.Slider(minimum=3, maximum=10, value=5, step=1, label="생성할 질문 수")
            generate_btn = gr.Button("질문 생성", variant="primary", interactive=False)
            generate_status = gr.Textbox(label="생성 상태", interactive=False)
            questions_display = gr.Textbox(label="생성된 질문", lines=10, interactive=False)
            
        with gr.Tab("💬 면접 진행") as interview_tab:
            with gr.Column(visible=False) as interview_section:
                current_question = gr.Markdown("질문을 먼저 생성해주세요.")
                answer_input = gr.Textbox(label="답변 입력", lines=5, placeholder="답변을 입력해주세요...")
                submit_btn = gr.Button("답변 제출", variant="primary")
                
                with gr.Row():
                    with gr.Column():
                        gr.Markdown("### 📝 피드백")
                        feedback_display = gr.Textbox(label="답변 피드백", lines=8, interactive=False)
                    with gr.Column():
                        gr.Markdown("### 🔄 꼬리질문")
                        following_display = gr.Textbox(label="꼬리질문", lines=4, interactive=False)
                
                final_btn = gr.Button("최종 평가", variant="secondary", visible=False)
                
        with gr.Tab("📊 최종 평가"):
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### 🎯 면접 종합 평가")
                    overall_evaluation = gr.Textbox(label="전체 면접 평가", lines=15, interactive=False)
                with gr.Column():
                    gr.Markdown("### 📋 포트폴리오 평가")
                    portfolio_evaluation = gr.Textbox(label="포트폴리오 평가", lines=15, interactive=False)
        
        # 이벤트 핸들러
        parse_btn.click(
            fn=lambda pdf: asyncio.run(demo_instance.parse_pdf(pdf)),
            inputs=[pdf_input],
            outputs=[parse_status, html_preview, extract_btn]
        )
        
        extract_btn.click(
            fn=lambda: asyncio.run(demo_instance.extract_keywords()),
            outputs=[keyword_status, keywords_display]
        ).then(
            fn=lambda: gr.update(interactive=True),
            outputs=[generate_btn]
        )
        
        generate_btn.click(
            fn=lambda count: asyncio.run(demo_instance.generate_questions(count)),
            inputs=[question_count],
            outputs=[generate_status, questions_display, interview_section]
        ).then(
            fn=lambda: demo_instance.get_current_question(),
            outputs=[current_question]
        )
        
        submit_btn.click(
            fn=lambda answer: asyncio.run(demo_instance.submit_answer(answer)),
            inputs=[answer_input],
            outputs=[feedback_display, following_display, current_question, final_btn]
        ).then(
            fn=lambda: "",
            outputs=[answer_input]
        )
        
        final_btn.click(
            fn=lambda: asyncio.run(demo_instance.final_evaluation()),
            outputs=[overall_evaluation, portfolio_evaluation]
        )
    
    return interface

if __name__ == "__main__":
    interface = create_interface()
    interface.launch(server_name="0.0.0.0", server_port=7860, share=False)
