from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('', views.HomePageView.as_view(), name='home'),
    path('contact/', views.ContactPageView.as_view(), name='contact'),
    path('services/', views.ServicesPageView.as_view(), name='services'),
    path('account/', views.personalAccView, name='account'),
    path('account/edit/', views.edit_profile, name='account_edit'),
    path('mypakeges/', views.personalPackages, name='mypakeges'),
    path('createPakages/', views.package_create_view, name='createPakages'),
    path('createPakagesEmployeer/', views.package_create_employeer_view, name='createPakagesEmployeer'),
    path('employeerpakages/', views.EmployeerPakegesPageView.as_view(), name='employeerpakages'),
    path('employeerpakages/edit/<int:package_id>/', views.edit_package, name='edit_package'),
]