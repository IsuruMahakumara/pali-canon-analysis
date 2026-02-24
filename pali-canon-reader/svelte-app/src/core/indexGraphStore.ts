import { writable } from 'svelte/store';
import { parseGraphML, findRoot, transformToHierarchy, type TreeNode } from './parseGraphML';
import { ElementDefinition } from 'cytoscape';


// 1. Define the State
const initialState = {
  nodes: [] as ElementDefinition[],
  edges: [] as ElementDefinition[],
  navTree: null as TreeNode | null,
  loading: false,
  error: null as string | null  
};

const indexGraph = writable(initialState);

// 2. Define the "Actions" (Custom Methods)
export const indexGraphStore = {
  subscribe: indexGraph.subscribe, // Makes it a store

  async load(url: string) {
    indexGraph.update(s => ({ ...s, loading: true }));
    
    try {
      const res = await fetch(url);
      const xml = await res.text();
      const { nodes, edges } = parseGraphML(xml);
      const rootId = findRoot(nodes, edges);
      const navTree = transformToHierarchy(nodes, edges, rootId);

      indexGraph.set({
        nodes,
        edges,
        navTree,
        loading: false,
        error: null
      });
    } catch (e) {
      indexGraph.update(s => ({ ...s, error: 'Failed to load', loading: false }));
    }
  },


};