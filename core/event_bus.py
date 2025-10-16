import logging
import asyncio
import inspect
import threading
from concurrent.futures import ThreadPoolExecutor
from core.event import Event


class EventBus:
    def __init__(self) -> None:
        self._executor = ThreadPoolExecutor(max_workers=4)

    @staticmethod
    def dispatch(event: Event) -> None:
        # TEMPORARILY DISABLED - Event handling simplified for now
        logging.info(f"Event dispatched: {type(event).__name__}")
        # TODO: Implement proper event handling system
        pass

    @staticmethod
    def _run_async_handler(handler, event):
        """Run async handler in a separate thread with its own event loop"""
        def run_in_thread():
            try:
                # Create new event loop for this thread
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                # Run the async handler
                loop.run_until_complete(handler.handle(event))
                
            except Exception as e:
                logging.error(f"Error in async event handler: {e}")
            finally:
                loop.close()
        
        # Run in background thread
        thread = threading.Thread(target=run_in_thread, daemon=True)
        thread.start()