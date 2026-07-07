from django.urls import path

from accounts.views import (
    LogoutView,
    MeView, 
    RegisterView,
    UpdateView,
    LoginView,
    RefreshView,
    VerifyView,
)

urlpatterns = [
    path('me/', MeView.as_view(), name="me"),
    path('register/', RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('updade/', UpdateView.as_view(), name="update"),
    path('refresh/', RefreshView.as_view(), name="refresh"),
    path('verify/', VerifyView.as_view(), name="verify"),
]
