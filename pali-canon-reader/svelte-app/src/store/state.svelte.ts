import { indexGraphStore } from '../core/indexGraphStore';
import type { TreeNode } from '../core/parseGraphML';


export interface Verse {
  index: string;
  text: string;
  hela_text?: string;
}

export interface DictionaryEntry {
  entry: string;
  definitions: Record<string, unknown> | null;
}

export interface AppState {
  current: string;
  verses: Verse[];
  loading: boolean;
  navOpen: boolean;
  showHela: boolean;
  dictionaryEntry: DictionaryEntry | null;
  navTree: TreeNode | null;
}


// Unified reactive state using Svelte 5 $state
export const state: AppState = $state({
  current: '',
  verses: [],
  loading: false,
  navOpen: true,
  showHela: false,
  dictionaryEntry: null,
  navTree: null
});

export const api = {


  async init(url: string = '/Canon.graphml') {
    // 1. Trigger the load in the specialized graph store
    await indexGraphStore.load(url);
    
    //[cite_start]
    // 2. Sync the resulting tree into our global state for easy access [cite: 10, 11]
    // We subscribe once to get the value or use a reactive effect in a component
    indexGraphStore.subscribe(value => {
      state.navTree = value.navTree;
    });
  },
  /**
   * Loads a specific Sutta (reading unit) by ID
   * Updates state.verses and state.current [cite: 1, 8]
   */
  async loadSutta(id: string): Promise<void> {
    if (!id || id === state.current) return;
    
    state.current = id;
    state.loading = true;
    
    try {
      const res = await fetch(`/api/sutta/${id}`);
      if (!res.ok) throw new Error('Network response was not ok');
      state.verses = await res.json();
    } catch (error) {
      console.error("Failed to load sutta:", error);
      state.verses = [];
    } finally {
      state.loading = false;
      // Close sidebar on mobile after selection
      if (window.innerWidth < 800) state.navOpen = false;
    }
  },

  /**
   * Updates URL hash and triggers the sutta load 
   */
  selectSutta(id: string): void {
    history.pushState(null, '', `#${id}`);
    this.loadSutta(id);
  },

  /**
   * Cleans a word string and fetches its definition [cite: 1, 8]
   */
  async lookupWord(word: string): Promise<void> {
    const entry = word.trim().replace(/[.,;:!?()[\]'"–—]/g, '');
    if (!entry) return;
    
    try {
      const res = await fetch(`/api/dictionary/${encodeURIComponent(entry)}`);
      const data = await res.json();
      state.dictionaryEntry = data;
    } catch (error) {
      console.error("Dictionary lookup failed:", error);
      state.dictionaryEntry = null;
    }
  }
};

export function getSuttaName(hela: boolean = false): string {
  const v = state.verses.find(v => v.index === `${state.current}:0.2`);
  const latin = v?.text?.trim() || state.current.toUpperCase();
  return hela ? (v?.hela_text?.trim() || latin) : latin;
}



if (typeof window !== 'undefined') {
  Object.defineProperty(window, 'appState', {
    get: () => $state.snapshot(state),
    configurable: true
  });
}