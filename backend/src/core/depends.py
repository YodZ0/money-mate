from typing import Annotated
from fastapi import Depends

from src.core.database import SessionDep
from src.core.session_manager import SessionManagerProtocol, SessionManagerImpl


def get_session_manager(session: SessionDep) -> SessionManagerProtocol:
    return SessionManagerImpl(session)  # type: ignore


SessionManager = Annotated[
    SessionManagerProtocol,
    Depends(get_session_manager),
]
