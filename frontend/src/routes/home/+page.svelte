<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { PUBLIC_API_BASE_URL } from '$env/static/public';
  import { Button } from '$lib/components/ui/button';
  import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '$lib/components/ui/table';
  import { Badge } from '$lib/components/ui/badge';
  import { Inbox, Plus } from '@lucide/svelte';

  let jobs = $state([]);
  let searchQuery = $state('');
  let searchInput: HTMLInputElement;
  let selectedIndex = $state(0);

  const filteredJobs = $derived(jobs.filter(job => 
    job.company_name.toLowerCase().includes(searchQuery.toLowerCase()) || 
    job.role.toLowerCase().includes(searchQuery.toLowerCase())
  ));

  $effect(() => {
    const savedIndex = sessionStorage.getItem('home_selected_index');
    if (savedIndex) selectedIndex = parseInt(savedIndex);

    const savedSearch = sessionStorage.getItem('home_search');
    if (savedSearch) searchQuery = savedSearch;
  });

  $effect(() => {
    sessionStorage.setItem('home_search', searchQuery);
  });

  function selectJob(index: number, id: string) {
    selectedIndex = index;
    sessionStorage.setItem('home_selected_index', index.toString());
    goto(`/jobs/${id}`);
  }

  async function fetchJobs() {
    console.log('fetchJobs called');
    const token = localStorage.getItem('access');
    console.log('Token from localStorage:', token);
    const response = await fetch(`${PUBLIC_API_BASE_URL}/api/jobs/`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    if (response.ok) {
      jobs = await response.json();
      console.log('Jobs fetched:', jobs);
    } else {
      console.error('Failed to fetch jobs, status:', response.status);
    }
  }

  onMount(() => {
    console.log('Home page mounted, calling fetchJobs');
    fetchJobs();

    const handleKeydown = (e: KeyboardEvent) => {
      const target = document.activeElement as HTMLElement;
      const isInput = target.tagName === 'INPUT' || target.tagName === 'TEXTAREA';

      if (e.key === '/') {
        if (!isInput) {
          e.preventDefault();
          searchInput.focus();
        }
      }
      if ((e.key === 'Escape' || e.key==='Enter') && isInput && target === searchInput) {
        searchInput.blur();
      }

      if (isInput) return;

      if (e.key === 'a' || e.key === 'A') goto('/add');
      if (e.key === 'j') {
        selectedIndex = Math.min(filteredJobs.length - 1, selectedIndex + 1);
        sessionStorage.setItem('home_selected_index', selectedIndex.toString());
      }
      if (e.key === 'k') {
        selectedIndex = Math.max(0, selectedIndex - 1);
        sessionStorage.setItem('home_selected_index', selectedIndex.toString());
      }
      if (e.key === 'Enter' && filteredJobs[selectedIndex]) selectJob(selectedIndex, filteredJobs[selectedIndex].id);
    };

    window.addEventListener('keydown', handleKeydown);
    return () => window.removeEventListener('keydown', handleKeydown);
  });

  function getBadgeColor(score: number | null) {
    if (score === null) return 'bg-zinc-700';
    if (score < 40) return 'bg-red-900/50 text-red-200 border-red-800';
    if (score < 70) return 'bg-yellow-900/50 text-yellow-200 border-yellow-800';
    return 'bg-green-900/50 text-green-200 border-green-800';
  }
</script>

<div class="min-h-screen bg-zinc-950 text-zinc-100 flex flex-col">
  <header class="border-b border-zinc-800 px-8 py-4 flex items-center justify-between">
    <h1 class="text-xl font-bold tracking-tight">Tailor</h1>
    <input 
      bind:this={searchInput}
      bind:value={searchQuery}
      placeholder="Search jobs..."
      class="bg-zinc-900 border border-zinc-700 rounded-md px-3 py-1 text-sm text-zinc-200 w-48 focus:outline-none focus:border-zinc-500"
    />
    <div class="flex gap-2">
      <Button variant="outline" size="sm" onclick={() => goto('/add')} class="gap-2">
        <Plus class="w-4 h-4" /> Add Job
      </Button>
      <Button variant="outline" size="sm" onclick={() => goto('/profile')}>Profile</Button>
    </div>
  </header>

  <main class="flex-1 p-8">
    {#if jobs.length === 0}
      <div class="flex flex-col items-center justify-center h-[60vh] gap-4 text-zinc-400">
        <Inbox class="w-12 h-12 stroke-1" />
        <p class="text-lg">No applications yet. Press 'A' to add one.</p>
      </div>
    {:else if filteredJobs.length === 0}
      <div class="flex flex-col items-center justify-center h-[60vh] gap-4 text-zinc-400">
        <p class="text-lg">No matches found.</p>
      </div>
    {:else}
      <div class="rounded-md border border-zinc-800">
        <Table>
          <TableHeader>
            <TableRow class="hover:bg-transparent border-zinc-800">
              <TableHead class="text-zinc-400">Company</TableHead>
              <TableHead class="text-zinc-400">Role</TableHead>
              <TableHead class="text-zinc-400">Score</TableHead>
              <TableHead class="text-zinc-400">Status</TableHead>
              <TableHead class="text-zinc-400">Added</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {#each filteredJobs as job, i}
              <TableRow 
              class="cursor-pointer border-zinc-800 transition-colors {i === selectedIndex ? 'bg-zinc-700/30 border-l-2 border-l-white' : 'hover:bg-zinc-800/50'}"
              onclick={() => selectJob(i, job.id)}
              >                <TableCell class="font-medium">{job.company_name}</TableCell>
                <TableCell>{job.role}</TableCell>
                <TableCell>
                  <Badge variant="outline" class="font-mono {getBadgeColor(job.profile_score)} rounded-full px-2 py-0.5 text-[10px]">
                    {job.profile_score ?? '-'}
                  </Badge>
                </TableCell>
                <TableCell>
                  {job.status.charAt(0).toUpperCase() + job.status.slice(1).toLowerCase()}
                </TableCell>
                <TableCell class="text-zinc-500">{new Date(job.created_at).toLocaleString(undefined, {
                  month: 'numeric',
                  day: 'numeric',
                  year: 'numeric',
                  hour: 'numeric',
                  minute: 'numeric',
                  hour12: true
                })}</TableCell>
              </TableRow>
            {/each}
          </TableBody>
        </Table>
      </div>
    {/if}
  </main>
</div>
