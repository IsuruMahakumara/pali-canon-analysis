<script>
  import NikayaSection from './NikayaSection.svelte';
  import { nikayas, navOpen } from './stores.js';
  
  let { onSelectSutta } = $props();
</script>

<nav class:collapsed={!$navOpen}>
  <div class="nav-header">Pāli Canon</div>
  {#each $nikayas as nikaya (nikaya.id)}
    <NikayaSection {nikaya} {onSelectSutta} />
  {/each}
</nav>
