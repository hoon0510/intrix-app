/** @type {import('next').NextConfig} */
const path = require('path');

const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  images: {
    domains: [],
  },
  transpilePackages: ['recharts'],
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'https://intrix-app-production.up.railway.app/api/:path*',
      },
    ];
  },
  webpack: (config) => {
    config.resolve.alias = {
      ...config.resolve.alias,
      '@': path.resolve(__dirname),
      '@/components': path.resolve(__dirname, 'components'),
      '@/lib': path.resolve(__dirname, 'lib'),
      '@/utils': path.resolve(__dirname, 'utils')
    };
    return config;
  },
};

module.exports = nextConfig; 