from flask import Flask, request
from .requestHandler import RequestHandler
import os

api = Flask(__name__)

request_handler = None

base_route = "/api/v1"
data_path = f"{os.getcwd()}/binarys"

@api.route("/", methods=["GET"])
def index():
    return "200 OK from mail-service"

@api.route(f"{base_route}/healthz", methods=["GET"])
def healthz():
    return "200 OK from mail-service"

@api.route(f"{base_route}/send-mail", methods=["POST"])
def send_mail():
    return request_handler.send_mail(request)

def run(conf):
    global config, request_handler
    config = conf
    request_handler = RequestHandler(config)
    if config["account_service"]["cors_enabled"]:
        from flask_cors import CORS
        cors = CORS(api)
    api.run(host=config["account_service"]["hostname"], port=config["account_service"]["port"])
