from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.views.generic import TemplateView
from .models import Package, CustomUser
from django.http import JsonResponse
from . import models
from django.shortcuts import render
from django import forms
from .forms import CustomUserCreationForm, CustomUserChangeForm, PackageForm, ChangeUserForm
# Create your views here.


class HomePageView(TemplateView):
    template_name = 'home.html'

class ContactPageView(TemplateView):
        template_name = 'contact.html'


class ServicesPageView(TemplateView):
    template_name = 'services.html'

class AccountPageView(TemplateView):
    template_name = 'account.html'

def package_create_view(request):
    if request.method == 'POST':
        form = PackageForm(request.POST)
        if form.is_valid():
            Package.client_id = request.CustomUser
            form.save()
    else:
        form = PackageForm()
    return render(request, 'mypakages.html')

def personalAccView(request):
    # Получаем текущего пользователя
    user = request.user


    if user.is_authenticated and not user.is_anonymous:
        # reservations = Reservation.objects.filter(client=user)
        return render(request, 'account.html', {'user': user})
    else:
        return redirect('login')

class MypakegesPageView(TemplateView):
    template_name = 'mypakeges.html'
class SignUp(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

def package_detail(request):
    package_id = request.GET.get('id')

    if package_id:
        try:
            package = get_object_or_404(Package, pk=package_id)
            # Формируйте ответ в JSON-формате
            return JsonResponse({'message': 'Информация о посылке: ...'})  # Здесь должны быть детали посылки
        except ValueError:
            return JsonResponse({'message': 'Неверный формат ID'})

    return JsonResponse({'message': 'Введите ID посылки'})

def package_create_view(request):
    if request.method == 'POST':
        form = PackageForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = PackageForm()
    return render(request, 'package_create.html', {'form': form})

class CustomUserUpdateView(LoginRequiredMixin, UpdateView):

    form_class = ChangeUserForm
    # fields = ('first_name', 'last_name', 'patronymic', 'phone_number', 'email', 'passport', 'date_of_birth',
    #           'username')
    widgets = {
        'date_of_birth': forms.DateInput(attrs={'type': 'date', 'required': 'required'},
                                             format='%Y-%m-%d')
    }
    template_name = 'account_edit.html'