// Assumption: Using React Context for global state management
import React, { createContext, useContext, useReducer, ReactNode } from 'react'
import { AppState, Keyword, Question } from '../types'

interface AppContextType {
  state: AppState
  setExtractedText: (text: string) => void
  setKeywords: (keywords: Keyword[]) => void
  setSelectedCompany: (company: string) => void
  setQuestions: (questions: Question[]) => void
  nextStep: () => void
  resetApp: () => void
}

const AppContext = createContext<AppContextType | undefined>(undefined)

const initialState: AppState = {
  extractedText: '',
  keywords: [],
  selectedCompany: '',
  questions: [],
  currentStep: 0
}

type Action = 
  | { type: 'SET_EXTRACTED_TEXT'; payload: string }
  | { type: 'SET_KEYWORDS'; payload: Keyword[] }
  | { type: 'SET_SELECTED_COMPANY'; payload: string }
  | { type: 'SET_QUESTIONS'; payload: Question[] }
  | { type: 'NEXT_STEP' }
  | { type: 'RESET' }

function appReducer(state: AppState, action: Action): AppState {
  switch (action.type) {
    case 'SET_EXTRACTED_TEXT':
      return { ...state, extractedText: action.payload }
    case 'SET_KEYWORDS':
      return { ...state, keywords: action.payload }
    case 'SET_SELECTED_COMPANY':
      return { ...state, selectedCompany: action.payload }
    case 'SET_QUESTIONS':
      return { ...state, questions: action.payload }
    case 'NEXT_STEP':
      return { ...state, currentStep: state.currentStep + 1 }
    case 'RESET':
      return initialState
    default:
      return state
  }
}

export function AppProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(appReducer, initialState)

  const contextValue: AppContextType = {
    state,
    setExtractedText: (text) => dispatch({ type: 'SET_EXTRACTED_TEXT', payload: text }),
    setKeywords: (keywords) => dispatch({ type: 'SET_KEYWORDS', payload: keywords }),
    setSelectedCompany: (company) => dispatch({ type: 'SET_SELECTED_COMPANY', payload: company }),
    setQuestions: (questions) => dispatch({ type: 'SET_QUESTIONS', payload: questions }),
    nextStep: () => dispatch({ type: 'NEXT_STEP' }),
    resetApp: () => dispatch({ type: 'RESET' })
  }

  return (
    <AppContext.Provider value={contextValue}>
      {children}
    </AppContext.Provider>
  )
}

export function useApp() {
  const context = useContext(AppContext)
  if (!context) {
    throw new Error('useApp must be used within AppProvider')
  }
  return context
}
