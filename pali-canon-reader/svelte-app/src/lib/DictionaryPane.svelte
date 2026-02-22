<script lang="ts">
  import { state } from './state.svelte';

  function close(): void {
    state.dictionaryEntry = null;
  }

  function renderDefs(defs: unknown): string {
    if (defs == null) return '';
    if (Array.isArray(defs)) return defs.join('\n');
    if (typeof defs === 'object' && defs !== null && 'definition' in defs) {
      const d = (defs as { definition: unknown }).definition;
      return Array.isArray(d) ? d.join('\n') : String(d);
    }
    if (typeof defs === 'object') return JSON.stringify(defs, null, 2);
    return String(defs);
  }
</script>

{#if state.dictionaryEntry}
  {@const defs = renderDefs(state.dictionaryEntry.definitions)}
  <aside class="dictionary-pane">
    <header class="pane-header">
      <h2 class="pane-title">{state.dictionaryEntry.entry}</h2>
      <button type="button" class="pane-close" onclick={close} aria-label="Close">×</button>
    </header>
    <div class="pane-content">
      {#if defs}
        <div class="definitions">{@html defs.replace(/\n/g, '<br>')}</div>
      {:else}
        <p class="muted">No definition available</p>
      {/if}
    </div>
  </aside>
{/if}

<style>
  .dictionary-pane {
    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
    width: min(420px, 90vw);
    background: var(--surface);
    border-left: 1px solid var(--border);
    display: flex;
    flex-direction: column;
    z-index: 90;
    box-shadow: -4px 0 24px rgba(0, 0, 0, 0.3);
  }

  .pane-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 1.25rem;
    border-bottom: 1px solid var(--border);
    flex-shrink: 0;
  }

  .pane-title {
    font-family: var(--font-sans);
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--accent);
    margin: 0;
  }

  .pane-close {
    background: none;
    border: none;
    color: var(--muted);
    font-size: 1.5rem;
    cursor: pointer;
    padding: 0.25rem;
    line-height: 1;
  }

  .pane-close:hover {
    color: var(--text);
  }

  .pane-content {
    flex: 1;
    overflow-y: auto;
    padding: 1.25rem;
  }

  .definitions {
    font-family: var(--font-sans);
    font-size: 0.9rem;
    line-height: 1.6;
    word-break: break-word;
    margin: 0;
    color: var(--text);
  }

  .definitions :global(b) {
    color: var(--accent);
    font-weight: 600;
  }

  .muted {
    color: var(--muted);
    font-style: italic;
    margin: 0;
  }
</style>
