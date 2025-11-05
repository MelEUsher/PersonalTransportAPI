import { useEffect, useMemo, useState } from 'react'
import axios from 'axios'
import { useLocation, useParams } from 'react-router-dom'
import api from '../lib/api'

type RentalPreview = {
  name?: string
  email?: string
  phone?: string
  start_date?: string
  end_date?: string
  selected_bike?: number
  bike_name?: string | null
  total_price_cents?: number
  duration_days?: number
}

type RentalRecord = {
  id: number
  start_date?: string
  end_date?: string | null
  total_price_cents?: number
  bike_id?: number
  user_id?: number
  bike_name?: string | null
  name?: string
  email?: string
  phone?: string | null
  customer_name?: string
  customer_email?: string
  customer_phone?: string | null
  [key: string]: unknown
}

type FetchStatus = 'idle' | 'loading' | 'success' | 'error'

const currencyFormatter = new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD',
  minimumFractionDigits: 2,
})

const dateFormatter = new Intl.DateTimeFormat('en-US', { dateStyle: 'medium' })

function parseIsoDate(value: string | undefined | null): Date | null {
  if (!value) {
    return null
  }

  const match = /^(\d{4})-(\d{2})-(\d{2})$/.exec(value)
  if (!match) {
    return null
  }

  const [, year, month, day] = match
  const yearNum = Number(year)
  const monthNum = Number(month)
  const dayNum = Number(day)

  if (
    !Number.isFinite(yearNum) ||
    !Number.isFinite(monthNum) ||
    !Number.isFinite(dayNum)
  ) {
    return null
  }

  return new Date(Date.UTC(yearNum, monthNum - 1, dayNum))
}

function formatDisplayDate(value: string | undefined | null): string | null {
  const parsed = parseIsoDate(value)
  if (!parsed) {
    return null
  }
  return dateFormatter.format(parsed)
}

function computeDurationDays(
  start: string | undefined | null,
  end: string | undefined | null,
): number | null {
  const startDate = parseIsoDate(start)
  const endDate = parseIsoDate(end)
  if (!startDate || !endDate) {
    return null
  }

  const diffMs = endDate.getTime() - startDate.getTime()
  if (diffMs <= 0) {
    return null
  }

  const diffDays = diffMs / (1000 * 60 * 60 * 24)
  const rounded = Math.round(diffDays)
  return Number.isFinite(rounded) ? rounded : null
}

function getString(value: unknown): string | null {
  if (typeof value !== 'string') {
    return null
  }
  const trimmed = value.trim()
  return trimmed.length > 0 ? trimmed : null
}

function getPhone(value: unknown): string | null {
  if (value == null) {
    return null
  }
  if (typeof value === 'string') {
    const trimmed = value.trim()
    return trimmed.length > 0 ? trimmed : null
  }
  return null
}

export function Confirmation() {
  const { id } = useParams<{ id: string }>()
  const location = useLocation()
  const preview: RentalPreview | undefined = (location.state as {
    rentalPreview?: RentalPreview
  })?.rentalPreview

  const [status, setStatus] = useState<FetchStatus>('idle')
  const [errorMessage, setErrorMessage] = useState<string | null>(null)
  const [rental, setRental] = useState<RentalRecord | null>(null)

  useEffect(() => {
    if (!id) {
      setErrorMessage('Rental identifier was not provided.')
      setStatus('error')
      return
    }

    let isActive = true

    async function loadRental() {
      setStatus('loading')
      try {
        const response = await api.get<RentalRecord>(`/api/rentals/${id}`)
        if (!isActive) {
          return
        }
        setRental(response.data)
        setStatus('success')
      } catch (error) {
        if (!isActive) {
          return
        }

        let message =
          'We could not load your rental details. Please try again shortly.'
        if (axios.isAxiosError(error)) {
          message =
            error.response?.data?.error?.message ??
            error.response?.data?.message ??
            error.message ??
            message
        } else if (error instanceof Error) {
          message = error.message
        }

        setErrorMessage(message)
        setStatus('error')
      }
    }

    loadRental()

    return () => {
      isActive = false
    }
  }, [id])

  const startDate = useMemo(
    () => rental?.start_date ?? preview?.start_date ?? null,
    [rental, preview],
  )
  const endDate = useMemo(
    () => rental?.end_date ?? preview?.end_date ?? null,
    [rental, preview],
  )

  const previewDuration =
    typeof preview?.duration_days === 'number' ? preview.duration_days : null

  const formattedStartDate = useMemo(
    () => formatDisplayDate(startDate),
    [startDate],
  )
  const formattedEndDate = useMemo(
    () => formatDisplayDate(endDate),
    [endDate],
  )

  const durationDays = useMemo(() => {
    const computed = computeDurationDays(startDate, endDate)
    if (computed !== null) {
      return computed
    }
    return previewDuration
  }, [startDate, endDate, previewDuration])

  const rawRental = rental as Record<string, unknown> | null

  const contactName =
    getString(rawRental?.['name']) ??
    getString(rawRental?.['customer_name']) ??
    getString(preview?.name)

  const contactEmail =
    getString(rawRental?.['email']) ??
    getString(rawRental?.['customer_email']) ??
    getString(preview?.email)

  const contactPhone =
    getPhone(rawRental?.['phone']) ??
    getPhone(rawRental?.['customer_phone']) ??
    getPhone(preview?.phone)

  const bikeName =
    getString(rawRental?.['bike_name']) ??
    getString(preview?.bike_name) ??
    (rental?.bike_id != null ? `Bike #${rental.bike_id}` : null)

  const previewTotalPrice =
    typeof preview?.total_price_cents === 'number'
      ? preview.total_price_cents
      : null

  const totalPriceCents =
    rental?.total_price_cents ?? previewTotalPrice ?? null

  const totalPrice =
    totalPriceCents != null
      ? currencyFormatter.format(totalPriceCents / 100)
      : null

  return (
    <main className="container">
      <h1>Rental Confirmed</h1>
      <p>Thank you for reserving your ride with Personal Transport Rentals.</p>

      {status === 'loading' && (
        <p role="status" aria-live="polite">
          Retrieving your rental details&hellip;
        </p>
      )}

      {status === 'error' && errorMessage && (
        <p role="alert">{errorMessage}</p>
      )}

      {status === 'success' && rental && (
        <section className="confirmation-card" aria-label="Rental details">
          <h2>Reservation #{rental.id}</h2>

          <dl className="confirmation-card__details">
            {bikeName && (
              <div>
                <dt>Bike</dt>
                <dd>{bikeName}</dd>
              </div>
            )}
            {formattedStartDate && (
              <div>
                <dt>Start date</dt>
                <dd>{formattedStartDate}</dd>
              </div>
            )}
            {formattedEndDate && (
              <div>
                <dt>End date</dt>
                <dd>{formattedEndDate}</dd>
              </div>
            )}
            {durationDays !== null && durationDays > 0 && (
              <div>
                <dt>Duration</dt>
                <dd>
                  {durationDays} {durationDays === 1 ? 'day' : 'days'}
                </dd>
              </div>
            )}
            {totalPrice && (
              <div>
                <dt>Total price</dt>
                <dd>{totalPrice}</dd>
              </div>
            )}
            {rental.user_id != null && (
              <div>
                <dt>User ID</dt>
                <dd>{rental.user_id}</dd>
              </div>
            )}
          </dl>

          {(contactName || contactEmail || contactPhone) && (
            <section className="confirmation-card__contact">
              <h3>Contact details</h3>
              <ul>
                {contactName && <li>{contactName}</li>}
                {contactEmail && <li>{contactEmail}</li>}
                {contactPhone && <li>{contactPhone}</li>}
              </ul>
            </section>
          )}
        </section>
      )}
    </main>
  )
}
