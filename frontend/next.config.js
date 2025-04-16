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
  // Force App Router
  useFileSystemPublicRoutes: false,
  pageExtensions: ['tsx', 'ts', 'jsx', 'js']
};

module.exports = nextConfig; 