/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  reactStrictMode: true,
  swcMinify: true,
  experimental: {
    appDir: true,
  },
  env: {
    NEXT_PUBLIC_ADMIN_EMAIL: process.env.ADMIN_EMAIL,
  },
  // API 프록시 설정 (Railway에서 백엔드 서비스와 통신)
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: process.env.NEXT_PUBLIC_API_URL + '/api/:path*',
      },
    ];
  },
};

module.exports = nextConfig; 