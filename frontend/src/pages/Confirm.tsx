import { useParams } from 'react-router-dom'

export function Confirm() {
  const { id } = useParams<{ id: string }>()

  return (
    <main className="container">
      <h1>Confirm Rental</h1>
      <p>Reservation reference: {id}</p>
      <p>This confirmation screen is ready for future integration.</p>
    </main>
  )
}
