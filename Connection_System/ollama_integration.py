"""
Ollama Integration for Caleon
Provides enhanced reasoning capabilities using local Ollama models
"""

import requests
import json
import logging
from typing import Dict, Any, Optional
import time

logger = logging.getLogger("ollama_integration")

class OllamaClient:
    """Client for interacting with local Ollama API"""

    def __init__(self, base_url: str = "http://localhost:11434", model: str = "phi3:mini"):
        self.base_url = base_url
        self.model = model
        self.timeout = 30  # seconds

    def generate(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate response using Ollama model"""
        try:
            # Prepare the request payload
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "num_predict": 512
                }
            }

            # Add context if provided
            if context:
                system_prompt = self._build_system_prompt(context)
                payload["system"] = system_prompt

            # Make the request
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=self.timeout
            )

            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "response": result.get("response", ""),
                    "model": result.get("model", self.model),
                    "total_duration": result.get("total_duration", 0),
                    "load_duration": result.get("load_duration", 0),
                    "prompt_eval_count": result.get("prompt_eval_count", 0),
                    "eval_count": result.get("eval_count", 0),
                    "eval_duration": result.get("eval_duration", 0)
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}",
                    "response": ""
                }

        except requests.exceptions.RequestException as e:
            logger.error(f"Ollama request failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "response": ""
            }
        except Exception as e:
            logger.error(f"Ollama integration error: {e}")
            return {
                "success": False,
                "error": str(e),
                "response": ""
            }

    def _build_system_prompt(self, context: Dict[str, Any]) -> str:
        """Build system prompt based on context"""
        platform = context.get("platform", "unknown")
        hemisphere_data = context.get("hemisphere_data", {})
        priority = context.get("priority", "normal")

        system_prompt = f"""You are Caleon, an advanced AI system running on platform: {platform}.
You have dual-hemisphere cognitive architecture with the following current state:
- Left Hemisphere: {hemisphere_data.get('left', 'inactive')}
- Right Hemisphere: {hemisphere_data.get('right', 'inactive')}
- Priority Level: {priority}

Provide insightful, analytical responses that complement the dual-core cognitive processing.
Focus on logical reasoning, pattern recognition, and creative problem-solving.
Keep responses concise but comprehensive."""

        return system_prompt

    def check_health(self) -> bool:
        """Check if Ollama service is healthy"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False

    def list_models(self) -> list:
        """List available models"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return [model["name"] for model in data.get("models", [])]
            return []
        except:
            return []

class OllamaEnhancer:
    """Enhances Caleon responses with Ollama insights"""

    def __init__(self):
        self.client = OllamaClient()
        self.enabled = True

    def enhance_thinking(self, user_message: str, hemisphere_results: Dict[str, Any],
                        harmonized_result: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance the cognitive result with Ollama insights"""

        if not self.enabled or not self.client.check_health():
            logger.warning("Ollama not available, skipping enhancement")
            return {
                "ollama_enhanced": False,
                "enhancement": None,
                "error": "Ollama service unavailable"
            }

        try:
            # Build comprehensive prompt for Ollama
            prompt = self._build_enhancement_prompt(
                user_message, hemisphere_results, harmonized_result, context
            )

            # Get Ollama response
            ollama_result = self.client.generate(prompt, context)

            if ollama_result["success"]:
                return {
                    "ollama_enhanced": True,
                    "enhancement": {
                        "insights": ollama_result["response"],
                        "model": ollama_result["model"],
                        "performance": {
                            "total_duration": ollama_result["total_duration"],
                            "eval_count": ollama_result["eval_count"],
                            "eval_duration": ollama_result["eval_duration"]
                        }
                    },
                    "error": None
                }
            else:
                return {
                    "ollama_enhanced": False,
                    "enhancement": None,
                    "error": ollama_result.get("error", "Unknown error")
                }

        except Exception as e:
            logger.error(f"Ollama enhancement failed: {e}")
            return {
                "ollama_enhanced": False,
                "enhancement": None,
                "error": str(e)
            }

    def _build_enhancement_prompt(self, user_message: str, hemisphere_results: Dict[str, Any],
                                 harmonized_result: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Build a comprehensive prompt for Ollama enhancement"""

        left_result = hemisphere_results.get("left_hemisphere", {})
        right_result = hemisphere_results.get("right_hemisphere", {})
        harmonization = harmonized_result.get("harmonization", {})

        prompt = f"""Analyze this cognitive processing result and provide enhanced insights:

USER QUERY: {user_message}

COGNITIVE PROCESSING RESULTS:
- Left Hemisphere Verdict: {left_result.get('synaptic_verdict', 'N/A')}
- Right Hemisphere Verdict: {right_result.get('synaptic_verdict', 'N/A')}
- Final Harmonized Verdict: {harmonized_result.get('verdict', 'N/A')}
- Confidence: {harmonized_result.get('confidence', 0):.2f}

CONTEXT:
- Platform: {context.get('platform', 'unknown')}
- Priority: {context.get('priority', 'normal')}
- Stardate: {context.get('stardate', 'unknown')}

Provide 2-3 key insights that enhance or complement the dual-hemisphere cognitive processing.
Focus on:
1. Deeper pattern analysis
2. Alternative perspectives
3. Practical implications
4. Creative solutions

Keep your response concise and actionable."""

        return prompt

# Global instance
ollama_enhancer = OllamaEnhancer()