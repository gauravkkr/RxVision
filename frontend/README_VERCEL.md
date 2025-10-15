# Deploy frontend to Vercel

1. Set the Vercel project to point at this repository and the `frontend` directory.
2. In the Vercel project settings, add an Environment Variable named `VITE_API_URL` with the URL of your backend (for example, `https://your-backend.example.com`).
3. Build command: `npm run build`
4. Output directory: `dist`

Notes:
- The frontend now uses `import.meta.env.VITE_API_URL` to call the backend. If not set, it falls back to `http://127.0.0.1:8080` for local testing.
