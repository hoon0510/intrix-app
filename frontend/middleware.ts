export { default } from "next-auth/middleware";

export const config = {
  matcher: [
    "/mypage/:path*",
    "/analyze/:path*",
    "/api/analyze/:path*",
    "/api/mypage/:path*"
  ]
}; 