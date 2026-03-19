/** @type {import('next').NextConfig} */
const nextConfig = {
  // API proxy — in dev, forward /api/* to FastAPI on :8000
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: process.env.NEXT_PUBLIC_API_URL
          ? `${process.env.NEXT_PUBLIC_API_URL}/:path*`
          : 'http://localhost:8000/:path*',
      },
    ]
  },
  // Standalone output for Docker
  output: 'standalone',
}

module.exports = nextConfig
