import { LitElement, html } from 'https://esm.sh/lit@3.1.0';

const NIKAYA_NAMES = {
  dn: 'Dīgha Nikāya',
  mn: 'Majjhima Nikāya',
  sn: 'Saṃyutta Nikāya',
  an: 'Aṅguttara Nikāya',
  kn: 'Khuddaka Nikāya'
};

class SuttaApp extends LitElement {
  static properties = {
    nikayas: { type: Array },
    suttasByNikaya: { type: Object },
    expandedNikayas: { type: Object },
    verses: { type: Array },
    current: { type: String },
    suttaName: { type: String },
    helaSuttaName: { type: String },
    navOpen: { type: Boolean },
    loading: { type: Boolean },
    showHela: { type: Boolean }
  };

  createRenderRoot() {
    return this;
  }

  constructor() {
    super();
    this.nikayas = [];
    this.suttasByNikaya = {};
    this.expandedNikayas = {};
    this.verses = [];
    this.current = '';
    this.suttaName = '';
    this.helaSuttaName = '';
    this.navOpen = true;
    this.loading = false;
    this.showHela = false;
  }

  connectedCallback() {
    super.connectedCallback();
    this.loadNikayas();
    window.addEventListener('hashchange', () => this.handleHash());
  }

  async loadNikayas() {
    const res = await fetch('/api/nikayas');
    this.nikayas = await res.json();
    // Expand first nikaya by default
    if (this.nikayas.length > 0) {
      this.toggleNikaya(this.nikayas[0].id);
    }
    this.handleHash();
  }

  async toggleNikaya(nikayaId) {
    this.expandedNikayas = {
      ...this.expandedNikayas,
      [nikayaId]: !this.expandedNikayas[nikayaId]
    };
    
    // Load suttas if not already loaded
    if (this.expandedNikayas[nikayaId] && !this.suttasByNikaya[nikayaId]) {
      const res = await fetch(`/api/suttas/${nikayaId}`);
      const suttas = await res.json();
      this.suttasByNikaya = { ...this.suttasByNikaya, [nikayaId]: suttas };
    }
  }

  handleHash() {
    const id = location.hash.slice(1);
    if (id && id !== this.current) this.loadSutta(id);
  }

  async loadSutta(id) {
    this.current = id;
    this.loading = true;
    this.requestUpdate();
    
    const res = await fetch(`/api/sutta/${id}`);
    this.verses = await res.json();
    
    const nameVerse = this.verses.find(v => v.index === `${id}:0.2`);
    this.suttaName = nameVerse?.text?.trim() || id.toUpperCase();
    this.helaSuttaName = nameVerse?.hela_text?.trim() || this.suttaName;
    this.loading = false;
    
    if (window.innerWidth < 800) this.navOpen = false;
  }

  selectSutta(id) {
    history.pushState(null, '', `#${id}`);
    this.loadSutta(id);
  }

  toggleNav() {
    this.navOpen = !this.navOpen;
  }

  toggleScript() {
    this.showHela = !this.showHela;
  }

  renderNavSection(nikaya) {
    const isExpanded = this.expandedNikayas[nikaya.id];
    const suttas = this.suttasByNikaya[nikaya.id] || [];
    const name = NIKAYA_NAMES[nikaya.id] || nikaya.id.toUpperCase();
    
    return html`
      <div class="nav-section">
        <div class="nav-section-header" @click=${() => this.toggleNikaya(nikaya.id)}>
          <span class="nav-section-toggle">${isExpanded ? '▼' : '▶'}</span>
          <span class="nav-section-title">${name}</span>
          <span class="nav-section-count">${nikaya.count}</span>
        </div>
        ${isExpanded ? html`
          <div class="nav-section-items">
            ${suttas.map(s => html`
              <span 
                class="nav-item ${s === this.current ? 'active' : ''}" 
                @click=${() => this.selectSutta(s)}>
                ${s.toUpperCase()}
              </span>
            `)}
          </div>
        ` : ''}
      </div>
    `;
  }

  renderWelcome() {
    return html`
      <div class="welcome">
        <h1>Sutta Reader</h1>
        <p>Select a sutta from the collection</p>
      </div>
    `;
  }

  renderLoading() {
    return html`
      <div class="loading">
        <span class="spinner"></span>Loading...
      </div>
    `;
  }

  renderToolbar() {
    return html`
      <div class="toolbar">
        <button 
          class="script-toggle ${this.showHela ? 'active' : ''}" 
          @click=${this.toggleScript}>
          ${this.showHela ? 'Latin' : 'හෙළ'}
        </button>
      </div>
    `;
  }

  renderSutta() {
    const displayName = this.showHela ? this.helaSuttaName : this.suttaName;
    
    return html`
      <header class="sutta-header">
        <div class="sutta-header-top">
          <div>
            <div class="sutta-id">${this.current.toUpperCase()}</div>
            <h1 class="sutta-title">${displayName}</h1>
          </div>
          ${this.renderToolbar()}
        </div>
      </header>
      <div class="verses ${this.showHela ? 'hela-script' : ''}">
        ${this.verses.map(v => {
          const verseNum = v.index.split(':')[1];
          if (verseNum.startsWith('0.')) return '';
          const text = this.showHela ? (v.hela_text || v.text) : v.text;
          return html`
            <p class="verse">
              <span class="verse-ref">${verseNum}</span>${text || ''}
            </p>
          `;
        })}
      </div>
    `;
  }

  render() {
    const isMobile = window.innerWidth < 800;
    
    return html`
      <button class="hamburger" @click=${this.toggleNav}>
        ${this.navOpen ? '✕' : '☰'}
      </button>

      <nav class=${this.navOpen ? '' : 'collapsed'}>
        <div class="nav-header">Pāli Canon</div>
        ${this.nikayas.map(n => this.renderNavSection(n))}
      </nav>

      <main class="${this.navOpen ? '' : 'expanded'} ${isMobile && this.navOpen ? 'dimmed' : ''}">
        <div class="reader">
          ${!this.current 
            ? this.renderWelcome() 
            : this.loading 
              ? this.renderLoading() 
              : this.renderSutta()}
        </div>
      </main>
    `;
  }
}

customElements.define('sutta-app', SuttaApp);
