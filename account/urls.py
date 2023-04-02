from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('register/', views.RegisterUserView.as_view()),
    path('profile/', views.ProfileView.as_view()),
    path('profile/ad/', views.UserADView.as_view()),
    path('profile/update/', views.ProfileUpdateView.as_view()),
    path('profile/change-password/', views.ChangePasswordView.as_view()),
]
