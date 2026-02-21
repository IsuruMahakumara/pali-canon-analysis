export interface Nikaya {
  id: string;
  count: number;
}

export interface Verse {
  index: string;
  text: string;
  hela_text?: string;
}

export interface AppState {
  nikayas: Nikaya[];
  suttasByNikaya: Record<string, string[]>;
  expanded: Record<string, boolean>;
  current: string;
  verses: Verse[];
  loading: boolean;
  navOpen: boolean;
  showHela: boolean;
}

export const NIKAYA_NAMES: Record<string, string> = {
  dn: 'Dīgha Nikāya',
  mn: 'Majjhima Nikāya', 
  sn: 'Saṃyutta Nikāya',
  an: 'Aṅguttara Nikāya',
  kn: 'Khuddaka Nikāya'
};

export const state: AppState = $state({
  nikayas: [],
  suttasByNikaya: {},
  expanded: {},
  current: '',
  verses: [],
  loading: false,
  navOpen: true,
  showHela: false
});

export const api = {
  async loadNikayas(): Promise<void> {
    const res = await fetch('/api/nikayas');
    state.nikayas = await res.json();
    if (state.nikayas.length) await this.toggleNikaya(state.nikayas[0].id);
  },

  async toggleNikaya(id: string): Promise<void> {
    state.expanded[id] = !state.expanded[id];
    if (state.expanded[id] && !state.suttasByNikaya[id]) {
      const res = await fetch(`/api/suttas/${id}`);
      state.suttasByNikaya[id] = await res.json();
    }
  },

  async loadSutta(id: string): Promise<void> {
    if (!id || id === state.current) return;
    state.current = id;
    state.loading = true;
    const res = await fetch(`/api/sutta/${id}`);
    state.verses = await res.json();
    state.loading = false;
    if (window.innerWidth < 800) state.navOpen = false;
  },

  selectSutta(id: string): void {
    history.pushState(null, '', `#${id}`);
    this.loadSutta(id);
  }
};

export function getSuttaName(hela: boolean = false): string {
  const v = state.verses.find(v => v.index === `${state.current}:0.2`);
  const latin = v?.text?.trim() || state.current.toUpperCase();
  return hela ? (v?.hela_text?.trim() || latin) : latin;
}
