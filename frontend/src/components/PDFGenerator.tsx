import React, { useState, useRef } from 'react'
import { InterviewReport } from '../types'
import jsPDF from 'jspdf'
import html2canvas from 'html2canvas'

interface PDFGeneratorProps {
  report: InterviewReport
  onGenerateStart?: () => void
  onGenerateComplete?: () => void
  disabled?: boolean
  className?: string
}

const PDFGenerator: React.FC<PDFGeneratorProps> = ({
  report,
  onGenerateStart,
  onGenerateComplete,
  disabled = false,
  className = ''
}) => {
  const [isGenerating, setIsGenerating] = useState(false)
  const [progress, setProgress] = useState(0)
  const pdfContentRef = useRef<HTMLDivElement>(null)

  // PDF 생성 함수
  const generatePDF = async () => {
    if (isGenerating || disabled) return

    setIsGenerating(true)
    setProgress(0)
    onGenerateStart?.()

    try {
      // PDF 문서 생성
      const pdf = new jsPDF('p', 'mm', 'a4')
      const pageWidth = pdf.internal.pageSize.getWidth()
      const pageHeight = pdf.internal.pageSize.getHeight()
      const margin = 20

      // 한글 폰트 설정 (기본 폰트 사용)
      pdf.setFont('helvetica')

      // 1. 커버 페이지 생성
      await generateCoverPage(pdf, pageWidth, pageHeight, margin)
      setProgress(20)

      // 2. 요약 페이지 생성
      pdf.addPage()
      await generateSummaryPage(pdf, pageWidth, pageHeight, margin)
      setProgress(40)

      // 3. 분석 페이지 생성
      pdf.addPage()
      await generateAnalysisPage(pdf, pageWidth, pageHeight, margin)
      setProgress(60)

      // 4. 상세 결과 페이지들 생성
      for (let i = 0; i < report.detailedResults.length; i++) {
        pdf.addPage()
        await generateDetailPage(pdf, pageWidth, pageHeight, margin, report.detailedResults[i], i + 1)
        setProgress(60 + (i + 1) / report.detailedResults.length * 30)
      }

      // 5. PDF 다운로드
      const fileName = `Forky_면접결과_${new Date().toISOString().split('T')[0]}.pdf`
      pdf.save(fileName)
      setProgress(100)

    } catch (error) {
      console.error('PDF 생성 중 오류:', error)
      alert('PDF 생성 중 오류가 발생했습니다. 다시 시도해주세요.')
    } finally {
      setIsGenerating(false)
      setProgress(0)
      onGenerateComplete?.()
    }
  }

  // 커버 페이지 생성
  const generateCoverPage = async (pdf: jsPDF, pageWidth: number, pageHeight: number, margin: number) => {
    const centerX = pageWidth / 2

    // 로고 영역 (텍스트로 대체)
    pdf.setFontSize(32)
    pdf.setTextColor(59, 130, 246) // blue-600
    pdf.text('Forky', centerX, 60, { align: 'center' })

    pdf.setFontSize(16)
    pdf.setTextColor(107, 114, 128) // gray-500
    pdf.text('AI 기반 포트폴리오 기술면접 시뮬레이터', centerX, 75, { align: 'center' })

    // 제목
    pdf.setFontSize(28)
    pdf.setTextColor(17, 24, 39) // gray-900
    pdf.text('면접 결과 리포트', centerX, 120, { align: 'center' })

    // 면접 정보
    pdf.setFontSize(14)
    pdf.setTextColor(75, 85, 99) // gray-600
    
    const infoY = 150
    const lineHeight = 8
    
    pdf.text(`면접 완료일: ${report.completedAt.toLocaleDateString('ko-KR')}`, centerX, infoY, { align: 'center' })
    pdf.text(`총 소요 시간: ${report.totalDuration}분`, centerX, infoY + lineHeight, { align: 'center' })
    pdf.text(`답변한 질문 수: ${report.totalQuestions}개`, centerX, infoY + lineHeight * 2, { align: 'center' })

    // 전체 점수 (큰 글씨로)
    pdf.setFontSize(48)
    const scoreColor = report.averageScore >= 80 ? [34, 197, 94] : report.averageScore >= 60 ? [251, 191, 36] : [239, 68, 68]
    pdf.setTextColor(scoreColor[0], scoreColor[1], scoreColor[2])
    pdf.text(`${report.averageScore}점`, centerX, 200, { align: 'center' })

    pdf.setFontSize(16)
    pdf.setTextColor(107, 114, 128)
    pdf.text('전체 평균 점수', centerX, 215, { align: 'center' })

    // 하단 정보
    pdf.setFontSize(10)
    pdf.setTextColor(156, 163, 175) // gray-400
    pdf.text('본 리포트는 Forky AI 면접 시뮬레이터에서 생성되었습니다.', centerX, pageHeight - 30, { align: 'center' })
  }

  // 요약 페이지 생성
  const generateSummaryPage = async (pdf: jsPDF, pageWidth: number, pageHeight: number, margin: number) => {
    let currentY = margin + 10

    // 페이지 제목
    pdf.setFontSize(20)
    pdf.setTextColor(17, 24, 39)
    pdf.text('면접 요약', margin, currentY)
    currentY += 15

    // 전체 통계
    pdf.setFontSize(14)
    pdf.setTextColor(75, 85, 99)
    pdf.text('전체 통계', margin, currentY)
    currentY += 10

    pdf.setFontSize(11)
    const stats = [
      `• 전체 평균 점수: ${report.averageScore}점`,
      `• 총 소요 시간: ${report.totalDuration}분`,
      `• 답변한 질문 수: ${report.totalQuestions}개`,
      `• 질문당 평균 시간: ${Math.round(report.totalDuration / report.totalQuestions * 10) / 10}분`
    ]

    stats.forEach(stat => {
      pdf.text(stat, margin + 5, currentY)
      currentY += 6
    })

    currentY += 10

    // 카테고리별 점수
    pdf.setFontSize(14)
    pdf.setTextColor(75, 85, 99)
    pdf.text('카테고리별 성과', margin, currentY)
    currentY += 10

    pdf.setFontSize(11)
    Object.entries(report.categoryScores).forEach(([category, score]) => {
      pdf.text(`• ${category}: ${score}점`, margin + 5, currentY)
      currentY += 6
    })

    currentY += 15

    // 강점
    if (report.strengths.length > 0) {
      pdf.setFontSize(14)
      pdf.setTextColor(34, 197, 94) // green-500
      pdf.text('주요 강점', margin, currentY)
      currentY += 10

      pdf.setFontSize(11)
      pdf.setTextColor(75, 85, 99)
      report.strengths.slice(0, 5).forEach(strength => {
        const lines = pdf.splitTextToSize(`• ${strength}`, pageWidth - margin * 2 - 5)
        lines.forEach((line: string) => {
          pdf.text(line, margin + 5, currentY)
          currentY += 6
        })
      })
    }

    currentY += 10

    // 개선점
    if (report.weaknesses.length > 0) {
      pdf.setFontSize(14)
      pdf.setTextColor(251, 146, 60) // orange-400
      pdf.text('개선이 필요한 점', margin, currentY)
      currentY += 10

      pdf.setFontSize(11)
      pdf.setTextColor(75, 85, 99)
      report.weaknesses.slice(0, 5).forEach(weakness => {
        const lines = pdf.splitTextToSize(`• ${weakness}`, pageWidth - margin * 2 - 5)
        lines.forEach((line: string) => {
          pdf.text(line, margin + 5, currentY)
          currentY += 6
        })
      })
    }
  }

  // 분석 페이지 생성
  const generateAnalysisPage = async (pdf: jsPDF, pageWidth: number, pageHeight: number, margin: number) => {
    let currentY = margin + 10

    // 페이지 제목
    pdf.setFontSize(20)
    pdf.setTextColor(17, 24, 39)
    pdf.text('상세 분석 및 추천사항', margin, currentY)
    currentY += 20

    // 추천 학습 방향
    if (report.recommendations.length > 0) {
      pdf.setFontSize(14)
      pdf.setTextColor(59, 130, 246) // blue-500
      pdf.text('추천 학습 방향', margin, currentY)
      currentY += 10

      pdf.setFontSize(11)
      pdf.setTextColor(75, 85, 99)
      report.recommendations.forEach(recommendation => {
        const lines = pdf.splitTextToSize(`• ${recommendation}`, pageWidth - margin * 2 - 5)
        lines.forEach((line: string) => {
          pdf.text(line, margin + 5, currentY)
          currentY += 6
        })
        currentY += 2
      })
    }

    currentY += 15

    // 면접 팁
    pdf.setFontSize(14)
    pdf.setTextColor(147, 51, 234) // purple-600
    pdf.text('다음 면접을 위한 팁', margin, currentY)
    currentY += 10

    pdf.setFontSize(11)
    pdf.setTextColor(75, 85, 99)
    const tips = [
      '구체적인 예시와 수치를 포함하여 답변하세요',
      'STAR 기법(Situation, Task, Action, Result)을 활용하세요',
      '기술적 용어를 정확하게 사용하고 설명하세요',
      '프로젝트의 기술적 도전과 해결 과정을 강조하세요',
      '팀워크와 커뮤니케이션 경험을 구체적으로 설명하세요'
    ]

    tips.forEach(tip => {
      const lines = pdf.splitTextToSize(`• ${tip}`, pageWidth - margin * 2 - 5)
      lines.forEach((line: string) => {
        pdf.text(line, margin + 5, currentY)
        currentY += 6
      })
    })
  }

  // 상세 결과 페이지 생성
  const generateDetailPage = async (
    pdf: jsPDF, 
    pageWidth: number, 
    pageHeight: number, 
    margin: number, 
    result: any, 
    questionNumber: number
  ) => {
    let currentY = margin + 10

    // 질문 번호 및 제목
    pdf.setFontSize(18)
    pdf.setTextColor(17, 24, 39)
    pdf.text(`질문 ${questionNumber}: ${result.mainQuestion.title}`, margin, currentY)
    currentY += 12

    // 카테고리 및 난이도
    pdf.setFontSize(10)
    pdf.setTextColor(107, 114, 128)
    pdf.text(`카테고리: ${result.mainQuestion.category} | 난이도: ${result.mainQuestion.difficulty}`, margin, currentY)
    currentY += 15

    // 메인 질문
    pdf.setFontSize(12)
    pdf.setTextColor(75, 85, 99)
    pdf.text('질문:', margin, currentY)
    currentY += 8

    pdf.setFontSize(10)
    const questionLines = pdf.splitTextToSize(result.mainQuestion.content, pageWidth - margin * 2)
    questionLines.forEach((line: string) => {
      pdf.text(line, margin, currentY)
      currentY += 5
    })
    currentY += 8

    // 메인 답변
    pdf.setFontSize(12)
    pdf.setTextColor(75, 85, 99)
    pdf.text('답변:', margin, currentY)
    currentY += 8

    pdf.setFontSize(10)
    const answerLines = pdf.splitTextToSize(result.mainAnswer.content, pageWidth - margin * 2)
    answerLines.forEach((line: string) => {
      pdf.text(line, margin, currentY)
      currentY += 5
    })
    currentY += 8

    // 점수 및 피드백
    if (result.mainAnswer.feedback) {
      pdf.setFontSize(12)
      pdf.setTextColor(75, 85, 99)
      pdf.text(`점수: ${result.mainAnswer.feedback.overall_score}점`, margin, currentY)
      currentY += 10

      // 강점
      if (result.mainAnswer.feedback.strengths.length > 0) {
        pdf.setFontSize(11)
        pdf.setTextColor(34, 197, 94)
        pdf.text('강점:', margin, currentY)
        currentY += 6

        pdf.setFontSize(9)
        pdf.setTextColor(75, 85, 99)
        result.mainAnswer.feedback.strengths.slice(0, 3).forEach((strength: string) => {
          const lines = pdf.splitTextToSize(`• ${strength}`, pageWidth - margin * 2 - 5)
          lines.forEach((line: string) => {
            pdf.text(line, margin + 5, currentY)
            currentY += 4
          })
        })
        currentY += 5
      }

      // 개선점
      if (result.mainAnswer.feedback.improvement_suggestions.length > 0) {
        pdf.setFontSize(11)
        pdf.setTextColor(251, 146, 60)
        pdf.text('개선점:', margin, currentY)
        currentY += 6

        pdf.setFontSize(9)
        pdf.setTextColor(75, 85, 99)
        result.mainAnswer.feedback.improvement_suggestions.slice(0, 3).forEach((suggestion: string) => {
          const lines = pdf.splitTextToSize(`• ${suggestion}`, pageWidth - margin * 2 - 5)
          lines.forEach((line: string) => {
            pdf.text(line, margin + 5, currentY)
            currentY += 4
          })
        })
      }
    }

    // 꼬리 질문들 (간략하게)
    if (result.followUpResults.length > 0) {
      currentY += 10
      pdf.setFontSize(12)
      pdf.setTextColor(147, 51, 234)
      pdf.text('꼬리 질문들:', margin, currentY)
      currentY += 8

      result.followUpResults.forEach((followUp: any, index: number) => {
        pdf.setFontSize(10)
        pdf.setTextColor(75, 85, 99)
        pdf.text(`${index + 1}. ${followUp.question.content}`, margin, currentY)
        currentY += 6

        const answerPreview = followUp.answer.content.length > 100 
          ? followUp.answer.content.substring(0, 100) + '...'
          : followUp.answer.content
        
        pdf.setFontSize(9)
        pdf.setTextColor(107, 114, 128)
        const previewLines = pdf.splitTextToSize(`답변: ${answerPreview}`, pageWidth - margin * 2)
        previewLines.forEach((line: string) => {
          pdf.text(line, margin + 5, currentY)
          currentY += 4
        })

        if (followUp.answer.feedback) {
          pdf.text(`점수: ${followUp.answer.feedback.overall_score}점`, margin + 5, currentY)
          currentY += 6
        }
        currentY += 3
      })
    }

    // 페이지 번호
    pdf.setFontSize(8)
    pdf.setTextColor(156, 163, 175)
    pdf.text(`${questionNumber + 3}`, pageWidth - margin, pageHeight - 15, { align: 'right' })
  }

  return (
    <div className={className}>
      <button
        type="button"
        onClick={generatePDF}
        disabled={disabled || isGenerating}
        className={`
          px-6 py-3 rounded-lg font-medium transition-all duration-200 flex items-center justify-center space-x-2
          ${disabled || isGenerating
            ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
            : 'bg-red-600 text-white hover:bg-red-700 focus:ring-2 focus:ring-red-500 focus:ring-offset-2'
          }
        `}
      >
        {isGenerating ? (
          <>
            <svg className="animate-spin w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            <span>PDF 생성 중... ({Math.round(progress)}%)</span>
          </>
        ) : (
          <>
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <span>PDF 다운로드</span>
          </>
        )}
      </button>

      {/* 진행률 표시 */}
      {isGenerating && (
        <div className="mt-2 w-full bg-gray-200 rounded-full h-2">
          <div 
            className="bg-red-600 h-2 rounded-full transition-all duration-300"
            style={{ width: `${progress}%` }}
          />
        </div>
      )}

      {/* 숨겨진 PDF 컨텐츠 (필요시 사용) */}
      <div ref={pdfContentRef} className="hidden">
        {/* PDF 생성을 위한 숨겨진 컨텐츠 영역 */}
      </div>
    </div>
  )
}

export default PDFGenerator