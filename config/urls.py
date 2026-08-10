"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from apps.user.views import (
    RegisterView, CustomTokenObtainPairView,
    RequestPasswordResetView, ConfirmPasswordResetView,
    UserViewSet
)
from apps.project.views import ProjectViewSet
from apps.task.views import TaskViewSet
from apps.core.views import HealthCheckView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/register/', RegisterView.as_view(), name='register'),
    path('api/v1/password-reset/', RequestPasswordResetView.as_view(), name='password_reset'),
    path('api/v1/password-reset/confirm/', ConfirmPasswordResetView.as_view(), name='password_reset_confirm'),
    path('api/v1/health/', HealthCheckView.as_view(), name='health_check'),
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/v1/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/v1/jobs/<str:job_id>/', include('django_rq.urls')),  
]

