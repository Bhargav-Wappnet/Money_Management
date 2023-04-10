from authentication import views
from django.urls import path

urlpatterns = [
    path("", views.home, name='home'),
    path("signup", views.signup, name='signup'),
    path("verification/<int:user_id>/", views.verification, name='verification'),
    path('activation-success/', views.activation_success, name='activation_success'),
    path("signin", views.signin, name='signin'),
    path("forgetpass", views.forgetpass, name='forgetpass'),
    path("forgetpassform/<int:user_id>/", views.forgetpassform, name='forgetpassform'),
    path('logout', views.signout, name="logout"),
]
