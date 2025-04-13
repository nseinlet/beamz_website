from django.db import models

class FaqSection(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    name_fr = models.CharField(max_length=200, blank=True)
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
    question_fr = models.TextField(blank=True)
    short_answer = models.TextField()
    short_answer_fr = models.TextField(blank=True)
    answer = models.TextField()
    answer_fr = models.TextField(blank=True)

    def __str__(self):
        return self.question
