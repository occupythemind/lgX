from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.conf import settings

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        # check if the user wants to be remembered for 2 weeks
        remember_me = request.data.get('remember_me', False)

        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')

            if remember_me:
                refresh_max_age = 14 * 86400 # 14 days (2 weeks)
            else:
                refresh_max_age = 86400 # 1 day

            # set access token in HTTPOnly cookie
            response.set_cookie(
                key='access',
                value=access_token,
                httponly=True,
                secure=not settings.DEBUG, # True in Pro. env. and False in dev.
                samesite='Lax',
                # we may adjust this based on if the user chooses that his access token lasts 2wks max
                max_age=900, # 15 mins in sec.
                path='/'
            )

            # set refresh token in HTTPOnly cookie
            response.set_cookie(
                key='refresh',
                value=refresh_token,
                httponly=True,
                secure=not settings.DEBUG,
                samesite='Lax',
                max_age=refresh_max_age,
                path='/'
            )

            # remove token from response body
            response.data = {'detail': 'Successfully logged in', 'remember_me': remember_me}

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