"""Infrastructure layer - thin wrappers over shared components.

This module re-exports shared infrastructure for convenience.
All actual implementation is in shared/ to avoid duplication.
"""
from shared.http_clients import DataApiClient
from shared.rabbitmq import RabbitMQPublisher, RabbitMQConsumer

__all__ = ["DataApiClient", "RabbitMQPublisher", "RabbitMQConsumer"]
