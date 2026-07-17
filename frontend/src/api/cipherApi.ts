import type { AnalysisData, CipherType, CrackCandidate } from '../types/cipher';

export async function analyzeText(text: string): Promise<AnalysisData> {
  const res = await fetch('/api/cryptanalysis/analyze', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text }),
  });
  if (!res.ok) throw new Error('Analysis request failed');
  return res.json();
}

export async function encodeCipher(
  type: CipherType,
  text: string,
  params: Record<string, unknown>,
): Promise<string> {
  let endpoint = '';
  if (type === 'caesar') endpoint = '/api/ciphers/caesar/encode';
  else if (type === 'vigenere') endpoint = '/api/ciphers/vigenere/encode';
  else if (type === 'substitution') endpoint = '/api/ciphers/substitution/encode';
  else if (type === 'playfair') endpoint = '/api/ciphers/playfair/encode';
  else if (type === 'railfence') endpoint = '/api/ciphers/railfence/encode';
  else if (type === 'beaufort') endpoint = '/api/ciphers/beaufort/encode';
  else if (type === 'affine') endpoint = '/api/ciphers/affine/encode';
  else if (type === 'columnar') endpoint = '/api/ciphers/columnar/encode';

  const res = await fetch(endpoint, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, ...params }),
  });
  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.detail || 'Encryption failed');
  }
  const data = await res.json();
  return data.result;
}

export async function decodeCipher(
  type: CipherType,
  text: string,
  params: Record<string, unknown>,
): Promise<string> {
  let endpoint = '';
  if (type === 'caesar') endpoint = '/api/ciphers/caesar/decode';
  else if (type === 'vigenere') endpoint = '/api/ciphers/vigenere/decode';
  else if (type === 'substitution') endpoint = '/api/ciphers/substitution/decode';
  else if (type === 'playfair') endpoint = '/api/ciphers/playfair/decode';
  else if (type === 'railfence') endpoint = '/api/ciphers/railfence/decode';
  else if (type === 'beaufort') endpoint = '/api/ciphers/beaufort/decode';
  else if (type === 'affine') endpoint = '/api/ciphers/affine/decode';
  else if (type === 'columnar') endpoint = '/api/ciphers/columnar/decode';

  const res = await fetch(endpoint, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, ...params }),
  });
  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.detail || 'Decryption failed');
  }
  const data = await res.json();
  return data.result;
}

export async function crackCaesar(text: string): Promise<{
  best: CrackCandidate;
  all_shifts: CrackCandidate[];
}> {
  const res = await fetch('/api/cryptanalysis/crack/caesar', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text }),
  });
  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.detail || 'Cracking failed');
  }
  return res.json();
}

export async function crackVigenere(
  text: string,
  maxKeyLength: number,
): Promise<{
  best: CrackCandidate;
  candidates: CrackCandidate[];
}> {
  const res = await fetch('/api/cryptanalysis/crack/vigenere', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, max_key_length: maxKeyLength }),
  });
  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.detail || 'Cracking failed');
  }
  return res.json();
}
