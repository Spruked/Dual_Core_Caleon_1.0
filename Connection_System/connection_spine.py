"""
Connection Spine - Adapter Management System
Manages platform-specific adapters and provides unified connection interface.

This is the "spinal cord" that connects the brain (Caleon core) to the nerves (adapters).
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
import json
import time
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("connection_spine")

class CaleonAdapter(ABC):
    """Abstract base class for all Caleon platform adapters"""

    def __init__(self, platform_name: str, config: Optional[Dict[str, Any]] = None):
        self.platform_name = platform_name
        self.config = config or {}
        self.connected = False
        self.session_id = None
        self.caleon_port_url = self.config.get("caleon_port_url", "http://localhost:8000")
        self.auth_token = self.config.get("auth_token", "")

    @abstractmethod
    async def connect(self) -> bool:
        """Establish connection to Caleon Port"""
        pass

    @abstractmethod
    async def disconnect(self) -> bool:
        """Disconnect from Caleon Port"""
        pass

    @abstractmethod
    async def send_message(self, message: str, **kwargs) -> Dict[str, Any]:
        """Send message to Caleon for processing"""
        pass

    @abstractmethod
    async def receive_response(self, response: Dict[str, Any]) -> Any:
        """Process response from Caleon"""
        pass

    async def get_status(self) -> Dict[str, Any]:
        """Get adapter status"""
        return {
            "platform": self.platform_name,
            "connected": self.connected,
            "session_id": self.session_id,
            "config": self.config
        }

class ConnectionSpine:
    """
    The central nervous system for Caleon connections.
    Manages all adapters and provides unified interface.
    """

    def __init__(self, config_file: Optional[str] = None):
        self.adapters: Dict[str, CaleonAdapter] = {}
        self.config = self._load_config(config_file)
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
        self.message_queue = asyncio.Queue(maxsize=1000)

        # Start background message processor
        self.processor_task = None

    def _load_config(self, config_file: Optional[str]) -> Dict[str, Any]:
        """Load configuration from file or use defaults"""
        default_config = {
            "caleon_port_url": "http://localhost:8000",
            "max_connections": 100,
            "message_timeout": 30,
            "rate_limiting": {
                "enabled": True,
                "requests_per_minute": 60
            },
            "adapters": {
                "goat": {"enabled": False},
                "dals": {"enabled": False},
                "babythink": {"enabled": False}
            }
        }

        if config_file and Path(config_file).exists():
            with open(config_file, 'r') as f:
                user_config = json.load(f)
                default_config.update(user_config)

        return default_config

    def register_adapter(self, adapter: CaleonAdapter) -> bool:
        """Register a new adapter"""
        try:
            adapter_name = adapter.platform_name.lower()
            self.adapters[adapter_name] = adapter
            logger.info(f"Registered adapter: {adapter_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to register adapter {adapter.platform_name}: {e}")
            return False

    def unregister_adapter(self, platform_name: str) -> bool:
        """Unregister an adapter"""
        adapter_name = platform_name.lower()
        if adapter_name in self.adapters:
            # Disconnect first
            asyncio.create_task(self.adapters[adapter_name].disconnect())
            del self.adapters[adapter_name]
            logger.info(f"Unregistered adapter: {adapter_name}")
            return True
        return False

    async def connect_adapter(self, platform_name: str) -> bool:
        """Connect a specific adapter"""
        adapter_name = platform_name.lower()
        if adapter_name not in self.adapters:
            logger.error(f"Adapter not found: {adapter_name}")
            return False

        try:
            success = await self.adapters[adapter_name].connect()
            if success:
                logger.info(f"Connected adapter: {adapter_name}")
            else:
                logger.error(f"Failed to connect adapter: {adapter_name}")
            return success
        except Exception as e:
            logger.error(f"Error connecting adapter {adapter_name}: {e}")
            return False

    async def disconnect_adapter(self, platform_name: str) -> bool:
        """Disconnect a specific adapter"""
        adapter_name = platform_name.lower()
        if adapter_name not in self.adapters:
            return False

        try:
            success = await self.adapters[adapter_name].disconnect()
            logger.info(f"Disconnected adapter: {adapter_name}")
            return success
        except Exception as e:
            logger.error(f"Error disconnecting adapter {adapter_name}: {e}")
            return False

    async def send_to_caleon(self, platform_name: str, message: str, **kwargs) -> Dict[str, Any]:
        """Send message through specific adapter"""
        adapter_name = platform_name.lower()
        if adapter_name not in self.adapters:
            raise ValueError(f"Adapter not found: {adapter_name}")

        adapter = self.adapters[adapter_name]
        if not adapter.connected:
            # Auto-connect if not connected
            await adapter.connect()

        return await adapter.send_message(message, **kwargs)

    async def broadcast_message(self, message: str, platforms: Optional[List[str]] = None) -> Dict[str, Dict[str, Any]]:
        """Send message to multiple platforms"""
        if platforms is None:
            platforms = list(self.adapters.keys())

        results = {}
        for platform in platforms:
            try:
                result = await self.send_to_caleon(platform, message)
                results[platform] = result
            except Exception as e:
                results[platform] = {"error": str(e)}

        return results

    async def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        adapter_statuses = {}
        for name, adapter in self.adapters.items():
            adapter_statuses[name] = await adapter.get_status()

        return {
            "connection_spine": {
                "status": "active",
                "adapters_registered": len(self.adapters),
                "active_sessions": len(self.active_sessions),
                "queue_size": self.message_queue.qsize()
            },
            "adapters": adapter_statuses,
            "config": self.config
        }

    async def start_message_processor(self):
        """Start background message processing"""
        self.processor_task = asyncio.create_task(self._process_messages())

    async def stop_message_processor(self):
        """Stop background message processing"""
        if self.processor_task:
            self.processor_task.cancel()
            try:
                await self.processor_task
            except asyncio.CancelledError:
                pass

    async def _process_messages(self):
        """Background message processor"""
        while True:
            try:
                # Get message from queue
                message_data = await self.message_queue.get()

                platform = message_data.get("platform")
                message = message_data.get("message")
                callback = message_data.get("callback")

                # Process message
                result = await self.send_to_caleon(platform, message)

                # Call callback if provided
                if callback:
                    await callback(result)

                self.message_queue.task_done()

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Message processing error: {e}")

    async def queue_message(self, platform: str, message: str, callback: Optional[callable] = None):
        """Queue message for background processing"""
        await self.message_queue.put({
            "platform": platform,
            "message": message,
            "callback": callback
        })

    def get_available_adapters(self) -> List[str]:
        """Get list of available adapter platforms"""
        return list(self.adapters.keys())

    def get_adapter_info(self, platform_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific adapter"""
        adapter_name = platform_name.lower()
        if adapter_name not in self.adapters:
            return None

        adapter = self.adapters[adapter_name]
        return {
            "platform": adapter.platform_name,
            "connected": adapter.connected,
            "session_id": adapter.session_id,
            "config": adapter.config
        }

# Global instance
connection_spine = ConnectionSpine()

# Convenience functions
async def connect_platform(platform_name: str) -> bool:
    """Connect a platform adapter"""
    return await connection_spine.connect_adapter(platform_name)

async def send_message(platform_name: str, message: str) -> Dict[str, Any]:
    """Send message to Caleon through platform adapter"""
    return await connection_spine.send_to_caleon(platform_name, message)

async def get_status() -> Dict[str, Any]:
    """Get connection spine status"""
    return await connection_spine.get_system_status()

def register_adapter(adapter: CaleonAdapter) -> bool:
    """Register a new adapter"""
    return connection_spine.register_adapter(adapter)

def get_available_platforms() -> List[str]:
    """Get list of available platforms"""
    return connection_spine.get_available_adapters()