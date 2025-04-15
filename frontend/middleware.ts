import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export const runtime = 'edge';

export default function middleware(request: NextRequest) {
  const session = request.cookies.get("next-auth.session-token");
  
  if (!session) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    "/mypage/:path*",
    "/analyze/:path*",
    "/api/analyze/:path*",
    "/api/mypage/:path*"
  ]
}; 