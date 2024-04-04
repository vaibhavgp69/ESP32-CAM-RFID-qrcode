from django.urls import path
from . import views

urlpatterns = [
    

path('decode/', views.DecodeView.as_view(), name="decode"),

]
