
from django.test import Client, TestCase
from django.urls import reverse
from .models import *
# Create your tests here.
class CourseTestCase(TestCase):
    def setUp(self) -> None:
        course = Course.objects.create(course_code='cn001')
        user = User.objects.create(username='user1')
        user.set_password('password')
        user.save();
        return super().setUp()
    def test_Course(self):
        course = Course.objects.get(course_code='cn001')
    def test_home(self):
        c = Client()
        response = c.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
    def test_loginUser(self):
        c = Client()
        response = c.get(reverse('loginUser'))
        self.assertEqual(response.status_code, 200)
    def test_logoutUser(self):
        c = Client()
        response = c.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
    def test_registUser(self):
        c = Client()
        response = c.get(reverse('regist'))
        self.assertEqual(response.status_code, 200)
    def test_room(self):
        c = Client()
        response = c.get(reverse('regist'))
        self.assertEqual(response.status_code, 200)
    def test_userProfile(self):
        c = Client()
        user = User.objects.first()
        response = c.get(reverse('userProfile', args=[user.pk]))
        self.assertEqual(response.status_code, 200)
    def test_createCourse(self):
        c = Client()
        response = c.get(reverse('course_form'))
        self.assertEqual(response.status_code, 302)
    def test_editCourse(self):
        c = Client()
        response = c.get(reverse('course_form'))
        self.assertEqual(response.status_code, 302)
    def test_deleteCourse(self):
        c = Client()
        response = c.get(reverse('course_form'))
        self.assertEqual(response.status_code, 302)
    def test_home_context_q_None(self):
        c = Client()
        response = c.get(reverse('home'))
        CONTEXT_LIST = (
            'courses',
            'roomStatus',
            'q',
            'is_admin',
            'user')
        self.assertEqual(set(response.context['courses']), set(Course.objects.all()))
    def test_home_context_q_All(self):
        c = Client()
        url = '{url}?{filter}={value}'.format(
        url=reverse('home'),
        filter='q', value='All')
        response = c.get(url)
        CONTEXT_LIST = (
            'courses',
            'roomStatus',
            'q',
            'is_admin',
            'user')
        self.assertEqual(set(response.context['courses']), set(Course.objects.all()))