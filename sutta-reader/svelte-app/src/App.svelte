<script>
  import { onMount } from 'svelte';
  import Nav from './lib/Nav.svelte';
  import Reader from './lib/Reader.svelte';
  import { state, api } from './lib/state.svelte.js';
  
  onMount(() => {
    api.loadNikayas();
    api.loadSutta(location.hash.slice(1));
    window.addEventListener('hashchange', () => api.loadSutta(location.hash.slice(1)));
  });
</script>

<button class="hamburger" onclick={() => state.navOpen = !state.navOpen}>
  {state.navOpen ? '✕' : '☰'}
</button>

<Nav />

<main class:expanded={!state.navOpen} class:dimmed={innerWidth < 800 && state.navOpen}>
  <Reader />
</main>
