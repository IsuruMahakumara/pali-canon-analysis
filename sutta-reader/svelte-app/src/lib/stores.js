import { writable, derived } from 'svelte/store';

// Nikaya display names
export const NIKAYA_NAMES = {
  dn: 'Dīgha Nikāya',
  mn: 'Majjhima Nikāya',
  sn: 'Saṃyutta Nikāya',
  an: 'Aṅguttara Nikāya',
  kn: 'Khuddaka Nikāya'
};

// Core state
export const nikayas = writable([]);
export const suttasByNikaya = writable({});
export const expandedNikayas = writable({});
export const currentSuttaId = writable('');
export const verses = writable([]);
export const loading = writable(false);
export const navOpen = writable(true);
export const showHela = writable(false);

// Derived stores
export const suttaName = derived(
  [verses, currentSuttaId],
  ([$verses, $currentSuttaId]) => {
    const nameVerse = $verses.find(v => v.index === `${$currentSuttaId}:0.2`);
    return nameVerse?.text?.trim() || $currentSuttaId.toUpperCase();
  }
);

export const helaSuttaName = derived(
  [verses, currentSuttaId, suttaName],
  ([$verses, $currentSuttaId, $suttaName]) => {
    const nameVerse = $verses.find(v => v.index === `${$currentSuttaId}:0.2`);
    return nameVerse?.hela_text?.trim() || $suttaName;
  }
);

export const displayName = derived(
  [showHela, suttaName, helaSuttaName],
  ([$showHela, $suttaName, $helaSuttaName]) => 
    $showHela ? $helaSuttaName : $suttaName
);

