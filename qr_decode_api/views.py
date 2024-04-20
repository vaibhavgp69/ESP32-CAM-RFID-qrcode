
from rest_framework import generics
from .models import Decode, DecImage
from .serializers import DecodeViewSerializer, DecodeImageViewSerializer



class DecodeView(generics.ListCreateAPIView):
    queryset = Decode.objects.all()
    serializer_class = DecodeViewSerializer

class DecodeImageView(generics.ListCreateAPIView):
    queryset = DecImage.objects.all()
    serializer_class = DecodeImageViewSerializer

    