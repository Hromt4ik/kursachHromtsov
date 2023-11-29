from django.shortcuts import render
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.views.generic import TemplateView

from django.http import JsonResponse
from . import models
from .forms import CustomUserCreationForm
# Create your views here.


class HomePageView(TemplateView):
    template_name = 'home.html'

class ContactPageView(TemplateView):
        template_name = 'contact.html'


class ServicesPageView(TemplateView):
    template_name = 'services.html'

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