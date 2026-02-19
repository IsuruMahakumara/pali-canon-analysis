// API functions for sutta reader

export async function fetchNikayas() {
  const res = await fetch('/api/nikayas');
  return res.json();
}

export async function fetchSuttas(nikayaId) {
  const res = await fetch(`/api/suttas/${nikayaId}`);
  return res.json();
}

export async function fetchSutta(suttaId) {
  const res = await fetch(`/api/sutta/${suttaId}`);
  return res.json();
}

