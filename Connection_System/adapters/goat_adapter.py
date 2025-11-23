"""
GOAT Platform Adapter
Connects GOAT (Generative Operational AI Toolkit) to Dual Core Caleon.

This adapter handles GOAT-specific message formats, authentication,
and response processing.
"""

import aiohttp
import json
import logging
from typing import Dict, Any, Optional
from connection_spine import CaleonAdapter

logger = logging.getLogger("goat_adapter")

class GoatAdapter(CaleonAdapter):
    """
    GOAT platform adapter for Caleon integration.

    Handles GOAT's specific:
    - Authentication flow
    - Message format conversion
    - Response processing
    - Session management
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__("GOAT", config)

        # GOAT-specific configuration
        self.goat_api_url = self.config.get("goat_api_url", "https://api.goat.ai")
        self.goat_client_id = self.config.get("goat_client_id", "")
        self.goat_client_secret = self.config.get("goat_client_secret", "")
        self.session_token = None

        # HTTP client session
        self.session = None

    async def connect(self) -> bool:
        """Establish connection to Caleon Port via GOAT"""
        try:
            # Initialize HTTP session
            self.session = aiohttp.ClientSession()

            # Perform GOAT authentication
            auth_success = await self._authenticate_goat()
            if not auth_success:
                logger.error("GOAT authentication failed")
                return False

            # Connect to Caleon Port
            connect_data = {
                "client": "GOAT",
                "version": self.config.get("version", "1.0.0"),
                "auth_token": self.auth_token,
                "capabilities": ["text", "voice", "memory", "reasoning", "goat_integration"]
            }

            async with self.session.post(
                f"{self.caleon_port_url}/api/v1/connect",
                json=connect_data
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    self.session_id = result.get("session_id")
                    self.connected = True
                    logger.info(f"GOAT adapter connected - Session: {self.session_id}")
                    return True
                else:
                    error = await response.text()
                    logger.error(f"GOAT connection failed: {error}")
                    return False

        except Exception as e:
            logger.error(f"GOAT connection error: {e}")
            return False

    async def disconnect(self) -> bool:
        """Disconnect from Caleon Port"""
        try:
            if self.session and self.session_id:
                async with self.session.delete(
                    f"{self.caleon_port_url}/api/v1/connect/{self.session_id}"
                ) as response:
                    if response.status == 200:
                        logger.info("GOAT adapter disconnected")
                    else:
                        logger.warning("GOAT disconnect may not have completed cleanly")

            if self.session:
                await self.session.close()
                self.session = None

            self.connected = False
            self.session_id = None
            return True

        except Exception as e:
            logger.error(f"GOAT disconnect error: {e}")
            return False

    async def send_message(self, message: str, **kwargs) -> Dict[str, Any]:
        """Send message to Caleon through GOAT interface"""
        if not self.connected:
            raise ConnectionError("GOAT adapter not connected")

        try:
            # Convert GOAT message format to Caleon format
            caleon_request = self._convert_goat_to_caleon(message, **kwargs)

            async with self.session.post(
                f"{self.caleon_port_url}/api/v1/think",
                json=caleon_request,
                headers={"Authorization": f"Bearer {self.auth_token}"}
            ) as response:

                if response.status == 200:
                    caleon_response = await response.json()
                    # Convert Caleon response to GOAT format
                    goat_response = self._convert_caleon_to_goat(caleon_response)
                    return goat_response
                else:
                    error = await response.text()
                    logger.error(f"GOAT message send failed: {error}")
                    return {"error": f"HTTP {response.status}: {error}"}

        except Exception as e:
            logger.error(f"GOAT message send error: {e}")
            return {"error": str(e)}

    async def receive_response(self, response: Dict[str, Any]) -> Any:
        """Process response from Caleon (callback interface)"""
        # This method is called when responses come back through callbacks
        # Convert Caleon response to GOAT format and forward to GOAT system

        goat_formatted = self._convert_caleon_to_goat(response)

        # Forward to GOAT system (implementation depends on GOAT's API)
        await self._forward_to_goat(goat_formatted)

        return goat_formatted

    async def _authenticate_goat(self) -> bool:
        """Authenticate with GOAT platform"""
        try:
            auth_data = {
                "client_id": self.goat_client_id,
                "client_secret": self.goat_client_secret,
                "grant_type": "client_credentials"
            }

            async with aiohttp.ClientSession() as temp_session:
                async with temp_session.post(
                    f"{self.goat_api_url}/oauth/token",
                    json=auth_data
                ) as response:
                    if response.status == 200:
                        token_data = await response.json()
                        self.session_token = token_data.get("access_token")
                        self.auth_token = self.session_token  # Use for Caleon auth
                        return True
                    else:
                        logger.error(f"GOAT auth failed: {response.status}")
                        return False

        except Exception as e:
            logger.error(f"GOAT authentication error: {e}")
            return False

    def _convert_goat_to_caleon(self, goat_message: str, **kwargs) -> Dict[str, Any]:
        """Convert GOAT message format to Caleon format"""
        # GOAT messages might have specific structure
        # Extract the actual message content

        message_content = goat_message
        context = kwargs.get("context", {})
        priority = kwargs.get("priority", "normal")

        # Add GOAT-specific context
        context.update({
            "platform": "GOAT",
            "message_type": "user_input",
            "timestamp": kwargs.get("timestamp")
        })

        return {
            "message": message_content,
            "context": context,
            "priority": priority,
            "timeout": kwargs.get("timeout", 30.0)
        }

    def _convert_caleon_to_goat(self, caleon_response: Dict[str, Any]) -> Dict[str, Any]:
        """Convert Caleon response to GOAT format"""
        # Transform Caleon's structured response to GOAT's expected format

        return {
            "goat_response": {
                "message": caleon_response.get("final_verdict", ""),
                "metadata": {
                    "cycle_id": caleon_response.get("cycle_id"),
                    "stardate": caleon_response.get("stardate"),
                    "confidence": caleon_response.get("confidence", 0.0),
                    "processing_time": caleon_response.get("processing_time", 0.0)
                },
                "reasoning": caleon_response.get("reasoning_chain", {}),
                "audio": caleon_response.get("audio_file"),
                "platform": "Caleon",
                "version": "1.0.0"
            }
        }

    async def _forward_to_goat(self, goat_response: Dict[str, Any]):
        """Forward processed response back to GOAT system"""
        # Implementation depends on GOAT's callback/webhook system
        try:
            # Example: POST back to GOAT webhook
            webhook_url = self.config.get("goat_webhook_url")
            if webhook_url:
                async with self.session.post(webhook_url, json=goat_response) as response:
                    if response.status == 200:
                        logger.info("Response forwarded to GOAT successfully")
                    else:
                        logger.warning(f"GOAT webhook failed: {response.status}")
        except Exception as e:
            logger.error(f"Error forwarding to GOAT: {e}")

    async def get_goat_status(self) -> Dict[str, Any]:
        """Get GOAT-specific status information"""
        return {
            "platform": "GOAT",
            "authenticated": self.session_token is not None,
            "caleon_connected": self.connected,
            "session_id": self.session_id,
            "api_url": self.goat_api_url
        }

# Factory function for easy instantiation
def create_goat_adapter(config: Optional[Dict[str, Any]] = None) -> GoatAdapter:
    """Create and return a configured GOAT adapter"""
    return GoatAdapter(config)

# Auto-register with connection spine
try:
    from connection_spine import register_adapter
    # This would be called when the module is imported
    # register_adapter(create_goat_adapter())
except ImportError:
    pass  # Connection spine not available