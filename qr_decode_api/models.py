from django.db import models
import uuid
 

class Decode(models.Model):
    decoded_text = models.CharField(max_length=500,null=True, default = "")
    file_id = models.CharField(max_length=500,null=True, default = "" )             

    def __str__(self):
        return self.file_id + "--------------Decoded Text is:------------" + self.decoded_text
    

class DecImage(models.Model):
    rep = models.CharField(max_length=500,null=True, default = "")
    top_image = models.ImageField(upload_to='top_images', )   
    bottom_image = models.ImageField(upload_to='bottom_images', )    
    name =   models.CharField(max_length=500,null=True, default = "")    
    decoded_text = models.CharField(max_length=500,null=True, default = "")                                                                          


    
    def __str__(self):
        return self.rep + self.name + self.decoded_text
       