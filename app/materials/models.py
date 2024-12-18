from django.db import models

class Material(models.Model):
    link = models.URLField()
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
