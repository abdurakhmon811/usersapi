from django.urls import path
from rest_framework.authtoken import views
from .views import EmployeesView, ProfileView, RegisterView


urlpatterns = [
    path('get-user-token/', views.obtain_auth_token),
    path('register/', RegisterView.as_view()),
    path('employees/', EmployeesView.as_view()),
    path('profile/', ProfileView.as_view()),
]