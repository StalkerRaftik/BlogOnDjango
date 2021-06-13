from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


from .models import Post


class HomeTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@email.com',
            password='secret'
        )

        self.admin = get_user_model().objects.create_superuser(
            username='administrator',
            email='test2@email.com',
            password='secret2'
        )

        self.post = Post.objects.create(
            title='A good title',
            body='Nice body content',
            author=self.user,
        )

    def test_string_representation(self):
        post = Post(title='A sample title')
        self.assertEqual(str(post), post.title)

    def test_post_content(self):
        self.assertEqual(f'{self.post.title}', 'A good title')
        self.assertEqual(f'{self.post.author}', 'testuser')
        self.assertEqual(f'{self.post.body}', 'Nice body content')

    def test_post_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nice body content')
        self.assertTemplateUsed(response, 'home.html')

    def test_post_form_deny_for_non_admin(self):
        self.client.force_login(self.user, backend=None)
        response = self.client.post(
            reverse('home'), data={"title": "new title", 'body': "great form body"}
        )
        self.assertNotContains(response, 'great form body')

    def test_post_form_allow_for_admin(self):
        self.client.force_login(self.admin, backend=None)
        response = self.client.post(
            reverse('home'), data={"title": "new title 2", 'body': "great form body 2"}
        )
        self.assertContains(response, 'new title 2')


class PostDetailViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@email.com',
            password='secret'
        )

        self.post = Post.objects.create(
            title='A good title',
            body='Nice body content',
            author=self.user,
        )

    def test_detail_view_entry(self):
        response = self.client.get('/post/1/')
        no_response = self.client.get('/post/100000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'A good title')
        self.assertTemplateUsed(response, 'post_detail.html')

    def test_detail_view_deny_comment_for_non_authorised(self):
        response = self.client.post(
            "/post/1/", data={'body': "comment"}
        )
        self.assertNotContains(response, 'comment')

    def test_detail_view_allow_comment_for_authorised(self):
        self.client.force_login(self.user, backend=None)
        response = self.client.post(
            "/post/1/", data={'body': "comment 2"}
        )
        self.assertContains(response, 'comment 2')


class RegistrationTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@email.com',
            password='secret'
        )

    def test_registration_login_already_used(self):
        response = self.client.post(
            "/registration/", data={
                'username': ['testuser'],
                'password1': ['pass'],
                'password2': ['pass'],
                'email': ['example@site.com']
            }
        )
        self.assertContains(response, 'Такое имя пользователя уже занято')

    def test_registration_password_too_short(self):
        response = self.client.post(
            "/registration/", data={
                'username': ['newuser'],
                'password1': ['pass'],
                'password2': ['pass'],
                'email': ['example@site.com']
            }
        )
        self.assertContains(response, 'Пароль слишком короткий')

    def test_registration_password_doesnt_match(self):
        response = self.client.post(
            "/registration/", data={
                'username': ['newuser'],
                'password1': ['longpassword1234'],
                'password2': ['longpassword12345678'],
                'email': ['example@site.com']
            }
        )
        self.assertContains(response, 'Пароли не совпадают')

    def test_registration_password_only_numbers_in_it(self):
        response = self.client.post(
            "/registration/", data={
                'username': ['newuser'],
                'password1': ['1234567890'],
                'password2': ['1234567890'],
                'email': ['example@site.com']
            }
        )
        self.assertContains(response, 'В вашем пароле должны быть другие символы, помимо цифр')

    def test_registration_success(self):
        response = self.client.post(
            "/registration/", data={
                'username': ['newuser'],
                'password1': ['CorrectPassword12345!'],
                'password2': ['CorrectPassword12345!'],
                'email': ['example@site.com']
            }
        )
        self.assertContains(response, 'Вы успешно зарегистрировались!')
