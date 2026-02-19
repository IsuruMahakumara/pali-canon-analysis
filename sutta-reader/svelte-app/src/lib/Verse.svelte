<script>
  let { verse, showHela = false } = $props();
  
  let verseNum = $derived(verse.index.split(':')[1]);
  let isMetaVerse = $derived(verseNum.startsWith('0.'));
  let text = $derived(showHela ? (verse.hela_text || verse.text) : verse.text);
</script>

{#if !isMetaVerse}
  <p class="verse">
    <span class="verse-ref">{verseNum}</span>{text || ''}
  </p>
{/if}
