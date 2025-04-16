/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  experimental: {
    serverActions: {
      enabled: true
    },
    appDir: true
  },
  pageExtensions: ['tsx', 'ts', 'jsx', 'js']
};

module.exports = nextConfig; 