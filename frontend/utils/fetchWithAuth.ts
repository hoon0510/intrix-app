"use client";

import { getSession } from "next-auth/react";

interface User {
  id: string;
  name?: string | null;
  email?: string | null;
  image?: string | null;
}

interface Session {
  user?: User;
}

export async function fetchWithAuth(url: string, options: RequestInit = {}) {
  const session = await getSession() as Session | null;
  const userId = session?.user?.id;

  const headers = {
    ...options.headers,
    "Content-Type": "application/json",
    ...(userId && { "X-User-Id": userId }),
  };

  const response = await fetch(url, {
    ...options,
    headers,
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response.json();
} 