from backend_shared.database import db_connection, db_utils, db_executer
from backend_shared.security import verifier, token
from backend_shared.logger import logger
from backend_shared.utils import random
from backend_shared.types import BusinessResponse
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class RequestHandler:
    def __init__(self, config):
        self.config = config
        self.db_connection = db_connection.Connection(self.config["database"]["hostname"], self.config["database"]["user"]["username"], self.config["database"]["user"]["password"], self.config["database"]["name"], self.config["database"]["port"])
        self.verifier = verifier.Verifier(self.db_connection, self.config)
        self.db_executer = db_executer.Executer(self.db_connection, self.config)
        self.db_utils = db_utils.DBUtils()
        self.logger = logger.Logger()
        self.random = random.Random()
        self.tokenizer = token.Tokenizer(self.config)
        self.mailserver = self.init_mailserver()


    def init_mailserver(self):
        try:
            server = smtplib.SMTP(self.config["mail_server_credentials"]["host"], 587)
            server.starttls()
            server.login(self.config["mail_server_credentials"]["username"], self.config["mail_server_credentials"]["password"])
            return server
        except Exception as e: self.logger.log("ERROR", f"Can't initialize mail server connection || error => {e}")

    def send_mail(self, request):
        try:
            data = request.json
            if not self.mailserver: return BusinessResponse(self.random.CreateRandomId(), "error-sending-mail | no mail-server", []).toJson()
            if not data: return BusinessResponse(self.random.CreateRandomId(), "error-sending-mail | missing data", []).toJson()
            msg = MIMEMultipart("alternative")
            msg["Subject"] = data["Subject"]
            msg["From"] = data["From"]
            msg["To"] = data["To"]
            msg.attach(MIMEText("Open this email in a different programm please - I am sorry!", "text"))
            msg.attach(MIMEText(data["Content"], "html"))
            self.mailserver.send_message(msg)
            return BusinessResponse(self.random.CreateRandomId(), "email-send", []).toJson()
        except Exception as e: 
            self.logger.log("ERROR", f"Can't send email || error => {e}")
            return BusinessResponse(self.random.CreateRandomId(), "error-sending-mail", []).toJson()
    