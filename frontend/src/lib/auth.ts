import { goto } from '$app/navigation';
import { browser } from '$app/environment';

export function requireAuth() {
  if (browser) {
    const token = localStorage.getItem('access');
    if (!token) {
      goto('/');
      return null;
    }
    return token;
  }
  return null;
}
