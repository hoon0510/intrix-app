import { withAuth } from "next-auth/middleware";

export default withAuth({
  pages: {
    signIn: "/login",
  },
});

export const config = {
  matcher: [
    "/mypage/:path*",
    "/analyze/:path*",
    "/api/analyze/:path*",
    "/api/mypage/:path*"
  ]
}; 