from django.db import models

class UploadedFile(models.Model):
    file = models.FileField(upload_to="uploads/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

class ExtractedData(models.Model):
    file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE)
    content = models.TextField()
    extracted_at = models.DateTimeField(auto_now_add=True)
