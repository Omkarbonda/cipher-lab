from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.ciphers import caesar, vigenere, substitution, playfair, rail_fence, beaufort, affine, columnar

router = APIRouter(prefix="/api/ciphers", tags=["Ciphers"])

# ─── Pydantic Schemas ───

class CaesarRequest(BaseModel):
    text: str = Field(..., description="Text to encode or decode")
    shift: int = Field(..., description="Caesar shift value (integer)")

class VigenereRequest(BaseModel):
    text: str = Field(..., description="Text to encode or decode")
    key: str = Field(..., description="Alphabetic key")

class SubstitutionRequest(BaseModel):
    text: str = Field(..., description="Text to encode or decode")
    key: str = Field(..., description="26-character unique substitution key")

class PlayfairRequest(BaseModel):
    text: str = Field(..., description="Text to encode or decode")
    key: str = Field(..., description="Playfair key square seed word")

class RailFenceRequest(BaseModel):
    text: str = Field(..., description="Text to encode or decode")
    rails: int = Field(..., description="Number of rails (2+)")

class BeaufortRequest(BaseModel):
    text: str = Field(..., description="Text to encode or decode")
    key: str = Field(..., description="Alphabetic key")

class AffineRequest(BaseModel):
    text: str = Field(..., description="Text to encode or decode")
    a: int = Field(..., description="Multiplier (must be coprime with 26)")
    b: int = Field(..., description="Shift (0-25)")

class ColumnarRequest(BaseModel):
    text: str = Field(..., description="Text to encode or decode")
    key: str = Field(..., description="Columnar transposition key")

class CipherResponse(BaseModel):
    result: str = Field(..., description="Resulting ciphertext or plaintext")

# ─── Caesar Routes ───

@router.post("/caesar/encode", response_model=CipherResponse)
def encode_caesar(req: CaesarRequest):
    return {"result": caesar.encode(req.text, req.shift)}

@router.post("/caesar/decode", response_model=CipherResponse)
def decode_caesar(req: CaesarRequest):
    return {"result": caesar.decode(req.text, req.shift)}

# ─── Vigenère Routes ───

@router.post("/vigenere/encode", response_model=CipherResponse)
def encode_vigenere(req: VigenereRequest):
    try:
        return {"result": vigenere.encode(req.text, req.key)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/vigenere/decode", response_model=CipherResponse)
def decode_vigenere(req: VigenereRequest):
    try:
        return {"result": vigenere.decode(req.text, req.key)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# ─── Substitution Routes ───

@router.post("/substitution/encode", response_model=CipherResponse)
def encode_substitution(req: SubstitutionRequest):
    try:
        return {"result": substitution.encode(req.text, req.key)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/substitution/decode", response_model=CipherResponse)
def decode_substitution(req: SubstitutionRequest):
    try:
        return {"result": substitution.decode(req.text, req.key)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# ─── Playfair Routes ───

@router.post("/playfair/encode", response_model=CipherResponse)
def encode_playfair(req: PlayfairRequest):
    try:
        return {"result": playfair.encode(req.text, req.key)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/playfair/decode", response_model=CipherResponse)
def decode_playfair(req: PlayfairRequest):
    try:
        return {"result": playfair.decode(req.text, req.key)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# ─── Rail Fence Routes ───

@router.post("/railfence/encode", response_model=CipherResponse)
def encode_railfence(req: RailFenceRequest):
    try:
        return {"result": rail_fence.encode(req.text, req.rails)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/railfence/decode", response_model=CipherResponse)
def decode_railfence(req: RailFenceRequest):
    try:
        return {"result": rail_fence.decode(req.text, req.rails)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# ─── Beaufort Routes ───

@router.post("/beaufort/encode", response_model=CipherResponse)
def encode_beaufort(req: BeaufortRequest):
    try:
        return {"result": beaufort.encode(req.text, req.key)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/beaufort/decode", response_model=CipherResponse)
def decode_beaufort(req: BeaufortRequest):
    try:
        return {"result": beaufort.decode(req.text, req.key)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# ─── Affine Routes ───

@router.post("/affine/encode", response_model=CipherResponse)
def encode_affine(req: AffineRequest):
    try:
        return {"result": affine.encode(req.text, req.a, req.b)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/affine/decode", response_model=CipherResponse)
def decode_affine(req: AffineRequest):
    try:
        return {"result": affine.decode(req.text, req.a, req.b)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# ─── Columnar Routes ───

@router.post("/columnar/encode", response_model=CipherResponse)
def encode_columnar(req: ColumnarRequest):
    try:
        return {"result": columnar.encode(req.text, req.key)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/columnar/decode", response_model=CipherResponse)
def decode_columnar(req: ColumnarRequest):
    try:
        return {"result": columnar.decode(req.text, req.key)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
