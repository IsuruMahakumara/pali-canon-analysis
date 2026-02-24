import type { ElementDefinition } from 'cytoscape';

export function parseGraphML(xml: string): { nodes: ElementDefinition[]; edges: ElementDefinition[] } {
  const parser = new DOMParser();
  const doc = parser.parseFromString(xml, 'text/xml');
  const nodes: ElementDefinition[] = [];
  const edges: ElementDefinition[] = [];

  const keyMap = new Map<string, string>();
  doc.querySelectorAll('key[for="node"]').forEach((k) => {
    const kid = k.getAttribute('id');
    const name = k.getAttribute('attr.name');
    if (kid && name) keyMap.set(kid, name);
  });

  const nodeEls = doc.querySelectorAll('node');
  nodeEls.forEach((el) => {
    const id = el.getAttribute('id') || '';
    const attrs: Record<string, string> = { id };
    el.querySelectorAll('data').forEach((d) => {
      const key = d.getAttribute('key');
      const name = keyMap.get(key || '');
      if (name) attrs[name] = d.textContent?.trim() ?? '';
    });
    nodes.push({ data: { id, label: id, attrs } });
  });

  const edgeEls = doc.querySelectorAll('edge');
  edgeEls.forEach((el, i) => {
    const source = el.getAttribute('source') || '';
    const target = el.getAttribute('target') || '';
    edges.push({ data: { id: `e${i}`, source, target } });
  });

  return { nodes, edges };
}

export function findRoot(nodes: ElementDefinition[], edges: ElementDefinition[]): string {
  const targets = new Set(edges.map((e) => e.data.target));
  const root = nodes.find((n) => !targets.has(n.data.id));
  return root?.data.id || nodes[0]?.data.id || '';
}

export interface TreeNode {
  id: string;
  label: string;
  children: TreeNode[];
  data: any; // original attributes
}

export function transformToHierarchy(nodes: any[], edges: any[], rootId: string): TreeNode | null {
  const nodeMap = new Map<string, TreeNode>();

  // 1. Initialize all nodes as potential tree nodes
  nodes.forEach(n => {
    nodeMap.set(n.data.id, {
      id: n.data.id,
      label: n.data.label || n.data.id,
      children: [],
      data: n.data.attrs || {}
    });
  });

  // 2. Build the parent-child relationships using edges
  edges.forEach(e => {
    const parent = nodeMap.get(e.data.source);
    const child = nodeMap.get(e.data.target);
    if (parent && child) {
      parent.children.push(child);
    }
  });

  // 3. Return the root (the starting point of your Nav)
  return nodeMap.get(rootId) || null;
}