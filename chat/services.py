# chat/services.py
import os
import json
from typing import Dict, Any, Optional
from openai import OpenAI, APIConnectionError, BadRequestError, RateLimitError, APIStatusError

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

_client: Optional[OpenAI] = None
def _get_client() -> OpenAI:
    global _client
    if _client is None:
        if not OPENAI_API_KEY:
            raise RuntimeError("Falta OPENAI_API_KEY. Define la variable en tu .env.")
        _client = OpenAI(api_key=OPENAI_API_KEY)
    return _client

def get_completion(prompt: str, model: str = "gpt-4o-mini", temperature: float = 0.3, max_tokens: int = 800) -> Dict[str, Any]:
    """
    Devuelve un dict con:
      - ok: bool
      - text: str  (respuesta plana)
      - json: Any  (si el modelo devolvió JSON válido; None si no)
      - error: str (mensaje de error si ok=False)
    """
    try:
        client = _get_client()
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Eres un asistente que sugiere rutinas de estudio fáciles de entender. Si puedes, devuelve JSON válido bajo la clave 'slots'."},
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=20,  # segundos
        )
        text = (resp.choices[0].message.content or "").strip()
        parsed = None
        if text:
            # Intento de extraer JSON si viene en un bloque
            try:
                # Busca el primer bloque {...}
                start = text.find("{")
                end = text.rfind("}")
                if start != -1 and end != -1 and end > start:
                    parsed = json.loads(text[start:end+1])
            except Exception:
                parsed = None

        return {"ok": True, "text": text, "json": parsed, "error": None}

    except (APIConnectionError, APIStatusError) as e:
        return {"ok": False, "text": "", "json": None, "error": f"Problema de conexión con OpenAI: {e}"}
    except RateLimitError:
        return {"ok": False, "text": "", "json": None, "error": "Límite de uso de OpenAI alcanzado. Intenta de nuevo en un momento."}
    except BadRequestError as e:
        return {"ok": False, "text": "", "json": None, "error": f"Solicitud inválida a OpenAI: {e}"}
    except Exception as e:
        return {"ok": False, "text": "", "json": None, "error": f"Error inesperado: {e}"}
