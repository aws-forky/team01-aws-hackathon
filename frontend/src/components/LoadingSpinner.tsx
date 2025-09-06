// Assumption: Simple CSS-based loading spinner
import React from 'react'

interface LoadingSpinnerProps {
  message?: string
}

export default function LoadingSpinner({ message = '처리 중...' }: LoadingSpinnerProps) {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      <p className="mt-4 text-gray-600">{message}</p>
    </div>
  )
}
