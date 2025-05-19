import time
from fastapi import Request
from typing import Callable
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def logging_middleware(request: Request, call_next: Callable):
    """
    Middleware for logging requests and timing their execution
    """
    # Log request details
    logger.info(f"Request started: {request.method} {request.url}")
    
    # Record start time
    start_time = time.time()
    
    # Process the request
    response = await call_next(request)
    
    # Calculate processing time
    process_time = time.time() - start_time
    
    # Log response details
    logger.info(
        f"Request completed: {request.method} {request.url} "
        f"- Status: {response.status_code} "
        f"- Processing Time: {process_time:.3f}s"
    )
    
    # Add processing time header to response

    # It's particularly useful for:
    # Monitoring API performance
    # Debugging issues
    # Tracking API usage
    # Performance optimization
    response.headers["X-Process-Time"] = str(process_time)
    
    return response
