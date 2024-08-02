from django.urls import path
from userauths import views
from userauths.views import *

app_name = "userauths"

urlpatterns = [
    path("sign-up/", views.register_view, name="sign-up"),
    path("sign-in/", views.login_view, name="sign-in"),
    path("sign-out/", views.logout_view, name="sign-out"),
    path('submit_consultation_form/', submit_consultation_form, name='submit_consultation_form'),
    path('password-reset-request/', password_reset_request_view, name='password-reset-request'),
    path('password-reset/<str:token>/', password_reset_view, name='password-reset'),
    path("verify/<str:token>/", views.verify_email, name="verify-email"),
]
