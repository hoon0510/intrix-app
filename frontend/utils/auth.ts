import React from 'react';
import { useRouter } from 'next/router';

export const isAuthenticated = (): boolean => {
  if (typeof window === 'undefined') return false;
  
  const token = localStorage.getItem('auth_token');
  return !!token;
};

export const getAuthToken = (): string | null => {
  if (typeof window === 'undefined') return null;
  
  return localStorage.getItem('auth_token');
};

export const requireAuth = () => {
  const router = useRouter();
  
  if (typeof window !== 'undefined' && !isAuthenticated()) {
    router.push('/login');
    return false;
  }
  
  return true;
};

export const withAuth = <P extends object>(WrappedComponent: React.ComponentType<P>) => {
  const WithAuthComponent: React.FC<P> = (props) => {
    const router = useRouter();
    
    React.useEffect(() => {
      if (!isAuthenticated()) {
        router.push('/login');
      }
    }, [router]);
    
    return <WrappedComponent {...props} />;
  };
  
  return WithAuthComponent;
}; 