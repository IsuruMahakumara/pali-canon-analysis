<script>
  import { onMount } from 'svelte';
  import { get } from 'svelte/store';
  import Nav from './lib/Nav.svelte';
  import Reader from './lib/Reader.svelte';
  import { 
    nikayas, 
    expandedNikayas, 
    suttasByNikaya,
    currentSuttaId, 
    verses, 
    loading, 
    navOpen 
  } from './lib/stores.js';
  import { fetchNikayas, fetchSuttas, fetchSutta } from './lib/api.js';
  
  let isMobile = $state(false);
  
  onMount(async () => {
    isMobile = window.innerWidth < 800;
    
    // Load nikayas
    const loadedNikayas = await fetchNikayas();
    nikayas.set(loadedNikayas);
    
    // Expand first nikaya by default
    if (loadedNikayas.length > 0) {
      const firstId = loadedNikayas[0].id;
      expandedNikayas.update(s => ({ ...s, [firstId]: true }));
      
      const suttas = await fetchSuttas(firstId);
      suttasByNikaya.update(s => ({ ...s, [firstId]: suttas }));
    }
    
    // Handle initial hash
    handleHash();
    
    // Listen for hash changes
    window.addEventListener('hashchange', handleHash);
    window.addEventListener('resize', () => {
      isMobile = window.innerWidth < 800;
    });
    
    return () => {
      window.removeEventListener('hashchange', handleHash);
    };
  });
  
  function handleHash() {
    const id = location.hash.slice(1);
    if (id && id !== get(currentSuttaId)) {
      loadSutta(id);
    }
  }
  
  async function loadSutta(id) {
    currentSuttaId.set(id);
    loading.set(true);
    
    const loadedVerses = await fetchSutta(id);
    verses.set(loadedVerses);
    loading.set(false);
    
    // Close nav on mobile after selection
    if (isMobile) {
      navOpen.set(false);
    }
  }
  
  function selectSutta(id) {
    history.pushState(null, '', `#${id}`);
    loadSutta(id);
  }
  
  function toggleNav() {
    navOpen.update(v => !v);
  }
</script>

<button class="hamburger" onclick={toggleNav}>
  {$navOpen ? '✕' : '☰'}
</button>

<Nav onSelectSutta={selectSutta} />

<main class:expanded={!$navOpen} class:dimmed={isMobile && $navOpen}>
  <Reader />
</main>
