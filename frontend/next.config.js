/** @type {import('next').NextConfig} */
const nextConfig = {
  webpack: (config) => {
    config.resolve.alias = {
      ...config.resolve.alias,
      '@': __dirname,
      '@/api': __dirname + '/api',
      '@/app': __dirname + '/app',
      '@/components': __dirname + '/components',
      '@/lib': __dirname + '/lib',
      '@/utils': __dirname + '/utils'
    };
    return config;
  },
  experimental: {
    serverActions: true,
    appDir: true
  },
  // Force App Router
  useFileSystemPublicRoutes: false,
  pageExtensions: ['tsx', 'ts', 'jsx', 'js']
};

module.exports = nextConfig; 