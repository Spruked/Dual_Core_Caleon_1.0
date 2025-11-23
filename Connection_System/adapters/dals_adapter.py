"""
DALS Platform Adapter
Connects DALS (Distributed AI Learning System) to Dual Core Caleon.

Handles DALS-specific message formats and integration patterns.
"""

import aiohttp
import json
import logging
from typing import Dict, Any, Optional
from connection_spine import CaleonAdapter

logger = logging.getLogger("dals_adapter")

class DalsAdapter(CaleonAdapter):
    """
    DALS platform adapter for Caleon integration.

    Handles DALS-specific:
    - Multi-node message routing
    - Learning context preservation
    - Distributed processing coordination
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__("DALS", config)

        # DALS-specific configuration
        self.dals_coordinator_url = self.config.get("dals_coordinator_url", "http://localhost:8080")
        self.node_id = self.config.get("node_id", "caleon_node_1")
        self.cluster_id = self.config.get("cluster_id", "default_cluster")

        # Learning context
        self.learning_context = {}
        self.session = None

    async def connect(self) -> bool:
        """Establish connection to Caleon Port via DALS coordinator"""
        try:
            self.session = aiohttp.ClientSession()

            # Register with DALS coordinator
            reg_data = {
                "node_id": self.node_id,
                "cluster_id": self.cluster_id,
                "capabilities": ["reasoning", "learning", "memory"],
                "caleon_integration": True
            }

            async with self.session.post(
                f"{self.dals_coordinator_url}/nodes/register",
                json=reg_data
            ) as response:
                if response.status != 200:
                    logger.error(f"DALS coordinator registration failed: {response.status}")
                    return False

            # Connect to Caleon Port
            connect_data = {
                "client": "DALS",
                "version": self.config.get("version", "1.0.0"),
                "auth_token": self.auth_token,
                "capabilities": ["text", "voice", "memory", "reasoning", "distributed_learning"]
            }

            async with self.session.post(
                f"{self.caleon_port_url}/api/v1/connect",
                json=connect_data
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    self.session_id = result.get("session_id")
                    self.connected = True
                    logger.info(f"DALS adapter connected - Node: {self.node_id}, Session: {self.session_id}")
                    return True
                else:
                    error = await response.text()
                    logger.error(f"DALS Caleon connection failed: {error}")
                    return False

        except Exception as e:
            logger.error(f"DALS connection error: {e}")
            return False

    async def disconnect(self) -> bool:
        """Disconnect from Caleon Port and DALS coordinator"""
        try:
            # Disconnect from Caleon
            if self.session and self.session_id:
                async with self.session.delete(
                    f"{self.caleon_port_url}/api/v1/connect/{self.session_id}"
                ) as response:
                    pass  # Log if needed

            # Unregister from DALS coordinator
            try:
                async with self.session.post(
                    f"{self.dals_coordinator_url}/nodes/unregister",
                    json={"node_id": self.node_id}
                ) as response:
                    pass
            except:
                pass  # DALS coordinator might be unavailable

            if self.session:
                await self.session.close()
                self.session = None

            self.connected = False
            self.session_id = None
            logger.info(f"DALS adapter disconnected - Node: {self.node_id}")
            return True

        except Exception as e:
            logger.error(f"DALS disconnect error: {e}")
            return False

    async def send_message(self, message: str, **kwargs) -> Dict[str, Any]:
        """Send message to Caleon with DALS learning context"""
        if not self.connected:
            raise ConnectionError("DALS adapter not connected")

        try:
            # Enhance message with DALS learning context
            enhanced_message = self._enhance_with_learning_context(message, **kwargs)

            caleon_request = {
                "message": enhanced_message,
                "context": {
                    "platform": "DALS",
                    "node_id": self.node_id,
                    "cluster_id": self.cluster_id,
                    "learning_context": self.learning_context,
                    "distributed_processing": True
                },
                "priority": kwargs.get("priority", "normal"),
                "timeout": kwargs.get("timeout", 45.0)  # Longer timeout for distributed processing
            }

            async with self.session.post(
                f"{self.caleon_port_url}/api/v1/think",
                json=caleon_request,
                headers={"Authorization": f"Bearer {self.auth_token}"}
            ) as response:

                if response.status == 200:
                    caleon_response = await response.json()

                    # Update learning context with response
                    self._update_learning_context(caleon_response)

                    # Distribute learning to DALS cluster
                    await self._distribute_learning(caleon_response)

                    return caleon_response
                else:
                    error = await response.text()
                    logger.error(f"DALS message send failed: {error}")
                    return {"error": f"HTTP {response.status}: {error}"}

        except Exception as e:
            logger.error(f"DALS message send error: {e}")
            return {"error": str(e)}

    async def receive_response(self, response: Dict[str, Any]) -> Any:
        """Process Caleon response and distribute to DALS cluster"""
        try:
            # Update local learning context
            self._update_learning_context(response)

            # Distribute to other DALS nodes
            await self._distribute_learning(response)

            # Format for DALS consumption
            dals_formatted = {
                "caleon_response": response,
                "node_id": self.node_id,
                "cluster_id": self.cluster_id,
                "distributed": True
            }

            return dals_formatted

        except Exception as e:
            logger.error(f"DALS response processing error: {e}")
            return {"error": str(e)}

    def _enhance_with_learning_context(self, message: str, **kwargs) -> str:
        """Enhance message with accumulated learning context"""
        # Add relevant learning patterns to the message
        context_str = ""

        if self.learning_context:
            # Extract relevant context based on message content
            relevant_patterns = []
            message_lower = message.lower()

            for pattern, data in self.learning_context.items():
                if pattern.lower() in message_lower:
                    relevant_patterns.append(f"{pattern}: {data.get('confidence', 0):.2f}")

            if relevant_patterns:
                context_str = f" [Learning Context: {', '.join(relevant_patterns[:3])}]"

        return message + context_str

    def _update_learning_context(self, response: Dict[str, Any]):
        """Update learning context from Caleon response"""
        try:
            reasoning = response.get("reasoning_chain", {})

            # Extract patterns and confidence scores
            for hemisphere, data in reasoning.items():
                if isinstance(data, dict):
                    verdict = data.get("synaptic_verdict")
                    if verdict:
                        # Store pattern with confidence
                        confidence = response.get("confidence", 0.5)
                        self.learning_context[verdict] = {
                            "confidence": confidence,
                            "hemisphere": hemisphere,
                            "timestamp": response.get("unix", 0)
                        }

            # Limit context size
            if len(self.learning_context) > 100:
                # Remove oldest entries
                sorted_items = sorted(
                    self.learning_context.items(),
                    key=lambda x: x[1]["timestamp"]
                )
                self.learning_context = dict(sorted_items[-50:])  # Keep 50 most recent

        except Exception as e:
            logger.warning(f"Learning context update failed: {e}")

    async def _distribute_learning(self, response: Dict[str, Any]):
        """Distribute learning updates to DALS cluster"""
        try:
            learning_update = {
                "node_id": self.node_id,
                "cluster_id": self.cluster_id,
                "learning_data": {
                    "caleon_response": response,
                    "context_size": len(self.learning_context),
                    "timestamp": response.get("unix", 0)
                }
            }

            async with self.session.post(
                f"{self.dals_coordinator_url}/learning/distribute",
                json=learning_update
            ) as cluster_response:
                if cluster_response.status == 200:
                    logger.debug("Learning distributed to DALS cluster")
                else:
                    logger.warning(f"DALS learning distribution failed: {cluster_response.status}")

        except Exception as e:
            logger.warning(f"DALS learning distribution error: {e}")

    async def get_cluster_status(self) -> Dict[str, Any]:
        """Get DALS cluster status"""
        try:
            async with self.session.get(
                f"{self.dals_coordinator_url}/cluster/status"
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return {"error": f"Cluster status unavailable: {response.status}"}
        except Exception as e:
            return {"error": str(e)}

# Factory function
def create_dals_adapter(config: Optional[Dict[str, Any]] = None) -> DalsAdapter:
    """Create and return a configured DALS adapter"""
    return DalsAdapter(config)