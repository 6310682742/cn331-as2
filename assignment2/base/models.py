from doctest import FAIL_FAST
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Course(models.Model):
    course_code = models.CharField(max_length=200, default="")
    course_semeter = models.CharField(max_length=200, default='1')
    course_year = models.IntegerField(default=2000)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=200)
    student = models.ManyToManyField(User, related_name='student', blank=True)
    max_student = models.IntegerField(default=100)
    current_student = models.IntegerField(default=0)
    TRUE_FALSE_CHOICES = (
        (True, 'Yes'),
        (False, 'No')
    )
    course_status = models.BooleanField(choices=TRUE_FALSE_CHOICES, default=False)
    def __str__(self) -> str:
        return self.course_name