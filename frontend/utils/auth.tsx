"use client";

import React, { useEffect } from "react";
import { useSession } from "next-auth/react";
import { useRouter } from "next/router";
import type { ComponentType, PropsWithChildren } from "react";

export function withAuth<P extends object>(
  WrappedComponent: ComponentType<P>
): ComponentType<P> {
  const WithAuthComponent = (props: P) => {
    const router = useRouter();
    const { data: session, status } = useSession({
      required: true,
      onUnauthenticated() {
        router.push("/login");
      },
    });

    if (status === "loading") {
      return <div>Loading...</div>;
    }

    return <WrappedComponent {...props} />;
  };

  WithAuthComponent.displayName = `withAuth(${WrappedComponent.displayName || WrappedComponent.name || "Component"})`;

  return WithAuthComponent;
}

export const requireAuth = () => {
  const { data: session } = useSession();
  const router = useRouter();
  
  if (!session) {
    router.replace("/login");
    return false;
  }
  
  return true;
}; 