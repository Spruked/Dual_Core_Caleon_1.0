# ollama_engine.py — Local LLM Connector for Dual Core Caleon
import json
import asyncio
import aiohttp
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger("ollama_engine")

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL_NAME = "phi3:mini"

class OllamaEngine:
    """Local LLM reasoning engine for Caleon cognitive processes"""

    def __init__(self):
        self.model = MODEL_NAME
        self.timeout = 60  # seconds - increased for slower systems

    async def query(self, prompt: str, system: str = None, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Query the local Ollama model with enhanced context"""
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "num_predict": 256  # Reasonable response length
                }
            }

            if system:
                payload["system"] = system

            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                async with session.post(OLLAMA_URL, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        result = {
                            "response": data.get("response", "").strip(),
                            "model": data.get("model", self.model),
                            "success": True,
                            "performance": {
                                "total_duration": data.get("total_duration", 0),
                                "eval_count": data.get("eval_count", 0),
                                "eval_duration": data.get("eval_duration", 0)
                            }
                        }

                        # Add ISS timing if available
                        try:
                            from .ISS_Brainstem import ISS
                            result["iss_pulse"] = ISS.pulse()
                            result["iss_stardate"] = ISS.stardate()
                        except ImportError:
                            pass

                        return result
                    else:
                        error_text = await response.text()
                        logger.error(f"Ollama API error: {response.status} - {error_text}")
                        return {
                            "response": "",
                            "success": False,
                            "error": f"HTTP {response.status}: {error_text}"
                        }

        except asyncio.TimeoutError:
            logger.error("Ollama query timeout")
            return {
                "response": "",
                "success": False,
                "error": "Query timeout"
            }
        except Exception as e:
            logger.error(f"Ollama query failed: {e}")
            return {
                "response": "",
                "success": False,
                "error": str(e)
            }

    def health_check(self) -> bool:
        """Check if Ollama service is available"""
        try:
            import requests
            response = requests.get("http://127.0.0.1:11434/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False

    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model"""
        try:
            import requests
            response = requests.get("http://127.0.0.1:11434/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                for model in data.get("models", []):
                    if model["name"] == self.model:
                        return model
            return {}
        except:
            return {}

# Global instance for use throughout Caleon
ollama_engine = OllamaEngine()