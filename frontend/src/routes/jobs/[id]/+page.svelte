<script lang="ts">
  import { onMount } from 'svelte';
  import { page } from '$app/state';
  import { goto } from '$app/navigation';
  import { PUBLIC_API_BASE_URL } from '$env/static/public';
  import { Button } from '$lib/components/ui/button';
  import { Tabs, TabsContent, TabsList, TabsTrigger } from '$lib/components/ui/tabs';
  import { Badge } from '$lib/components/ui/badge';
  import { Skeleton } from '$lib/components/ui/skeleton';
  import { ArrowLeft, CheckCircle, XCircle, Mail } from 'lucide-svelte';
  import { showToast } from '$lib/stores/polling';

  let job = $state<any>(null);
  let loading = $state(true);
  let gapResults = $state<any>(null);
  let questionResults = $state<any>(null);
  let emailResults = $state<any>(null);
  let activeTab = $state('overview');
  let selectedQuestionIndex = $state(0);
  let questionEls: HTMLDivElement[] = [];

  async function fetchJob() {
    const id = page.params.id;
    const token = localStorage.getItem('access');
    try {
      const response = await fetch(`${PUBLIC_API_BASE_URL}/api/jobs/${id}/`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        job = await response.json();
        console.log('API Response:', job);
        
        if (job.agent_results) {
          gapResults = job.agent_results['gap_analyzer']?.[0]?.result;
          questionResults = job.agent_results['question_generator']?.[0]?.result;
          emailResults = job.agent_results['message_generator']?.[0]?.result;
        }
      }
    } catch (e) {
      console.error('Failed to fetch job:', e);
    } finally {
      loading = false;
    }
  }

  $effect(() => {
    function handleKeydown(e: KeyboardEvent) {
      const target = document.activeElement as HTMLElement;
      const isInput = target.tagName === 'INPUT' || target.tagName === 'TEXTAREA';

      if (e.key === 'Escape' || e.key === '-') goto('/home');
      if (e.key === '1') activeTab = 'overview';
      if (e.key === '2') activeTab = 'questions';
      if (e.key === '3') activeTab = 'emails';
      if (e.key === '4') activeTab = 'raw';

      if (activeTab === 'questions' && !isInput) {
        if (e.key === 'j') {
          selectedQuestionIndex = Math.min((questionResults?.length ?? 1) - 1, selectedQuestionIndex + 1);
          questionEls[selectedQuestionIndex]?.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
        if (e.key === 'k') {
          selectedQuestionIndex = Math.max(0, selectedQuestionIndex - 1);
          questionEls[selectedQuestionIndex]?.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
      }
    }
    window.addEventListener('keydown', handleKeydown);
    return () => window.removeEventListener('keydown', handleKeydown);
  });

  onMount(() => {
    fetchJob();
  });
</script>

<div class="min-h-screen bg-zinc-950 p-8">
  {#if loading}
    <div class="space-y-4">
      <Skeleton class="h-8 w-1/3" />
      <Skeleton class="h-64 w-full" />
    </div>
  {:else if job}
    <header class="mb-8 flex items-center justify-between border-b border-zinc-800 pb-6">
      <div class="flex items-center gap-4">
        <Button variant="ghost" onclick={() => goto('/home')} class="text-zinc-400">
          <ArrowLeft class="w-4 h-4" />
        </Button>
        <div>
          <h1 class="text-2xl font-bold text-white">{job.company_name} - {job.role}</h1>
          <div class="flex items-center gap-2">
            <span class="text-sm text-zinc-500">Status:</span>
            <select 
              value={job.status?.toLowerCase() ?? 'in_progress'}
              onchange={async (e) => {
                const newStatus = (e.target as HTMLSelectElement).value;
                if (!newStatus) return;
                const oldStatus = job.status;
                job.status = newStatus;
                
                try {
                  const token = localStorage.getItem('access');
                  const response = await fetch(`${PUBLIC_API_BASE_URL}/api/jobs/${page.params.id}/status/`, {
                    method: 'PATCH',
                    headers: { 
                      'Authorization': `Bearer ${token}`,
                      'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ status: newStatus })
                  });
                  
                  if (!response.ok) throw new Error();
                  
                  showToast('Status updated');
                } catch (e) {
                  job.status = oldStatus;
                  showToast('Update failed');
                }
              }}
              style="background: #18181b; color: #d4d4d8; border: 1px solid #3f3f46; 
                     border-radius: 6px; padding: 2px 6px; font-size: 0.875rem; 
                     font-family: monospace; cursor: pointer; outline: none;"
            >
              <option value="in_progress">In Progress</option>
              <option value="applied">Applied</option>
              <option value="rejected">Rejected</option>
              <option value="offered">Offered</option>
            </select>
            <span class="text-sm text-zinc-500">• Added: {new Date(job.created_at).toLocaleDateString()}</span>
          </div>
        </div>
      </div>
      <Badge class="bg-zinc-800 text-zinc-100">{job.profile_score}% Match</Badge>
    </header>

    <Tabs value={activeTab} onValueChange={(v) => activeTab = v as string}>
      <TabsList class="mb-4 bg-transparent border-b border-zinc-800 rounded-none w-full justify-start gap-6 h-12">
        <TabsTrigger value="overview" class="data-[state=active]:border-b-2 data-[state=active]:border-white data-[state=active]:text-white rounded-none bg-transparent text-zinc-500 shadow-none px-0">Overview</TabsTrigger>
        <TabsTrigger value="questions" class="data-[state=active]:border-b-2 data-[state=active]:border-white data-[state=active]:text-white rounded-none bg-transparent text-zinc-500 shadow-none px-0">Questions</TabsTrigger>
        <TabsTrigger value="emails" class="data-[state=active]:border-b-2 data-[state=active]:border-white data-[state=active]:text-white rounded-none bg-transparent text-zinc-500 shadow-none px-0">Emails</TabsTrigger>
        <TabsTrigger value="raw" class="data-[state=active]:border-b-2 data-[state=active]:border-white data-[state=active]:text-white rounded-none bg-transparent text-zinc-500 shadow-none px-0">Raw</TabsTrigger>
      </TabsList>
      
      <TabsContent value="overview" class="mt-6 space-y-6 text-zinc-300">
        {#if gapResults}
          <div class="grid grid-cols-2 gap-8">
            <div>
              <h3 class="font-bold text-white mb-3">Strong Points</h3>
              <ul class="space-y-2">{#each gapResults?.strong_points ?? [] as point}<li class="flex gap-2"><CheckCircle class="text-green-500 w-4 h-4 shrink-0 mt-0.5" /> {point}</li>{/each}</ul>
            </div>
            <div>
              <h3 class="font-bold text-white mb-3">Weak Points</h3>
              <ul class="space-y-2">{#each gapResults?.weak_points ?? [] as point}<li class="flex gap-2"><XCircle class="text-red-500 w-4 h-4 shrink-0 mt-0.5" /> {point}</li>{/each}</ul>
            </div>
          </div>
          
          <div class="space-y-6 pt-6 border-t border-zinc-800">
            <div>
              <h4 class="text-sm font-semibold text-zinc-400 mb-2">Missing Skills</h4>
              <div class="flex flex-wrap gap-2">
                {#each gapResults?.missing_skills ?? [] as skill}
                  <span class="rounded-full bg-red-950 text-red-400 border border-red-800 text-xs px-2 py-1">{skill}</span>
                {/each}
              </div>
            </div>
            <div>
              <h4 class="text-sm font-semibold text-zinc-400 mb-2">Matching Skills</h4>
              <div class="flex flex-wrap gap-2">
                {#each gapResults?.matching_skills ?? [] as skill}
                  <span class="rounded-full bg-green-950 text-green-400 border border-green-800 text-xs px-2 py-1">{skill}</span>
                {/each}
              </div>
            </div>
            <div>
              <h4 class="text-sm font-semibold text-zinc-400 mb-2">Missing Keywords</h4>
              <div class="flex flex-wrap gap-2">
                {#each gapResults?.missing_keywords ?? [] as keyword}
                  <span class="rounded-full bg-yellow-950 text-yellow-400 border border-yellow-800 text-xs px-2 py-1">{keyword}</span>
                {/each}
              </div>
            </div>
            <div>
              <h4 class="text-sm font-semibold text-zinc-400 mb-2">Recommendations</h4>
              <ol class="list-decimal list-inside space-y-2 text-sm text-zinc-300">
                {#each gapResults?.recommendations ?? [] as rec}
                  <li>{rec}</li>
                {/each}
              </ol>
            </div>
          </div>
        {:else}
          <p class="text-zinc-500 italic">No overview data available</p>
        {/if}
      </TabsContent>

      <TabsContent value="questions" class="mt-6 space-y-4">
        {#if questionResults}
          {#each questionResults as q, i}
            <div 
              bind:this={questionEls[i]}
              class="border border-zinc-800 p-4 rounded bg-zinc-900/50 transition-colors {i === selectedQuestionIndex ? 'border-l-4 border-l-white' : ''}"
            >
              <div class="font-semibold">{q?.question ?? 'N/A'}</div>
              <div class="mt-2 text-sm text-zinc-400 italic">{q?.answer ?? 'No answer provided.'}</div>
              <div class="mt-2 text-xs text-zinc-500 italic">Why: {q?.why_asked ?? 'N/A'}</div>
            </div>
          {/each}
        {:else}
          <p class="text-zinc-500 italic">No questions available</p>
        {/if}
      </TabsContent>

      <TabsContent value="emails" class="mt-6 space-y-8">
        {#if emailResults}
          <div>
            <div class="flex items-center justify-between mb-2">
              <h3 class="font-bold text-white">HR Email</h3>
              <Button variant="ghost" size="sm" class="text-zinc-400 hover:text-zinc-200" asChild>
                <a href="mailto:?subject={encodeURIComponent(emailResults?.hr_email?.subject ?? '')}&body={encodeURIComponent(emailResults?.hr_email?.body ?? '')}">
                  <Mail class="w-4 h-4 mr-2" /> Compose Email
                </a>
              </Button>
            </div>
            <div class="p-4 bg-zinc-900 rounded font-mono text-sm">{emailResults?.hr_email?.body ?? 'No email body available.'}</div>
          </div>
          <div>
            <div class="flex items-center justify-between mb-2">
              <h3 class="font-bold text-white">Referral Email</h3>
              <Button variant="ghost" size="sm" class="text-zinc-400 hover:text-zinc-200" asChild>
                <a href="mailto:?subject={encodeURIComponent(emailResults?.referral_email?.subject ?? '')}&body={encodeURIComponent(emailResults?.referral_email?.body ?? '')}">
                  <Mail class="w-4 h-4 mr-2" /> Compose Email
                </a>
              </Button>
            </div>
            <div class="p-4 bg-zinc-900 rounded font-mono text-sm">{emailResults?.referral_email?.body ?? 'No email body available.'}</div>
          </div>
        {:else}
          <p class="text-zinc-500 italic">No email templates available</p>
        {/if}
      </TabsContent>

      <TabsContent value="raw" class="overflow-x-auto rounded border border-zinc-800 bg-zinc-900 p-4 font-mono text-xs text-zinc-400">
        <pre>{JSON.stringify(job, null, 2)}</pre>
      </TabsContent>
    </Tabs>
  {/if}
</div>
