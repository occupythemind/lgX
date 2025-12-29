from django.urls import path
from .views import CustomTokenObtainPairView, CustomTokenRefreshView, LogoutView, SignUpView

app_name = 'auth'

urlpatterns = [
    path('signup/', SignUpView.as_view()),
    path('token/', CustomTokenObtainPairView.as_view()), # get token
    path('token/refresh/', CustomTokenRefreshView.as_view()), # refresh token
    path('logout/', LogoutView.as_view()), # logout (ie. delete token)
]