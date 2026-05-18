import { requireAuth } from '$lib/auth';

export function load() {
  requireAuth();
}
