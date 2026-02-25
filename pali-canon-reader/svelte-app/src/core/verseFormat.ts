import type { Verse } from '../store/state.svelte';


export interface VerseBlock {
  type: string | '';
  ref: string;
  text: string;
  prependTag: string | '';
}

function classifyVerse(verse: string, ref: string, prevBlock: VerseBlock | null):  VerseBlock {

  const block : VerseBlock = { type: '', ref:ref, text: verse, prependTag: '' };

  if (block.ref.endsWith('.0') ) { block.type = 'h2'; block.prependTag = "<br>"; }

  else if (block.ref.endsWith('.1') && prevBlock?.type !== 'h2') block.prependTag = "<br>";
  
  else if (block.ref.startsWith('0.')) block.type = '';

  return block



}

export function formatVerses(verses: Verse[], showHela: boolean): VerseBlock[] {

  const blocks: VerseBlock[] = [];
  let prevBlock: VerseBlock | null = null;

  for (const v of verses) {

    const ref = v.index.split(':')[1];
    const verse = v.text
    const helaText = v.hela_text ?? '';

    if (ref.startsWith('0.')) continue;

    const block = classifyVerse(showHela ? helaText : verse, ref, prevBlock);
    blocks.push(block);
    prevBlock = block;
  }
  return blocks;
}
