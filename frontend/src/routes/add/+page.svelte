<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { PUBLIC_API_BASE_URL } from '$env/static/public';
  import { Button } from '$lib/components/ui/button';
  import { Input } from '$lib/components/ui/input';
  import { Label } from '$lib/components/ui/label';
  import { Textarea } from '$lib/components/ui/textarea';
  import { ArrowLeft, Loader2 } from 'lucide-svelte';
  import { startPolling } from '$lib/stores/polling';
  import { showToast } from '$lib/stores/polling';

  let jdUrl = $state('');
  let jdText = $state('');
  let isLoading = $state(false);
  let error = $state('');
  let queueMessage = $state('');

  onMount(() => {
    const handleKeydown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') goto('/home');
      if (e.ctrlKey && e.key === 'Enter') analyzeJob();
    };

    window.addEventListener('keydown', handleKeydown);
    return () => window.removeEventListener('keydown', handleKeydown);
  });

  async function analyzeJob() {
    if (!jdText) {
      error = 'Job description is required';
      return;
    }

    error = '';
    isLoading = true;
    queueMessage = '';

    try {
      const token = localStorage.getItem('access');
      const response = await fetch(`${PUBLIC_API_BASE_URL}/api/jobs/analyze/`, {
        method: 'POST',
        headers: { 
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ jd_url: jdUrl, jd_text: jdText })
      });

      if (!response.ok) throw new Error('Failed to analyze job');
      const data = await response.json();
      
      startPolling(data.job_application_id);
      queueMessage = "Analysis queued! You'll be notified when results are ready.";
      
      jdUrl = '';
      jdText = '';
    } catch (e: any) {
      error = e.message;
    } finally {
      isLoading = false;
    }
  }
</script>

<div class="min-h-screen bg-zinc-950 p-6 pt-8">
  <div class="max-w-2xl mx-auto">
    <Button variant="ghost" onclick={() => goto('/home')} class="mb-6 gap-2 text-zinc-400 hover:text-zinc-200">
      <ArrowLeft class="w-4 h-4" /> Back to Home
    </Button>

    <h1 class="text-2xl font-bold text-white mb-6">New Application</h1>

    {#if queueMessage}
      <div class="bg-blue-900/20 border border-blue-800 text-blue-200 px-4 py-4 rounded-md mb-6">
        {queueMessage}
      </div>
    {/if}

    <form onsubmit={(e) => { e.preventDefault(); analyzeJob(); }} class="flex flex-col gap-6">
      <div class="space-y-2">
        <Label for="url" class="text-zinc-400 text-sm">Job URL <span class="text-zinc-600">(optional)</span></Label>
        <Input id="url" bind:value={jdUrl} placeholder="https://linkedin.com/jobs/..." class="bg-zinc-900 border-zinc-700 focus-visible:ring-zinc-500" />
      </div>

      <div class="space-y-2">
        <Label for="jd" class="text-zinc-400 text-sm">Job Description</Label>
        <Textarea 
            id="jd" 
            bind:value={jdText} 
            placeholder="Paste the full JD here..." 
            class="h-64 overflow-y-auto resize-none bg-zinc-900 border-zinc-700 focus-visible:ring-zinc-500 font-mono" 
        />
      </div>

      {#if error}
        <p class="text-sm text-red-400">{error}</p>
      {/if}

      <div class="mt-4 flex flex-col gap-2">
        <Button type="submit" class="w-full bg-white text-black font-bold hover:bg-zinc-200" disabled={isLoading}>
          {#if isLoading}
            <Loader2 class="w-4 h-4 mr-2 animate-spin" /> Analyzing...
          {:else}
            Analyze
          {/if}
        </Button>
        <p class="text-xs text-zinc-500 text-center">Analysis takes 15-30 seconds</p>
      </div>
    </form>
  </div>
</div>
