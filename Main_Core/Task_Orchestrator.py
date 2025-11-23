# Task_Orchestrator.py
# Caleon's Executive Cortex
# Author: Bryan A. Spruk

from .ISS_Brainstem import ISSBrainstem
from collections import deque

class TaskOrchestrator:
    """
    Task scheduler and execution manager.
    Prioritizes and manages task queues with ISS timing.
    """

    def __init__(self):
        self.iss = ISSBrainstem()
        self.queue = deque()

    def queue(self, item: dict) -> str:
        """
        Add item to execution queue.
        Returns pulse timestamp of queuing.
        """
        pulse = self.iss.pulse()
        item["queued_at"] = pulse
        self.queue.append(item)
        return pulse

    def next(self) -> dict:
        """
        Get next item from queue.
        Returns item with execution timestamp.
        """
        if not self.queue:
            return {}
        item = self.queue.popleft()
        item["executed_at"] = self.iss.pulse()
        return item

    def mark_done(self, item: dict) -> str:
        """
        Mark item as completed.
        Returns completion timestamp.
        """
        pulse = self.iss.pulse()
        item["completed_at"] = pulse
        return pulse