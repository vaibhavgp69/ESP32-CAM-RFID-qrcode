from django.db import models
import uuid
 

class Decode(models.Model):
    decoded_text = models.CharField(max_length=500,null=True, default = "")
    file_id = models.CharField(max_length=500,null=True, default = "" )             

    def __str__(self):
        return self.file_id + "--------------Decoded Text is:------------" + self.decoded_text
    

class DecImage(models.Model):
    image = models.ImageField(upload_to='qr_images', )             
    decoded_text = models.CharField(max_length=500,null=True, default = "")                                                                          


    
    def __str__(self):
        return self.image.url
       