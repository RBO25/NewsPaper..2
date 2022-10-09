from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import ProtectedView

urlpatterns = [
    path('news/', login_required(ProtectedView.as_view())),
    ]