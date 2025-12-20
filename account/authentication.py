from rest_framework_simplejwt.authentication import JWTAuthentication

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # try to get access toke from the cookie first
        raw_token = request.COOKIES.get('access')

        if raw_token is None:
            # Fall back to Authorization header
            return super().authenticate(request)
        
        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token