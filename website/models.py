from django.db import models
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
import qrcode

class Website(models.Model):
    name = models.CharField(max_length=100)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        qr_image = qrcode.make(self.name)
        qr_image = qr_image.convert('RGB')
        qr_offset = Image.new('RGB', (310, 310), 'white')
        
        qr_image = qr_image.resize((290, 290), Image.LANCZOS)
        qr_offset.paste(qr_image, (10, 10))

        file_name = f'{self.name}.png'
        stream = BytesIO()
        qr_offset.save(stream, 'PNG')
        self.qr_code.save(file_name, File(stream), save=False)
        qr_offset.close()
        super().save(*args, **kwargs)