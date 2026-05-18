import { redirect } from '@sveltejs/kit';
import type { HandleClient } from '@sveltejs/kit';

export const handleClient: HandleClient = async ({ event, resolve }) => {
	const path = event.url.pathname;
	
	if (path !== '/' && !localStorage.getItem('access')) {
		throw redirect(302, '/');
	}

	return resolve(event);
};
