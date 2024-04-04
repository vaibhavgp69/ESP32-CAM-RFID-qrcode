
from rest_framework import generics
from .models import Decode
from .serializers import DecodeViewSerializer



class DecodeView(generics.ListCreateAPIView):
    queryset = Decode.objects.all()
    serializer_class = DecodeViewSerializer