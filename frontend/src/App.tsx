import { useEffect, useState } from 'react';
import type { CipherType } from './types/cipher';
import { analyzeText, encodeCipher, decodeCipher, crackCaesar, crackVigenere } from './api/cipherApi';
import Header from './components/Header';
import Footer from './components/Footer';
import WorkspaceConsole from './components/WorkspaceConsole';
import CipherConfig from './components/CipherConfig';
import LiveCryptanalysis from './components/LiveCryptanalysis';
import CrackerResults from './components/CrackerResults';
import Toast from './components/Toast';

function App() {
  const [activeTab, setActiveTab] = useState<CipherType>('caesar');
  const [inputText, setInputText] = useState<string>('Cryptography is the practice and study of techniques for secure communication in the presence of adversarial behavior.');
  const [outputText, setOutputText] = useState<string>('');

  // Cipher keys
  const [caesarShift, setCaesarShift] = useState<number>(3);
  const [vigenereKey, setVigenereKey] = useState<string>('LEMON');
  const [substitutionKey, setSubstitutionKey] = useState<string>('ZYXWVUTSRQPONMLKJIHGFEDCBA');
  const [playfairKey, setPlayfairKey] = useState<string>('KEYWORD');
  const [railFenceRails, setRailFenceRails] = useState<number>(3);
  const [beaufortKey, setBeaufortKey] = useState<string>('KEY');
  const [affineA, setAffineA] = useState<number>(5);
  const [affineB, setAffineB] = useState<number>(8);
  const [columnarKey, setColumnarKey] = useState<string>('KEY');

  // Toast notification state
  const [toast, setToast] = useState<{ message: string; type: 'error' | 'success' | 'info' } | null>(null);
  const showToast = (message: string, type: 'error' | 'success' | 'info' = 'error') => setToast({ message, type });

  // Analysis states
  const [ioc, setIoc] = useState<number>(0);
  const [frequencies, setFrequencies] = useState<Record<string, number>>({});

  // Cracking states
  const [isCracking, setIsCracking] = useState<boolean>(false);
  const [crackCandidates, setCrackCandidates] = useState<any[]>([]);
  const [crackVigenereCandidates, setCrackVigenereCandidates] = useState<any[]>([]);

  // Trigger analysis when input changes
  useEffect(() => {
    runAnalysis(inputText);
  }, [inputText]);

  const runAnalysis = async (text: string) => {
    if (!text.trim()) {
      setIoc(0);
      setFrequencies({});
      return;
    }
    try {
      const data = await analyzeText(text);
      setIoc(data.index_of_coincidence);
      setFrequencies(data.frequencies);
    } catch (err) {
      console.error('Failed to run analysis', err);
    }
  };

  const handleEncrypt = async () => {
    let params: Record<string, unknown> = {};
    if (activeTab === 'caesar') params = { shift: caesarShift };
    else if (activeTab === 'vigenere') params = { key: vigenereKey };
    else if (activeTab === 'substitution') params = { key: substitutionKey };
    else if (activeTab === 'playfair') params = { key: playfairKey };
    else if (activeTab === 'railfence') params = { rails: railFenceRails };
    else if (activeTab === 'beaufort') params = { key: beaufortKey };
    else if (activeTab === 'affine') params = { a: affineA, b: affineB };
    else if (activeTab === 'columnar') params = { key: columnarKey };
    try {
      const result = await encodeCipher(activeTab, inputText, params);
      setOutputText(result);
    } catch (err: any) {
      showToast(err.message ?? 'Encryption failed. Is backend running?');
    }
  };

  const handleDecrypt = async () => {
    let params: Record<string, unknown> = {};
    if (activeTab === 'caesar') params = { shift: caesarShift };
    else if (activeTab === 'vigenere') params = { key: vigenereKey };
    else if (activeTab === 'substitution') params = { key: substitutionKey };
    else if (activeTab === 'playfair') params = { key: playfairKey };
    else if (activeTab === 'railfence') params = { rails: railFenceRails };
    else if (activeTab === 'beaufort') params = { key: beaufortKey };
    else if (activeTab === 'affine') params = { a: affineA, b: affineB };
    else if (activeTab === 'columnar') params = { key: columnarKey };
    try {
      const result = await decodeCipher(activeTab, inputText, params);
      setOutputText(result);
    } catch (err: any) {
      showToast(err.message ?? 'Decryption failed.');
    }
  };

  const handleCrack = async () => {
    setIsCracking(true);
    setCrackCandidates([]);
    setCrackVigenereCandidates([]);
    try {
      if (activeTab === 'caesar') {
        const data = await crackCaesar(inputText);
        setOutputText(data.best.plaintext);
        setCaesarShift(data.best.shift!);
        setCrackCandidates(data.all_shifts.slice(0, 5));
      } else if (activeTab === 'vigenere') {
        const data = await crackVigenere(inputText, 15);
        if (data.best) {
          setOutputText(data.best.plaintext);
          setVigenereKey(data.best.key!);
          setCrackVigenereCandidates(data.candidates.slice(0, 5));
        } else {
          showToast('Failed to crack Vigenère. Ciphertext may lack English structure.', 'info');
        }
      } else {
        showToast('Substitution and Playfair cracking tools in development.', 'info');
      }
    } catch (err: any) {
      showToast(err.message ?? 'Cracking API failed.');
    } finally {
      setIsCracking(false);
    }
  };

  const generateRandomSubstitutionKey = () => {
    const letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');
    for (let i = letters.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [letters[i], letters[j]] = [letters[j], letters[i]];
    }
    setSubstitutionKey(letters.join(''));
  };

  return (
    <div className="min-h-screen bg-ink text-parchment flex flex-col font-mono selection:bg-brass/30 selection:text-parchment-50">
      <div className="scanlines" />
      <Header />

      <main className="flex-grow max-w-7xl w-full mx-auto px-4 py-6 grid grid-cols-1 lg:grid-cols-12 gap-5">
        {/* LEFT COLUMN: Workspace + Cipher Config (7 cols) */}
        <div className="lg:col-span-7 flex flex-col space-y-5">
          <WorkspaceConsole
            inputText={inputText}
            setInputText={setInputText}
            outputText={outputText}
            handleEncrypt={handleEncrypt}
            handleDecrypt={handleDecrypt}
            handleCrack={handleCrack}
            isCracking={isCracking}
            activeTab={activeTab}
          />
          <CipherConfig
            activeTab={activeTab}
            setActiveTab={setActiveTab}
            caesarShift={caesarShift}
            setCaesarShift={setCaesarShift}
            vigenereKey={vigenereKey}
            setVigenereKey={setVigenereKey}
            substitutionKey={substitutionKey}
            setSubstitutionKey={setSubstitutionKey}
            generateRandomSubstitutionKey={generateRandomSubstitutionKey}
            playfairKey={playfairKey}
            setPlayfairKey={setPlayfairKey}
            rails={railFenceRails}
            setRails={setRailFenceRails}
            beaufortKey={beaufortKey}
            setBeaufortKey={setBeaufortKey}
            affineA={affineA}
            setAffineA={setAffineA}
            affineB={affineB}
            setAffineB={setAffineB}
            columnarKey={columnarKey}
            setColumnarKey={setColumnarKey}
          />
        </div>

        {/* RIGHT COLUMN: Cryptanalysis (5 cols) */}
        <div className="lg:col-span-5 flex flex-col space-y-5">
          <LiveCryptanalysis ioc={ioc} frequencies={frequencies} />
          <CrackerResults
            activeTab={activeTab}
            crackCandidates={crackCandidates}
            crackVigenereCandidates={crackVigenereCandidates}
            setCaesarShift={setCaesarShift}
            setVigenereKey={setVigenereKey}
            setOutputText={setOutputText}
          />
        </div>
      </main>

      <Toast message={toast?.message ?? null} type={toast?.type ?? 'error'} onClose={() => setToast(null)} />
      <Footer />
    </div>
  );
}

export default App;
