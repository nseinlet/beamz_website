from django.db import models


class BlackList(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(max_length=255, unique=True)

    def __str__(self):
        return self.email
