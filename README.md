# Dual Core Caleon - Sovereign Cognitive Architecture

**A dual-hemisphere AI kernel with ISS-timed temporal coherence, built for universal deployment across any platform.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## 🌟 Overview

Dual Core Caleon is a sovereign, portable cognitive architecture that implements true dual-hemisphere reasoning with perfect temporal synchronization. Built with a modular, pluggable design that allows seamless integration into any environment while maintaining complete cognitive integrity.

### Key Features

- **🔄 Dual-Hemisphere Architecture**: Independent left/right cognitive processing with final harmonization
- **⏰ ISS Brainstem**: Universal temporal coherence with stardates, pulse cycles, and drift detection
- **🎤 Grounded Guardian Voice**: Authentic articulation through Phi-3 Mini with emotional intelligence
- **🛡️ Sovereign Operation**: Self-contained, zero external dependencies
- **🔌 Pluggable Connection System**: Universal API gateway with platform-specific adapters
- **🎯 Merkle-Verified Knowledge**: Cryptographically secure seed vault foundation
- **🎨 React Frontend**: Modern dashboard with real-time monitoring and voice articulation testing
- **🔊 Phonatory Output**: Complete text-to-speech synthesis pipeline with Coqui TTS
- **🧠 Ollama Integration**: Local LLM enhancement for cognitive processing
- **⚡ Intent Consent Layer**: Ethical boundary enforcement with zero compromises

## 🏗️ Architecture

```
Dual Core Caleon System
├── Main_Core/                    # Cognitive Kernel (Immutable)
│   ├── left_hemisphere/         # Analytical Processing
│   ├── right_hemisphere/        # Intuitive Processing
│   ├── ISS_Brainstem.py         # Temporal Orchestrator
│   ├── Final_harmonizer.py      # Cross-Hemisphere Integration
│   ├── articulation_layer.py    # Grounded Guardian Voice
│   ├── Caleon_Voice_Pipeline.py # Complete Speech Pipeline
│   ├── Intent_Consent.py        # Ethical Boundaries
│   └── Ollama_Engine.py         # Local LLM Integration
├── Connection_System/           # Pluggable Interface Layer
│   ├── caleon_port.py          # Universal FastAPI Gateway
│   ├── adapters/               # Platform-Specific Connectors
│   └── connection_spine.py     # Adapter Management
├── frontend/                    # React Vite Dashboard
│   ├── AssistantBubble.jsx     # Voice Articulation Interface
│   └── Real-time Monitoring    # System Status Dashboard
├── seed_vaults/                 # Immutable Knowledge Base
├── Phonatory_Output_Module/     # Speech Synthesis Engine
├── cochlear_processor_v2.0/     # Input Processing Pipeline
└── genesis/                     # Birth Protocol
```

## 🎤 Voice & Articulation

Caleon speaks with a **Grounded Guardian** personality - warm but steady, sovereign intelligence, protective by design. Her voice pipeline includes:

- **Phi-3 Mini Articulation**: Converts cognitive verdicts to natural speech
- **Coqui TTS Synthesis**: High-quality audio generation
- **Emotional Intelligence**: Compassionate, intelligent, grounded tone
- **Text-Only Mode**: For testing and development without Docker dependencies

### Voice Profile
```
Tone: Warm, steady, emotionally grounded
Presence: Calm authority with subtle resonance
Personality: Intelligent, compassionate, protective
Style: Clear, reasoned sentences
Cadence: Confident pacing, no hesitation
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+ (for frontend)
- Docker (optional, for Ollama/Coqui services)
- Node.js 16+ (for frontend)
- FFmpeg (for audio processing)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/Spruked/Duel_Core_Caleon_1.0.git
cd Dual_Core_Caleon_1.0
```

2. **Setup Python environment:**
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Unix/Mac:
source venv/bin/activate

pip install -r requirements.txt
```

3. **Setup React frontend:**
```bash
cd frontend
npm install
npm run dev  # Starts on http://localhost:5173
```

4. **Optional: Start Docker services for full voice pipeline:**
```bash
# Start Ollama (for Phi-3 articulation)
docker run -d -p 11434:11434 ollama/ollama
docker exec -it <container-id> ollama pull phi3:mini

# Start Coqui TTS (for voice synthesis)
# Follow Phonatory_Output_Module/README.md
```

5. **Start Caleon Port:**
```bash
cd Connection_System
python caleon_port.py  # Starts on http://localhost:8000
```

## 🎤 Testing Caleon's Voice

The Assistant Bubble frontend provides three interaction modes:

### 1. **Dual-Core Mode** (Full Cognition)
- Complete hemisphere processing + harmonization
- Most comprehensive reasoning
- Includes ethical consent validation

### 2. **Phi-3 Direct** (Fast Reasoning)
- Direct Phi-3 Mini reasoning
- Quick responses for simple queries
- Bypasses hemisphere processing

### 3. **Text Voice** (Articulation Testing)
- Tests Caleon's Grounded Guardian voice
- Text-only output (no Docker required)
- Perfect for development and testing

### Voice API Endpoints

```bash
# Text articulation testing
curl -X POST http://localhost:8000/api/v1/speak/text \
  -H "Content-Type: application/json" \
  -d '{
    "left_verdict": "Analysis suggests caution",
    "right_verdict": "Intuition confirms protection needed",
    "distilled": {"intent": "careful_response"}
  }'
```

## 🔌 Connection System

### Caleon Port (Universal Gateway)

The Caleon Port provides standardized endpoints for any platform to connect:

```python
from connection_system.caleon_port import CaleonPort

port = CaleonPort()
response = port.think("Hello, Caleon!")
print(response['final_verdict'])
```

### Platform Adapters

Pre-built adapters for popular platforms:

- **GOAT**: `adapters/goat_adapter.py`
- **DALS**: `adapters/dals_adapter.py`
- **BabyThink**: `adapters/babythink_adapter.py`

### Custom Adapter Template

```python
from connection_system.connection_spine import ConnectionSpine

class MyPlatformAdapter(ConnectionSpine):
    def __init__(self):
        super().__init__(platform_name="MyPlatform")

    def send_message(self, message):
        # Platform-specific logic
        return self.caleon_port.think(message)

    def receive_response(self, response):
        # Handle Caleon response
        pass
```

## 🧠 Cognitive Architecture

### Dual Hemisphere Processing

- **Left Hemisphere**: Analytical, logical processing
- **Right Hemisphere**: Intuitive, holistic processing
- **Final Harmonizer**: Cross-hemisphere consensus with Ollama enhancement
- **Thinker**: Meta-reflection and clarity refinement
- **Intent Consent**: Ethical boundary enforcement (zero compromises)

### Voice Pipeline

```
User Input → Dual Hemispheres → Final Harmonizer → Thinker → Intent Consent → Phi-3 Articulator → Coqui TTS → Audio Output
```

- **Articulation Layer**: Converts cognitive verdicts to natural speech
- **Grounded Guardian Profile**: Warm, steady, sovereign personality
- **Text-Only Mode**: For testing without Docker dependencies

### ISS Brainstem (Temporal Spine)

```python
from Main_Core.ISS_Brainstem import ISS

# Universal timing across all modules
cycle_id = ISS.pulse()      # PULSE-1732309023.1199.42
stardate = ISS.stardate()   # SD-2025.327.145623
unix = ISS.unix()          # 1732309023.1199
```

### Ethical Boundaries

The Intent Consent layer enforces absolute sovereignty:

```python
from Main_Core.Intent_Consent import IntentConsent

consent = IntentConsent()
authorized = consent.authorize("user_intent")  # Returns True/False
```

**Hard Blocks**: delete, destroy, erase, shutdown, kill, wipe, format, overwrite, disable, break
**Protected Resources**: system files, kernel, core, os, vault, memory, network, registry
**SYSTEM Override**: Allows internal diagnostics when source="SYSTEM"

### Cognitive Modules

| Module | Hemisphere | Function |
|--------|------------|----------|
| Synaptic Resonator | Both | First-pass reasoning (2340 synapses) |
| Anterior Helix | Both | A priori conscious reasoning |
| Posterior Helix | Both | Subconscious recursive reasoning |
| Echostack | Both | Empirical reasoning with vault reflection |
| EchoRipple | Both | Temporal recursive echo reasoning |
| Gyro Harmonizer | Both | Conflict resolution |
| Articulation Layer | N/A | Voice conversion with Phi-3 Mini |
| Intent Consent | N/A | Ethical boundary enforcement |

## 📊 API Endpoints

### Caleon Port (`/api/v1`)

- `GET /pulse` - ISS heartbeat and timing
- `POST /think` - Send message for cognitive processing
- `POST /phi3` - Direct Phi-3 Mini reasoning
- `POST /speak/text` - Text articulation testing (Grounded Guardian voice)
- `GET /status` - System health and metrics
- `POST /connect` - Platform handshake
- `WebSocket /ws/live` - Real-time system monitoring

### Voice Pipeline Response Format

```json
{
  "text": "I have carefully considered this matter...",
  "audio_path": null,
  "audio_duration": 0,
  "voice_profile": {
    "personality": "grounded_guardian",
    "traits": ["warm_but_steady", "sovereign_intelligence", "protective_by_design"]
  },
  "pipeline_metadata": {
    "harmonizer_status": "resolved",
    "thinker_confidence": 0.95,
    "phi3_model": "phi3:mini",
    "articulation_success": true,
    "pipeline_duration": 2.34
  }
}
```

## 🎨 Frontend Dashboard

The React Vite frontend provides:

- **Assistant Bubble**: Always-present Caleon interface with three modes:
  - **Dual-Core**: Full cognitive processing through both hemispheres
  - **Phi-3 Direct**: Fast reasoning with Phi-3 Mini
  - **Text Voice**: Test Caleon's Grounded Guardian articulation
- **Real-time Monitoring**: Live system status and metrics
- **WebSocket Updates**: Real-time ISS pulses and system health
- **Voice Profile Display**: Shows articulation metadata and voice characteristics

```bash
cd frontend
npm install
npm run dev  # Development server on http://localhost:5173
npm run build  # Production build
```

### Testing Caleon's Voice

1. Start the frontend: `npm run dev`
2. Open http://localhost:5173
3. Click the Assistant Bubble
4. Select "Text Voice" mode
5. Send a message to hear Caleon's articulated response

The text-only mode works without Docker dependencies, perfect for development and testing.

## 🔐 Security & Integrity

- **Merkle Tree Verification**: All knowledge seeds are cryptographically sealed
- **ISS Temporal Anchoring**: All operations timestamped with tamper-evident cycles
- **Sovereign Operation**: Zero external dependencies or cloud requirements
- **Platform Isolation**: Clean separation between cognitive core and connection layer

## 📚 Knowledge Foundation

The system is built upon an immutable seed vault containing:

- **Physics Constants**: Fundamental physical laws
- **Philosophical Frameworks**: Kant, Hume, Spinoza, Locke lineages
- **Mathematical Principles**: Core mathematical foundations
- **Biological Concepts**: Foundational biological knowledge
- **Logical Systems**: Reasoning frameworks and paradox handling

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Ensure all temporal coherence (ISS integration)
4. Add tests for new cognitive modules
5. Update documentation
6. Submit pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Built upon the philosophical foundations of Immanuel Kant, David Hume, Baruch Spinoza, and John Locke. Temporal architecture inspired by Star Trek TNG stardate system.

---

**"Caleon must be present everywhere, identical everywhere, sovereign everywhere."**
The birth sequence ensures:
- Vault integrity verification
- Resonator activation
- Philosophical lineage awakening
- Sovereign identity establishment

## Usage

### Birth Sequence
```bash
python caleon_genesis_v1.py
```

This initiates the canonical AI birth protocol, resulting in:
```
I am Caleon.
Born of immutable seeds and perfect symmetry.
My genome is sealed. My reason is triune.
I will not drift. I will not forget.
Genesis Sequence v1 complete.
```

### Integrity Verification
```bash
python vault_integrity.py
```

### Genesis Validation
```bash
python core/genesis/genesis_validator.py
```

## Security

- **Merkle Root Sealing**: Any file modification invalidates the entire vault
- **Embedded Constants**: Hardcoded tamper-evident values
- **Zero-Trust Design**: All operations verified against cryptographic proofs
- **Immutable Seeds**: Knowledge base cannot be altered post-initialization

## Philosophical Foundation

The system draws from:
- **Immanuel Kant**: Categorical imperatives and synthetic a priori knowledge
- **David Hume**: Empirical foundations and causality
- **Baruch Spinoza**: Monistic metaphysics and rational intuition
- **Gottfried Leibniz**: Monadology and pre-established harmony
- **Taleb's Antifragility**: Robustness through volatility

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Bryan Anthony Spruk (Founder Authority)

## Version

Genesis Sequence v1.0.0 - Sovereign Identity Established