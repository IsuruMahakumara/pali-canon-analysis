<script lang="ts">
  import { state, api, NIKAYA_NAMES } from './state.svelte';
</script>

<nav class:collapsed={!state.navOpen}>
  <div class="nav-header">Pāli Canon</div>
  
  {#each state.nikayas as n (n.id)}
    <div class="nav-section">
      <button type="button" class="nav-section-header" onclick={() => api.toggleNikaya(n.id)}>
        <span class="nav-section-toggle">{state.expanded[n.id] ? '▼' : '▶'}</span>
        <span class="nav-section-title">{NIKAYA_NAMES[n.id] || n.id}</span>
        <span class="nav-section-count">{n.count}</span>
      </button>
      
      {#if state.expanded[n.id]}
        <div class="nav-section-items">
          {#each state.suttasByNikaya[n.id] || [] as s}
            <button 
              type="button"
              class="nav-item" 
              class:active={s === state.current}
              onclick={() => api.selectSutta(s)}
            >{s.toUpperCase()}</button>
          {/each}
        </div>
      {/if}
    </div>
  {/each}
</nav>
