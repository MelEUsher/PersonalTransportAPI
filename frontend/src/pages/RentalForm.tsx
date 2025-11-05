import { useEffect, useMemo, useState } from 'react'
import type { FormEvent } from 'react'
import axios from 'axios'
import { useNavigate, useParams } from 'react-router-dom'
import type { Bike } from '../components/BikeCard'
import api from '../lib/api'

type FormValues = {
  name: string
  email: string
  phone: string
  startDate: string
  endDate: string
  bikeId: string
}

type FieldErrors = Partial<Record<keyof FormValues, string>>

type FetchStatus = 'idle' | 'loading' | 'success' | 'error'

function calculateDurationDays(start: string, end: string): number | null {
  if (!start || !end) {
    return null
  }

  const startDate = new Date(start)
  const endDate = new Date(end)

  if (Number.isNaN(startDate.getTime()) || Number.isNaN(endDate.getTime())) {
    return null
  }

  const diffMs = endDate.getTime() - startDate.getTime()
  return diffMs / (1000 * 60 * 60 * 24)
}

const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

export function RentalForm() {
  const navigate = useNavigate()
  const { bikeId: bikeIdParam } = useParams<{ bikeId?: string }>()

  const [bikes, setBikes] = useState<Bike[]>([])
  const [bikeFetchStatus, setBikeFetchStatus] = useState<FetchStatus>('idle')
  const [values, setValues] = useState<FormValues>({
    name: '',
    email: '',
    phone: '',
    startDate: '',
    endDate: '',
    bikeId: bikeIdParam ?? '',
  })
  const [fieldErrors, setFieldErrors] = useState<FieldErrors>({})
  const [formError, setFormError] = useState<string | null>(null)
  const [isSubmitting, setIsSubmitting] = useState(false)

  useEffect(() => {
    let isMounted = true

    async function loadBikes() {
      setBikeFetchStatus('loading')
      try {
        const response = await api.get<Bike[]>('/api/bikes')
        if (!isMounted) {
          return
        }
        setBikes(response.data)
        setBikeFetchStatus('success')
      } catch (error) {
        console.error('Failed to fetch bikes for rental form', error)
        if (!isMounted) {
          return
        }
        setBikeFetchStatus('error')
      }
    }

    loadBikes()

    return () => {
      isMounted = false
    }
  }, [])

  const availableBikes = useMemo(
    () => bikes.filter((bike) => bike.availability_status === 'available'),
    [bikes],
  )

  useEffect(() => {
    if (availableBikes.length === 0) {
      return
    }

    setValues((previous) => {
      const hasValidSelection = availableBikes.some(
        (bike) => bike.id === Number(previous.bikeId),
      )

      if (hasValidSelection) {
        return previous
      }

      const preferredBike =
        availableBikes.find((bike) => bike.id === Number(bikeIdParam)) ??
        availableBikes[0]

      return {
        ...previous,
        bikeId: preferredBike ? String(preferredBike.id) : '',
      }
    })
  }, [availableBikes, bikeIdParam])

  const selectedBike = useMemo(() => {
    const id = Number(values.bikeId)
    if (!Number.isFinite(id)) {
      return undefined
    }
    return availableBikes.find((bike) => bike.id === id)
  }, [availableBikes, values.bikeId])

  const normalizedDurationDays = (() => {
    const raw = calculateDurationDays(values.startDate, values.endDate)
    if (raw === null) {
      return null
    }
    const rounded = Math.round(raw)
    return Number.isFinite(rounded) ? rounded : null
  })()

  function updateField<Key extends keyof FormValues>(
    field: Key,
    value: FormValues[Key],
  ) {
    setValues((previous) => ({
      ...previous,
      [field]: value,
    }))
  }

  function validate(): FieldErrors {
    const errors: FieldErrors = {}

    if (!values.name.trim()) {
      errors.name = 'Name is required.'
    }

    if (!values.email.trim()) {
      errors.email = 'Email is required.'
    } else if (!emailRegex.test(values.email.trim())) {
      errors.email = 'Enter a valid email address.'
    }

    if (!values.startDate) {
      errors.startDate = 'Start date is required.'
    }

    if (!values.endDate) {
      errors.endDate = 'End date is required.'
    }

    if (!values.bikeId) {
      errors.bikeId = 'Select a bike to continue.'
    }

    const duration = calculateDurationDays(values.startDate, values.endDate)
    if (duration === null) {
      if (!errors.endDate && values.startDate && values.endDate) {
        errors.endDate = 'Provide valid rental dates.'
      }
    } else if (duration <= 0) {
      errors.endDate = 'End date must be after start date.'
    } else if (duration > 3) {
      errors.endDate = 'Rentals cannot exceed 3 days.'
    }

    return errors
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setFormError(null)

    const validationErrors = validate()

    if (Object.keys(validationErrors).length > 0) {
      setFieldErrors(validationErrors)
      return
    }

    setFieldErrors({})
    if (!selectedBike) {
      setFormError(
        'The selected bike is no longer available. Please choose another bike.',
      )
      return
    }

    if (normalizedDurationDays === null || normalizedDurationDays <= 0) {
      setFormError('Provide valid rental dates (up to three days).')
      return
    }

    const totalPriceCents =
      selectedBike.rate_per_day_cents * normalizedDurationDays
    setIsSubmitting(true)

    try {
      const payload = {
        name: values.name.trim(),
        email: values.email.trim(),
        phone: values.phone.trim() || undefined,
        start_date: values.startDate,
        end_date: values.endDate,
        selected_bike: Number(values.bikeId),
        bike_id: Number(values.bikeId),
        total_price_cents: totalPriceCents,
        duration_days: normalizedDurationDays,
      }

      const response = await api.post('/api/rentals', payload)
      const rentalId: unknown = response.data?.id

      if (typeof rentalId !== 'number') {
        throw new Error('Rental created but id was not returned.')
      }

      navigate(`/confirmation/${rentalId}`, {
        state: {
          rentalPreview: {
            name: values.name.trim(),
            email: values.email.trim(),
            phone: values.phone.trim(),
            start_date: values.startDate,
            end_date: values.endDate,
            selected_bike: Number(values.bikeId),
            bike_name: selectedBike?.name ?? null,
            total_price_cents: totalPriceCents,
            duration_days: normalizedDurationDays,
          },
        },
      })
    } catch (error) {
      if (axios.isAxiosError(error)) {
        const serverMessage =
          error.response?.data?.error?.message ??
          error.response?.data?.message ??
          error.message
        setFormError(serverMessage)
      } else if (error instanceof Error) {
        setFormError(error.message)
      } else {
        setFormError('An unexpected error occurred. Please try again.')
      }
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <main className="container">
      <h1>Create a Rental</h1>
      <p>
        Reserve your bike by completing the form. Rentals are limited to three
        consecutive days.
      </p>

      {bikeFetchStatus === 'loading' && (
        <p role="status" aria-live="polite">
          Loading available bikes&hellip;
        </p>
      )}

      {bikeFetchStatus === 'error' && (
        <p role="alert">
          We could not load bikes right now. Please refresh the page and try
          again.
        </p>
      )}

      <form className="rental-form" onSubmit={handleSubmit} noValidate>
        <fieldset className="rental-form__section">
          <legend>Contact details</legend>

          <label className="rental-form__field">
            <span>Name*</span>
            <input
              type="text"
              name="name"
              value={values.name}
              onChange={(event) => updateField('name', event.target.value)}
              aria-invalid={fieldErrors.name ? 'true' : 'false'}
              aria-describedby={fieldErrors.name ? 'name-error' : undefined}
              required
            />
            {fieldErrors.name && (
              <span className="rental-form__error" id="name-error" role="alert">
                {fieldErrors.name}
              </span>
            )}
          </label>

          <label className="rental-form__field">
            <span>Email*</span>
            <input
              type="email"
              name="email"
              value={values.email}
              onChange={(event) => updateField('email', event.target.value)}
              aria-invalid={fieldErrors.email ? 'true' : 'false'}
              aria-describedby={fieldErrors.email ? 'email-error' : undefined}
              required
            />
            {fieldErrors.email && (
              <span
                className="rental-form__error"
                id="email-error"
                role="alert"
              >
                {fieldErrors.email}
              </span>
            )}
          </label>

          <label className="rental-form__field">
            <span>Phone (optional)</span>
            <input
              type="tel"
              name="phone"
              value={values.phone}
              onChange={(event) => updateField('phone', event.target.value)}
            />
          </label>
        </fieldset>

        <fieldset className="rental-form__section">
          <legend>Rental details</legend>

          <label className="rental-form__field">
            <span>Start date*</span>
            <input
              type="date"
              name="start_date"
              value={values.startDate}
              onChange={(event) => updateField('startDate', event.target.value)}
              aria-invalid={fieldErrors.startDate ? 'true' : 'false'}
              aria-describedby={
                fieldErrors.startDate ? 'start-date-error' : undefined
              }
              required
            />
            {fieldErrors.startDate && (
              <span
                className="rental-form__error"
                id="start-date-error"
                role="alert"
              >
                {fieldErrors.startDate}
              </span>
            )}
          </label>

          <label className="rental-form__field">
            <span>End date*</span>
            <input
              type="date"
              name="end_date"
              value={values.endDate}
              onChange={(event) => updateField('endDate', event.target.value)}
              aria-invalid={fieldErrors.endDate ? 'true' : 'false'}
              aria-describedby={
                fieldErrors.endDate ? 'end-date-error' : undefined
              }
              required
            />
            {fieldErrors.endDate && (
              <span
                className="rental-form__error"
                id="end-date-error"
                role="alert"
              >
                {fieldErrors.endDate}
              </span>
            )}
          </label>

          <label className="rental-form__field">
            <span>Bike*</span>
            <select
              name="selected_bike"
              value={values.bikeId}
              onChange={(event) => updateField('bikeId', event.target.value)}
              aria-invalid={fieldErrors.bikeId ? 'true' : 'false'}
              aria-describedby={fieldErrors.bikeId ? 'bike-error' : undefined}
              required
              disabled={availableBikes.length === 0}
            >
              {availableBikes.length === 0 && (
                <option value="">No bikes available</option>
              )}
              {availableBikes.length > 0 && (
                <option value="">Select a bike</option>
              )}
              {availableBikes.map((bike) => (
                <option key={bike.id} value={bike.id}>
                  {bike.name}
                </option>
              ))}
            </select>
            {fieldErrors.bikeId && (
              <span className="rental-form__error" id="bike-error" role="alert">
                {fieldErrors.bikeId}
              </span>
            )}
          </label>

          {selectedBike &&
            normalizedDurationDays !== null &&
            normalizedDurationDays > 0 &&
            normalizedDurationDays <= 3 && (
            <p className="rental-form__summary">
              You are reserving the {selectedBike.name} for {normalizedDurationDays}{' '}
              {normalizedDurationDays === 1 ? 'day' : 'days'}.
            </p>
            )}
        </fieldset>

        {formError && (
          <div className="rental-form__error-panel" role="alert">
            {formError}
          </div>
        )}

        <button
          type="submit"
          className="rental-form__submit"
          disabled={
            isSubmitting || bikeFetchStatus !== 'success' || availableBikes.length === 0
          }
        >
          {isSubmitting ? 'Submitting…' : 'Submit rental request'}
        </button>
      </form>
    </main>
  )
}
