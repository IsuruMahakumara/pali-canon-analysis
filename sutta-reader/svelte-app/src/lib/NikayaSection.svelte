<script>
  import { NIKAYA_NAMES, suttasByNikaya, expandedNikayas, currentSuttaId } from './stores.js';
  import { fetchSuttas } from './api.js';
  
  let { nikaya, onSelectSutta } = $props();
  
  let isExpanded = $derived($expandedNikayas[nikaya.id] || false);
  let suttas = $derived($suttasByNikaya[nikaya.id] || []);
  let name = $derived(NIKAYA_NAMES[nikaya.id] || nikaya.id.toUpperCase());
  
  async function toggle() {
    const willExpand = !$expandedNikayas[nikaya.id];
    
    expandedNikayas.update(state => ({
      ...state,
      [nikaya.id]: willExpand
    }));
    
    // Load suttas if expanding and not loaded yet
    if (willExpand && !$suttasByNikaya[nikaya.id]) {
      const loaded = await fetchSuttas(nikaya.id);
      suttasByNikaya.update(state => ({
        ...state,
        [nikaya.id]: loaded
      }));
    }
  }
</script>

<div class="nav-section">
  <div class="nav-section-header" onclick={toggle} role="button" tabindex="0" onkeydown={(e) => e.key === 'Enter' && toggle()}>
    <span class="nav-section-toggle">{isExpanded ? '▼' : '▶'}</span>
    <span class="nav-section-title">{name}</span>
    <span class="nav-section-count">{nikaya.count}</span>
  </div>
  
  {#if isExpanded}
    <div class="nav-section-items">
      {#each suttas as sutta}
        <span 
          class="nav-item" 
          class:active={sutta === $currentSuttaId}
          onclick={() => onSelectSutta(sutta)}
          role="button"
          tabindex="0"
          onkeydown={(e) => e.key === 'Enter' && onSelectSutta(sutta)}
        >
          {sutta.toUpperCase()}
        </span>
      {/each}
    </div>
  {/if}
</div>
