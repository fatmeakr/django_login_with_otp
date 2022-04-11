from django.urls import path
from .views import HomeView, LogoutView, OtpGenerateView, OtpVerificationView


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("login/", OtpGenerateView.as_view(), name="login"),
    path(
        "login/verification", OtpVerificationView.as_view(), name="login_verification"
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
]
