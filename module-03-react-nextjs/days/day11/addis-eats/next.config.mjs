/** @type {import('next').NextConfig} */
const nextConfig = {
  /**
   * Enable React Compiler (experimental) for automatic memoisation.
   * This is a Day 36 teaching exercise — in production, verify
   * compatibility with all packages before enabling.
   */
  experimental: {
    reactCompiler: true,
  },

  /**
   * Custom HTTP security headers applied to every response.
   * Good practice even for development — mirrors what you would
   * deploy to production.
   */
  async headers() {
    return [
      {
        source: "/(.*)",
        headers: [
          {
            key: "X-Frame-Options",
            value: "DENY",
          },
          {
            key: "X-Content-Type-Options",
            value: "nosniff",
          },
          {
            key: "Referrer-Policy",
            value: "strict-origin-when-cross-origin",
          },
          {
            key: "Permissions-Policy",
            value: "camera=(), microphone=(), geolocation=()",
          },
        ],
      },
    ];
  },
};

export default nextConfig;
