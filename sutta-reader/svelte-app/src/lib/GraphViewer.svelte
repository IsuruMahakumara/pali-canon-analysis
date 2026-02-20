<script>
  import { onMount } from 'svelte';
  import cytoscape from 'cytoscape';

  let container;
  let cy;
  let query = $state('MATCH (n)-[r]->(m) RETURN n, r, m LIMIT 50');
  let loading = $state(false);
  let error = $state('');

  const GRAPHQL_URL = '/graphql';

  async function runQuery() {
    loading = true;
    error = '';
    
    try {
      const gqlQuery = `
        query($q: String!, $cols: [String!]) {
          cypher(query: $q, columns: $cols)
        }
      `;
      
      const res = await fetch(GRAPHQL_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: gqlQuery,
          variables: { q: query, cols: ['n', 'r', 'm'] }
        })
      });
      
      const json = await res.json();
      if (json.errors) {
        error = json.errors[0].message;
        return;
      }
      
      renderGraph(json.data.cypher);
    } catch (e) {
      error = e.message;
    } finally {
      loading = false;
    }
  }

  function renderGraph(data) {
    const nodes = new Map();
    const edges = [];

    for (const row of data) {
      if (row.n) {
        const id = String(row.n.id);
        nodes.set(id, {
          data: { 
            id, 
            label: row.n.properties?.name || row.n.label || id 
          }
        });
      }
      if (row.m) {
        const id = String(row.m.id);
        nodes.set(id, {
          data: { 
            id, 
            label: row.m.properties?.name || row.m.label || id 
          }
        });
      }
      if (row.r) {
        edges.push({
          data: {
            id: String(row.r.id),
            source: String(row.r.start_id),
            target: String(row.r.end_id),
            label: row.r.label || ''
          }
        });
      }
    }

    cy.elements().remove();
    cy.add([...nodes.values(), ...edges]);
    cy.layout({ name: 'cose', animate: false }).run();
    cy.fit();
  }

  onMount(() => {
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
            'shape': 'roundrectangle'
          }
        },
        {
          selector: 'edge',
          style: {
            'width': 1.5,
            'line-color': '#718096',
            'target-arrow-color': '#718096',
            'target-arrow-shape': 'triangle',
            'curve-style': 'bezier',
            'label': 'data(label)',
            'font-size': '8px',
            'color': '#a0aec0'
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
      layout: { name: 'grid' }
    });
    
    runQuery();
  });
</script>

<div class="graph-page">
  <header class="graph-header">
    <a href="#reader" class="back-link">← Reader</a>
    <h1>Graph Explorer</h1>
  </header>
  
  <div class="query-bar">
    <textarea bind:value={query} rows="2" placeholder="Cypher query..."></textarea>
    <button onclick={runQuery} disabled={loading}>
      {loading ? '...' : 'Run'}
    </button>
  </div>
  
  {#if error}
    <div class="error">{error}</div>
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
  
  .query-bar {
    display: flex;
    gap: 0.5rem;
    padding: 0.75rem 1rem;
    background: #2d3748;
  }
  
  .query-bar textarea {
    flex: 1;
    padding: 0.5rem;
    background: #1a202c;
    border: 1px solid #4a5568;
    border-radius: 4px;
    color: #e2e8f0;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    resize: vertical;
  }
  
  .query-bar button {
    padding: 0.5rem 1.5rem;
    background: #4299e1;
    border: none;
    border-radius: 4px;
    color: white;
    font-weight: 500;
    cursor: pointer;
  }
  
  .query-bar button:hover:not(:disabled) {
    background: #3182ce;
  }
  
  .query-bar button:disabled {
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
  }
</style>

