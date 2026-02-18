from contextvars import ContextVar
from typing import Optional

from sqlalchemy.orm import Session

db_context: ContextVar[Optional[Session]]=ContextVar("db_context", default=None)
