from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from .forms import SignUpForm
from .models import CustomUser


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'signup.html'
    success_url = reverse_lazy('○○○○')  #成功した場合飛ばしたい場所のurl おそらくTOP画面

    def form_valid(self, form):
        valid_response = super().form_valid(form)
        login(self.request, self.object)

        return valid_response
    
class MyLoginView(LoginView):
    template_name = 'login.html'