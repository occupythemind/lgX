from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.throttling import AnonRateThrottle
from rest_framework import status
from django.conf import settings
from .serializers import AccountSerializer, EmailTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        remember_me = request.data.get("remember_me", False)

        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data.get("access")
            refresh_token = response.data.get("refresh")

            refresh_max_age = 14 * 86400 if remember_me else 86400

            response.set_cookie(
                key="access",
                value=access_token,
                httponly=True,
                secure=not settings.DEBUG,
                samesite="Lax",
                max_age=900,  # 15 min
                path="/",
            )

            response.set_cookie(
                key="refresh",
                value=refresh_token,
                httponly=True,
                secure=not settings.DEBUG,
                samesite="Lax",
                max_age=refresh_max_age,
                path="/",
            )

            response.data = {
                "detail": "Successfully logged in",
                "remember_me": remember_me,
            }

        return response

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh')
        remember_me = request.data.get('remember_me', False) # remember me

        if refresh_token is None:
            return Response(
                {'detail': 'Refresh token not found in cookies'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Build serializer data explicitly
        serializer = self.get_serializer(
            data={'refresh': refresh_token}
        )

        serializer.is_valid(raise_exception=True)

        response = Response(
            {'detail': 'Token refreshed successfully'},
            status=status.HTTP_200_OK
        )

        access_token = serializer.validated_data.get('access')

        if remember_me:
            refresh_max_age = 14 * 86400 # 14 days (2 weeks)
        else:
            refresh_max_age = 86400 # 1 day

        # Set access token cookie
        response.set_cookie(
            key='access',
            value=access_token,
            httponly=True,
            secure=not settings.DEBUG,
            samesite='Lax',
            max_age=900, # 15 mins
            path='/'
        )

        # Handle refresh token rotation
        if 'refresh' in serializer.validated_data:
            response.set_cookie(
                key='refresh',
                value=serializer.validated_data['refresh'],
                httponly=True,
                secure=not settings.DEBUG,
                samesite='Lax',
                max_age=refresh_max_age,
                path='/'
            )

        return response

class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        response = Response({'detail': 'Successfully logged out'}, status=status.HTTP_200_OK)

        # delete the access token cookie
        response.delete_cookie(
            key='access',
            path='/',
            samesite='Lax'
        )

        # delete the refresh token cookie
        response.delete_cookie(
            key='refresh',
            path='/',
            samesite='Lax'
        )

        return response
    

class SignUpView(CreateAPIView):
    # This view will auto-reject GET/PUT/PATCH/DELETE requests
    serializer_class = AccountSerializer
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

