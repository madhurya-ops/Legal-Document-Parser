import { useEffect } from 'react';
import { useAuth0 } from '@auth0/auth0-react';

export default function AuthCallback() {
  const { handleRedirectCallback, isLoading, error } = useAuth0();

  useEffect(() => {
    handleRedirectCallback();
  }, [handleRedirectCallback]);

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error.message}</div>;
  }

  return null; // Redirect will happen automatically
}

