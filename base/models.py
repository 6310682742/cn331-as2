from doctest import FAIL_FAST
from pydoc import describe
from timeit import repeat
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Course(models.Model):
    course_code = models.CharField(max_length=200, default="" ,unique=True)
    course_name = models.CharField(max_length=200)

    course_semeter = models.CharField(max_length=200, default='1')
    course_year = models.IntegerField(default=2000)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    student = models.ManyToManyField(User, related_name='student', blank=True)
    max_student = models.IntegerField(default=100)
    TRUE_FALSE_CHOICES = (
        (True, 'Yes'),
        (False, 'No')
    )
    course_status = models.BooleanField(choices=TRUE_FALSE_CHOICES, default=True)
    describetion = models.TextField(blank=True, max_length=500)
    def __str__(self) -> str:
        return self.course_code
    def is_registable(self) -> bool:
        return True if self.max_student > len(self.student.all()) else False