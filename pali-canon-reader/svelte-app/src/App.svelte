<script lang="ts">
  import { onMount } from 'svelte';
  import Nav from './components/Nav.svelte';
  import Reader from './components/Reader.svelte';
  import GraphViewer from './components/GraphViewer.svelte';
  //import GraphViewer from './lib/G6GraphViewer.svelte';
  import { state as appState, api } from './store/state.svelte';

  let currentPage = $state<'reader' | 'graph'>('reader');
  let innerWidth = $state(window.innerWidth);
  let dictQuery = $state('');

  function onDictSearch() {
    const q = dictQuery.trim().toLowerCase();
    if (q) api.lookupWord(q);
  }

  function updateRoute(): void {
    const hash = location.hash;
    if (hash === '#graph') {
      currentPage = 'graph';
    } else {
      currentPage = 'reader';
      const readingUnitId = hash.replace('#reader', '').replace('#', '');
      if (readingUnitId) api.loadReadingUnit(readingUnitId);
    }
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
  
  onMount(() => {
    api.init('/Canon.graphml');
    updateRoute();
    window.addEventListener('hashchange', updateRoute);
  });
</script>

<svelte:window bind:innerWidth />

{#if currentPage === 'graph'}
  <GraphViewer />
{:else}
  <button class="hamburger" onclick={() => appState.navOpen = !appState.navOpen}>
    {appState.navOpen ? '✕' : '☰'}
  </button>

  {#if appState.current}
    <button
      class="script-toggle"
      class:active={appState.showHela}
      onclick={() => appState.showHela = !appState.showHela}
    >{appState.showHela ? 'Latin' : 'හෙළ'}</button>
  {/if}

  <a href="#graph" class="graph-link" title="Graph Explorer">⬡</a>

  <nav class:collapsed={!appState.navOpen}>
    <div class="nav-tabs">
      <button class:active={appState.navMode === 'index'} onclick={() => appState.navMode = 'index'}>Index</button>
      <button class:active={appState.navMode === 'dictionary'} onclick={() => appState.navMode = 'dictionary'}>Dictionary</button>
    </div>

    {#if appState.navMode === 'index'}
      <div class="nav-panel">
        <Nav node={appState.navTree} />
      </div>
    {:else}
      <form class="dict-search" onsubmit={e => { e.preventDefault(); onDictSearch(); }}>
        <input type="text" bind:value={dictQuery} placeholder={appState.dictionaryEntry?.entry ?? 'Search Pāli '} />
      </form>
      <div class="nav-panel dictionary-panel">
        {#if appState.dictionaryEntry}
          {@const defs = renderDefs(appState.dictionaryEntry.definitions)}
          <h2 class="dict-title">{appState.dictionaryEntry.entry}</h2>
          {#if defs}
            <div class="dict-definitions">{@html defs.replace(/\n/g, '<br>')}</div>
          {:else}
            <p class="dict-muted">No definition available</p>
          {/if}
        {:else}
          <p class="dict-muted">Double-click a word to look it up</p>
        {/if}
      </div>
    {/if}
  </nav>

  <main class:expanded={!appState.navOpen} class:dimmed={innerWidth < 800 && appState.navOpen}>
    <Reader />
  </main>
{/if}

<style>
  .script-toggle {
    position: fixed;
    top: 0.5rem;
    right: 3.5rem;
    z-index: 100;
    height: 2.5rem;
    padding: 0 0.75rem;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #2d3748;
    border: 1px solid #4a5568;
    border-radius: 6px;
    color: #e2e8f0;
    font-size: 0.85rem;
    cursor: pointer;
  }

  .script-toggle:hover {
    background: #4a5568;
  }

  .script-toggle.active {
    background: #4a5568;
    color: #63b3ed;
  }

  .graph-link {
    position: fixed;
    top: 0.5rem;
    right: 0.5rem;
    z-index: 100;
    width: 2.5rem;
    height: 2.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #2d3748;
    border: 1px solid #4a5568;
    border-radius: 6px;
    color: #63b3ed;
    font-size: 1.25rem;
    text-decoration: none;
  }
  
  .graph-link:hover {
    background: #4a5568;
    color: #90cdf4;
  }

  .nav-tabs {
    display: flex;
    gap: 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1rem;
    flex-shrink: 0;
  }

  .nav-tabs button {
    flex: 1;
    padding: 0.6rem 0;
    background: none;
    border: none;
    border-bottom: 2px solid transparent;
    color: var(--muted);
    font-family: var(--font-sans);
    font-size: 0.8rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    cursor: pointer;
    transition: color 0.15s, border-color 0.15s;
  }

  .nav-tabs button:hover {
    color: var(--text);
  }

  .nav-tabs button.active {
    color: var(--accent);
    border-bottom-color: var(--accent);
  }

  .nav-panel {
    flex: 1;
    overflow-y: auto;
    min-height: 0;
  }

  .dict-search {
    flex-shrink: 0;
    padding: 0 0.25rem 0.75rem;
  }

  .dict-search input {
    width: 100%;
    padding: 0.45rem 0.6rem;
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 6px;
    color: var(--text);
    font-family: var(--font-sans);
    font-size: 0.85rem;
    outline: none;
    transition: border-color 0.15s;
  }

  .dict-search input::placeholder {
    color: var(--muted);
  }

  .dict-search input:focus {
    border-color: var(--accent);
  }

  .dictionary-panel {
    padding: 0 0.5rem;
  }

  .dict-title {
    font-family: var(--font-sans);
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--accent);
    margin: 0 0 1rem;
  }

  .dict-definitions {
    font-family: var(--font-sans);
    font-size: 0.85rem;
    line-height: 1.6;
    word-break: break-word;
    color: var(--text);
  }

  .dict-definitions :global(b) {
    color: var(--accent);
    font-weight: 600;
  }

  .dict-muted {
    color: var(--muted);
    font-style: italic;
    font-family: var(--font-sans);
    font-size: 0.85rem;
    margin: 0;
  }
</style>
