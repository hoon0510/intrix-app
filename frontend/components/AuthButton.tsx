"use client";

import { signIn, signOut, useSession } from "next-auth/react";

export default function AuthButton() {
  const { data: session, status } = useSession();

  if (status === "loading") return <p>Loading...</p>;

  return (
    <div>
      {session ? (
        <div className="flex items-center gap-2">
          <p>{session.user?.email}</p>
          <button onClick={() => signOut()}>Logout</button>
        </div>
      ) : (
        <button onClick={() => signIn("google")}>Login with Google</button>
      )}
    </div>
  );
} 