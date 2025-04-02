import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..schemas import PromptRequest, PromptResponse
router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)



@router.post("/generate", response_model=PromptResponse)
async def generate_response(req: PromptRequest):
    try:
        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                "http://localhost:11434/api/generate",
                json={"model": "tinyllama", "prompt": req.prompt, "stream": True},
            ) as res:
                res.raise_for_status()
                full_response = ""
                async for line in res.aiter_lines():
                    if line.strip():
                        chunk = httpx.Response(200, content=line).json()
                        full_response += chunk.get("response", "")
        return {"response": full_response.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
