<script lang="ts">
  import { state as appState, api, getUnitName } from '../store/state.svelte';
  import { formatVerses } from '../core/verseFormat';

  let blocks = $derived(formatVerses(appState.verses, appState.showHela));
  let hoveredRef = $state("");
  let headingCollapsed = $state(new Set<string>());

  let currentHeading = $derived.by(() => {
    const map = new Map<string, string>();
    let heading = '';
    for (const b of blocks) {
      if (b.type === 'h2') heading = b.ref;
      else map.set(b.ref, heading);
    }
    return map;
  });

  function toggleHeading(ref: string) {
    headingCollapsed = new Set(headingCollapsed.has(ref)
      ? [...headingCollapsed].filter(r => r !== ref)
      : [...headingCollapsed, ref]);
  }

  function onWordDblClick(word: string): void {
    api.lookupWord(word);
  }

  function onEmptyDblClick(e: MouseEvent): void {
    const el = e.target instanceof Element ? e.target : (e.target as Node).parentElement;
    if (el?.closest('.word')) return;
    appState.dictionaryEntry = null;
  }
</script>

<div class="reader">
  {#if !appState.current}
    <div class="welcome">
      <h1>Sutta Reader</h1>
      <p>Select a sutta from the collection</p>
    </div>
  {:else if appState.loading}
    <div class="loading"><span class="spinner"></span>Loading...</div>
  {:else}
    <header class="reader-header">
      <div class="reader-header-top">
        <div>
          <div class="reader-id">{appState.current.toUpperCase()}</div>
          <h1 class="reader-title">{getUnitName(appState.showHela)}</h1>
        </div>
      </div>
    </header>
    
    <!-- svelte-ignore a11y_no_static_element_interactions -->
    <div class="verses" class:hela-script={appState.showHela} ondblclick={onEmptyDblClick}>
      {#each blocks as block (block.ref)}
        {#if block.type === 'h1'}
          <h1 class="verse-heading">{block.text}</h1>
        {:else if block.type === 'h2'}
          <h2 class="verse-heading collapsible" class:collapsed={headingCollapsed.has(block.ref)}>
            <button type="button" class="collapse-toggle" onclick={() => toggleHeading(block.ref)}>
              <span class="collapse-indicator">{headingCollapsed.has(block.ref) ? '▶' : '▼'}</span>
              {block.text}
            </button>
          </h2>
        {:else if block.type === 'h3'}
          <h3 class="verse-heading">{block.text}</h3>
        {:else if block.type === 'list-item'}
          <li class="verse-list-item">{block.text}</li>
        {:else if !headingCollapsed.has(currentHeading.get(block.ref) ?? '')}
          <!-- svelte-ignore a11y_no_static_element_interactions -->
          <span class="verse"
            onmouseover={() => hoveredRef = block.ref}
            onmouseout={() => hoveredRef = ''}
            onfocus={() => hoveredRef = block.ref}
            onblur={() => hoveredRef = ''}
          >
            {@html block.prependTag ?? ''}
            {#each block.text.split(/(\s+)/) as part}
              {#if /^\s+$/.test(part)}
                {part}
              {:else}
                <span class="word" ondblclick={() => onWordDblClick(part)} role="button" tabindex="-1">{part}</span>
              {/if}
            {/each}
          </span>
        {/if}
      {/each}
    </div>
  {/if}

  {#if hoveredRef}
    <div class="status-bar">{hoveredRef}</div>
  {/if}
</div>



<style>

.verses {
  line-height: 2.2;
  font-size: 1.4rem;
}

.verses.hela-script {
  font-family: var(--font-hela);
  font-size: 1.3rem;
  line-height: 2.4;
}

.verse {
  margin-bottom: 0.2rem;
  padding: 0.3rem 0;
  border-radius: 4px;
  transition: background 0.15s;
}

.verse:hover {
  background: rgba(254, 227, 227, 0.15);
}

.word {
  cursor: pointer;
  border-radius: 2px;
  padding: 0 0.05em;
}

/* .word:hover {
  text-decoration: underline;
} */

.collapse-toggle {
  all: unset;
  cursor: pointer;
  user-select: none;
  font: inherit;
  color: inherit;
  width: 100%;
  display: inline;
}

.collapse-indicator {
  font-size: 0.6em;
  margin-right: 0.4em;
  vertical-align: middle;
}

.status-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  padding: 0.25rem 0.75rem;
  font-size: 0.75rem;
  color: #a0aec0;
  background: #1a202c;
  border-top: 1px solid #2d3748;
  z-index: 50;
}

</style>