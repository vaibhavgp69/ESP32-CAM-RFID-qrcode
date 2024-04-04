from rest_framework import serializers

from uuid import uuid4

from .models import Decode


import requests
import cv2

class DecodeViewSerializer(serializers.ModelSerializer):
    status = serializers.CharField(required=False, read_only=True)
    decoded_text = serializers.CharField(required=False, read_only = True)
    class Meta:
        
        model = Decode
        fields = ["id","file_id",  "decoded_text", "status"]    
    
    
    def create(self, data):

        decoded_text = "some stuff"


        diag = Decode.objects.create(
            file_id= data.get("file_id"),
            decoded_text=decoded_text,
        )


        diag.save()
        decoded_text = self.decode_qr(data.get("file_id"))
        diag.decoded_text = decoded_text
        diag.save()
        data['status'] = "Decode Created"
        data['decoded_text'] = diag.decoded_text
        return data
    


    def decode_qr(self, file_id):
        url = f'https://drive.google.com/uc?export=download&id={file_id}'

        response = requests.get(url)

        # Save the image to a local file
        with open('qr_code_image.jpg', 'wb') as f:
            f.write(response.content)
        filename = 'qr_code_image.jpg'
        image = cv2.imread(filename)
        detector = cv2.QRCodeDetector()
        dec, vertices_array, binary_qrcode = detector.detectAndDecode(image)
        if vertices_array is not None:
            print("QRCode data:")
            print(dec)
            return dec
        else:
            print("There was some error")
            return "error"
        
        