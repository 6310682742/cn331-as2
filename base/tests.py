

from urllib import response
from django.test import Client, TestCase
from django.urls import reverse
from .models import *
# Create your tests here.


class CourseTestCase(TestCase):
    # setup test case
    def setUp(self) -> None:
        course = Course.objects.create(
            course_code='cn000', course_status=False)
        course1 = Course.objects.create(course_code='cn001', max_student=1)
        course2 = Course.objects.create(course_code='cn002')
        user = User.objects.create(username='user1')
        user.set_password('password')
        user.save()
        course1.student.add(user)
        course1.save()
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        return super().setUp()

    def test_Course(self):
        course = Course.objects.get(course_code='cn001')

    # ทดสอบว่าโปรแกรมสามารถไปยังหน้า home ที่ถูกต้องได้
    def test_home(self):
        c = Client()
        response = c.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    # ทดสอบว่าโปรแกรมสามารถไปยังหน้า loginUser ที่ถูกต้องได้
    def test_loginUser(self):
        c = Client()
        response = c.get(reverse('loginUser'))
        self.assertEqual(response.status_code, 200)

    # ทดสอบว่าโปรแกรมสามารถไปยังหน้า logoutUser ที่ถูกต้องได้
    def test_logoutUser(self):
        c = Client()
        login = c.login(username='user1', password='password')
        response = c.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    # ทดสอบว่าโปรแกรมสามารถไปยังหน้า regisUser ที่ถูกต้องได้
    def test_registUser(self):
        c = Client()
        response = c.get(reverse('regist'))
        self.assertEqual(response.status_code, 200)

    # ทดสอบว่าโปรแกรมสามารถไปยังหน้า roomของCourse ที่ถูกต้องได้
    def test_room(self):
        c = Client()
        response = c.get(reverse('regist'))
        self.assertEqual(response.status_code, 200)

    # ทดสอบว่าโปรแกรมสามารถไปยังหน้า uerProfile ที่ถูกต้องได้
    def test_userProfile(self):
        c = Client()
        user = User.objects.first()
        response = c.get(reverse('userProfile', args=[user.pk]))
        self.assertEqual(response.status_code, 200)

    # ทดสอบว่าโปรแกรมสามารถไปยังหน้า createCourse ที่ถูกต้องได้
    def test_createCourse(self):
        c = Client()
        response = c.get(reverse('course_form'))
        self.assertEqual(response.status_code, 302)

    # ทดสอบว่าโปรแกรมสามารถไปยังหน้า editCourse ที่ถูกต้องได้
    def test_editCourse(self):
        c = Client()
        response = c.get(reverse('course_form'))
        self.assertEqual(response.status_code, 302)

    # ทดสอบว่าโปรแกรมสามารถไปยังหน้า deleteCourse ที่ถูกต้องได้
    def test_deleteCourse(self):
        c = Client()
        response = c.get(reverse('course_form'))
        self.assertEqual(response.status_code, 302)
    # ทดสอบว่าโปรแกรมสามารถส่งข้อมูลไปหน้า home ได้ถูกต้อง

    def test_home_context_q_None(self):
        c = Client()
        response = c.get(reverse('home'))
        CONTEXT_LIST = (
            'courses',
            'roomStatus',
            'q',
            'is_admin',
            'user')
        self.assertEqual(
            set(response.context['courses']), set(Course.objects.all()))
    # ทดสอบว่าโปรแกรมสามารถส่งข้อมูลไปหน้า home โดยมี q = All ได้ถูกต้อง

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
        self.assertEqual(
            set(response.context['courses']), set(Course.objects.all()))

        self.assertEqual(response.context['roomStatus'], (
            "All",
            "Available",
            "Open",
            "Closed",
            "Registered",
        ))
        self.assertEqual(response.context['q'], 'All')
        self.assertFalse(response.context['is_admin'])
        self.assertTrue(response.context['user'].is_anonymous)
    # ทดสอบว่าโปรแกรมสามารถส่งข้อมูลไปหน้า home โดยมี q = Available ได้ถูกต้อง

    def test_home_context_q_available(self):
        c = Client()
        url = '{url}?{filter}={value}'.format(
            url=reverse('home'),
            filter='q', value='Available')
        # response = c.get(url)
        CONTEXT_LIST = (
            'courses',
            'roomStatus',
            'q',
            'is_admin',
            'user')
        login = c.login(username='user1', password='password')
        response = c.get(url)
        self.assertEqual(response.context['courses'], [
                         Course.objects.get(course_code='cn002')])
        self.assertEqual(response.context['roomStatus'], (
            "All",
            "Available",
            "Open",
            "Closed",
            "Registered",
        ))
        # print(User.objects.get(username='user1'))
        self.assertEqual(response.context['q'], 'Available')
        self.assertFalse(response.context['is_admin'])
        self.assertEqual(
            response.context['user'], User.objects.get(username='user1'))
        # self.ass
    # ทดสอบว่าโปรแกรมสามารถส่งข้อมูลไปหน้า home โดยมี q = Open ได้ถูกต้อง

    def test_home_context_q_Open(self):
        c = Client()
        url = '{url}?{filter}={value}'.format(
            url=reverse('home'),
            filter='q', value='Open')
        # response = c.get(url)
        CONTEXT_LIST = (
            'courses',
            'roomStatus',
            'q',
            'is_admin',
            'user')
        login = c.login(username='user1', password='password')
        response = c.get(url)
        self.assertEqual(set(response.context['courses']), set([Course.objects.get(
            course_code='cn001'), Course.objects.get(course_code='cn002')]))
        self.assertEqual(response.context['roomStatus'], (
            "All",
            "Available",
            "Open",
            "Closed",
            "Registered",
        ))
        print(response.context['user'])
        self.assertEqual(response.context['q'], 'Open')
        self.assertFalse(response.context['is_admin'])
        self.assertEqual(
            response.context['user'], User.objects.get(username='user1'))

        # self.assertEqual(response.request['user'], )
    # ทดสอบว่าโปรแกรมสามารถส่งข้อมูลไปหน้า home โดยมี q = Closed ได้ถูกต้อง

    def test_home_context_q_Closed(self):
        c = Client()
        url = '{url}?{filter}={value}'.format(
            url=reverse('home'),
            filter='q', value='Closed')
        # response = c.get(url)
        CONTEXT_LIST = (
            'courses',
            'roomStatus',
            'q',
            'is_admin',
            'user')
        login = c.login(username='user1', password='password')
        print(login)
        response = c.get(url)
        self.assertEqual(set(response.context['courses']), set(
            [Course.objects.get(course_code='cn000')]))
        self.assertEqual(response.context['roomStatus'], (
            "All",
            "Available",
            "Open",
            "Closed",
            "Registered",
        ))
        self.assertEqual(response.context['q'], 'Closed')
        self.assertFalse(response.context['is_admin'])
        self.assertEqual(
            response.context['user'], User.objects.get(username='user1'))

        # self.assertEqual(response.request['user'], )
    # ทดสอบว่าโปรแกรมสามารถส่งข้อมูลไปหน้า home โดยมี q = Registered ได้ถูกต้อง

    def test_home_context_q_Registered(self):
        c = Client()
        url = '{url}?{filter}={value}'.format(
            url=reverse('home'),
            filter='q', value='Registered')
        # response = c.get(url)
        CONTEXT_LIST = (
            'courses',
            'roomStatus',
            'q',
            'is_admin',
            'user')
        login = c.login(username='user1', password='password')
        print(login)
        response = c.get(url)
        self.assertEqual(set(response.context['courses']), set(
            [Course.objects.get(course_code='cn001')]))
        self.assertEqual(response.context['roomStatus'], (
            "All",
            "Available",
            "Open",
            "Closed",
            "Registered",
        ))
        self.assertEqual(response.context['q'], 'Registered')
        self.assertFalse(response.context['is_admin'])
        self.assertEqual(
            response.context['user'], User.objects.get(username='user1'))
    # ทดสอบว่าโปรแกรมสามารถส่งข้อมูลไปหน้า room ได้ถูกต้อง

    def test_room(self):

        c = Client()
        logged_in = c.login(username='user1', password='password')
        url = reverse(
            'room', args=[Course.objects.get(course_code='cn000').pk])
        reponse = c.get((url))
        self.assertEqual(reponse.context['room'],
                         Course.objects.get(course_code='cn000'))
        self.assertEqual(reponse.context['func'], 'regist')
        self.assertEqual(reponse.context['students'], '')
        self.assertEqual(reponse.context['registable'], True)
        self.assertEqual(reponse.context['is_teacher'], False)
        self.assertEqual(reponse.context['user'],
                         User.objects.get(username='user1'))
