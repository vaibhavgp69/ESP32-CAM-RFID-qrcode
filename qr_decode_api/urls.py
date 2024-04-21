from django.urls import path
from . import views

urlpatterns = [
    

path('decode/', views.DecodeView.as_view(), name="decode"),
path('decode/image/', views.DecodeImageView.as_view(), name="decodeimage"),
path('decode/image/top/', views.DecodeTopImageView.as_view(), name="decodetopimage"),
path('decode/image/bottom/', views.DecodeBottomImageView.as_view(), name="decodebottomimage"),
]
