# ISS_Brainstem.py
# Caleon Internal Time & Pulse Engine
# Author: Bryan A. Spruk

import time
import hashlib
import threading

class ISSBrainstem:
    """
    Ultra-minimal internal time oracle for Caleon.
    Provides:
        - canonical stardates
        - pulse timestamps
        - cycle counters
        - drift detection
        - cryptographic digests for state anchoring
    """

    def __init__(self):
        self._cycle = 0
        self._lock = threading.Lock()
        self._last_ts = time.time()

    # -----------------------------------------------------------
    # Basic Time Sources
    # -----------------------------------------------------------
    def unix(self) -> float:
        """Return high-precision unix time."""
        return time.time()

    def pulse(self) -> str:
        """
        Canonical machine pulse.
        Format: PULSE-<UNIX>.<CYCLE>
        """
        with self._lock:
            self._cycle += 1
            ts = self.unix()
            return f"PULSE-{ts:.6f}.{self._cycle}"

    def stardate(self) -> str:
        """
        Human-readable stardate.
        Example: SD-2025.326.45219
        """
        now = time.time()
        year = time.gmtime(now).tm_year
        day_of_year = time.gmtime(now).tm_yday
        fractional = int((now % 86400) * 100)  # hundredths of seconds

        return f"SD-{year}.{day_of_year}.{fractional}"

    # -----------------------------------------------------------
    # Drift Detection
    # -----------------------------------------------------------
    def detect_drift(self, threshold_seconds: float = 0.250) -> bool:
        """
        Detect abnormal jumps forward/backward in time.
        Returns True if drift is detected.
        """
        now = time.time()
        delta = abs(now - self._last_ts)

        self._last_ts = now
        return delta > threshold_seconds

    # -----------------------------------------------------------
    # State Anchoring
    # -----------------------------------------------------------
    def digest(self, data: str) -> str:
        """Return SHA-256 digest of any string."""
        return hashlib.sha256(data.encode()).hexdigest()

    def anchor_state(self, *fields: str) -> str:
        """
        Return a stable hash anchor for a set of fields
        (useful for sealing reasoning cycles).
        """
        joined = "|".join(fields)
        return hashlib.sha256(joined.encode()).hexdigest()

# -----------------------------------------------------------
# Singleton Instance for Easy Import
# -----------------------------------------------------------
ISS = ISSBrainstem()
