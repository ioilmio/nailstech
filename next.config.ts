import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'export',
  basePath: '/nailstech',
  assetPrefix: '/nailstech',
  images: {
    unoptimized: true,
  },
};

export default nextConfig;
