// Assumption: Main App component with routing and context provider
import React from 'react'
import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import { AppProvider } from './context/AppContext'
import SetupPage from './pages/SetupPage'
import UploadPage from './pages/UploadPage'
import CompanyPage from './pages/CompanyPage'
import InterviewPage from './pages/InterviewPage'
import ResultPage from './pages/ResultPage'

function App() {
  return (
    <AppProvider>
      <Layout>
        <Routes>
          <Route path="/" element={<SetupPage />} />
          <Route path="/upload" element={<UploadPage />} />
          <Route path="/company" element={<CompanyPage />} />
          <Route path="/interview" element={<InterviewPage />} />
          <Route path="/result" element={<ResultPage />} />
        </Routes>
      </Layout>
    </AppProvider>
  )
}

export default App
