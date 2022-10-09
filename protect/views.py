from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class ProtectedView(LoginRequiredMixin, TemplateView):
    template_name = 'prodected_page.html'
