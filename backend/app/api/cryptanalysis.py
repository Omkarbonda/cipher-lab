from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from app.cryptanalysis import frequency, index_of_coincidence as ic, brute_force

router = APIRouter(prefix="/api/cryptanalysis", tags=["Cryptanalysis"])

# ─── Pydantic Schemas ───

class AnalysisRequest(BaseModel):
    text: str = Field(..., description="Ciphertext or plaintext to analyze")

class AnalysisResponse(BaseModel):
    letter_counts: Dict[str, int] = Field(..., description="Raw count of each letter A-Z")
    frequencies: Dict[str, float] = Field(..., description="Relative frequency (0-1) of each letter A-Z")
    index_of_coincidence: float = Field(..., description="Calculated Index of Coincidence (IC)")
    top_5: List[List] = Field(..., description="Top 5 most frequent letters with their frequencies")

class CrackCaesarResponse(BaseModel):
    best: dict = Field(..., description="The most likely shift and its decoded plaintext")
    all_shifts: List[dict] = Field(..., description="All tried shifts sorted best-first")

class CrackVigenereRequest(BaseModel):
    text: str = Field(..., description="Vigenère ciphertext to crack")
    max_key_length: int = Field(15, description="Maximum key length to estimate")

class CrackVigenereResponse(BaseModel):
    best: Optional[dict] = Field(None, description="The recovered Vigenère key and plaintext")
    candidates: List[dict] = Field(..., description="All tried key lengths and decoded texts")

class CrackSubstitutionResponse(BaseModel):
    candidates: List[dict] = Field(..., description="Top candidate substitution keys with decrypted text and scores")

class CrackPlayfairResponse(BaseModel):
    candidates: List[dict] = Field(..., description="Top candidate Playfair keys with decrypted text and scores")
    note: str = Field(..., description="Note about the best-effort nature of Playfair cracking")

# ─── Endpoints ───

@router.post("/analyze", response_model=AnalysisResponse)
def analyze_text(req: AnalysisRequest):
    counts = frequency.count(req.text)
    rel = frequency.relative(req.text)
    ioc = ic.index_of_coincidence(req.text)
    top = [[letter, freq] for letter, freq in frequency.top_letters(req.text, 5)]
    return {
        "letter_counts": counts,
        "frequencies": rel,
        "index_of_coincidence": round(ioc, 6),
        "top_5": top
    }

@router.post("/crack/caesar", response_model=CrackCaesarResponse)
def crack_caesar(req: AnalysisRequest):
    if not any(ch.isalpha() for ch in req.text):
         raise HTTPException(status_code=400, detail="Text must contain at least one alphabetic character")
    return brute_force.crack_caesar(req.text)

@router.post("/crack/vigenere", response_model=CrackVigenereResponse)
def crack_vigenere(req: CrackVigenereRequest):
    if not any(ch.isalpha() for ch in req.text):
         raise HTTPException(status_code=400, detail="Text must contain at least one alphabetic character")
    return brute_force.crack_vigenere(req.text, max_key_len=req.max_key_length)


@router.post("/crack/substitution", response_model=CrackSubstitutionResponse)
def crack_substitution(req: AnalysisRequest):
    if not any(ch.isalpha() for ch in req.text):
        raise HTTPException(status_code=400, detail="Text must contain at least one alphabetic character")
    return brute_force.crack_substitution(req.text)


@router.post("/crack/playfair", response_model=CrackPlayfairResponse)
def crack_playfair(req: CrackVigenereRequest):
    if not any(ch.isalpha() for ch in req.text):
        raise HTTPException(status_code=400, detail="Text must contain at least one alphabetic character")
    return brute_force.crack_playfair(req.text, max_key_len=req.max_key_length)
