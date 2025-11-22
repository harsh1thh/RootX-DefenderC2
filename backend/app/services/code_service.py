import secrets
import threading
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional, Any

class CodeService:
    def __init__(self):
        self._storage: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()

    def gen_12hex(self) -> str:
        """Generates a secure 12-hex Centralized ID."""
        return secrets.token_hex(6).upper()

    def create_code(self, owner: Optional[str] = None, ttl_seconds: int = 3600) -> Dict[str, Any]:
        """
        Generates a code and stores it with an expiry timestamp.
        """
        central_id = self.gen_12hex()
        now = datetime.now(timezone.utc)
        expires_at = now + timedelta(seconds=ttl_seconds)
        
        record = {
            "central_id": central_id,
            "owner": owner,
            "created_at": now.isoformat(),
            "expires_at": expires_at.isoformat()
        }

        with self._lock:
            self._storage[central_id] = record
            
        return {
            "central_id": central_id,
            "expires_at": expires_at.isoformat()
        }

    def validate_code(self, code: str) -> Optional[Dict[str, Any]]:
        """
        Checks if a code exists and is not expired.
        """
        with self._lock:
            record = self._storage.get(code)
            if not record:
                return None
            
            expires_at = datetime.fromisoformat(record["expires_at"])
            if datetime.now(timezone.utc) > expires_at:
                return None
                
            return record

    def cleanup_expired(self) -> int:
        """
        Removes expired codes from storage. Returns count of removed items.
        """
        now = datetime.now(timezone.utc)
        to_remove = []
        
        with self._lock:
            for code, record in self._storage.items():
                expires_at = datetime.fromisoformat(record["expires_at"])
                if now > expires_at:
                    to_remove.append(code)
            
            for code in to_remove:
                del self._storage[code]
                
        return len(to_remove)

code_service = CodeService()
