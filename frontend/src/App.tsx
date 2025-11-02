import { Route, Routes } from 'react-router-dom'
import './App.css'
import { Confirm } from './pages/Confirm'
import { Home } from './pages/Home'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/confirm/:id" element={<Confirm />} />
    </Routes>
  )
}

export default App
