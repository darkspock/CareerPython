"""Dramatiq broker configuration."""

import os

import dramatiq
from dramatiq.brokers.redis import RedisBroker
from dramatiq.middleware import ShutdownNotifications, Callbacks, Retries

from .middleware.async_job_middleware import AsyncJobMiddleware


def create_broker() -> RedisBroker:
    """Create and configure the Dramatiq broker."""
    # Get Redis URL from environment
    redis_url = os.getenv("DRAMATIQ_BROKER_URL", "redis://localhost:6379/0")

    # Create Redis broker with custom middleware configuration
    # We explicitly set middleware=[] to avoid automatic TimeLimit middleware
    broker = RedisBroker(url=redis_url, middleware=[])

    # Add only the middleware we want (excluding TimeLimit)
    broker.add_middleware(ShutdownNotifications())
    broker.add_middleware(Callbacks())
    broker.add_middleware(Retries())  # Required for max_retries on actors
    broker.add_middleware(AsyncJobMiddleware())

    return broker


# Create the broker instance
broker = create_broker()

# Set as default broker
dramatiq.set_broker(broker)

# Import actors to register them
