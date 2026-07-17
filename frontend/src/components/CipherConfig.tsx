import type { CipherType } from '../types/cipher';
import CaesarConfig from './configs/CaesarConfig';
import VigenereConfig from './configs/VigenereConfig';
import SubstitutionConfig from './configs/SubstitutionConfig';
import PlayfairConfig from './configs/PlayfairConfig';
import RailFenceConfig from './configs/RailFenceConfig';
import BeaufortConfig from './configs/BeaufortConfig';
import AffineConfig from './configs/AffineConfig';
import ColumnarConfig from './configs/ColumnarConfig';

interface CipherConfigProps {
  activeTab: CipherType;
  setActiveTab: (tab: CipherType) => void;
  caesarShift: number;
  setCaesarShift: (shift: number) => void;
  vigenereKey: string;
  setVigenereKey: (key: string) => void;
  substitutionKey: string;
  setSubstitutionKey: (key: string) => void;
  generateRandomSubstitutionKey: () => void;
  playfairKey: string;
  setPlayfairKey: (key: string) => void;
  rails: number;
  setRails: (rails: number) => void;
  beaufortKey: string;
  setBeaufortKey: (key: string) => void;
  affineA: number;
  setAffineA: (a: number) => void;
  affineB: number;
  setAffineB: (b: number) => void;
  columnarKey: string;
  setColumnarKey: (key: string) => void;
}

const CIPHER_TABS: CipherType[] = ['caesar', 'vigenere', 'substitution', 'playfair', 'railfence', 'beaufort', 'affine', 'columnar'];

export default function CipherConfig({
  activeTab,
  setActiveTab,
  caesarShift,
  setCaesarShift,
  vigenereKey,
  setVigenereKey,
  substitutionKey,
  setSubstitutionKey,
  generateRandomSubstitutionKey,
  playfairKey,
  setPlayfairKey,
  rails,
  setRails,
  beaufortKey,
  setBeaufortKey,
  affineA,
  setAffineA,
  affineB,
  setAffineB,
  columnarKey,
  setColumnarKey,
}: CipherConfigProps) {
  return (
    <div className="border border-ink-500 bg-ink-700/60">
      {/* Panel header */}
      <div className="flex items-center justify-between px-4 py-2 bg-ink-600/80 border-b border-ink-500">
        <span className="text-[10px] text-parchment/40 tracking-[0.2em] uppercase">Cipher Configuration</span>
        <span className="text-[9px] text-brass/50 tracking-[0.15em] uppercase">Selector</span>
      </div>

      {/* Mechanical selector tabs */}
      <div className="flex flex-wrap border-b border-ink-500">
        {CIPHER_TABS.map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`flex-1 min-w-[70px] py-2 text-[10px] font-semibold uppercase tracking-[0.15em] border-r border-ink-500 last:border-r-0 transition-all ${
              activeTab === tab
                ? 'bg-brass/10 text-brass border-b-2 border-b-brass'
                : 'bg-ink-800/40 text-parchment/30 hover:bg-ink-700 hover:text-parchment/60'
            }`}
          >
            {tab}
          </button>
        ))}
      </div>

      {/* Active cipher params */}
      <div key={activeTab} className="p-4 min-h-[80px] animate-fade-in">
        {activeTab === 'caesar' && (
          <CaesarConfig caesarShift={caesarShift} setCaesarShift={setCaesarShift} />
        )}
        {activeTab === 'vigenere' && (
          <VigenereConfig vigenereKey={vigenereKey} setVigenereKey={setVigenereKey} />
        )}
        {activeTab === 'substitution' && (
          <SubstitutionConfig
            substitutionKey={substitutionKey}
            setSubstitutionKey={setSubstitutionKey}
            generateRandomSubstitutionKey={generateRandomSubstitutionKey}
          />
        )}
        {activeTab === 'playfair' && (
          <PlayfairConfig playfairKey={playfairKey} setPlayfairKey={setPlayfairKey} />
        )}
        {activeTab === 'railfence' && (
          <RailFenceConfig rails={rails} setRails={setRails} />
        )}
        {activeTab === 'beaufort' && (
          <BeaufortConfig beaufortKey={beaufortKey} setBeaufortKey={setBeaufortKey} />
        )}
        {activeTab === 'affine' && (
          <AffineConfig affineA={affineA} setAffineA={setAffineA} affineB={affineB} setAffineB={setAffineB} />
        )}
        {activeTab === 'columnar' && (
          <ColumnarConfig columnarKey={columnarKey} setColumnarKey={setColumnarKey} />
        )}
      </div>
    </div>
  );
}
