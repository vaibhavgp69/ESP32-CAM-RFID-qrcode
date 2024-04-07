from rest_framework import serializers

from uuid import uuid4

from .models import Decode


import requests
import cv2

class DecodeViewSerializer(serializers.ModelSerializer):
    status = serializers.CharField(required=False, read_only=True)
    decoded_text = serializers.CharField(required=False, read_only = True)
    decoded_text2 = serializers.CharField(required=False, read_only = True)
    class Meta:
        
        model = Decode
        fields = ["id","file_id",  "decoded_text", "decoded_text2", "status"]    
    
    
    def create(self, data):

        decoded_text = "some stuff"


        diag = Decode.objects.create(
            file_id= data.get("file_id"),
            decoded_text=decoded_text,
        )


        diag.save()
        decoded_text, dt2 = self.decode_qr(data.get("file_id"))
        data['decoded_text'] = decoded_text
        data['decoded_text2'] = dt2
        diag.decoded_text = " qr1 decoded : "+ decoded_text + " qr2 decoded : " + dt2
        diag.save()
        data['status'] = "Decode Created"

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
        qrCodeDetector = cv2.QRCodeDetector()
        all_qrcodes = qrCodeDetector.detectAndDecodeMulti(image)
        if len(all_qrcodes[1]) > 1:
            v1 = all_qrcodes[1][0]
            v2= all_qrcodes[1][1]
            return v1,v2
        elif vertices_array is not None:
            print("QRCode data:")
            print(dec)
            return dec,"no 2nd qr"
             
        else:
            print("There was some error")
            return "error","error"
        
        