from django.db import models

class Dataset(models.Model):
    file = models.FileField(upload_to='datasets/')
    filename = models.CharField(max_length=255, blank = True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    summary = models.JSONField(default = dict, blank = True)

    def __str__(self):
        return self.filename or f"Dataset {self.id}"
