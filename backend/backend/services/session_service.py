import datetime
from backend.models import ActiveSessions


def get_active_sessions(request, user_id):
    """ Obtiene las sesiones activas de un usuario """
    return request.dbsession.query(ActiveSessions).filter_by(user_id=user_id, is_active=True).all()

def close_session(request, session_id, user_id):
    """ Cierra una sesión específica del usuario """
    session = request.dbsession.query(ActiveSessions).filter_by(id=session_id, user_id=user_id).first()
    if session:
        request.dbsession.delete(session)
        request.dbsession.flush()
        return True
    return False

def close_all_sessions(request, user_id):
    """ Cierra todas las sesiones activas del usuario """
    request.dbsession.query(ActiveSessions).filter_by(user_id=user_id).delete()
    request.dbsession.flush()
    return True
