from django.db import models

class Documents(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/', null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Query(models.Model):
    query_text = models.TextField()
    response_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.query_text
