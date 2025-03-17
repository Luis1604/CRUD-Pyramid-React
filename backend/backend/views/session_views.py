import logging
from cornice.resource import resource, view
from backend.services.session_service import get_active_sessions, close_session, close_all_sessions
from backend.services.auth_service import verify_jwt

log = logging.getLogger(__name__)

@resource(path="/api/sessions/{id}", collection_path="/api/sessions")
class SessionResource:

    def __init__(self, request):
        self.request = request
        self.user_id = verify_jwt(request)
        if not self.user_id:
            self.request.errors.add("authorization", "invalid", "No autorizado")

    @view(renderer="json", permission="view")
    def collection_get(self):
        """ Obtiene todas las sesiones activas del usuario """
        if self.request.errors:
            return {"error": "No autorizado"}, 401

        sessions = get_active_sessions(self.request, self.user_id)
        return {
            "success": True,
            "sessions": [
                {
                    "id": s.id,
                    "ip_address": s.ip_address,
                    "device": s.device,
                    "created_at": s.created_at.strftime("%Y-%m-%d %H:%M"),
                }
                for s in sessions
            ],
        }

    @view(renderer="json", permission="delete")
    def delete(self):
        """ Cierra una sesión específica """
        if self.request.errors:
            return {"error": "No autorizado"}, 401

        session_id = self.request.matchdict.get("id")
        if close_session(self.request, session_id, self.user_id):
            return {"message": "Sesión cerrada correctamente"}, 200
        return {"error": "Sesión no encontrada"}, 404

    @view(renderer="json", permission="delete")
    def collection_delete(self):
        """ Cierra todas las sesiones activas """
        if self.request.errors:
            return {"error": "No autorizado"}, 401

        close_all_sessions(self.request, self.user_id)
        return {"message": "Todas las sesiones han sido cerradas"}, 200


