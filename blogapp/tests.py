from django.test import TestCase
from django.test import Client
from blogapp.forms import *
from blogapp.models import *
from blog_auth.models import *
# from django.urls import reverse
from blogapp.views import *
from eventapp.models import *
from datetime import date
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class Category_Form_Test(TestCase):

    def test_CategoryForm_valid(self):
        form = CategoryForm(
            data={'name': "Meghana", 'description': "abcd", 'slug': "meghana"})
        self.assertTrue(form.is_valid())

    def test_CategoryForm_invalid(self):
        form = CategoryForm(
            data={'name': "", 'description': "xyz", 'slug': "abc"})
        self.assertFalse(form.is_valid())


class Contact_Form_Test(TestCase):

    def test_ContactForm_valid(self):
        form = ContactForm(
            data={'name': "meghana",
                  'email': "meghana@gmail.com",
                  'message': "Hai"})
        self.assertTrue(form.is_valid())

    def test_ContactForm_invalid(self):
        form = ContactForm(
            data={'name': "", 'email': "abc@gmail.com", 'message': ""})
        self.assertFalse(form.is_valid())


class Post_Form_Test(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Abc def", slug="abc-def")

    def test_PostForm_valid(self):
        form = PostForm(data={'title': "abcd", 'short_desc': "xyz",
                              'category': self.category.id,
                              "is_featured_news": "t", "slug": "abcd",
                              "description": "asdfg"})
        self.assertTrue(form.is_valid())

    def test_PostForm_invalid(self):
        form = PostForm(data={'title': "", 'short_desc': "sdfg",
                              'category': "xyz", "is_featured_news": "",
                              "slug": "", "description": ""})
        self.assertFalse(form.is_valid())


class Menu_Form_Test(TestCase):

    def setUp(self):
        self.menu = Menu.objects.create(name="Abc", slug="abc", lvl=1)
        print(self.menu)
        self.menu.parent = self.menu
        self.menu.save()

    def test_MenuForm_valid(self):

        form = MenuForm(
            data={'name': "Xyz", 'parent': self.menu.id,
                  'slug': "xyz", 'lvl': 1})
        print(form.errors)
        self.assertTrue(form.is_valid())

    def test_MenuForm_invalid(self):
        form = MenuForm(data={'name': "", 'parent': "", 'slug': ""})
        self.assertFalse(form.is_valid())


class Page_Form_Test(TestCase):

    def test_PageForm_valid(self):
        form = PageForm(
            data={'title': "Meghana", 'content': "abcd", 'slug': 'meghana'})
        self.assertTrue(form.is_valid())

    def test_PageForm_invalid(self):
        form = PageForm(data={'title': "", 'content': "dfggh", 'slug': ''})
        self.assertFalse(form.is_valid())


class Banner_Form_Test(TestCase):

    def test_BannerForm_valid(self):
        form = bannerForm(data={'title': "abcd", 'short_desc': "xyz"})
        self.assertTrue(form.is_valid())

    def test_BannerForm_invalid(self):
        form = bannerForm(data={'title': "", 'short_desc': "asdf"})
        self.assertFalse(form.is_valid())


class Password_Form_Test(TestCase):

    def test_PasswordForm_valid(self):
        form = PasswordForm(
            data={'old_password': "12345",
                  'new_password': "admin123",
                  're_password': "admin123"})
        self.assertTrue(form.is_valid())

    def test_PasswordForm_invalid(self):
        form = PasswordForm(
            data={'old_password': "",
                  'new_password': " ",
                  're_password': "abcd123"})
        self.assertFalse(form.is_valid())


class index_view_testing(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(email="abc@gmail.com")
        self.user.set_password("magy123")
        self.user.save()
        self.category = Category.objects.create(name="abcd", slug="abcd")

    def test_index_get_view(self):
        self.client.login(
            email="abc@gmail.com", password="magy123")
        url = '/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class contact_view_testing(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(email="abc@gmail.com")
        self.user.set_password("magy123")
        self.user.save()
        self.category = Category.objects.create(name="abcd", slug="abcd")

    def test_contact_get_view(self):
        self.client.login(
            email="abc@gmail.com", password="magy123")
        url = '/contact-us/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_contact_post_view(self):
        self.client.login(
            email="abc@gmail.com", password="magy123")
        url = '/contact-us/'
        data = {'name': "meghana",
                'email': "meghana@gmail.com", 'message': "Haii"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

    def test_contact_post_view_invalid(self):
        self.client.login(
            email="abc@gmail.com", password="magy123")
        url = '/contact-us/'
        data = {'name': "", 'email': "", 'message': ""}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)


class postlist_view_testing(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(email="abc@gmail.com")
        self.user.set_password("magy123")
        self.user.save()

    def test_postlist_get_view(self):
        self.client.login(
            email="abc@gmail.com", password="magy123")
        url = '/news/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class postdetail_view_testing(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(email="abc@gmail.com")
        self.user.set_password("magy123")
        self.user.save()
        self.category = Category.objects.create(
            name="abc", description="asdfg", slug="abc")
        self.post = Post.objects.create(title="xyz", category=self.category,
                                        short_desc="asdfg",
                                        description="qwerty",
                                        image="image.png", slug="xyz")

    def test_postdetail_get_view(self):
        self.client.login(
            email="abc@gmail.com", password="magy123")
        url = '/news/' + self.post.slug + '/details/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class eventlist_view_testing(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(email="abc@gmail.com")
        self.user.set_password("magy123")
        self.user.save()

    def test_eventlist_get_view(self):
        self.client.login(
            email="abc@gmail.com", password="magy123")
        url = '/events/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class eventdetail_view_testing(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(email="abc@gmail.com")
        self.user.set_password("magy123")
        self.user.save()
        self.event = Event.objects.create(
            name="abc", short_desc="asdfg", image="image.png", slug="abc")

    def test_eventdetail_get_view(self):
        self.client.login(
            email="abc@gmail.com", password="magy123")
        url = '/events/' + self.event.slug + '/details/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class sitemap_view_testing(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(email="abc@gmail.com")
        self.user.set_password("magy123")
        self.user.save()

    def test_sitemap_get_view(self):
        self.client.login(
            email="abc@gmail.com", password="magy123")
        url = '/sitemap/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class category_posts_view_testing(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(email="abc@gmail.com")
        self.user.set_password("magy123")
        self.user.save()
        self.category = Category.objects.create(
            name="abc", description="asdfg", slug="abc")

    def test_category_posts_get_view(self):
        self.client.login(
            email="abc@gmail.com", password="magy123")
        url = '/news/category/' + self.category.slug + '/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class pagedetail_view_testing(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(email="abc@gmail.com")
        self.user.set_password("magy123")
        self.user.save()
        self.page = Page.objects.create(
            title="abc", content="asdfg", slug="abc")

    def test_pagedetail_get_view(self):
        self.client.login(
            email="abc@gmail.com", password="magy123")
        url = '/page/' + self.page.slug + '/display/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class archiveposts_view_testing(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(email="abc@gmail.com")
        self.user.set_password("magy123")
        self.user.save()
        self.category = Category.objects.create(
            name="abc", description="asdfg", slug="abc")
        self.post = Post.objects.create(title="xyz", category=self.category,
                                        short_desc="asdfg",
                                        description="qwerty",
                                        image="image.png", slug="xyz")

    def test_archiveposts_get_view(self):
        self.client.login(
            email="abc@gmail.com", password="magy123")
        myDate = date.today()
        dateStr = str(myDate.year) + "/" + str(myDate.month)
        url = '/news/archives/' + dateStr + "/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class rss_view_testing(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(email="abc@gmail.com")
        self.user.set_password("magy123")
        self.user.save()

    def test_rss_get_view(self):
        self.client.login(
            email="abc@gmail.com", password="magy123")
        url = '/rss.xml'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class pagination_testing(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(email="abc@gmail.com")
        self.user.set_password("magy123")
        self.user.save()
        self.category = Category.objects.create(
            name="abc", description="asdfg", slug="abc")
        for i in range(1, 11):
            self.post = Post.objects.create(title="xyz" + str(i),
                                            category=self.category,
                                            short_desc="asdfg",
                                            description="qwerty",
                                            image="image.png", slug="xyz" +
                                            str(i))
            self.event = Event.objects.create(name="abc" + str(i),
                                              short_desc="asdfg",
                                              image="image.png",
                                              slug="abc" + str(i))

    def test_pagination_post(self):
        paginator = Paginator(Post.objects.all(), 5)
        self.assertEqual(10, paginator.count)
        self.assertEqual(2, paginator.num_pages)
        self.assertEqual([1, 2], list(paginator.page_range))

    def test_pagination_event(self):
        paginator = Paginator(Event.objects.all(), 5)
        self.assertEqual(10, paginator.count)
        self.assertEqual(2, paginator.num_pages)
        self.assertEqual([1, 2], list(paginator.page_range))

    def test_empty_post_empty_page(self):
        url = "/news" + "/?page=2"
        paginator = Paginator(Post.objects.all(), 5)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertRaises(EmptyPage, paginator.page, 0)
        self.assertRaises(EmptyPage, paginator.page, 3)