<script lang="ts">
  import { onMount } from 'svelte';
  import Nav from './lib/Nav.svelte';
  import Reader from './lib/Reader.svelte';
  import GraphViewer from './lib/GraphViewer.svelte';
  import { state as appState, api } from './lib/state.svelte';

  let currentPage = $state<'reader' | 'graph'>('reader');
  let innerWidth = $state(window.innerWidth);

  function updateRoute(): void {
    const hash = location.hash;
    if (hash === '#graph') {
      currentPage = 'graph';
    } else {
      currentPage = 'reader';
      const suttaId = hash.replace('#reader', '').replace('#', '');
      if (suttaId) api.loadSutta(suttaId);
    }
  }
  
  onMount(() => {
    api.loadNikayas();
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

  <a href="#graph" class="graph-link" title="Graph Explorer">⬡</a>

  <Nav />

  <main class:expanded={!appState.navOpen} class:dimmed={innerWidth < 800 && appState.navOpen}>
    <Reader />
  </main>
{/if}

<style>
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
</style>
