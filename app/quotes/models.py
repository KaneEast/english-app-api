from django.db import models

class Celebrity(models.Model):
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)

class Quote(models.Model):
    content = models.TextField()
    tag = models.CharField(max_length=255)
    celebrity = models.ForeignKey(
        Celebrity, on_delete=models.CASCADE, related_name='quotes'
    )
