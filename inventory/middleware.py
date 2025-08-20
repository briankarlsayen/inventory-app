import time
import json
from django.utils.deprecation import MiddlewareMixin
from .models import Logs, User
from django.utils.timezone import now
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import JsonResponse
from rest_framework.permissions import BasePermission

class RequestLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.method.upper() == "GET":
            request._skip_logging = True
            return
        
        request._start_time = time.time()
        
        body = ""
        if request.body:
            try:
                body_data = json.loads(request.body)
                body_data.pop("password", None)  # remove password params on req body
                
                body = json.dumps(body_data)
            except Exception:
                body = request.body.decode("utf-8", errors="ignore")

        log = Logs.objects.create(
            method=request.method,
            path=request.path,
            query_params=request.META.get("QUERY_STRING", ""),
            body=body,
            remote_addr=self.get_client_ip(request)
        )
        request._log_id = log.id

    def process_response(self, request, response):
        if getattr(request, "_skip_logging", False):
            return response
        
        try:
            log = Logs.objects.get(id=getattr(request, "_log_id", None))
            log.status_code = response.status_code
            log.response_body = getattr(response, "content", b"").decode("utf-8", errors="ignore")
            log.finished_at = now()
            log.duration_ms = round((time.time() - request._start_time) * 1000, 2)
            log.save()
        except Exception:
            pass

        return response
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")
    

class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        user_id = validated_token.get('user_id')

        try:
            # Use this if you use MongoEngine or ObjectId string keys
            return User.objects.get(id=str(user_id))
        except User.DoesNotExist:
            return None

class RoleBasedMethodPermission(BasePermission):
    # Let's assume roles: 1=SuperAdmin, 2=Admin, 3=Guest
    RESTRICTED_METHODS = {
        3: ["POST", "PUT", "DELETE"],  # guest cannot modify
        # role 1 & 2 (admin) has no restrictions
    }

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False  # or True if you allow anonymous access

        role = getattr(request.user, "role", None)
        restricted = self.RESTRICTED_METHODS.get(role, [])
        if request.method in restricted:
            return False
        return True