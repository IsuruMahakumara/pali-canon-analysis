<script lang="ts">
  import { onMount } from 'svelte';
  import { Graph, treeToGraphData } from '@antv/g6';
  import { indexGraphStore } from './indexGraphStore';

  let container = $state<HTMLDivElement>();
  let graph: Graph | null = null;

  // function toG6Data(nodes: any[], edges: any[]) {
  //   return {
  //     nodes: nodes.map((n) => ({
  //       id: n.data.id as string,
  //       data: { label: n.data.label, attrs: n.data.attrs },
  //     })),
  //     edges: edges.map((e) => ({
  //       id: e.data.id as string,
  //       source: e.data.source as string,
  //       target: e.data.target as string,
  //     })),
  //   };
  // }

  function collapseByDepth(node: any, depth: number = 0, maxDepth: number = 2) {
  const isCollapsed = depth >= maxDepth;
  
  return {
    ...node,
    // G6 v5 looks here to decide if a node starts collapsed
    style: {
      ...node.style,
      collapsed: isCollapsed
    },
    // Continue through children
    children: node.children?.map((child: any) => 
      collapseByDepth(child, depth + 1, maxDepth)
    ) || []
  };
}

  onMount(() => {
    if (!container) return;

    graph = new Graph({
      container,
      autoFit: 'view',
      node: {
        style: {
          labelText: (d: any) => d.data?.label ?? d.id,
          labelFill: '#e2e8f0',
          labelFontSize: 10,
          fill: '#4a5568',
          stroke: '#718096',
          lineWidth: 1,
        },
        state: {
          selected: { fill: '#ed8936', stroke: '#dd6b20' },
        },
      },
      edge: {
        style: {
          stroke: '#718096',
          lineWidth: 1.5,
          endArrow: true,
          endArrowFill: '#718096',
        },
      },
      layout: {
        type: 'compact-box',
        direction: 'LR',
        getWidth: () => 80,
        getHeight: () => 30,
        getVGap: () => 20,
        getHGap: () => 30,
      },
      behaviors: [
        'drag-canvas',
        'zoom-canvas',
        { type: 'collapse-expand', trigger: 'click' },
      ],
      plugins: [
        {
          type: 'tooltip',
          key: 'tooltip',
          getContent: (_: any, items: any[]) => {
            const item = items[0];
            if (!item) return '';
            const attrs = item.data?.attrs;
            if (!attrs) return `<b>${item.id}</b>`;
            const rows = Object.entries(attrs as Record<string, string>)
              .map(([k, v]) => `<span style="color:#63b3ed">${k}:</span> ${v}`)
              .join('<br>');
            return `<div style="font-size:12px;color:#e2e8f0">${rows}</div>`;
          },
          style: {
            '.tooltip': {
              background: '#2d3748',
              border: '1px solid #4a5568',
              'border-radius': '4px',
              padding: '6px 10px',
              'box-shadow': '0 2px 8px rgba(0,0,0,0.3)',
            },
          },
        },
        {
          type: 'contextmenu',
          key: 'contextmenu',
          getItems: (_: any, items: any[]) => {
            const item = items[0];
            if (!item) return [];
            return [{ name: 'Copy name', value: item.data?.label ?? item.id }];
          },
          onClick: (value: string) => {
            navigator.clipboard.writeText(value);
          },
        },
      ],
      background: '#1a202c',
    });

    const unsub = indexGraphStore.subscribe((s) => {
      if (!graph || !s.navTree || s.nodes.length === 0) return;
      const data = treeToGraphData(s.navTree);


      const collapsedData = collapseByDepth(data, 0, 2);
      graph.setData(collapsedData);
      graph.render();
    });

    indexGraphStore.load('/Canon.graphml');

    return () => {
      unsub();
      graph?.destroy();
      graph = null;
    };
  });
</script>

<div class="graph-page">
  <header class="graph-header">
    <a href="#reader" class="back-link">← Reader</a>
    <h1>Pali Canon Index</h1>
  </header>

  <div class="graph-toolbar">
    <button onclick={() => indexGraphStore.load('/Canon.graphml')} disabled={$indexGraphStore.loading}>
      {$indexGraphStore.loading ? 'Loading...' : 'Reload'}
    </button>
  </div>

  {#if $indexGraphStore.error}
    <div class="error">{$indexGraphStore.error}</div>
  {/if}

  <div class="graph-container" bind:this={container}></div>
</div>

<style>
  .graph-page {
    display: flex;
    flex-direction: column;
    height: 100vh;
    background: #1a202c;
    color: #e2e8f0;
  }

  .graph-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.75rem 1rem;
    background: #2d3748;
    border-bottom: 1px solid #4a5568;
  }

  .graph-header h1 {
    margin: 0;
    font-size: 1.25rem;
    font-weight: 500;
  }

  .back-link {
    color: #63b3ed;
    text-decoration: none;
    font-size: 0.9rem;
  }

  .back-link:hover {
    text-decoration: underline;
  }

  .graph-toolbar {
    display: flex;
    gap: 0.5rem;
    padding: 0.75rem 1rem;
    background: #2d3748;
  }

  .graph-toolbar button {
    padding: 0.5rem 1.5rem;
    background: #4299e1;
    border: none;
    border-radius: 4px;
    color: white;
    font-weight: 500;
    cursor: pointer;
  }

  .graph-toolbar button:hover:not(:disabled) {
    background: #3182ce;
  }

  .graph-toolbar button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .error {
    padding: 0.5rem 1rem;
    background: #742a2a;
    color: #feb2b2;
    font-size: 0.85rem;
  }

  .graph-container {
    flex: 1;
    min-height: 0;
    position: relative;
  }
</style>
