// Shared reactive state using Svelte 5 runes
export const NIKAYA_NAMES = {
  dn: 'Dīgha Nikāya',
  mn: 'Majjhima Nikāya', 
  sn: 'Saṃyutta Nikāya',
  an: 'Aṅguttara Nikāya',
  kn: 'Khuddaka Nikāya'
};

export const state = $state({
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
  async loadNikayas() {
    const res = await fetch('/api/nikayas');
    state.nikayas = await res.json();
    if (state.nikayas.length) await this.toggleNikaya(state.nikayas[0].id);
  },

  async toggleNikaya(id) {
    state.expanded[id] = !state.expanded[id];
    if (state.expanded[id] && !state.suttasByNikaya[id]) {
      const res = await fetch(`/api/suttas/${id}`);
      state.suttasByNikaya[id] = await res.json();
    }
  },

  async loadSutta(id) {
    if (!id || id === state.current) return;
    state.current = id;
    state.loading = true;
    const res = await fetch(`/api/sutta/${id}`);
    state.verses = await res.json();
    state.loading = false;
    if (window.innerWidth < 800) state.navOpen = false;
  },

  selectSutta(id) {
    history.pushState(null, '', `#${id}`);
    this.loadSutta(id);
  }
};

export function getSuttaName(hela = false) {
  const v = state.verses.find(v => v.index === `${state.current}:0.2`);
  const latin = v?.text?.trim() || state.current.toUpperCase();
  return hela ? (v?.hela_text?.trim() || latin) : latin;
}

