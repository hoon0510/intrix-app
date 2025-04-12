import { NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { get_api_key_by_user } from "@/api/services/api_key_manager";

export async function GET() {
  const session = await getServerSession();
  
  if (!session?.user?.email) {
    return NextResponse.json(
      { error: "인증되지 않은 사용자입니다" },
      { status: 401 }
    );
  }

  try {
    const apiKey = get_api_key_by_user(session.user.email);
    return NextResponse.json({ api_key: apiKey });
  } catch (error) {
    console.error("API 키 조회 중 오류 발생:", error);
    return NextResponse.json(
      { error: "API 키 조회 중 오류가 발생했습니다" },
      { status: 500 }
    );
  }
} 