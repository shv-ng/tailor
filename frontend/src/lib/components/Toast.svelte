<script lang="ts">
    import { toast } from '$lib/stores/polling';

    function close() {
        toast.set(null);
    }

    function handleClick() {
        if ($toast?.link) {
            window.location.href = $toast.link;
            close();
        }
    }

    function handleKeydown(e: KeyboardEvent) {
        if (e.key === 'Enter' || e.key === ' ') {
            handleClick();
        }
    }
</script>

{#if $toast}
    <div 
        class="fixed bottom-4 right-4 bg-zinc-800 text-white p-4 rounded shadow-lg cursor-pointer flex items-center gap-4 z-50"
        onclick={handleClick}
        onkeydown={handleKeydown}
        role="button"
        tabindex="0"
    >
        <span>{$toast.message}</span>
        <button 
            type="button"
            onclick={(e) => { e.stopPropagation(); close(); }} 
            class="text-zinc-400 hover:text-white"
        >
            ✕
        </button>
    </div>
{/if}
