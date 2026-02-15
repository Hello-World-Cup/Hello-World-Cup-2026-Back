from functools import wraps
import inspect

from app.adapters.routing.utils.response import ResponseFormatter
from app.domain.exceptions.base_exceptions import DomainException


def format_response(func):

    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            if inspect.isawaitable(result):
                result = await result

            return ResponseFormatter.format_response(data=result)
        
        except DomainException as e:
            return ResponseFormatter.format_response(
                success=False, status_code=e.error_code, error=e.message
            )
        
        except Exception as e:
            return ResponseFormatter.format_response(
                success=False, status_code="UNKNOWN_ERROR", error=str(e)
            )

    return wrapper
    
