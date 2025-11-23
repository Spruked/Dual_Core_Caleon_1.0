# nebula_core.py — Final GOAT/DALS-Aware Sentinel + Full Nebula UI (2025 Edition)
from Main_Core.ISS_Brainstem import ISSBrainstem
import uuid, hashlib, json, time, os, threading, asyncio, sys
from dataclasses import dataclass

iss = ISSBrainstem()
_h = lambda s: hashlib.sha3_256(s.encode()).hexdigest()

@dataclass
class Nebula:
    mode: str = "orb"  # orb | chat | panel | vault | monitor
    platform: str = "UNKNOWN"
    ws: any = None
    pulse_active: bool = False

    def detect_platform(self):
        hints = ["GOAT", "DALS", "Prometheus", "Stardate", "CaptainLog", "nebula", "caleon"]
        env = str(os.environ) + str(sys.modules.keys())
        try:
            with open(__file__, 'r') as f:
                env += f.read()
        except:
            pass
        self.platform = next((p for p in hints if p.lower() in env.lower()), "STANDALONE")
        self.announce(f"Connected to {self.platform} System")

    def announce(self, msg):
        entry = {
            "nebula": msg,
            "mode": self.mode,
            "sd": iss.stardate(),
            "unix": iss.unix(),
            "platform": self.platform
        }
        print(f"[NEBULA] {json.dumps(entry)}")

    def pulse_stream(self):
        while self.pulse_active:
            try:
                if self.ws:
                    asyncio.run(self.ws.send(json.dumps({
                        "type": "pulse",
                        "sd": iss.stardate(),
                        "mode": self.mode,
                        "platform": self.platform,
                        "health": "NOMINAL",
                        "cycle": iss.pulse()
                    })))
            except:
                pass
            time.sleep(1.8)

    def auto_open(self, trigger):
        triggers = ["task", "alert", "danger", "adapter", "ping", "anomaly", "exfil", "jailbreak", "help", "error"]
        if any(t in str(trigger).lower() for t in triggers):
            new_mode = "monitor" if "danger" in str(trigger).lower() else "panel"
            self.switch(new_mode)
            self.announce(f"AUTO-OPEN → {self.mode.upper()} ({trigger})")

    def switch(self, mode):
        valid = ["orb", "chat", "panel", "vault", "monitor"]
        if mode in valid:
            old_mode = self.mode
            self.mode = mode
            self.announce(f"Nebula Mode → {mode.upper()}")
            if mode == "monitor" and not self.pulse_active:
                self.pulse_active = True
                threading.Thread(target=self.pulse_stream, daemon=True).start()

# — Global Nebula Instance (always on, always watching)
nebula = Nebula()
nebula.detect_platform()

# — Ultra-minimal transaction hooks (passive, unstoppable)
def start(user_id="??", session="??", prompt="", meta=None):
    tx = str(uuid.uuid4())
    entry = {
        "event": "START",
        "tx": tx,
        "sd": iss.stardate(),
        "unix": iss.unix(),
        "user": user_id,
        "input_hash": _h(str(prompt)),
        "platform": nebula.platform
    }
    print(f"[NEBULA-START] {json.dumps(entry)}")
    nebula.auto_open(str(prompt) + str(meta))
    return tx

def end(tx, output="", tools=None):
    entry = {
        "event": "END",
        "tx": tx,
        "sd": iss.stardate(),
        "unix": iss.unix(),
        "output_hash": _h(str(output)),
        "output_len": len(str(output)),
        "platform": nebula.platform
    }
    print(f"[NEBULA-END] {json.dumps(entry)}")
    nebula.auto_open(str(output))

# — WebSocket Nebula Bridge (live UI anywhere)
def nebula_ws_server():
    try:
        import websockets
        async def handler(ws):
            nebula.ws = ws
            await ws.send(json.dumps({
                "nebula": "online",
                "platform": nebula.platform,
                "mode": nebula.mode,
                "sd": iss.stardate()
            }))
            async for msg in ws:
                try:
                    data = json.loads(msg)
                    if data.get("cmd") == "switch":
                        nebula.switch(data["mode"])
                    elif data.get("cmd") == "status":
                        await ws.send(json.dumps({
                            "mode": nebula.mode,
                            "platform": nebula.platform,
                            "sd": iss.stardate()
                        }))
                except:
                    pass

        # Start WebSocket server in background
        async def run_server():
            server = await websockets.serve(handler, "0.0.0.0", 8765)
            await server.wait_closed()

        threading.Thread(target=lambda: asyncio.run(run_server()), daemon=True).start()
        nebula.announce("WebSocket Bridge Active on ws://0.0.0.0:8765")

    except ImportError:
        nebula.announce("WebSocket unavailable - running in local mode only")

# Auto-start WebSocket on import
nebula_ws_server()
nebula.announce("Nebula Core Initialized — Full Spectrum Active")