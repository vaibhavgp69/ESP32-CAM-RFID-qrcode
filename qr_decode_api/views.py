
from rest_framework import generics
from .models import Decode, DecImage
from .serializers import DecodeViewSerializer, DecodeImageViewSerializer, DecodeTopImageViewSerializer,DecodeBottomImageViewSerializer



class DecodeView(generics.ListCreateAPIView):
    queryset = Decode.objects.all()
    serializer_class = DecodeViewSerializer

class DecodeImageView(generics.ListCreateAPIView):
    queryset = DecImage.objects.all()
    serializer_class = DecodeImageViewSerializer

class DecodeTopImageView(generics.ListCreateAPIView):
    queryset = DecImage.objects.all()
    serializer_class = DecodeTopImageViewSerializer


class DecodeBottomImageView(generics.ListCreateAPIView):
    queryset = DecImage.objects.all()
    serializer_class = DecodeBottomImageViewSerializer



    