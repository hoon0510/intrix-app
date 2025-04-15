import React from "react";
import { useSession } from "next-auth/react";
import { useRouter } from "next/router";
import type { ComponentType } from "react";

export function withAuth<P extends object>(WrappedComponent: ComponentType<P>) {
  const WithAuthComponent: React.FC<P> = (props) => {
    const { data: session, status } = useSession();
    const router = useRouter();

    React.useEffect(() => {
      if (status === "loading") return;
      
      if (!session) {
        router.replace("/login");
      }
    }, [session, status, router]);

    if (status === "loading") {
      return <div>Loading...</div>;
    }

    if (!session) {
      return null;
    }

    return <WrappedComponent {...props} />;
  };

  WithAuthComponent.displayName = `withAuth(${WrappedComponent.displayName || WrappedComponent.name || "Component"})`;

  return WithAuthComponent;
} 