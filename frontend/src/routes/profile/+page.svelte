<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { PUBLIC_API_BASE_URL } from '$env/static/public';
  import { Button } from '$lib/components/ui/button';
  import { Badge } from '$lib/components/ui/badge';
  import { ArrowLeft, FileText, Upload, User, LogOut, Loader2 } from 'lucide-svelte';

  let resume = $state<any>(null);
  let email = $state('');
  let loading = $state(true);
  let uploading = $state(false);
  let fileInput: HTMLInputElement;

  async function fetchProfile() {
    const token = localStorage.getItem('access');
    email = localStorage.getItem('user_email') ?? '';
    
    try {
      const response = await fetch(`${PUBLIC_API_BASE_URL}/api/resumes/me/`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) resume = await response.json();
    } catch (e) {
      console.error(e);
    } finally {
      loading = false;
    }
  }

  async function handleUpload(e: Event) {
    const file = (e.target as HTMLInputElement).files?.[0];
    if (!file) return;

    uploading = true;
    const formData = new FormData();
    formData.append('file', file);
    
    const token = localStorage.getItem('access');
    const response = await fetch(`${PUBLIC_API_BASE_URL}/api/resumes/upload/`, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${token}` },
      body: formData
    });

    if (response.ok) {
      alert('Resume updated successfully');
      fetchProfile();
    } else {
      alert('Failed to upload resume');
    }
    uploading = false;
  }

  function logout() {
    localStorage.clear();
    goto('/');
  }

  onMount(() => {
    fetchProfile();
    const handleKeydown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') goto('/home');
      if (e.key === 'u' || e.key === 'U') fileInput?.click();
    };
    window.addEventListener('keydown', handleKeydown);
    return () => window.removeEventListener('keydown', handleKeydown);
  });
</script>

<div class="min-h-screen bg-zinc-950 p-6 pt-8 text-zinc-100">
  <div class="max-w-2xl mx-auto">
    <Button variant="ghost" onclick={() => goto('/home')} class="mb-6 gap-2 text-zinc-400 hover:text-zinc-200">
      <ArrowLeft class="w-4 h-4" /> Back to Home
    </Button>

    <h1 class="text-2xl font-bold text-white mb-8">Profile</h1>

    <div class="space-y-8">
      <section>
        <h2 class="flex items-center gap-2 font-semibold text-lg mb-4 text-white">
          <FileText class="w-5 h-5 text-zinc-400" /> Resume
        </h2>
        {#if loading}
          <p class="text-zinc-500">Loading...</p>
        {:else if resume?.id}
          <div class="flex items-center justify-between bg-zinc-900 p-4 rounded-lg border border-zinc-800">
            <div>
              <p class="font-medium">{resume.original_filename}</p>
              <p class="text-xs text-zinc-500">Uploaded: {new Date(resume.uploaded_at).toLocaleDateString()}</p>
            </div>
            <Badge class="bg-green-900/50 text-green-300 border-green-800">Active</Badge>
          </div>
        {:else}
          <p class="text-zinc-500 italic mb-4">No resume uploaded.</p>
        {/if}
        <Button variant="outline" onclick={() => fileInput?.click()} disabled={uploading} class="gap-2 mt-4">
          {#if uploading} <Loader2 class="w-4 h-4 animate-spin" /> {/if}
          <Upload class="w-4 h-4" /> Upload Resume
        </Button>
        <input type="file" accept=".pdf" class="hidden" bind:this={fileInput} onchange={handleUpload} />
      </section>

      <hr class="border-zinc-800" />

      <section>
        <h2 class="flex items-center gap-2 font-semibold text-lg mb-4 text-white">
          <User class="w-5 h-5 text-zinc-400" /> Account
        </h2>
        <div class="flex items-center justify-between bg-zinc-900 p-4 rounded-lg border border-zinc-800">
          <p class="text-zinc-300 font-mono">{email}</p>
          <Button variant="destructive" size="sm" onclick={logout} class="gap-2">
            <LogOut class="w-4 h-4" /> Logout
          </Button>
        </div>
      </section>
    </div>
  </div>
</div>
