/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  experimental: {
    serverActions: {
      enabled: true
    }
  },
  pageExtensions: ['tsx', 'ts', 'jsx', 'js']
};

module.exports = nextConfig; 