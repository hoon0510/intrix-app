"use client";

import { getSession } from "next-auth/react";

export async function fetchWithAuth(url: string, options: RequestInit = {}) {
  const session = await getSession();
  const userId = session?.user?.id;

  const headers = {
    ...options.headers,
    "Content-Type": "application/json",
    "X-User-ID": userId || "",
  };

  const res = await fetch(url, { ...options, headers });
  return res.json();
} 