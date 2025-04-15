import React from "react";
import { useSession } from "next-auth/react";
import { useRouter } from "next/router";
import type { ComponentType, FC } from "react";

export function withAuth<P extends object>(Component: ComponentType<P>): FC<P> {
  const WithAuthComponent: FC<P> = (props) => {
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

    return <Component {...props} />;
  };

  WithAuthComponent.displayName = `withAuth(${Component.displayName || Component.name || "Component"})`;

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