from django.db import models


from users.models import User


class ShortURL(models.Model):
    user=models.ForeignKey(User , on_delete=models.CASCADE , related_name='short_urls')
    original_url=models.URLField(max_length=2048)
    short_code=models.CharField(unique=True, db_index=True)
    clicks=models.IntegerField(default=0)
    is_active=models.BooleanField(default=True)
    custom_alias = models.CharField(max_length=50, unique=True, null=True, blank=True)
    qr_code=models.ImageField(upload_to='qr_code/%Y/%m/%d', null=True, blank=True)
    created_time=models.DateTimeField(auto_now_add=True)
    expires_time=models.DateTimeField(blank=True , null=True)
    last_clicked=models.DateTimeField(blank=True , null=True)

    def __str__(self):
        return self.short_code

    class Meta:
        verbose_name='ShortURL'
        verbose_name_plural='ShortURLs'
        indexes=[
            models.Index(fields=['short_code']),
            models.Index(fields=['created_time']),
        ]
        ordering=['-created_time']


