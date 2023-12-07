from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.views.generic import TemplateView
from .models import Package, CustomUser, PointIssue
from django.http import JsonResponse
from . import models
from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from django import forms

from .forms import CustomUserCreationForm, CustomUserChangeForm, PakagesForm, ChangeUserForm, PakagesEmployeeForm
# Create your views here.

class HomePageView(TemplateView):
    template_name = 'home.html'

class ContactPageView(TemplateView):
        template_name = 'contact.html'


class ServicesPageView(TemplateView):
    template_name = 'services.html'
    model = Package

    def get_context_data(self, **kwargs):
        context = super(ServicesPageView, self).get_context_data(**kwargs)
        search_id = self.request.GET.get('search_id')
        if search_id:
            context['packages'] = Package.objects.filter(id = search_id)
        else:
            context['packages'] = Package.objects.none()
        return context
            # queryset =queryset.filter(id = search_id)
        # search_id = self.request.GET.get('search_id')
        # queryset = Package.objects.all()
        # if search_id:
        #     queryset =queryset.filter(id = search_id)
        # return queryset

class AccountPageView(TemplateView):
    template_name = 'account.html'

def package_create_view(request):
    if request.method == 'POST':
        form = PakagesForm(request.POST)
        if form.is_valid():
            Package.client_id = request.CustomUser
            form.save()
    else:
        form = PakagesForm()
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

class EmployeerPakegesPageView(TemplateView):
        template_name = 'employeerpakages.html'
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
        form = PakagesForm(request.POST)
        if form.is_valid():
            Package.Packages_as_client = request.user
            form.save()
            return redirect('mypakeges')
    else:
        form = PakagesForm()
    return render(request, 'package_create.html', {'form': form})

def package_create_employeer_view(request):
    if request.method == 'POST':
        form = PakagesEmployeeForm(request.POST)
        if form.is_valid():

            form.save()
            return redirect('base')
    else:
        form = PakagesEmployeeForm()
    return render(request, 'package_create_employeer.html', {'form': form})

class CustomUserUpdateView(LoginRequiredMixin, UpdateView):

    form_class = ChangeUserForm
    # fields = ('first_name', 'last_name', 'patronymic', 'phone_number', 'email', 'passport', 'date_of_birth',
    #           'username')
    widgets = {
        'date_of_birth': forms.DateInput(attrs={'type': 'date', 'required': 'required'},
                                             format='%Y-%m-%d')
    }
    template_name = 'account_edit.html'



def search_adress(request):
    result = PointIssue.city
    return render(request, "packege_create.html",{"PointIssue": result})

def edit_profile(request):
    if request.method == 'POST':
        form = ChangeUserForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            #if not form.cleaned_data['password']:
               # user.password = CustomUser.objects.get(pk=user.pk).password
           # else:
                #new_password = form.cleaned_data['password']
                #user.password = make_password(new_password)
            user.save()
            return redirect('home')
    else:
        form = ChangeUserForm(instance=request.user)

    return render(request, 'account_edit.html', {'form': form})

def personalPackages(request):
    user = request.user
    if user.is_authenticated and not user.is_anonymous:
        packages = Package.objects.filter(client_id = user)
        return render(request, 'mypakeges.html', {'user': user, 'packeges': packages})
    else:
        return redirect('login')

class ClpersonalPackages(LoginRequiredMixin, ListView):
    model = Package
    template_name = 'mypakeges.html'
    login_url = 'login'

    def get_form(self, form_class=None):
        user = self.request.user
        packages = Package.objects.filter(client_id=user)
        return render(self.request, 'mypackages.html', {'user': user, 'packages': packages})



