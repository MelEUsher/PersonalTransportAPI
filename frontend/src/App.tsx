import { Route, Routes } from 'react-router-dom'
import './App.css'
import { Confirm } from './pages/Confirm'
import { Home } from './pages/Home'
import { BikeList } from './pages/BikeList'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/bikes" element={<BikeList />} />
      <Route path="/confirm/:id" element={<Confirm />} />
    </Routes>
  )
}

export default App
