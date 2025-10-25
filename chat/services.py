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


def get_completion(
    prompt: str,
    system: Optional[str] = None,
    model: str = "gpt-4o-mini",
    temperature: float = 0.3,
    max_tokens: int = 800
) -> Dict[str, Any]:
    """
    Devuelve un dict con:
      - ok: bool
      - text: str  (respuesta del modelo)
      - json: Any  (si el modelo devolvió JSON válido)
      - error: str (mensaje de error si ok=False)
    """
    try:
        client = _get_client()

        system_message = system or (
            "Eres un asistente que sugiere rutinas de estudio o ejercicio fáciles de entender. "
            "Si puedes, devuelve JSON válido bajo la clave 'slots'."
        )

        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=20,
        )

        text = (resp.choices[0].message.content or "").strip()
        parsed = None

        if text:
            try:
                # Busca un bloque JSON dentro del texto
                start = text.find("{")
                end = text.rfind("}")
                if start != -1 and end != -1 and end > start:
                    parsed = json.loads(text[start:end + 1])
            except Exception:
                parsed = None

        return {"ok": True, "text": text, "json": parsed, "error": None}

    except (APIConnectionError, APIStatusError) as e:
        return {"ok": False, "text": "", "json": None, "error": f"Problema de conexión con OpenAI: {e}"}
    except RateLimitError:
        return {"ok": False, "text": "", "json": None, "error": "Límite de uso de OpenAI alcanzado. Intenta de nuevo más tarde."}
    except BadRequestError as e:
        return {"ok": False, "text": "", "json": None, "error": f"Solicitud inválida a OpenAI: {e}"}
    except Exception as e:
        return {"ok": False, "text": "", "json": None, "error": f"Error inesperado: {e}"}
