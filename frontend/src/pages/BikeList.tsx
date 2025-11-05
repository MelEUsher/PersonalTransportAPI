import { useEffect, useState } from 'react'
import { BikeCard } from '../components/BikeCard'
import type { Bike } from '../components/BikeCard'
import api from '../lib/api'

type FetchState = 'idle' | 'loading' | 'success' | 'error'

export function BikeList() {
  const [bikes, setBikes] = useState<Bike[]>([])
  const [status, setStatus] = useState<FetchState>('idle')

  useEffect(() => {
    let isActive = true

    async function loadBikes() {
      setStatus('loading')

      try {
        const response = await api.get<Bike[]>('/api/bikes')
        if (!isActive) return
        setBikes(response.data)
        setStatus('success')
      } catch (error) {
        console.error('Failed to fetch bikes', error)
        if (!isActive) return
        setStatus('error')
      }
    }

    loadBikes()

    return () => {
      isActive = false
    }
  }, [])

  const showEmptyState = status === 'success' && bikes.length === 0

  return (
    <main className="container">
      <h1>Available Bikes</h1>
      <p>Choose the perfect ride for your next adventure.</p>

      {status === 'loading' && (
        <p role="status" aria-live="polite">
          Loading bikes&hellip;
        </p>
      )}

      {status === 'error' && (
        <p role="alert">
          We could not load the bike list. Please try again in a moment.
        </p>
      )}

      {showEmptyState && (
        <p role="status" aria-live="polite">
          No bikes are currently available. Please check back soon.
        </p>
      )}

      {status === 'success' && bikes.length > 0 && (
        <section className="bike-grid" aria-label="Available bikes">
          {bikes.map((bike) => (
            <BikeCard key={bike.id} bike={bike} />
          ))}
        </section>
      )}
    </main>
  )
}
