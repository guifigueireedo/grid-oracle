import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "media.formula1.com",
        port: "",
        pathname: "/**",
      },
    ],
  },
};

export default nextConfig;