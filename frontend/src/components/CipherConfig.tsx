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
    <div className="bg-slate-900/60 border border-slate-800/80 rounded-2xl p-6 shadow-xl backdrop-blur-sm flex flex-col space-y-4">
      <h2 className="text-lg font-bold text-slate-200 flex items-center">
        <svg className="w-5 h-5 mr-2 text-violet-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" />
        </svg>
        Cipher Configuration
      </h2>

      {/* Tab buttons */}
      <div className="flex flex-wrap border-b border-slate-850 p-1 bg-slate-950/80 rounded-xl gap-1">
        {CIPHER_TABS.map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`flex-1 min-w-[80px] py-2 text-xs font-semibold rounded-lg capitalize transition-all ${
              activeTab === tab
                ? 'bg-indigo-600/15 text-indigo-400 border border-indigo-500/25'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/40'
            }`}
          >
            {tab}
          </button>
        ))}
      </div>

      {/* Tab Inputs */}
      <div key={activeTab} className="bg-slate-950/40 border border-slate-850 rounded-xl p-4 min-h-[100px] flex flex-col justify-center animate-fade-in">
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
