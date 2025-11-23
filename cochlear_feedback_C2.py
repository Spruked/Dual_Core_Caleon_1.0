# ================================================================
#   C2 FEEDBACK COCHLEAR PROCESSOR  (Core-Resident)
#   Module Name: cochlear_feedback_C2.py
#   Author: Bryan Anthony Spruk / Pro Prime Series AI
# ================================================================

import asyncio
import time
import os
import yaml
import numpy as np
from dataclasses import dataclass
from typing import AsyncGenerator, Optional, List
from pydantic import BaseModel

# ---------------------------------------------------------
#  Core Logging (ISS-Core if available)
# ---------------------------------------------------------
try:
    from core.iss_core_logger import iss_core_log
    logger = iss_core_log("cochlear_feedback_C2")
except:
    import logging
    logger = logging.getLogger("cochlear_feedback_C2")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        h = logging.StreamHandler()
        h.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        logger.addHandler(h)

# ---------------------------------------------------------
#  Core Utilities (Genesis-safe fallbacks included)
# ---------------------------------------------------------
try:
    from core.utils.embeddings import embed
    from core.utils.metrics import cosine_sim, lexical_similarity, prosodic_rms
except:

    def embed(text):
        # deterministic fallback embedding
        np.random.seed(abs(hash(text)) % (2**32))
        return np.random.normal(0, 1, 384)

    def cosine_sim(a, b):
        return float(np.dot(a, b))

    def lexical_similarity(ref, hyp):
        from Levenshtein import distance
        return 1.0 - (distance(ref.lower(), hyp.lower()) / max(len(ref), len(hyp), 1))

    def prosodic_rms(audio):
        return 0.0


# =========================================================
#   SHARED MODELS SENT TO THE EXTERIOR HARMONIZER
# =========================================================
class DriftDetail(BaseModel):
    transcript: str
    expected_text: str
    verdict_vector: List[float]
    cosine: float
    lexical: float
    prosodic_rms: Optional[float] = None


class HarmonizerPing(BaseModel):
    type: str = "PING_FROM_C2"
    utterance_id: str
    drift: DriftDetail
    timestamp: float


# =========================================================
#     CORE CLASS: Feedback Cochlear Cortex C2 (Core-Resident)
# =========================================================
@dataclass
class CochlearFeedbackC2:
    """
    C2 Feedback Cochlear Cortex
    -------------------------------------------
    • Lives **inside** Core.
    • Monitors Caleon's OWN spoken output.
    • Computes drift across: embeddings, lexical, prosody.
    • Sends drift signals OUTWARD to the External Harmonizer.
    • Never mutates core — Genesis-safe.
    """

    config: dict
    outward_queue: asyncio.Queue
    _last_ping_ts: float = 0.0
    _ping_count: int = 0

    # ----------------------------------------------------
    #  Genesis-safe initializer
    # ----------------------------------------------------
    @classmethod
    async def create(cls, outward_queue: asyncio.Queue):

        search_paths = [
            "core/config/c2_feedback.yaml",
            os.path.join(os.getcwd(), "core", "config", "c2_feedback.yaml"),
        ]

        cfg = None
        for path in search_paths:
            try:
                with open(path, "r") as f:
                    cfg = yaml.safe_load(f)
                    logger.info(f"[C2] Loaded config: {path}")
                    break
            except:
                pass

        if cfg is None:
            logger.warning("[C2] No config found; using Genesis fallback defaults")
            cfg = {
                "monitor": {
                    "enabled": True,
                    "similarity_threshold": 0.93,
                    "lexical_threshold": 0.88,
                    "debounce_seconds": 0.8,
                    "max_pings_per_utterance": 3
                },
                "stt": {
                    "chunk_seconds": 1.0,
                    "overlap_seconds": 0.2
                }
            }

        return cls(config=cfg, outward_queue=outward_queue)

    # ----------------------------------------------------
    #  Tiny Genesis-safe STT placeholder
    # ----------------------------------------------------
    async def _transcribe_stream(self, audio_gen: AsyncGenerator[bytes, None]) -> str:
        transcript = []
        async for chunk in audio_gen:
            text = await mock_stt(chunk)
            if text.strip():
                transcript.append(text)
        return " ".join(transcript)

    # ----------------------------------------------------
    #  Main Drift Monitoring Function
    # ----------------------------------------------------
    async def monitor(
        self,
        audio_stream: AsyncGenerator[bytes, None],
        expected_text: str,
        verdict_vector: np.ndarray,
        utterance_id: str
    ):
        if not self.config["monitor"]["enabled"]:
            return

        transcript = await self._transcribe_stream(audio_stream)
        if not transcript.strip():
            return

        cos = cosine_sim(embed(transcript), verdict_vector)
        lex = lexical_similarity(expected_text, transcript)

        drift = DriftDetail(
            transcript=transcript,
            expected_text=expected_text,
            verdict_vector=verdict_vector.tolist(),
            cosine=cos,
            lexical=lex
        )

        now = time.time()
        cfg = self.config["monitor"]

        if cos < cfg["similarity_threshold"] or lex < cfg["lexical_threshold"]:

            # Debounce protection
            if (
                now - self._last_ping_ts > cfg["debounce_seconds"]
                and self._ping_count < cfg["max_pings_per_utterance"]
            ):
                ping = HarmonizerPing(
                    utterance_id=utterance_id,
                    drift=drift,
                    timestamp=now,
                )

                # Bounded outward queue
                if self.outward_queue.qsize() >= 100:
                    try:
                        dropped = self.outward_queue.get_nowait()
                        logger.warning(f"[C2] Dropping old ping: {dropped.utterance_id}")
                    except:
                        pass

                await self.outward_queue.put(ping)

                logger.info(
                    f"[C2] Drift detected for {utterance_id} "
                    f"(cos={cos:.3f}, lex={lex:.3f}) — sent outward"
                )

                self._last_ping_ts = now
                self._ping_count += 1

        asyncio.create_task(self._reset_counter_after(5.0))

    async def _reset_counter_after(self, delay: float):
        await asyncio.sleep(delay)
        self._ping_count = 0


# ---------------------------------------------------------
#   Genesis-safe STT placeholder
# ---------------------------------------------------------
async def mock_stt(chunk: bytes) -> str:
    await asyncio.sleep(0.01)
    return "speech output placeholder"
