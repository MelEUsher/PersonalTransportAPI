import { useEffect, useState } from 'react'
import api from '../lib/api'

export function Home() {
  const [apiBase, setApiBase] = useState<string>(
    import.meta.env.VITE_API_BASE_URL ?? 'relative /api',
  )

  useEffect(() => {
    setApiBase(api.defaults.baseURL ?? 'relative /api')
  }, [])

  return (
    <main className="container">
      <h1>Personal Transport Rentals</h1>
      <p>Welcome! This is a placeholder home view for the rental experience.</p>
      <p className="api-hint">
        API Base URL: <code>{apiBase}</code>
      </p>
    </main>
  )
}
