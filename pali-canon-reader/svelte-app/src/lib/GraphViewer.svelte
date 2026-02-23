<script lang="ts">
  import { onMount } from 'svelte';
  import cytoscape, { type Core, type ElementDefinition } from 'cytoscape';
  import dagre from 'cytoscape-dagre';
  import { indexGraphStore } from './indexGraphStore';

  let container = $state<HTMLDivElement>();
  let tooltip = $state<{ x: number; y: number; attrs: Record<string, string> } | null>(null);
  let contextMenu = $state<{ x: number; y: number; label: string } | null>(null);

  const ROOT_ID = 'Canon';
  const LEVEL_COLORS: Record<number, string> = {
    0: '#d69e2e',
    1: '#3182ce',
    2: '#319795',
    3: '#38a169',
    4: '#805ad5',
  };

  let cy: Core;
  let childrenMap = new Map<string, string[]>();
  let expanded = new Set<string>();

  cytoscape.use(dagre);

  function copyLabel(label: string): void {
    navigator.clipboard.writeText(label);
    contextMenu = null;
  }

  function dagreOpts() {
    return {
      name: 'dagre',
      rankDir: 'TB',
      nodeSep: 40,
      rankSep: 60,
      animate: true,
      animationDuration: 300,
      fit: true,
      padding: 30,
    };
  }

  function visibleIds(): Set<string> {
    const vis = new Set<string>();
    const queue = [ROOT_ID];
    while (queue.length) {
      const id = queue.shift()!;
      if (vis.has(id)) continue;
      vis.add(id);
      if (expanded.has(id)) {
        for (const c of childrenMap.get(id) || []) queue.push(c);
      }
    }
    return vis;
  }

  function refresh() {
    const vis = visibleIds();
    cy.batch(() => {
      cy.nodes().forEach(n => {
        const id = n.id();
        if (vis.has(id)) {
          (n as any).show();
          const hasKids = (childrenMap.get(id)?.length ?? 0) > 0;
          n.data('label', hasKids
            ? `${id} ${expanded.has(id) ? '▾' : '▸'}`
            : id
          );
        } else {
          (n as any).hide();
        }
      });
      cy.edges().forEach(e => {
        if (vis.has(e.data('source')) && vis.has(e.data('target')))
          (e as any).show();
        else
          (e as any).hide();
      });
    });
    cy.elements(':visible').layout(dagreOpts()).run();
  }

  function collapseSubtree(nodeId: string) {
    expanded.delete(nodeId);
    for (const c of childrenMap.get(nodeId) || []) collapseSubtree(c);
  }

  function handleCollapseAll() {
    expanded = new Set([ROOT_ID]);
    refresh();
  }

  onMount(() => {
    if (!container) return;

    cy = cytoscape({
      container,
      style: [
        {
          selector: 'node',
          style: {
            'background-color': '#4a5568',
            'label': 'data(label)',
            'color': '#e2e8f0',
            'text-valign': 'center',
            'text-halign': 'center',
            'font-size': '10px',
            'width': 'label',
            'height': 'label',
            'padding': '8px',
            'shape': 'roundrectangle',
          }
        },
        ...Object.entries(LEVEL_COLORS).map(([lv, bg]) => ({
          selector: `node[level = ${lv}]`,
          style: { 'background-color': bg }
        })),
        {
          selector: 'node[level = 0]',
          style: { 'font-size': '14px', 'font-weight': 'bold' } as any
        },
        {
          selector: 'node[level = 1]',
          style: { 'font-size': '12px', 'font-weight': 'bold' } as any
        },
        {
          selector: 'edge',
          style: {
            'width': 1.5,
            'line-color': '#718096',
            'target-arrow-color': '#718096',
            'target-arrow-shape': 'triangle',
            'curve-style': 'bezier',
          }
        },
        {
          selector: 'node:selected',
          style: {
            'background-color': '#ed8936',
            'color': '#1a202c'
          }
        }
      ],
      layout: { name: 'preset' },
      wheelSensitivity: 0.3,
    });

    const unsub = indexGraphStore.subscribe(s => {
      if (!cy || s.nodes.length === 0) return;

      childrenMap = new Map();
      for (const e of s.edges) {
        const src = e.data.source as string;
        if (!childrenMap.has(src)) childrenMap.set(src, []);
        childrenMap.get(src)!.push(e.data.target as string);
      }

      const elems: ElementDefinition[] = [
        ...s.nodes.map(n => ({
          data: { ...n.data, level: parseInt(n.data.attrs?.level ?? '0') }
        })),
        ...s.edges,
      ];

      cy.batch(() => {
        cy.elements().remove();
        cy.add(elems);
      });

      expanded = new Set([ROOT_ID]);
      refresh();
    });

    cy.on('tap', 'node', evt => {
      contextMenu = null;
      const id = evt.target.id();
      if (!childrenMap.get(id)?.length) return;
      if (expanded.has(id)) collapseSubtree(id);
      else expanded.add(id);
      refresh();
    });

    cy.on('tap', evt => {
      if (evt.target === cy) contextMenu = null;
    });

    cy.on('mouseover', 'node', evt => {
      const attrs = evt.target.data('attrs');
      if (attrs) tooltip = { x: evt.originalEvent.clientX, y: evt.originalEvent.clientY, attrs };
    });

    cy.on('mouseout', 'node', () => (tooltip = null));

    cy.on('cxttap', 'node', e => {
      contextMenu = { x: e.originalEvent.clientX, y: e.originalEvent.clientY, label: e.target.id() };
    });

    indexGraphStore.load('/Canon.graphml');

    return () => { unsub(); cy.destroy(); };
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
    <button onclick={handleCollapseAll}>Collapse All</button>
  </div>
  
  {#if $indexGraphStore.error}
    <div class="error">{$indexGraphStore.error}</div>
  {/if}
  
  <div class="graph-container" bind:this={container}>
    {#if contextMenu}
      <!-- svelte-ignore a11y_click_events_have_key_events a11y_no_static_element_interactions -->
      <div
        class="context-menu"
        role="menu"
        tabindex="-1"
        style="left: {contextMenu.x}px; top: {contextMenu.y}px"
        onclick={(e) => e.stopPropagation()}
      >
        <button type="button" role="menuitem" onclick={() => copyLabel(contextMenu!.label)}>Copy name</button>
      </div>
    {/if}
    {#if tooltip}
      <div
        class="tooltip"
        style="left: {tooltip.x + 12}px; top: {tooltip.y + 12}px"
      >
        {#each Object.entries(tooltip.attrs) as [key, val]}
          <div class="tooltip-row"><span class="tooltip-key">{key}:</span> {val}</div>
        {/each}
      </div>
    {/if}
  </div>
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

  .tooltip {
    position: fixed;
    background: #2d3748;
    border: 1px solid #4a5568;
    border-radius: 4px;
    padding: 0.5rem 0.75rem;
    font-size: 0.8rem;
    color: #e2e8f0;
    pointer-events: none;
    z-index: 1000;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  }

  .tooltip-row {
    white-space: nowrap;
  }

  .tooltip-key {
    color: #63b3ed;
    font-weight: 500;
    margin-right: 0.25rem;
  }

  .context-menu {
    position: fixed;
    background: #2d3748;
    border: 1px solid #4a5568;
    border-radius: 4px;
    padding: 0.25rem 0;
    z-index: 1001;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  }

  .context-menu button {
    display: block;
    width: 100%;
    padding: 0.4rem 1rem;
    background: none;
    border: none;
    color: #e2e8f0;
    font-size: 0.9rem;
    text-align: left;
    cursor: pointer;
  }

  .context-menu button:hover {
    background: #4a5568;
  }
</style>
