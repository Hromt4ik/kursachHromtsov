from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('', views.HomePageView.as_view(), name='home'),
    path('contact/', views.ContactPageView.as_view(), name='contact'),
    path('services/', views.ServicesPageView.as_view(), name='services'),
    path('account/', views.personalAccView, name='account'),
    path('account/edit/<int:pk>', views.CustomUserUpdateView.as_view(), name='account_edit'),
    path('mypakeges/', views.MypakegesPageView.as_view(), name='mypakeges'),
    path('createPakages/', views.package_create_view, name='createPakages')
]