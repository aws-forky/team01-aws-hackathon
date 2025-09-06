// Assumption: Simple layout with header and main content area
import React, { ReactNode } from 'react'

interface LayoutProps {
  children: ReactNode
}

export default function Layout({ children }: LayoutProps) {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <h1 className="text-2xl font-bold text-primary">🍴 Forky</h1>
          <p className="text-sm text-gray-600">AI 기반 포트폴리오 기술면접 시뮬레이터</p>
        </div>
      </header>
      
      <main className="max-w-4xl mx-auto px-4 py-8">
        {children}
      </main>
      
      <footer className="bg-white border-t mt-16">
        <div className="max-w-4xl mx-auto px-4 py-6 text-center text-gray-500">
          <p>&copy; 2025 Forky. AI로 더 나은 면접 준비를.</p>
        </div>
      </footer>
    </div>
  )
}
