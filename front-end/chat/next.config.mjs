/** @type {import('next').NextConfig} */
const nextConfig = {
  eslint: { // eslintのlint checkをbuild時にoff
    ignoreDuringBuilds: true,
  },
  typescript: { // type checkをbuild時にoff
    ignoreBuildErrors: true,
  }
}
export default nextConfig;
