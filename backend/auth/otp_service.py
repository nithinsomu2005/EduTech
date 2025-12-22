import random
from datetime import datetime, timedelta
from typing import Optional

class OTPService:
    def __init__(self):
        self.otp_store = {}
    
    def generate_otp(self, mobile: str) -> str:
        otp = str(random.randint(100000, 999999))
        expires_at = datetime.utcnow() + timedelta(minutes=5)
        self.otp_store[mobile] = {
            'otp': otp,
            'expires_at': expires_at,
            'attempts': 0
        }
        return otp
    
    def verify_otp(self, mobile: str, otp: str) -> bool:
        if mobile not in self.otp_store:
            return False
        
        stored = self.otp_store[mobile]
        
        if datetime.utcnow() > stored['expires_at']:
            del self.otp_store[mobile]
            return False
        
        if stored['attempts'] >= 3:
            del self.otp_store[mobile]
            return False
        
        stored['attempts'] += 1
        
        if stored['otp'] == otp:
            del self.otp_store[mobile]
            return True
        
        return False

otp_service = OTPService()
