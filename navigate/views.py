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
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserChangeForm,PackageFilterForm, PakagesForm, ChangeUserForm, PakagesEmployeeForm, PackageEditForm
# Create your views here.

class HomePageView(TemplateView):
    template_name = 'home.html'

class ContactPageView(TemplateView):
        template_name = 'contact.html'


class ServicesPageView(TemplateView):
    template_name = 'services.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tracking_number = self.request.GET.get('tracking_number', '')

        if tracking_number:
            try:
                tracking_number = int(tracking_number)
                package = Package.objects.filter(id=tracking_number).first()
                if package:
                    context['package'] = package
                else:
                    context['error'] = 'Посылка с таким номером не найдена.'
            except ValueError:
                context['error'] = 'Некорректный номер посылки.'
        return context

class AccountPageView(TemplateView):
    template_name = 'account.html'

# def package_create_view(request):
#     if request.method == 'POST':
#         form = PakagesForm(request.POST)
#         if form.is_valid():
#             Package.client_id = request.CustomUser
#             form.save()
#     else:
#         form = PakagesForm()
#     return render(request, 'mypakages.html')

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = PackageFilterForm(self.request.GET or None)

        queryset = Package.objects.all()
        if form.is_valid():
            if form.cleaned_data.get('status'):
                queryset = queryset.filter(status=form.cleaned_data['status'])
            if form.cleaned_data.get('sending_address'):
                queryset = queryset.filter(sending_address=form.cleaned_data['sending_address'])
            if form.cleaned_data.get('delivery_address'):
                queryset = queryset.filter(delivery_address=form.cleaned_data['delivery_address'])
            if form.cleaned_data.get('date_of_issue'):
                queryset = queryset.filter(date_of_issue=form.cleaned_data['date_of_issue'])
            if form.cleaned_data.get('delivery_date'):
                queryset = queryset.filter(delivery_date=form.cleaned_data['delivery_date'])
            if form.cleaned_data.get('date_of_receipt'):
                queryset = queryset.filter(date_of_receipt=form.cleaned_data['date_of_receipt'])
            if form.cleaned_data.get('cargo_category'):
                queryset = queryset.filter(cargo_category=form.cleaned_data['cargo_category'])
            if form.cleaned_data.get('client'):
                queryset = queryset.filter(client_id=form.cleaned_data['client'])
            if form.cleaned_data.get('package_id'):
                queryset = queryset.filter(id=form.cleaned_data['package_id'])

        context['object_list'] = queryset
        context['filter_form'] = form
        return context
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


@login_required
def package_create_view(request):
    if request.user.is_authenticated and not request.user.is_anonymous:
        if request.method == 'POST':
            form = PakagesForm(request.POST)
            if form.is_valid():
                package = form.save(commit=False)
                package.client_id = request.user
                package.save()
                return redirect('mypakeges')
        else:
            form = PakagesForm()
        return render(request, 'package_create.html', {'form': form})
    else:
        return redirect('login')

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

            user.save()
            return redirect('home')
    else:
        form = ChangeUserForm(instance=request.user)

    return render(request, 'account_edit.html', {'form': form})
@login_required
def personalPackages(request):
    user = request.user
    if user.is_authenticated and not user.is_anonymous:
        packages = Package.objects.filter(client_id = user)
        return render(request, 'mypakeges.html', {'user': user, 'packages': packages})
    else:
        return redirect('login')

# class ClpersonalPackages(LoginRequiredMixin, ListView):
#     model = Package
#     template_name = 'mypakeges.html'
#     login_url = 'login'
#
#     def get_form(self, form_class=None):
#         user = self.request.user
#         packages = Package.objects.filter(client_id=user)
#         return render(self.request, 'mypackages.html', {'user': user, 'packages': packages})


def edit_package(request, package_id):
    package = get_object_or_404(Package, id=package_id)

    if request.method == 'POST':
        form = PackageEditForm(request.POST, instance=package)
        if form.is_valid():
            form.save()
            return redirect('employeerpakages')
    else:
        form = PackageEditForm(instance=package)

    return render(request, 'edit_package.html', {'form': form})

