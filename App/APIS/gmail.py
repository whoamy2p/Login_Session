
import httplib2
from .Google import Create_Service
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

CLIENTE = "App/APIS/trchatbot.json"
API_NAME = "gmail"
API_VERSION = "v1"
SCOPES = ["https://mail.google.com/"]

try:
    service = Create_Service (CLIENTE, API_NAME, API_VERSION, SCOPES)
except httplib2.error.ServerNotFoundError as googleerror:
    print ("conectate a internet")


def email_send (user, code, email):
    # instacionamos la clase que nos permitira crear el mensaje
    mimeMessage = MIMEMultipart ()
    mimeMessage['subject'] = "restore password".upper ()
    emailMsg = f"""Hi {user}:\n
    We have received a password reset request for your account.\n
    \t\t\t{code}\n
    Copy the code below to change your password.\n
    Please note that this code is only valid for 24 hours. Once the period has elapsed, you will have to request the password reset again."""
    mimeMessage['to'] = f"{email}"

    mimeMessage.attach (MIMEText (emailMsg, 'plain'))  # tipo de texto plain osea sin nada modificado (color o subrayado)

    # decodificamos el mensaje
    Decode_string = base64.urlsafe_b64encode (mimeMessage.as_bytes ()).decode ()

    # consegir la ID del email
    message = service.users().messages().send(userId = "me", body={'raw': Decode_string}).execute()

