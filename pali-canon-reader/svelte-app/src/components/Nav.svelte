<script lang="ts">
  import { state as appState, api } from '../store/state.svelte';
  import type { TreeNode } from '../core/parseGraphML';
  import Nav from './Nav.svelte';

  let { node, depth = 0 }: { node?: TreeNode | null; depth?: number } = $props();
  let open = $state(false);

  $effect(() => { open = depth < 1; });
</script>

{#if node}
  {#if node.children.length}
    <button class="branch" style:padding-left="{depth * 0.75 + 0.5}rem" onclick={() => open = !open}>
      <span class="arrow">{open ? '▾' : '▸'}</span> {node.label}
    </button>
    {#if open}
      {#each node.children as child (child.id)}
        <Nav node={child} depth={depth + 1} />
      {/each}
    {/if}
  {:else}
    <button
      class="leaf"
      class:active={node.id === appState.current}
      style:padding-left="{depth * 0.75 + 0.5}rem"
      onclick={() => api.selectSutta(node!.id)}
    >{node.label}</button>
  {/if}
{/if}

<style>
  button { display: block; width: 100%; text-align: left; background: none; border: none; color: #cbd5e0; cursor: pointer; padding: 0.3rem 0.5rem; font-size: 0.85rem; }
  .branch { font-weight: 600; color: #e2e8f0; }
  .branch:hover { background: #2d3748; }
  .leaf:hover { background: #2d3748; }
  .leaf.active { background: #2b6cb0; color: #fff; }
  .arrow { display: inline-block; width: 1em; text-align: center; }
</style>
