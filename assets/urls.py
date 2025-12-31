from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = 'assets'

urlpatterns = [
    path('', RedirectView.as_view(url='/admin/', permanent=False), name='index'),
]
