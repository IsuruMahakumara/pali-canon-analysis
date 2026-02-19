<script>
  import Verse from './Verse.svelte';
  import { currentSuttaId, verses, loading, showHela, displayName } from './stores.js';
  
  function toggleScript() {
    showHela.update(v => !v);
  }
</script>

<div class="reader">
  {#if !$currentSuttaId}
    <!-- Welcome screen -->
    <div class="welcome">
      <h1>Sutta Reader</h1>
      <p>Select a sutta from the collection</p>
    </div>
  {:else if $loading}
    <!-- Loading state -->
    <div class="loading">
      <span class="spinner"></span>Loading...
    </div>
  {:else}
    <!-- Sutta content -->
    <header class="sutta-header">
      <div class="sutta-header-top">
        <div>
          <div class="sutta-id">{$currentSuttaId.toUpperCase()}</div>
          <h1 class="sutta-title">{$displayName}</h1>
        </div>
        <div class="toolbar">
          <button 
            class="script-toggle" 
            class:active={$showHela}
            onclick={toggleScript}
          >
            {$showHela ? 'Latin' : 'හෙළ'}
          </button>
        </div>
      </div>
    </header>
    
    <div class="verses" class:hela-script={$showHela}>
      {#each $verses as verse (verse.index)}
        <Verse {verse} showHela={$showHela} />
      {/each}
    </div>
  {/if}
</div>
