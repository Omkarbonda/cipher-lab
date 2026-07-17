from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.vault import crypto

router = APIRouter(prefix="/api/vault", tags=["Vault"])

# ─── Pydantic Schemas ───

class EncryptRequest(BaseModel):
    plaintext: str = Field(..., min_length=1, description="Plaintext message to encrypt")
    passphrase: str = Field(..., min_length=1, description="Passphrase for key derivation")

class EncryptResponse(BaseModel):
    ciphertext: str = Field(..., description="Base64-encoded encrypted payload")
    algorithm: str = Field("AES-256-GCM + PBKDF2-HMAC-SHA256")

class DecryptRequest(BaseModel):
    ciphertext: str = Field(..., description="Base64-encoded encrypted payload from /encrypt")
    passphrase: str = Field(..., min_length=1, description="Passphrase used during encryption")

class DecryptResponse(BaseModel):
    plaintext: str = Field(..., description="Decrypted plaintext")
    algorithm: str = Field("AES-256-GCM + PBKDF2-HMAC-SHA256")

class EntropyRequest(BaseModel):
    passphrase: str = Field(..., description="Passphrase to evaluate")

class EntropyResponse(BaseModel):
    length: int
    charset_size: int
    entropy_bits: float
    strength: str

# ─── Endpoints ───

@router.post("/encrypt", response_model=EncryptResponse)
def vault_encrypt(req: EncryptRequest):
    try:
        ciphertext = crypto.encrypt(req.plaintext, req.passphrase)
        return {"ciphertext": ciphertext, "algorithm": "AES-256-GCM + PBKDF2-HMAC-SHA256"}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/decrypt", response_model=DecryptResponse)
def vault_decrypt(req: DecryptRequest):
    try:
        plaintext = crypto.decrypt(req.ciphertext, req.passphrase)
        return {"plaintext": plaintext, "algorithm": "AES-256-GCM + PBKDF2-HMAC-SHA256"}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/entropy", response_model=EntropyResponse)
def vault_entropy(req: EntropyRequest):
    return crypto.estimate_entropy(req.passphrase)
