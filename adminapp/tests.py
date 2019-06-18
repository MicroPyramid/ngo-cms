from django.test import TestCase
from django.test import Client
from adminapp.views import *
from blog_auth.views import *
from blog_auth.models import *
from blogapp.models import *
# from django.urls import reverse
from eventapp.models import *
# from PIL import Image
# import tempfile


class User_view_Test(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(email="abc@gmail.com")
        self.user.set_password("abc123")
        self.user.save()

    def test_login_get(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)

    def test_get_issuper(self):
        user = User.objects.create(email="admin@gmail.com")
        user.set_password("abc12345")
        user.is_admin = "True"
        user.is_staff = "True"
        user.is_active = "True"
        user.save()
        self.client.login(
            email="admin@gmail.com", password="abc12345")
        response = self.client.get('/admin/')
        self.assertContains(response, "View All Categories")
        # self.assertEqual(response.status_code,302)

    def test_post_login(self):
        User.objects.create(
            email="admin@gmail.com", is_admin=True, is_active=True)
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Admin-Login")

    def test_login_post(self):
        data = {"email": "abc@gmail.com", "password": "abc123"}
        response = self.client.post('/admin/', data)
        self.assertEqual(response.status_code, 200)

    def test_login_post_invalid(self):
        data = {"email": "admin@gmail.com", "password": "abc123"}
        response = self.client.post('/admin/', data)
        self.assertEqual(response.status_code, 200)

    def test_login_post_issuperuser(self):
        user = User.objects.create(email="admin@gmail.com")
        user.set_password("abc12345")
        user.is_admin = "True"
        user.is_active = "True"
        user.is_staff = "True"
        user.save()
        data = {"email": "admin@gmail.com", "password": "abc12345"}
        response = self.client.post('/admin/', data)
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        self.client = Client()
        response = self.client.post("/admin/admin_logout/")
        self.assertEqual(response.status_code, 302)


class change_password_view_Test(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(email="abc@gmail.com")
        self.user.set_password("abc123")
        self.user.save()

    def test_change_pwd_get(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = "/admin/change_password/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_change_pwd_form_valid(self):
        user_login = self.client.login(
            email="abc@gmail.com", password="abc123")
        url = "/admin/change_password/"
        data = {'old_password': "abc123",
                'new_password': "abc123", 're_password': "abc123"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.client.logout()
        user_login = self.client.login(
            email="abc@gmail.com", password="abc123")
        self.assertTrue(user_login)

    def test_change_pwd_form_invalid(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = "/admin/change_password/"
        data = {'old_password': "abc123",
                'new_password': "", 're_password': ""}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

    def test_change_re_pwd(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = "/admin/change_password/"
        data = {'old_password': "abc123",
                'new_password': "magy123", 're_password': "admin123"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

    def test_change_old_pwd(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = "/admin/change_password/"
        data = {'old_password': "admin123",
                'new_password': "test123", 're_password': "test123"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)


class category_view_testing(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(email="abc@gmail.com")
        self.user.set_password("abc123")
        self.user.save()
        self.category = Category.objects.create(
            name="abc", description="asdfg", slug="abc")

    def add_category(self):
        return Category.objects.create(name="meghana",
                                       description="asdfg",
                                       slug="meghana")

    def test_category_get_view(self):

        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = '/admin/category/add/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_category_post_form_valid(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = '/admin/category/add/'
        data = {'name': "meghana", 'description': "asdfg", 'slug': "meghana"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

    def test_category_post_form_invalid(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = '/admin/category/add/'
        data = {'name': "", 'description': "asdfg", 'slug': ""}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

    def test_category_list_view(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = '/admin/category/list/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_category_edit_view(self):
        user_login = self.client.login(
            email="abc@gmail.com", password="abc123")
        self.assertTrue(user_login)
        url = '/admin/category/edit/' + str(self.category.id) + '/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_category_edit_post_form_valid_view(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = '/admin/category/edit/' + str(self.category.id) + '/'
        data = {'name': 'magy', 'description': "qwerty", 'slug': 'magy'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

    def test_category_edit_post_form_invalid_view(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = '/admin/category/edit/' + str(self.category.id) + '/'
        data = {'name': "", 'description': "", 'slug': ""}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

    def test_category_delete(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = '/admin/category/delete/' + str(self.category.id) + '/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)


class banner_view_testing(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(email="abc@gmail.com")
        self.user.set_password("abc123")
        self.user.save()
        self.banner = Banner.objects.create(
            title="abcd", image="image.png", short_desc="asdfg")

    def test_banner_get_view(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = '/admin/banner/add/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_banner_post_view(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = '/admin/banner/add/'
        data = {'title': "12457axs", 'image': "abc.png", 'short_desc': "asdfg"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

    def test_banner_invalid_view(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = '/admin/banner/add/'
        data = {'title': "", 'image': "", 'short_desc': ""}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

    def test_banner_list_view(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = "/admin/banner/list/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_banner_delete(self):
        self.client.login(
            email="abc@gmail.com", password="magy13")
        url = '/admin/banner/delete/' + str(self.banner.id) + '/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)


class banner_edit_testing(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(email="abc@gmail.com")
        self.user.set_password("abc123")
        self.user.save()
        self.banner = Banner.objects.create(
            title="abcd", image="image.png", short_desc="asdfg")

    def test_banner_edit_get(self):
        user_login = self.client.login(
            email="abc@gmail.com", password="abc123")
        self.assertTrue(user_login)
        url = '/admin/banner/edit/' + str(self.banner.id) + '/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_banner_edit_post(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = '/admin/banner/edit/' + str(self.banner.id) + '/'
        data = {'title': "abcd", 'image': "abc.png", 'short_desc': "asdfg"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

    def test_banner_edit_post_invalid(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = '/admin/banner/edit/' + str(self.banner.id) + '/'
        data = {'title': "", 'image': "abc.png", 'short_desc': "asdfg"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)


class event_view_testing(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(email="abc@gmail.com")
        self.user.set_password("abc123")
        self.user.save()
        self.event = Event.objects.create(
            name="abcd", short_desc="xyz",
            description="asdfg", image="image.png",
            slug="abcd")

    def test_event_get_view(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = '/admin/event/add/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_event_post_view(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = '/admin/event/add/'
        data = {'name': "test", 'short_desc': "xyz",
                'description': "asdfg", 'slug': "test"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

    def test_event_invalid(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = '/admin/event/add/'
        data = {'name': "", 'short_desc': "",
                'description': "", 'slug': ""}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

    def test_event_list_view(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = '/admin/event/list/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_event_edit_get_view(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = "/admin/event/edit/" + str(self.event.id) + '/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_event_edit_post_view(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = "/admin/event/edit/" + str(self.event.id) + '/'
        data = {'name': "magy", 'short_desc': "abc",
                'description': "qwer", 'slug': "magy"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

    def test_event_edit_invalid(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = "/admin/event/edit/" + str(self.event.id) + '/'
        data = {'name': "", 'short_desc': "abc",
                'description': "", 'slug': ""}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

    def test_event_delete(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = '/admin/event/delete/' + str(self.event.id) + '/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

    def test_event_state(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = '/admin/event/change_state/' + str(self.event.id) + '/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_event_date_view(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = '/admin/event/add/'
        data = {'name': "mag", 'short_desc': "xyz",
                'description': "asdfg", "start_date": "2018-12-31",
                "end_date": "2018-12-01", 'slug': "mag"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

    def test_event_edit_date(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = '/admin/event/edit/' + str(self.event.id) + '/'
        data = {'name': "mag", 'short_desc': "xyz",
                'description': "asdfg", "start_date": "2018-12-31",
                "end_date": "2018-12-01", 'slug': "mag"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)


class page_view_testing(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(email="abc@gmail.com")
        self.user.set_password("abc123")
        self.user.save()
        # self.page = Page.objects.create(
        #     title="abcd", content="asdfg", slug="abcd")
        self.image = Gal_Image.objects.create(image="image.png")
        self.page = Page.objects.create(
            title="abcd", content="asdfg", slug="abcd")
        self.page.photos.add(self.image)

    def test_page_get_view(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = '/admin/page/add/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_page_post_view(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = '/admin/page/add/'
        data = {'title': "mag", 'content': "asdfg", 'slug': "mag"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

    def test_page_invalid_view(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = '/admin/page/add/'
        data = {'title': " ", 'content': "asdfg", 'slug': ""}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

    def test_page_edit_get_view(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = "/admin/page/edit/" + str(self.page.id) + '/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_page_edit_post_view(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = "/admin/page/edit/" + str(self.page.id) + '/'
        data = {'title': "xyz", 'content': "qwerty", 'slug': "xyz"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

    def test_page_edit_invalid(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = "/admin/page/edit/" + str(self.page.id) + '/'
        data = {'title': "", 'content': "", 'slug': ""}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

    def test_page_list_view(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = "/admin/page/list/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_page_delete(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = '/admin/page/delete/' + str(self.page.id) + '/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_page_image(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = "/admin/page/edit/" + str(self.page.id) + '/'
        data = {'title': "mag", 'content': "asdf",
                'slug': "mag", "photos": self.image}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)


class post_view_testing(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(email="abc@gmail.com")
        self.user.set_password("abc123")
        self.user.save()
        self.category = Category.objects.create(name="abcd", slug="abcd")
        self.post = Post.objects.create(
            title="abc", short_desc="qwerty",
            category=self.category, slug="abc",
            description="asdfg", image="image.png")

    def test_post_get_view(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = '/admin/article/add/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_form_valid(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = '/admin/article/add/'
        data = {'title': "xyz", 'short_desc': "qwerty",
                'category': self.category.id, 'slug': "xyz",
                'description': "asdfg", 'image': "image.png"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

    def test_post_form_invalid(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = '/admin/article/add/'
        data = {'title': "abc", 'short_desc': "qwerty",
                'category': "", 'slug': "abc", 'description': ""}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

    def test_post_edit_get_view(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = "/admin/article/edit/" + str(self.post.id) + '/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_edit_post_form_valid(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = "/admin/article/edit/" + str(self.post.id) + '/'
        data = {'title': "xyz", 'short_desc': "qwerty",
                'category': self.category, 'slug': "xyz",
                'description': "asdfg", 'image': "abc.png"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

    def test_post_edit_post_form_invalid(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = "/admin/article/edit/" + str(self.post.id) + '/'
        data = {'title': "", 'short_desc': "qwerty", 'category': self.category,
                'slug': "", 'description': "", 'image': "abc.png"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

    def test_post_list_view(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = "/admin/article/list/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_delete(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = '/admin/article/delete/' + str(self.post.id) + '/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_post_state(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = '/admin/article/change_state/' + str(self.post.id) + '/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)


class menu_view_testing(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(email="abc@gmail.com")
        self.user.set_password("abc123")
        self.user.save()
        self.menu = Menu.objects.create(name="abc", slug="abc", lvl=2)
        self.menu1 = Menu.objects.create(
            name="xyz", parent=self.menu, slug="xyz", lvl=1)
        self.menu2 = Menu.objects.create(
            name="asdf", parent=self.menu, slug="asdf", lvl=0)

    def test_menu_get_view(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = "/admin/menu/add/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_menu_post_view(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = "/admin/menu/add/"
        data = {'name': "mag", 'slug': "mag", 'lvl': 1}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

    def test_menu_post_invalid(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = "/admin/menu/add/"
        data = {'name': "", 'slug': "", 'lvl': ""}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

    def test_menu_list_view(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = "/admin/menu/list/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_menu_edit_get_view(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = "/admin/menu/edit/" + str(self.menu.id) + '/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_menu_edit_post_view(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = "/admin/menu/edit/" + str(self.menu.id) + '/'
        data = {'name': "mag", 'slug': "mag", 'lvl': 1}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

    def test_menu_edit_invalid(self):
        user_login = self.client.login(
            email="abc@gmail.com", password="abc123")
        self.assertTrue(user_login)
        url = "/admin/menu/edit/" + str(self.menu.id) + '/'
        data = {'name': "", 'parent': "", 'slug': "", 'lvl': ""}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

    def test_menu_delete(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = '/admin/menu/delete/' + str(self.menu.id) + '/'
        self.post = Menu.objects.create(name="magy", slug="magy", lvl=2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_menu_state(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = '/admin/menu/change_state/' + str(self.menu.id) + '/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_menu_lvl_up(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = '/admin/menu/lvl-up/' + str(self.menu1.id) + '/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_menu_lvl_down(self):
        self.menu = Menu.objects.create(name="nav", slug="nav", lvl=0)
        self.menu1 = Menu.objects.create(
            name="mag", parent=self.menu, slug="mag", lvl=1)
        self.menu2 = Menu.objects.create(
            name="def", parent=self.menu, slug="def", lvl=2)
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = '/admin/menu/lvl-down/' + str(self.menu1.id) + '/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)


class menu_edit_testing(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(email="abc@gmail.com")
        self.user.set_password("abc123")
        self.user.save()
        self.menu = Menu.objects.create(name="abc", slug="abc", lvl=2)
        self.menu1 = Menu.objects.create(
            name="xyz", parent=self.menu, slug="xyz", lvl=1)
        self.menu2 = Menu.objects.create(
            name="asdf", parent=self.menu, slug="asdf", lvl=0)


class Gal_image_view_testing(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(email="abc@gmail.com")
        self.user.set_password("abc123")
        self.user.save()
        self.image = Gal_Image.objects.create(image="image.png")
        self.category = Category.objects.create(name="abcd", slug="abcd")
        self.post = Post.objects.create(
            title="abc", short_desc="qwerty",
            category=self.category, slug="abc", description="asdfg")
        self.post.photos.add(self.image)

    def test_del_image(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = '/admin/delete_gal_img' + '/' + \
            str(self.image.id) + '/' + str(self.post.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)


class page_image_view_testing(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(email="abc@gmail.com")
        self.user.set_password("abc123")
        self.user.save()
        self.image = Gal_Image.objects.create(image="image.png")
        self.page = Page.objects.create(
            title="abcd", content="asdfg", slug="abcd")
        self.page.photos.add(self.image)

    def test_page_del_image(self):
        self.client.login(
            email="abc@gmail.com", password="abc123")
        url = '/admin/delete_page_imgs' + '/' + \
            str(self.image.id) + '/' + str(self.page.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)


class recent_photos_testing(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(email="abc@gmail.com")
        self.user.set_password("abc123")
        self.user.save()

    def test_recent_photos_get(self):
        self.client.login(email="abc@gmail.com", password="abc123")
        url = "/admin/ajax/photos/recent/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


# class upload_photos_testing(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create(email="abc@gmail.com")
#         self.user.set_password("abc123")
#         self.user.save()

#     def test_upload_photos_get(self):
#         self.client.login(email="abc@gmail.com", password="abc123")
#         url = "/admin/ajax/photos/upload/"
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
