/** @type {import('next').NextConfig} */
const allowIframes = process.env.USE_SECURE_MODE !== "true";

const nextConfig = {
  async headers() {
    return [
      {
        // Apply these headers to all routes
        source: "/(.*)",
        headers: [
          {
            key: "X-Frame-Options",
            value: allowIframes ? "ALLOWALL" : "SAMEORIGIN",
          },
          // Optionally add a Content-Security-Policy header here too.
        ],
      },
    ];
  },
};

module.exports = nextConfig;
