/** @type {import('next').NextConfig} */
const nextConfig = {
  webpack: (config) => {
    config.resolve.alias = {
      ...config.resolve.alias,
      '@': __dirname,
      '@/api': __dirname + '/api',
      '@/app': __dirname + '/app',
    };
    return config;
  },
  experimental: {
    serverActions: true,
  },
};

module.exports = nextConfig; 