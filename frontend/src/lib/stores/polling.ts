import { writable } from 'svelte/store';
import { PUBLIC_API_BASE_URL } from '$env/static/public';

export const toast = writable<{ message: string; link?: string } | null>(null);

export function showToast(message: string, link?: string) {
    toast.set({ message, link });
    setTimeout(() => toast.set(null), 6000);
}

export function startPolling(jobId: number) {
    const startTime = Date.now();
    const interval = setInterval(async () => {
        if (Date.now() - startTime > 180000) { // 3 minutes
            clearInterval(interval);
            showToast("Analysis timed out. Please try again later.");
            return;
        }

        try {
            const token = localStorage.getItem('access');
            const response = await fetch(`${PUBLIC_API_BASE_URL}/api/jobs/${jobId}/`, {
                headers: { 
                    'Authorization': `Bearer ${token}`
                }
            });
            const data = await response.json();

            if (data.agent_results) {
                clearInterval(interval);
                showToast(`Analysis complete for ${data.company} - ${data.role}! Click to view.`, `/jobs/${jobId}`);
            }
        } catch (e) {
            console.error("Polling error", e);
        }
    }, 4000);
}
