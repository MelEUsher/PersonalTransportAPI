# Personal Transport Frontend

React + TypeScript SPA scaffolded with Vite for the Personal Transport API project.

## Getting Started

```bash
cd frontend
npm install
cp .env.local.example .env.local # configure VITE_API_BASE_URL
npm run dev
```

The app exposes two placeholder routes:

- `/` — landing screen with environment details
- `/confirm/:id` — reservation confirmation placeholder

## Environment

`VITE_API_BASE_URL` is read at build time and injected into the shared Axios instance (`src/lib/api.ts`). Use `.env.local` for local development; an example file is provided.

## Tooling

- ESLint + Prettier configured for React + TypeScript (`npm run lint`, `npm run format`)
- Production build via `npm run build`
