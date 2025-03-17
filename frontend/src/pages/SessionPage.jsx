import { useEffect, useState } from "react";
import { FaTrash, FaSignOutAlt } from "react-icons/fa";

const SessionsList = () => {
    const [sessions, setSessions] = useState([]);
    const [currentSession, setCurrentSession] = useState(null);

    useEffect(() => {
        fetch("http://localhost:6543/api/sessions", {
            headers: { "Authorization": localStorage.getItem("token") }
        })
        .then(res => res.json())
        .then(data => {
            setSessions(data.sessions);
            setCurrentSession(data.sessions.find(session => session.is_current)); // Identifica la sesión actual
        });
    }, []);

    const closeSession = async (sessionId) => {
        await fetch(`http://localhost:6543/api/sessions/${sessionId}`, {
            method: "DELETE",
            headers: { "Authorization": localStorage.getItem("token") }
        });
        setSessions(sessions.filter(session => session.id !== sessionId));
    };

    const closeAllSessions = async () => {
        await fetch("http://localhost:6543/api/sessions", {
            method: "DELETE",
            headers: { "Authorization": localStorage.getItem("token") }
        });
        setSessions([]);
    };

    return (
        <div className="max-w-5xl mx-auto mt-10 p-6 bg-white shadow-lg rounded-lg">
            <h2 className="text-3xl font-bold text-gray-700 mb-6 text-center">Sesiones Activas</h2>

            <div className="overflow-x-auto">
                <table className="w-full border-collapse border border-gray-300 rounded-lg shadow-sm">
                    <thead className="bg-gray-200">
                        <tr className="text-gray-700 text-left">
                            <th className="px-4 py-3 border">IP</th>
                            <th className="px-4 py-3 border">Dispositivo</th>
                            <th className="px-4 py-3 border">Inicio</th>
                            <th className="px-4 py-3 border text-center">Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        {sessions.length > 0 ? (
                            sessions.map(session => (
                                <tr
                                    key={session.id}
                                    className={`text-gray-800 text-left ${session.is_current ? "bg-green-100" : "hover:bg-gray-50"}`}
                                >
                                    <td className="px-4 py-3 border">{session.ip_address}</td>
                                    <td className="px-4 py-3 border">{session.device}</td>
                                    <td className="px-4 py-3 border">{session.created_at}</td>
                                    <td className="px-4 py-3 border text-center">
                                        {!session.is_current && (
                                            <button
                                                onClick={() => closeSession(session.id)}
                                                className="bg-red-500 text-white px-3 py-1 rounded flex items-center gap-2 mx-auto hover:bg-red-600 transition"
                                            >
                                                <FaTrash /> Cerrar
                                            </button>
                                        )}
                                    </td>
                                </tr>
                            ))
                        ) : (
                            <tr>
                                <td colSpan="4" className="px-4 py-4 text-center text-gray-500">No hay sesiones activas</td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>

            {sessions.length > 1 && (
                <button
                    onClick={closeAllSessions}
                    className="mt-6 bg-red-600 text-white px-5 py-3 rounded-md w-full flex justify-center items-center gap-2 hover:bg-red-700 transition"
                >
                    <FaSignOutAlt /> Cerrar todas las sesiones
                </button>
            )}
        </div>
    );
};

export default SessionsList;
