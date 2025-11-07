from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from config.settings import EMAIL_HOST_USER
from .forms import CustomUserCreationForm
from django.contrib.auth import login
from django.core.mail import send_mail

class RegisterView(FormView):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.send_welcome_email(user.email)
        return super().form_valid(form)

    def send_welcome_email(self, user_email):
        subject = 'Добро пожаловать в SkyAppStore'
        message = 'Спасибо, что зарегистрировались в SkyAppStore!'
        from_email = EMAIL_HOST_USER
        recipient_list = [user_email,]
        send_mail(subject, message, from_email, recipient_list)
