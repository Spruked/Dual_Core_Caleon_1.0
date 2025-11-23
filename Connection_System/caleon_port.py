"""
Caleon Port - Universal API Gateway
The standardized connection point for all platforms to access Dual Core Caleon.

This sits OUTSIDE the cognitive core and provides:
- Universal /think endpoint
- Platform handshake
- ISS pulse feed
- System status
- Clean abstraction layer
"""

from fastapi import FastAPI, HTTPException, Depends, Query, Body, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
import logging
import asyncio
import time
import json
from pathlib import Path

# Import Caleon cognitive core
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Main_Core.ISS_Brainstem import ISS
from Main_Core.left_hemisphere.synaptic_resonator import SynapticResonator as LeftSynaptic
from Main_Core.right_hemisphere.synaptic_resonator import SynapticResonator as RightSynaptic
from Main_Core.Final_harmonizer import FinalHarmonizer
from Main_Core.Task_Orchestrator import TaskOrchestrator
from Main_Core.Intent_Consent import IntentConsent
from Main_Core.nebula_core import nebula, start, end
from Main_Core.Task_Orchestrator import TaskOrchestrator
from Main_Core.Intent_Consent import IntentConsent
from ollama_integration import ollama_enhancer
from Main_Core.Caleon_Voice_Pipeline import CaleonVoicePipeline

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("caleon_port")

# Pydantic models
class ThinkRequest(BaseModel):
    """Request model for cognitive processing"""
    message: str = Field(..., min_length=1, max_length=10000, description="User message to process")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context")
    priority: Optional[str] = Field("normal", pattern="^(low|normal|high|urgent)$")
    timeout: Optional[float] = Field(30.0, gt=0, le=300, description="Processing timeout in seconds")

class ThinkResponse(BaseModel):
    """Response model for cognitive processing"""
    cycle_id: str
    stardate: str
    unix: float
    final_verdict: str
    reasoning_chain: Dict[str, Any]
    confidence: float
    processing_time: float
    audio_file: Optional[str] = None
    ollama_enhancement: Optional[Dict[str, Any]] = None

class PulseResponse(BaseModel):
    """ISS pulse and timing information"""
    cycle_id: str
    stardate: str
    unix: float
    drift_detected: bool
    system_uptime: float

class StatusResponse(BaseModel):
    """System status information"""
    status: str
    version: str
    active_connections: int
    cognitive_load: float
    memory_usage: Dict[str, Any]
    hemisphere_status: Dict[str, str]
    task_orchestrator_status: str
    intent_consent_status: str
    vault_system_status: str
    nebula_status: str
    platform_context: str
    ollama_status: str
    last_pulse: str

class TaskRequest(BaseModel):
    """Request model for task queuing"""
    task_data: Dict[str, Any] = Field(..., description="Task data to queue")
    priority: Optional[str] = Field("normal", pattern="^(low|normal|high|urgent)$")

class TaskResponse(BaseModel):
    """Response model for task operations"""
    task_id: str
    status: str
    timestamp: str

class VaultQueryRequest(BaseModel):
    """Request model for vault queries"""
    query: str = Field(..., description="Query string")
    category: Optional[str] = Field(None, description="Vault category filter")

class VaultQueryResponse(BaseModel):
    """Response model for vault queries"""
    results: List[Dict[str, Any]]
    query_time: float
    total_results: int
    last_pulse: str

class ConnectRequest(BaseModel):
    """Platform connection handshake"""
    client: str = Field(..., description="Client/platform name")
    version: str = Field(..., description="Client version")
    auth_token: str = Field(..., description="Authentication token")
    capabilities: List[str] = Field(..., description="Supported capabilities")

class ConnectResponse(BaseModel):
    """Connection handshake response"""
    connected: bool
    session_id: str
    server_version: str
    supported_capabilities: List[str]
    auth_valid: bool

class VoiceRequest(BaseModel):
    """Request model for voice synthesis"""
    left_verdict: Any = Field(..., description="Left hemisphere verdict")
    right_verdict: Any = Field(..., description="Right hemisphere verdict")
    distilled: Dict[str, Any] = Field(..., description="Distilled cognitive context")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context")

class VoiceResponse(BaseModel):
    """Response model for voice synthesis"""
    text: str
    audio_path: Optional[str]
    audio_duration: Optional[float]
    voice_profile: Dict[str, Any]
    pipeline_metadata: Dict[str, Any]
    stardate: str

# Initialize FastAPI app
app = FastAPI(
    title="Caleon Port - Universal API Gateway",
    description="Standardized connection point for Dual Core Caleon cognitive architecture",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer(auto_error=False)

# Global instances
left_hemisphere = None
right_hemisphere = None
final_harmonizer = None
task_orchestrator = None
intent_consent = None
vault_system = None
voice_pipeline = None
active_connections = {}
server_start_time = time.time()

@app.on_event("startup")
async def startup_event():
    """Initialize the Caleon cognitive system"""
    global left_hemisphere, right_hemisphere, final_harmonizer, task_orchestrator, intent_consent, vault_system

    try:
        logger.info("Initializing Dual Core Caleon...")

        # Initialize hemispheres
        left_hemisphere = LeftSynaptic("left")
        right_hemisphere = RightSynaptic("right")

        # Initialize final harmonizer
        final_harmonizer = FinalHarmonizer()

        # Initialize task orchestrator
        task_orchestrator = TaskOrchestrator()

        # Initialize intent consent
        intent_consent = IntentConsent()

        # Initialize vault system
        from Vault_System_1_0.vault_system.main import IntegratedVaultSystem
        vault_system = IntegratedVaultSystem(master_key="caleon_master_key_2025", node_id="caleon_port")

        # Initialize voice pipeline (text-only mode for testing)
        global voice_pipeline
        voice_pipeline = CaleonVoicePipeline(vault_system, text_only_mode=True)

        logger.info(f"Caleon Port startup complete - connected to {nebula.platform} system")

    except Exception as e:
        logger.error(f"Failed to initialize Caleon: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    global active_connections
    active_connections.clear()
    logger.info("Caleon Port shutdown complete")

# Authentication dependency
async def verify_auth(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Simple authentication - extend as needed"""
    if credentials is None:
        raise HTTPException(status_code=401, detail="Authentication required")

    # For now, accept any token - implement proper auth logic
    return {"client": "authenticated", "token": credentials.credentials}

# Routes
@app.get("/api/v1/pulse", response_model=PulseResponse)
async def get_pulse():
    """Get current ISS pulse and timing information"""
    try:
        cycle_id = ISS.pulse()
        stardate = ISS.stardate()
        unix = ISS.unix()
        drift = ISS.detect_drift()

        return PulseResponse(
            cycle_id=cycle_id,
            stardate=stardate,
            unix=unix,
            drift_detected=drift,
            system_uptime=time.time() - server_start_time
        )
    except Exception as e:
        logger.error(f"Pulse endpoint error: {e}")
        raise HTTPException(status_code=500, detail="Pulse generation failed")

@app.post("/api/v1/think", response_model=ThinkResponse)
async def think(
    request: ThinkRequest,
    auth=Depends(verify_auth)
):
    """Process a message through the full cognitive pipeline"""
    start_time = time.time()

    # Start nebula transaction
    tx = start(session=str(auth), prompt=request.message, meta={"priority": request.priority})

    try:
        # Get timing baseline
        cycle_id = ISS.pulse()
        stardate = ISS.stardate()
        unix = ISS.unix()

        # Authorize the intent
        auth_result = intent_consent.authorize(request.message, {"priority": request.priority})
        if not auth_result:
            end(tx, "DENIED")
            return ThinkResponse(
                cycle_id=cycle_id,
                stardate=stardate,
                unix=unix,
                final_verdict="DENIED",
                reasoning_chain={"authorization": "Intent denied by consent layer"},
                confidence=0.0,
                processing_time=time.time() - start_time
            )

        # Process through left hemisphere
        left_stimulus = float(hash(request.message) % 1000) / 1000.0  # Convert to 0-1 range
        left_result = left_hemisphere.resonate(left_stimulus)

        # Process through right hemisphere
        right_stimulus = float(hash(request.message[::-1]) % 1000) / 1000.0
        right_result = right_hemisphere.resonate(right_stimulus)

        # Final harmonization
        harmonized = final_harmonizer.harmonize(
            left_result['synaptic_verdict'],
            right_result['synaptic_verdict'],
            request.message
        )

        # Queue the result as a task for execution
        task_item = {
            "verdict": harmonized['verdict'],
            "reasoning_chain": {
                "left_hemisphere": left_result,
                "right_hemisphere": right_result,
                "harmonization": harmonized
            },
            "cycle_id": cycle_id
        }
        task_orchestrator.queue(task_item)

        processing_time = time.time() - start_time

        # Generate audio response (placeholder - integrate with phonatory)
        audio_file = None
        # TODO: Integrate with phonatory module for speech synthesis

        # Enhance with Ollama insights
        context = {
            "platform": nebula.platform if nebula else "standalone",
            "priority": request.priority,
            "stardate": stardate,
            "hemisphere_data": {
                "left": "active" if left_hemisphere else "inactive",
                "right": "active" if right_hemisphere else "inactive"
            }
        }

        ollama_result = ollama_enhancer.enhance_thinking(
            request.message,
            {
                "left_hemisphere": left_result,
                "right_hemisphere": right_result
            },
            harmonized,
            context
        )

        result = ThinkResponse(
            cycle_id=cycle_id,
            stardate=stardate,
            unix=unix,
            final_verdict=harmonized['verdict'],
            reasoning_chain={
                "left_hemisphere": left_result,
                "right_hemisphere": right_result,
                "harmonization": harmonized
            },
            confidence=harmonized.get('confidence', 0.8),
            processing_time=processing_time,
            audio_file=audio_file,
            ollama_enhancement=ollama_result if ollama_result["ollama_enhanced"] else None
        )

        # End nebula transaction
        end(tx, harmonized['verdict'])

        return result

    except Exception as e:
        logger.error(f"Think endpoint error: {e}")
        end(tx, f"ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail="Cognitive processing failed")

@app.post("/api/v1/speak/text", response_model=VoiceResponse)
async def speak_text_only(request: VoiceRequest, auth=Depends(verify_auth)):
    """Text-only speech synthesis for testing Caleon's articulation"""
    try:
        if voice_pipeline is None:
            raise HTTPException(status_code=500, detail="Voice pipeline not initialized")

        # Start nebula transaction
        tx = start(session=str(auth), action="speak_text", meta={"mode": "text_only"})

        # Process through voice pipeline (text-only mode)
        result = await voice_pipeline.speak(
            request.left_verdict,
            request.right_verdict,
            request.distilled,
            request.context
        )

        end(tx, "success")
        return VoiceResponse(
            text=result["text"],
            audio_path=result["audio_path"],
            audio_duration=result["audio_duration"],
            voice_profile=result["voice_profile"],
            pipeline_metadata=result["pipeline_metadata"],
            stardate=result["pipeline_metadata"]["stardate"]
        )

    except Exception as e:
        logger.error(f"Text speech endpoint error: {e}")
        end(tx, f"ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail="Text articulation failed")

        result = await ollama_engine.query(prompt, system, context)

        # End nebula transaction
        end(tx, "completed" if result["success"] else "failed")

        if not result["success"]:
            raise HTTPException(status_code=500, detail=result.get("error", "Phi-3 reasoning failed"))

        return result

    except Exception as e:
        logger.error(f"Phi-3 endpoint error: {e}")
        raise HTTPException(status_code=500, detail="Phi-3 reasoning failed")

@app.post("/api/v1/voice", response_model=VoiceResponse)
async def caleon_voice(request: VoiceRequest, auth=Depends(verify_auth)):
    """Caleon's complete voice pipeline - hemispheres to speech"""
    try:
        if not voice_pipeline:
            raise HTTPException(status_code=503, detail="Voice pipeline not initialized")

        # Start nebula transaction
        tx = start(session=str(auth), prompt="voice_synthesis", meta={"endpoint": "voice"})

        # Run complete voice pipeline
        result = await voice_pipeline.speak(
            left_verdict=request.left_verdict,
            right_verdict=request.right_verdict,
            distilled=request.distilled,
            context=request.context
        )

        # End nebula transaction
        end(tx, "voice_synthesized" if result["audio_path"] else "text_only")

        # Add stardate to response
        result["stardate"] = result["pipeline_metadata"]["stardate"]

        return result

    except Exception as e:
        logger.error(f"Voice endpoint error: {e}")
        raise HTTPException(status_code=500, detail="Voice synthesis failed")

@app.post("/api/v1/task/queue", response_model=TaskResponse)
async def queue_task(
    request: TaskRequest,
    auth=Depends(verify_auth)
):
    """Queue a task for execution"""
    try:
        task_item = {
            "data": request.task_data,
            "priority": request.priority,
            "submitted_at": ISS.unix()
        }
        pulse = task_orchestrator.queue(task_item)
        return TaskResponse(
            task_id=pulse,
            status="queued",
            timestamp=ISS.stardate()
        )
    except Exception as e:
        logger.error(f"Task queue error: {e}")
        raise HTTPException(status_code=500, detail="Task queuing failed")

@app.get("/api/v1/task/next", response_model=TaskResponse)
async def get_next_task(auth=Depends(verify_auth)):
    """Get next task from queue"""
    try:
        task = task_orchestrator.next()
        if not task:
            return TaskResponse(
                task_id="",
                status="no_tasks",
                timestamp=ISS.stardate()
            )
        return TaskResponse(
            task_id=task.get("executed_at", ""),
            status="executing",
            timestamp=ISS.stardate()
        )
    except Exception as e:
        logger.error(f"Task next error: {e}")
        raise HTTPException(status_code=500, detail="Task retrieval failed")

@app.post("/api/v1/task/done", response_model=TaskResponse)
async def mark_task_done(
    task_data: Dict[str, Any] = Body(..., description="Task data to mark as done"),
    auth=Depends(verify_auth)
):
    """Mark a task as completed"""
    try:
        pulse = task_orchestrator.mark_done(task_data)
        return TaskResponse(
            task_id=pulse,
            status="completed",
            timestamp=ISS.stardate()
        )
    except Exception as e:
        logger.error(f"Task done error: {e}")
        raise HTTPException(status_code=500, detail="Task completion failed")

@app.post("/api/v1/vault/query", response_model=VaultQueryResponse)
async def query_vault(
    request: VaultQueryRequest,
    auth=Depends(verify_auth)
):
    """Query the integrated vault system"""
    start_time = time.time()
    try:
        # Placeholder for vault query - integrate with actual vault methods
        results = []  # vault_system.query(request.query, request.category)
        query_time = time.time() - start_time
        return VaultQueryResponse(
            results=results,
            query_time=query_time,
            total_results=len(results)
        )
    except Exception as e:
        logger.error(f"Vault query error: {e}")
        raise HTTPException(status_code=500, detail="Vault query failed")

@app.get("/api/v1/status", response_model=StatusResponse)
async def get_status(auth=Depends(verify_auth)):
    """Get comprehensive system status"""
    try:
        # Get hemisphere status
        hemisphere_status = {
            "left": "active" if left_hemisphere else "inactive",
            "right": "active" if right_hemisphere else "inactive"
        }

        # Get component status
        task_orchestrator_status = "active" if task_orchestrator else "inactive"
        intent_consent_status = "active" if intent_consent else "inactive"
        vault_system_status = "active" if vault_system else "inactive"
        nebula_status = "active" if nebula else "inactive"
        platform_context = nebula.platform if nebula else "unknown"
        ollama_status = "active" if ollama_enhancer.client.check_health() else "inactive"

        # Calculate cognitive load (simplified)
        cognitive_load = len(active_connections) / 10.0  # Scale 0-1

        # Memory usage (simplified)
        memory_usage = {
            "active_connections": len(active_connections),
            "hemispheres_loaded": sum(1 for h in hemisphere_status.values() if h == "active"),
            "uptime_seconds": time.time() - server_start_time
        }

        return StatusResponse(
            status="operational",
            version="1.0.0",
            active_connections=len(active_connections),
            cognitive_load=min(cognitive_load, 1.0),
            memory_usage=memory_usage,
            hemisphere_status=hemisphere_status,
            task_orchestrator_status=task_orchestrator_status,
            intent_consent_status=intent_consent_status,
            vault_system_status=vault_system_status,
            nebula_status=nebula_status,
            platform_context=platform_context,
            ollama_status=ollama_status,
            last_pulse=ISS.stardate()
        )

    except Exception as e:
        logger.error(f"Status endpoint error: {e}")
        raise HTTPException(status_code=500, detail="Status retrieval failed")

@app.websocket("/ws/live")
async def websocket_live_updates(websocket: WebSocket):
    """WebSocket endpoint for real-time system updates"""
    await websocket.accept()
    logger.info("WebSocket connection established")

    try:
        while True:
            # Send periodic status updates
            status_data = {
                "type": "status_update",
                "timestamp": ISS.unix(),
                "stardate": ISS.stardate(),
                "platform": nebula.platform if nebula else "unknown",
                "active_connections": len(active_connections),
                "cognitive_load": min(len(active_connections) / 10.0, 1.0),
                "hemisphere_status": {
                    "left": "active" if left_hemisphere else "inactive",
                    "right": "active" if right_hemisphere else "inactive"
                },
                "ollama_status": "active" if ollama_enhancer.client.check_health() else "inactive"
            }
            await websocket.send_json(status_data)

            # Wait before next update
            await asyncio.sleep(5)  # Update every 5 seconds

    except WebSocketDisconnect:
        logger.info("WebSocket connection closed")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")

@app.post("/api/v1/connect", response_model=ConnectResponse)
async def connect(request: ConnectRequest):
    """Platform connection handshake"""
    try:
        # Generate session ID
        session_id = f"session_{ISS.pulse().replace('PULSE-', '').replace('.', '_')}"

        # Store connection
        active_connections[session_id] = {
            "client": request.client,
            "version": request.version,
            "connected_at": ISS.unix(),
            "capabilities": request.capabilities
        }

        # Supported capabilities
        supported = ["text", "voice", "memory", "audio", "reasoning"]

        # Simple auth check (extend as needed)
        auth_valid = len(request.auth_token) > 10  # Basic check

        logger.info(f"New connection: {request.client} v{request.version} - Session: {session_id}")

        return ConnectResponse(
            connected=True,
            session_id=session_id,
            server_version="1.0.0",
            supported_capabilities=supported,
            auth_valid=auth_valid
        )

    except Exception as e:
        logger.error(f"Connect endpoint error: {e}")
        raise HTTPException(status_code=500, detail="Connection failed")

@app.delete("/api/v1/connect/{session_id}")
async def disconnect(session_id: str, auth=Depends(verify_auth)):
    """Disconnect a client session"""
    if session_id in active_connections:
        del active_connections[session_id]
        logger.info(f"Disconnected session: {session_id}")
        return {"message": "Disconnected successfully"}
    else:
        raise HTTPException(status_code=404, detail="Session not found")

# Health check
@app.get("/health")
async def health_check():
    """Simple health check"""
    return {
        "status": "healthy",
        "service": "Caleon Port",
        "uptime": time.time() - server_start_time,
        "stardate": ISS.stardate()
    }

# Development info
@app.get("/info")
async def system_info():
    """Development system information"""
    voice_health = voice_pipeline.health_check() if voice_pipeline else {"status": "unavailable"}

    return {
        "name": "Dual Core Caleon",
        "version": "1.0.0",
        "architecture": "Dual Hemisphere Cognitive Kernel",
        "timing": "ISS Brainstem Synchronized",
        "connections": len(active_connections),
        "capabilities": ["reasoning", "memory", "speech", "temporal_coherence", "voice_synthesis"],
        "voice_pipeline": voice_health
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "connection_system.caleon_port:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )