import { Route, Routes } from 'react-router-dom'
import './App.css'
import { Home } from './pages/Home'
import { BikeList } from './pages/BikeList'
import { RentalForm } from './pages/RentalForm'
import { Confirmation } from './pages/Confirmation'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/bikes" element={<BikeList />} />
      <Route path="/rent" element={<RentalForm />} />
      <Route path="/rent/:bikeId" element={<RentalForm />} />
      <Route path="/confirmation/:id" element={<Confirmation />} />
    </Routes>
  )
}

export default App
