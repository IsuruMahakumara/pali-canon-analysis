<script>
  import { state, getSuttaName } from './state.svelte.js';
</script>

<div class="reader">
  {#if !state.current}
    <div class="welcome">
      <h1>Sutta Reader</h1>
      <p>Select a sutta from the collection</p>
    </div>
  {:else if state.loading}
    <div class="loading"><span class="spinner"></span>Loading...</div>
  {:else}
    <header class="sutta-header">
      <div class="sutta-header-top">
        <div>
          <div class="sutta-id">{state.current.toUpperCase()}</div>
          <h1 class="sutta-title">{getSuttaName(state.showHela)}</h1>
        </div>
        <button 
          class="script-toggle" 
          class:active={state.showHela}
          onclick={() => state.showHela = !state.showHela}
        >{state.showHela ? 'Latin' : 'හෙළ'}</button>
      </div>
    </header>
    
    <div class="verses" class:hela-script={state.showHela}>
      {#each state.verses as v (v.index)}
        {@const num = v.index.split(':')[1]}
        {#if !num.startsWith('0.')}
          <p class="verse">
            <span class="verse-ref">{num}</span>{state.showHela ? (v.hela_text || v.text) : v.text}
          </p>
        {/if}
      {/each}
    </div>
  {/if}
</div>
