from rest_framework import serializers

from uuid import uuid4

from .models import Decode, DecImage


import os


import requests
import cv2
import base64
import pyqrcode
from pyzbar.pyzbar import decode
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------


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
        

# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------








class DecodeImageViewSerializer(serializers.ModelSerializer):
    status = serializers.CharField(required=False, read_only=True)
    top_img_url = serializers.CharField(required=False, read_only = True)
    bottom_img_url = serializers.CharField(required=False, read_only = True)
    decoded_text = serializers.CharField(required=False, read_only = True)
    decoded_text2 = serializers.CharField(required=False, read_only = True)
    class Meta:
        
        model = DecImage
        fields = ["id","rep","name","top_image","bottom_image", "top_img_url","bottom_img_url", "decoded_text", "decoded_text2", "status"]    
    
    
    def create(self, data):

        decoded_text = "write"
        data['status'] = ''

        diag_filter = DecImage.objects.filter(rep=data.get("rep")).first()
        if diag_filter == None:
            diag = DecImage.objects.create(
                rep = data.get("rep"),
                name = data.get("name"),
                top_image = data.get("top_image"),
                bottom_image = data.get("bottom_image"),
                decoded_text=decoded_text,
            )
                
            diag.save()
            data['status'] += self.name_sheet(diag.name,decoded_text) + " -----> "
            decoded_text, dt2 = self.decode_qr(diag.top_image.url)
            data['decoded_text'] = decoded_text
            data['decoded_text2'] = dt2
            diag.decoded_text = "aqr1 decoded : "+ decoded_text + " qr2 decoded : " + dt2
            diag.save()
            data['status'] += self.img1_sheet(diag.top_image.url,decoded_text,dt2) + " -----> "
            data['status'] += self.img2_sheet(diag.bottom_image.url,"none") 
        else:
            data['status'] += " Updating existing entry -----> "
            diag =  DecImage.objects.get(rep = data.get("rep"), name = data.get("name"))
            diag.top_image = data.get("top_image")
            diag.bottom_image = data.get("bottom_image")
            decoded_text = "write"
            diag.save()
            data['status'] += self.name_sheet(diag.name,decoded_text) + " -----> "
            decoded_text, dt2 = self.decode_qr(diag.top_image.url)
            data['decoded_text'] = decoded_text
            data['decoded_text2'] = dt2
            diag.decoded_text = "aqr1 decoded : "+ decoded_text + " qr2 decoded : " + dt2
            diag.save()
            data['status'] += self.img1_sheet(diag.top_image.url,decoded_text,dt2) + " -----> "
            data['status'] += self.img2_sheet(diag.bottom_image.url,"update") 


        data['top_img_url'] = diag.top_image.url
        data['bottom_img_url'] = diag.bottom_image.url

        return data
    


    def decode_qr(self, filename):

        image = cv2.imread("."+filename)

        # Define the dimensions for resizing
        width = 3000  # New width
        height = 4000  # New height

        # Resize the image
        resized_image = cv2.resize(image, (width, height))
        decocdeQR = decode(resized_image)
        print(decocdeQR)
        print(decocdeQR[1].data.decode('ascii'))
        print(decocdeQR[0].data.decode('ascii'))
        return decocdeQR[1].data.decode('ascii'), decocdeQR[0].data.decode('ascii')
        

    def name_sheet(self,name,sts):
        url = f'https://script.google.com/macros/s/AKfycbwhsPa5xJPl4zruZI0BxKH0i3JUTBq0M9Gr9YthIgAvgnU3fANK-5XSUS5ipb1SfylU7g/exec/exec?sts={sts}e&mac=&ser=&nam={name}&im1='   
        response = requests.get(url)
        return "Name added"
    
    def img1_sheet(self,filename,d1,d2):
                
        url = 'https://script.google.com/macros/s/AKfycbxU3VZpsrBlMhFfa4uO-X38-4p9jEEMXA1gjVG21ZpcQr0tBHXvdRpgzpjm6u9_jOLs/exec'
        filename = "."+filename
        with open(filename, 'rb') as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        params = {
            'filename': 'ESP32-CAM.jpg',
            'mimetype': 'image/jpeg',
                'data': encoded_image,
            'decoded_text': d1,
            'decoded_text2': d2
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': str(len(encoded_image))
        }

        response = requests.post(url, data=params, headers=headers)

        return " Image 1 uploaded"
    
    def img2_sheet(self,filename,condition):
            

        url = 'https://script.google.com/macros/s/AKfycbxQdVJsQ9Cg0WoiTcdIhnduicmj7QO86mfiXVh3mXESs8yNXQodTTomUlrXCsgCqm-Z/exec'
        filename = "."+filename
        with open(filename, 'rb') as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        params = {
            'filename': 'ESP32-CAM.jpg',
            'mimetype': 'image/jpeg',
                'data': encoded_image,
                'condition': condition,
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': str(len(encoded_image))
        }

        response = requests.post(url, data=params, headers=headers)
        return " Image 2 uploaded"

# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------

class DecodeTopImageViewSerializer(serializers.ModelSerializer):
    status = serializers.CharField(required=False, read_only=True)
    top_img_url = serializers.CharField(required=False, read_only = True)
    bottom_img_url = serializers.CharField(required=False, read_only = True)
    decoded_text = serializers.CharField(required=False, read_only = True)
    decoded_text2 = serializers.CharField(required=False, read_only = True)
    bottom_image = serializers.ImageField(required=False,read_only = True)
    class Meta:
        
        model = DecImage
        fields = ["id","rep","name","top_image","bottom_image", "top_img_url","bottom_img_url", "decoded_text", "decoded_text2", "status"]    
    
    
    def create(self, data):
        decoded_text = "write"
        data['status'] = ''
        diag_filter = DecImage.objects.filter(rep=data.get("rep")).first()
        if diag_filter == None:
            diag = DecImage.objects.create(
                rep = data.get("rep"),
                name = data.get("name"),
                top_image = data.get("top_image"),
                bottom_image = data.get("top_image"),
                decoded_text=decoded_text,
            )
            diag.save()
            data['status'] += self.name_sheet(diag.name,decoded_text) + " -----> "
            decoded_text, dt2 = self.decode_qr(diag.top_image.url)
            data['decoded_text'] = decoded_text
            data['decoded_text2'] = dt2
            diag.decoded_text = "qr1 decoded : "+ decoded_text + " qr2 decoded : " + dt2
        else:
            data['status'] += " Updating existing entry -----> "
            diag =  DecImage.objects.get(rep = data.get("rep"), name = data.get("name"))
            diag.top_image = data.get("top_image")
            diag.bottom_image = data.get("top_image")
            decoded_text = 'update'
            diag.save()
            data['status'] += self.name_sheet(diag.name,decoded_text) + " -----> "
            decoded_text, dt2 = self.decode_qr(diag.top_image.url)
            data['decoded_text'] = decoded_text
            data['decoded_text2'] = dt2
            diag.decoded_text = "aqr1 decoded : "+ decoded_text + " qr2 decoded : " + dt2
        diag.save()
        data['status'] += self.img1_sheet(diag.top_image.url,decoded_text,dt2) + " -----> "
        data['top_img_url'] = diag.top_image.url
        data['bottom_img_url'] = diag.bottom_image.url

        return data
    


    def decode_qr(self, filename):

        image = cv2.imread("."+filename)

        # Define the dimensions for resizing
        width = 3000  # New width
        height = 4000  # New height

        # Resize the image
        resized_image = cv2.resize(image, (width, height))
        decocdeQR = decode(resized_image)
        print(decocdeQR)
        print(decocdeQR[1].data.decode('ascii'))
        print(decocdeQR[0].data.decode('ascii'))
        return decocdeQR[1].data.decode('ascii'), decocdeQR[0].data.decode('ascii')
        

        
    def name_sheet(self,name,sts):
        print(sts)
        url = f'https://script.google.com/macros/s/AKfycbwhsPa5xJPl4zruZI0BxKH0i3JUTBq0M9Gr9YthIgAvgnU3fANK-5XSUS5ipb1SfylU7g/exec?sts={sts}&mac=&ser=&nam={name}&im1='   
        response = requests.get(url)
        print(response)
        return "Name added"
    
    def img1_sheet(self,filename,d1,d2):
                
        url = 'https://script.google.com/macros/s/AKfycbxU3VZpsrBlMhFfa4uO-X38-4p9jEEMXA1gjVG21ZpcQr0tBHXvdRpgzpjm6u9_jOLs/exec'
        filename = "."+filename
        with open(filename, 'rb') as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        params = {
            'filename': 'ESP32-CAM.jpg',
            'mimetype': 'image/jpeg',
                'data': encoded_image,
            'decoded_text': d1,
            'decoded_text2': d2
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': str(len(encoded_image))
        }

        response = requests.post(url, data=params, headers=headers)

        return " Image 1 uploaded"
    

# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------

class DecodeBottomImageViewSerializer(serializers.ModelSerializer):
    status = serializers.CharField(required=False, read_only=True)
    top_img_url = serializers.CharField(required=False, read_only = True)
    name = serializers.CharField(required=False, read_only=True)
    bottom_img_url = serializers.CharField(required=False, read_only = True)
    decoded_text = serializers.CharField(required=False, read_only = True)
    decoded_text2 = serializers.CharField(required=False, read_only = True)
    top_image = serializers.ImageField(required=False,read_only = True)
    class Meta:
        
        model = DecImage
        fields = ["id","rep","name","top_image","bottom_image", "top_img_url","bottom_img_url", "decoded_text", "decoded_text2", "status"]    
    
    
    def create(self, data):

        data['status'] = ''
        diag =  DecImage.objects.get(rep = data.get("rep"))
        if diag.decoded_text[0] == 'q':
            data['decoded_text2'] = 'new'
            diag.decoded_text = "a"+diag.decoded_text
            diag.save()
            print("Here in new")
        else:
           
            print("Here in bototm")
            data['decoded_text2'] = 'update'


        diag.bottom_image = data.get("bottom_image")
        diag.save()
        data['status'] += self.img2_sheet(diag.bottom_image.url,data['decoded_text2'] ) 
        data['top_img_url'] = diag.top_image.url
        data['bottom_img_url'] = diag.bottom_image.url
        data['name'] = diag.name
        data['decoded_text'] = diag.decoded_text
        data['decoded_text2'] = 'Not relevant for bottom qr'

        return data
    
    def img2_sheet(self,filename,condition):
            

        url = 'https://script.google.com/macros/s/AKfycbxQdVJsQ9Cg0WoiTcdIhnduicmj7QO86mfiXVh3mXESs8yNXQodTTomUlrXCsgCqm-Z/exec'
        filename = "."+filename
        with open(filename, 'rb') as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        params = {
            'filename': 'ESP32-CAM.jpg',
            'mimetype': 'image/jpeg',
                'data': encoded_image,
                'condition': condition,
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': str(len(encoded_image))
        }

        response = requests.post(url, data=params, headers=headers)
        return " Image 2 uploaded"
    
    
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
         

        