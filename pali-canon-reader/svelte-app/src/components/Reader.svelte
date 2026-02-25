<script lang="ts">
  import { state, api, getUnitName } from '../store/state.svelte';

  function onWordDblClick(word: string): void {
    api.lookupWord(word);
  }

  function onEmptyDblClick(e: MouseEvent): void {
    const el = e.target instanceof Element ? e.target : (e.target as Node).parentElement;
    if (el?.closest('.word')) return;
    state.dictionaryEntry = null;
  }
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
    <header class="reader-header">
      <div class="reader-header-top">
        <div>
          <div class="reader-id">{state.current.toUpperCase()}</div>
          <h1 class="reader-title">{getUnitName(state.showHela)}</h1>
        </div>
        <button 
          class="script-toggle" 
          class:active={state.showHela}
          onclick={() => state.showHela = !state.showHela}
        >{state.showHela ? 'Latin' : 'හෙළ'}</button>
      </div>
    </header>
    
    <!-- svelte-ignore a11y_no_static_element_interactions -->
    <div class="verses" class:hela-script={state.showHela} ondblclick={onEmptyDblClick}>
      {#each state.verses as v (v.index)}
        {@const num = v.index.split(':')[1]}
        {#if !num.startsWith('0.')}
          {@const raw = state.showHela ? (v.hela_text || v.text || '') : (v.text || '')}
          <p class="verse">
            <span class="verse-ref">{num}</span>
            {#each raw.split(/(\s+)/) as part}
              {#if /^\s+$/.test(part)}
                {part}
              {:else}
                <span class="word" ondblclick={() => onWordDblClick(part)} role="button" tabindex="-1">{part}</span>
              {/if}
            {/each}
          </p>
        {/if}
      {/each}
    </div>
  {/if}
</div>
