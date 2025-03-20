from backend.models.user import User
import logging
import smtplib
from email.message import EmailMessage
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pyramid_tm import transaction


logger = logging.getLogger(__name__)

def create_user(db: Session, name: str, email: str, password_hash: str):
    """Registra un nuevo usuario con contraseña cifrada"""
     # Verificar si el usuario ya existe
    usuario_existente = db.query(User).filter(User.email == email).first()
    if usuario_existente:
        logging.warning(f"El email {email} ya está en uso")
        return None
    else:
        user = User(
            name=name,
            email=email,
            hashed_password=User.set_password(password_hash),
        )
        db.add(user)
        try:
            logging .info(f"Registrando nuevo usuario: {name}")
            db.flush()
            db.refresh(user)
            transaction.manager.commit()
            return user
        except IntegrityError:
            transaction.manager.abort()
            return None
    

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_all_users(db: Session):
    return db.query(User).all()


def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        transaction.commit()
        return user
    return None


def send_email(recipient, code):
    """ Función para enviar un correo electrónico desde Pyramid. """
    # Extraer configuraciones SMTP
    smtp_server = "smtp-relay.brevo.com"
    smtp_port = 587
    smtp_user = "82cb39001@smtp-brevo.com"
    smtp_password = "65kyLsVKjm9WX1vD"
    smtp_from = "verification@genixqr.com"
    logger.info(f"SMTP Server: {smtp_server} Puerto: {smtp_port} Usuario: {smtp_user} De: {smtp_from}")
    message_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f4f4f4;">
                <div style="width: 100%; max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
                    <div style="text-align: center; color: #2E86C1;">
                        <h2>Verificación de Cuenta</h2>
                    </div>
                    <div style="text-align: center; font-size: 16px; color: #333;">
                        <p>Tu código de verificación es:</p>
                        <div style="font-size: 30px; color: #2E86C1; font-weight: bold; margin: 20px 0;">
                            {code}
                        </div>
                        <p>Este código es válido por un tiempo limitado.</p>
                        <p>Si no solicitaste este código, puedes ignorar este correo.</p>
                    </div>
                    <div style="text-align: center; font-size: 14px; color: #888; margin-top: 30px;">
                        <p>Atentamente,<br><strong>CRUD</strong></p>
                    </div>
                </div>
            </body>
        </html>
        """


    # Crear el mensaje de correo electrónico
    msg = EmailMessage()
    msg.set_content(f"Tu código de verificación es: {code}", subtype="plain")
    msg.add_alternative(message_body, subtype="html")
    msg['Subject'] = "Codigo de Verificación CRUD"
    msg['From'] = smtp_from
    msg['To'] = recipient

    try:
        # Conectar al servidor SMTP y enviar el mensaje
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.ehlo()  # Identificación con el servidor
            server.starttls()  # Iniciar cifrado TLS
            server.ehlo()  # Vuelve a identificarse
            logger.info(f"Conectado al servidor SMTP {smtp_server}")
            server.login(smtp_user, smtp_password)
            server.send_message(msg)

        logger.info(f"Correo enviado a {recipient}")
        return True

    except Exception as e:
        # En caso de error, registrar y retornar error
        logger.error(f"Error al enviar el correo try Exception: {str(e)}")
        return False