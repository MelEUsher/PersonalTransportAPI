import { useNavigate } from 'react-router-dom'

export type BikeAvailability = 'available' | 'unavailable'

export type Bike = {
  id: number
  name: string
  type: string
  rate_per_day_cents: number
  availability_status: BikeAvailability
}

type BikeCardProps = {
  bike: Bike
}

const currencyFormatter = new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD',
  minimumFractionDigits: 2,
})

export function BikeCard({ bike }: BikeCardProps) {
  const navigate = useNavigate()

  const pricePerDay = currencyFormatter.format(bike.rate_per_day_cents / 100)
  const isAvailable = bike.availability_status === 'available'

  return (
    <article className="bike-card" aria-label={`${bike.name} details`}>
      <header className="bike-card__header">
        <h2>{bike.name}</h2>
        <p className="bike-card__type">{bike.type}</p>
      </header>

      <dl className="bike-card__details">
        <div>
          <dt>Price per day</dt>
          <dd>{pricePerDay}</dd>
        </div>
        <div>
          <dt>Availability</dt>
          <dd>
            <span
              className={`bike-card__availability bike-card__availability--${bike.availability_status}`}
              aria-live="polite"
            >
              {isAvailable ? 'Available now' : 'Currently unavailable'}
            </span>
          </dd>
        </div>
      </dl>

      <button
        type="button"
        className="bike-card__rent-button"
        onClick={() => navigate(`/rent/${bike.id}`)}
        disabled={!isAvailable}
      >
        Rent
      </button>
    </article>
  )
}

