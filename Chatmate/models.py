from django.db import models

class Documents(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/', null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.pk:
            old_file = Documents.objects.get(pk=self.pk).file
            if old_file != self.file:
                old_file.delete()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Query(models.Model):
    query_text = models.TextField()
    response_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if Query.objects.filter(query_text=self.query_text).exists():
            return
        super().save(*args, **kwargs)

    def __str__(self):
        return self.query_text
