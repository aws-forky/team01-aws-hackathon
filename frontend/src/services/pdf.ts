// Assumption: Using jsPDF and html2canvas for PDF generation
import jsPDF from 'jspdf'
import html2canvas from 'html2canvas'
import { Question } from '../types'

export const pdfService = {
  async generatePDF(questions: Question[], company: string): Promise<void> {
    const pdf = new jsPDF()
    
    // Add title
    pdf.setFontSize(20)
    pdf.text(`${company} 면접 질문 및 답안`, 20, 30)
    
    let yPosition = 50
    
    questions.forEach((q, index) => {
      // Check if we need a new page
      if (yPosition > 250) {
        pdf.addPage()
        yPosition = 30
      }
      
      // Question
      pdf.setFontSize(14)
      pdf.text(`Q${index + 1}. ${q.question}`, 20, yPosition)
      yPosition += 15
      
      // Answer
      pdf.setFontSize(10)
      const splitAnswer = pdf.splitTextToSize(q.answer, 170)
      pdf.text(splitAnswer, 20, yPosition)
      yPosition += splitAnswer.length * 5 + 10
    })
    
    pdf.save(`${company}_면접질문.pdf`)
  }
}
