from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from account.views import CustomTokenObtainPairView, CustomTokenRefreshView, LogoutView
from .views import TopicAPIView, EntryAPIView

app_name = 'notepad'

urlpatterns = [
    path('api/token/', CustomTokenObtainPairView.as_view()),
    path('api/token/refresh/', CustomTokenRefreshView.as_view()),
    path('api/logout/', LogoutView.as_view()),
]

router = DefaultRouter()
router.register('topics', TopicAPIView, basename='topics')
router.register('entries', EntryAPIView, basename='entries')

topic_router = NestedDefaultRouter(router, 'topics', lookup='topic')
topic_router.register('entries', EntryAPIView, basename='topic-entry')

urlpatterns += [
    path('api/', include(router.urls)),
    path('api/', include(topic_router.urls)),
]