from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.db.session import SessionLocal
from app.models.audit import AuditLog
from app.core.security import SECRET_KEY, ALGORITHM
from jose import jwt
import json

class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Only audit modification requests
        if request.method not in ["POST", "PUT", "DELETE", "PATCH"]:
            return response
            
        # Only audit successful requests (or client errors?) - let's audit all non-GET
        # But we need user info.
        # User info is in Authorization header.
        
        try:
            auth = request.headers.get("Authorization")
            user_id = None
            tenant_id = None # We might not be able to get tenant_id easily from token if it's not in it, but we can try.
            # Token usually has 'sub' which is user_id.
            
            if auth and auth.startswith("Bearer "):
                token = auth.split(" ")[1]
                try:
                     payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                     user_id = payload.get("sub")
                     # We could fetch user to get tenant_id, but that's expensive for middleware?
                     # Ideally token should have tenant_id.
                except:
                    pass
            
            # Helper to extract resource from path
            # /api/v1/contacts/ -> contacts
            path_parts = request.url.path.strip("/").split("/")
            resource = path_parts[-1] if path_parts else "unknown"
            if len(path_parts) > 3: # api/v1/contacts/123
                resource = path_parts[-2] # contacts

            # We can't easily read request body here without consuming it (unless we duplicate it)
            # For now, just log action and resource
            
            db = SessionLocal()
            audit = AuditLog(
                user_id=uuid.UUID(user_id) if user_id else None,
                # tenant_id: skipping for now as we don't have it in token payload yet
                action=request.method,
                resource=resource,
                details={"path": request.url.path, "status": response.status_code}
            )
            db.add(audit)
            db.commit()
            db.close()
            
        except Exception as e:
            print(f"Audit Error: {e}")
            
        return response

import uuid
