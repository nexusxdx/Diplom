from django.views import generic
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

from django.db.models import Q
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required

from . import forms
from main_app import models


class HomePageView(generic.ListView):
    model = models.Author
    template_name = 'home.html'

    def get_queryset(self, *args, **kwargs):
        lists = models.Author.objects.all()
        f_query = self.request.GET.get('f')
        l_query = self.request.GET.get('l')
        p_query = self.request.GET.get('p')
        r_query = self.request.GET.get('r')

        if f_query or l_query or p_query or r_query:
            lists = lists.filter(rank__icontains=r_query)
            lists = lists.filter(first_name__icontains=f_query)
            lists = lists.filter(last_name__icontains=l_query)
            lists = lists.filter(profession__icontains=p_query)

        return lists


class SignUpView(generic.CreateView):
    template_name = 'accounts/signup.html'
    form_class = forms.SignUpForm
    success_url = reverse_lazy('login')


class LoginView(generic.FormView):
    template_name = 'accounts/login.html'
    form_class = forms.LoginForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(self.request, user)
            return super().form_valid(form)
        else:
            return super().form_invalid(form)


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('home'))
