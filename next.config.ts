import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'export',
  basePath: '/nailstech',
  images: {
    unoptimized: true,
  },
};

export default nextConfig;
