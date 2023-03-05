from django.db import models

class FaqSection(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    order = models.IntegerField(default=10)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Faq(models.Model):
    id = models.BigAutoField(primary_key=True)
    section_id = models.ForeignKey(FaqSection, on_delete=models.RESTRICT, null=False)
    order = models.IntegerField(default=10)
    active = models.BooleanField(default=True)
    question = models.TextField()
    short_answer = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return self.question
