
from controller.BaseController import BaseController

import hmac
import hashlib
import base64
import time

from errors.security.AuthHeaderMissingException import AuthHeaderMissingException
from errors.security.HmacAuth.InvalidSignatureException import InvalidSignatureException
from errors.security.HmacAuth.OutsideTimestampException import OutsideTimestampException
from errors.security.InvalidAuthHeaderException import InvalidAuthHeaderException
from globals import HMAC_SECRET_KEY, HMAC_TIME_WINDOW

class HmacAuthController(BaseController):
    
    def __init__(self):
        super().__init__()
        
    def verify_hmac_signature(self, client_id, signature, timestamp, data) -> bool:
        
        if abs(time.time() - float(timestamp)) > HMAC_TIME_WINDOW:
            raise OutsideTimestampException()
        
        message = f"{client_id}{timestamp}{data}"
        
        expected_signature = hmac.new(
            HMAC_SECRET_KEY.encode(), message.encode(), hashlib.sha256
        ).digest()
        
        expected_signature_base64 = base64.b64encode(expected_signature).decode()
        
        if not hmac.compare_digest(signature, expected_signature_base64):
            raise InvalidSignatureException()
        
        return True
    
    def read_signature_header(self, headers) -> str:
        
        auth_header = headers.get("Authorization")
        if not auth_header:
            raise AuthHeaderMissingException()
        
        try:
            scheme, credentials = auth_header.split(" ", 1)
            if scheme.lower() != "hmac":
                raise InvalidAuthHeaderException("Authorization scheme must be 'hmac'")
            client_id, signature, timestamp = credentials.split(":")
        except ValueError:
            raise InvalidAuthHeaderException()

        return client_id, signature, timestamp
    
    def generate_hmac_signature(client_id, secret_key:str, timestamp, data):
        message = f"{client_id}{timestamp}{data}"
        signature = hmac.new(secret_key.encode(), message.encode(), hashlib.sha256).digest()
        signature_base64 = base64.b64encode(signature).decode()
        return signature_base64