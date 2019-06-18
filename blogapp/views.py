from django.shortcuts import render, render_to_response
from django.http import HttpResponse, JsonResponse
from blogapp.models import Category, Post, Menu, Page, Banner
from blogapp.forms import ContactForm
from eventapp.models import Event
from django.core.mail import send_mail
import math
import datetime
import calendar


def index(request):
    news_list = Post.objects.filter(
        is_featured_news=True, is_active=True).order_by('-created_on')[0:8]
    post_list = Post.objects.filter(
        is_active=True).order_by('-created_on')[0:2]
    event_list = Event.objects.filter(is_active=True)[0:2]
    footer_events = Event.objects.filter(
        is_active=True).order_by('-start_date')[0:4]
    menu_list = Menu.objects.filter(parent=None, is_active=True)
    banner_list = Banner.objects.all()
    return render_to_response("site/home_page.html",
                              {'news_list': news_list,
                               'banner_list': banner_list,
                               'footer_events': footer_events,
                               'menu_list': menu_list,
                               'event_list': event_list,
                               'post_list': post_list})


def contact_us(request):
    if request.method == "GET":
        menu_list = Menu.objects.filter(parent=None, is_active=True)
        event_list = Event.objects.filter(
            is_active=True).order_by('-start_date')[0:1]
        footer_events = Event.objects.filter(
            is_active=True).order_by('-start_date')[0:4]
        return render(request, "site/contact.html",
                      {'menu_list': menu_list, 'footer_events': footer_events,
                       'event_list': event_list})

  
    validate_contact = ContactForm(request.POST)
    errors = {}
    if validate_contact.is_valid():
        contact = validate_contact.save()
        try:
            send_mail(contact.name, contact.message, contact.email, [
                      'hello@cjws.in'], fail_silently=False)
            data = {"data": 'Thank you,  For Ur Message.!', "error": False}
            return JsonResponse(data)
        except Exception:
            data = {"data": 'Server Error.!', "error": False}
            return JsonResponse(data)
    else:
        for k in validate_contact.errors:
            errors[k] = validate_contact.errors[k][0]
    return JsonResponse(errors)


def post_list(request):
    post_list = Post.objects.filter(is_active=True).order_by('-created_on')
    present_date = datetime.date.today()
    archives = []
    for p in range(-3, 1):
        archives.append(present_date + datetime.timedelta(p * 365 / 12))

    items_per_page = 5
    if "page" in request.GET:
        page = int(request.GET.get('page'))
    else:
        page = 1

    no_pages = int(math.ceil(float(post_list.count()) / items_per_page))
    post_list = post_list[(page - 1) * items_per_page:page * items_per_page]
    if page <= 5:
        start_page = 1
    else:
        start_page = page - 5
    if no_pages <= 10:
        end_page = no_pages
    else:
        end_page = start_page + 10
        if end_page > no_pages:
            end_page = no_pages

    pages = range(start_page, end_page + 1)
    menu_list = Menu.objects.filter(parent=None, is_active=True)
    event_list = Event.objects.filter(
        is_active=True).order_by('-start_date')[0:2]
    footer_events = Event.objects.filter(
        is_active=True).order_by('-start_date')[0:4]
    category_list = Category.objects.all()
    return render_to_response("site/post_list.html",
                              {'current_page': page,
                               'archives': archives,
                               'category_list': category_list,
                               'event_list': event_list,
                               'footer_events': footer_events,
                               'menu_list': menu_list,
                               'pages': pages,
                               'last_page': no_pages,
                               'post_list': post_list})


def post_detail(request, slug):
    post = Post.objects.filter(slug=slug, is_active=True).first()
    menu_list = Menu.objects.filter(parent=None, is_active=True)
    post_list = Post.objects.filter(
        is_active=True).order_by('-created_on')[0:2]
    footer_events = Event.objects.filter(
        is_active=True).order_by('-start_date')[0:4]
    category_list = Category.objects.all()
    present_date = datetime.date.today()
    archives = []
    for p in range(-3, 1):
        archives.append(present_date + datetime.timedelta(p * 365 / 12))
    return render_to_response("site/post_detail.html",
                              {'post': post,
                               'archives': archives,
                               'category_list': category_list,
                               'footer_events': footer_events,
                               'post_list': post_list,
                               'menu_list': menu_list})


def event_list(request):
    event_list = Event.objects.filter(is_active=True).order_by('-start_date')
    items_per_page = 5
    if "page" in request.GET:
        page = int(request.GET.get('page'))
    else:
        page = 1

    no_pages = int(math.ceil(float(event_list.count()) / items_per_page))
    event_list = event_list[(page - 1) * items_per_page:page * items_per_page]
    if page <= 5:
        start_page = 1
    else:
        start_page = page - 5
    if no_pages <= 10:
        end_page = no_pages
    else:
        end_page = start_page + 10
        if end_page > no_pages:
            end_page = no_pages

    pages = range(start_page, end_page + 1)
    menu_list = Menu.objects.filter(parent=None, is_active=True)
    footer_events = Event.objects.filter(
        is_active=True).order_by('-start_date')[0:4]
    post_list = Post.objects.filter(
        is_active=True).order_by('-created_on')[0:2]
    return render_to_response("site/event_list.html",
                              {'current_page': page,
                               'footer_events': footer_events,
                               'post_list': post_list,
                               'menu_list': menu_list,
                               'pages': pages,
                               'last_page': no_pages,
                               'event_list': event_list})


def event_detail(request, slug):
    event = Event.objects.get(slug=slug)
    menu_list = Menu.objects.filter(parent=None, is_active=True)
    event_list = Event.objects.filter(
        is_active=True).order_by('-start_date')[0:2]
    footer_events = Event.objects.filter(
        is_active=True).order_by('-start_date')[0:4]
    return render_to_response('site/event_detail.html',
                              {'menu_list': menu_list,
                               'footer_events': footer_events,
                               'event_list': event_list,
                               'event': event})


def category_posts(request, slug):
    present_date = datetime.date.today()
    archives = []
    for p in range(-3, 1):
        archives.append(present_date + datetime.timedelta(p * 365 / 12))
    cat = Category.objects.get(slug=slug)
    post_list = Post.objects.filter(category_id=cat.id, is_active=True)
    items_per_page = 5
    if "page" in request.GET:
        page = int(request.GET.get('page'))
    else:
        page = 1

    no_pages = int(math.ceil(float(post_list.count()) / items_per_page))
    post_list = post_list[(page - 1) * items_per_page:page * items_per_page]
    if page <= 5:
        start_page = 1
    else:
        start_page = page - 5
    if no_pages <= 10:
        end_page = no_pages
    else:
        end_page = start_page + 10
        if end_page > no_pages:
            end_page = no_pages

    menu_list = Menu.objects.filter(parent=None, is_active=True)
    event_list = Event.objects.filter(
        is_active=True).order_by('-start_date')[0:2]
    footer_events = Event.objects.filter(
        is_active=True).order_by('-start_date')[0:4]
    return render_to_response("site/category_posts.html",
                              {'current_page': page,
                               'archives': archives,
                               'cat': cat,
                               'category_list': Category.objects.all(),
                               'event_list': event_list,
                               'footer_events': footer_events,
                               'menu_list': menu_list,
                               'pages': range(start_page, end_page + 1),
                               'last_page': no_pages,
                               'post_list': post_list})


def archive_posts(request, year, month):
    post_list = Post.objects.filter(
        created_on__year=year, created_on__month=month, is_active=True)
    present_date = datetime.date.today()
    archives = []
    for p in range(-3, 1):
        archives.append(present_date + datetime.timedelta(p * 365 / 12))

    items_per_page = 5
    if "page" in request.GET:
        page = int(request.GET.get('page'))
    else:
        page = 1

    no_pages = int(math.ceil(float(post_list.count()) / items_per_page))
    post_list = post_list[(page - 1) * items_per_page:page * items_per_page]
    if page <= 5:
        start_page = 1
    else:
        start_page = page - 5
    if no_pages <= 10:
        end_page = no_pages
    else:
        end_page = start_page + 10
        if end_page > no_pages:
            end_page = no_pages

    menu_list = Menu.objects.filter(parent=None, is_active=True)
    event_list = Event.objects.filter(
        is_active=True).order_by('-start_date')[0:2]
    footer_events = Event.objects.filter(
        is_active=True).order_by('-start_date')[0:4]
    return render_to_response("site/archive-posts.html",
                              {'current_page': page,
                               'month_name': calendar.month_name[int(month)],
                               'year': year,
                               'month': month,
                               'archives': archives,
                               'category_list': Category.objects.all(),
                               'event_list': event_list,
                               'footer_events': footer_events,
                               'menu_list': menu_list,
                               'pages': range(start_page, end_page + 1),
                               'last_page': no_pages,
                               'post_list': post_list})


def rss(request):

    xml_cont = '''<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
                        <channel>
                        <atom:link href="http://www.cjws.com/rss.xml"
                        rel="self" type="application/rss+xml" />
                        <title>cjws | blog</title>
                        <description>
                        cjws blog and events
                        </description>
                        <language>en-us</language>
                            '''
    post = Post.objects.filter(is_active=True).order_by('-created_on')[:20]

    for i in post:

        xml_cont = xml_cont + \
            '<item><title><![CDATA[' + i.title + ']]></title>'
        xml_cont = xml_cont + \
            '<description><![CDATA[' + i.description + \
            ']]></description></item>'

    pages = Page.objects.all()[::-1]
    for p in pages:
        xml_cont = xml_cont + \
            '<item><title><![CDATA[' + p.title + ']]></title>'
        xml_cont = xml_cont + \
            '<description><![CDATA[' + p.content + ']]></description></item>'

    event_list = Event.objects.filter(
        is_active=True).order_by('-start_date')[:20]
    for i in event_list:
        xml_cont = xml_cont + '<item><title><![CDATA[' + i.name + ']]></title>'
        xml_cont = xml_cont + \
            '<description><![CDATA[' + i.description + ']]></description>'
        xml_cont = xml_cont + \
            '<location><![CDATA[' + str(i.location) + ']]></location>'
        xml_cont = xml_cont + \
            '<contact_details ><![CDATA[' + \
            str(i.contact_details) + ']]></contact_details ></item>'
    xml_cont = xml_cont + '</channel></rss>'

    return HttpResponse(xml_cont, content_type="text/xml")


def page_display(request, slug):
    page = Page.objects.get(slug=slug)
    menu_list = Menu.objects.filter(parent=None, is_active=True)
    event_list = Event.objects.filter(
        is_active=True).order_by('-start_date')[0:2]
    footer_events = Event.objects.filter(
        is_active=True).order_by('-start_date')[0:4]
    return render_to_response('site/page_detail.html',
                              {'menu_list': menu_list,
                               'footer_events': footer_events,
                               'event_list': event_list,
                               'page': page})


def banner_content(request, slug):
    banner = Banner.objects.get(slug=slug)
    menu_list = Menu.objects.filter(parent=None, is_active=True)
    event_list = Event.objects.filter(
        is_active=True).order_by('-start_date')[0:2]
    footer_events = Event.objects.filter(
        is_active=True).order_by('-start_date')[0:4]
    return render_to_response('site/page_detail.html',
                              {'menu_list': menu_list,
                               'footer_events': footer_events,
                               'event_list': event_list,
                               'banner': banner})


def sitemap(request):
    xml_cont = '''<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'''
    xml_cont = xml_cont + \
        '<url><loc>http://www.cjws.com/</loc> + \
        <changefreq>daily</changefreq><priority>0.85</priority></url>'
    xml_cont = xml_cont + '<url><loc>http://www.cjws.com/post_list/</loc> + \
        <changefreq>daily</changefreq><priority>0.85</priority></url>'
    xml_cont = xml_cont + '<url><loc>http://www.cjws.com/event_list/</loc> + \
        <changefreq>daily</changefreq><priority>0.85</priority></url>'
    xml_cont = xml_cont + '<url><loc>http://www.cjws.com/contact_us/</loc> + \
        <changefreq>daily</changefreq><priority>0.85</priority></url>'
    s = Menu.objects.all()
    for i in s:
        xml_cont = xml_cont + '<url><loc>http://www.cjws.com/' + i.slug + \
            '</loc><changefreq>daily</changefreq> + \
            <priority>0.85</priority></url>'

    posts = Post.objects.filter(is_active=True)
    for i in posts:
        xml_cont = xml_cont + '<url><loc>http://www.cjws.com/post_detail/' + \
            str(i.id) + '</loc><changefreq>daily</changefreq> + \
            <priority>0.85</priority></url>'

    events = Event.objects.filter(is_active=True)
    for e in events:
        xml_cont = xml_cont + '<url><loc>http://www.cjws.com/event_detail/' + \
            str(e.id) + '</loc><changefreq>daily</changefreq> + \
            <priority>0.85</priority></url>'

    pages = Page.objects.all()

    for p in pages:
        xml_cont = xml_cont + '<url><loc>http://www.cjws.com/' + p.slug + \
            '</loc><changefreq>daily</changefreq> + \
            <priority>0.85</priority></url>'

    xml_cont = xml_cont + '</urlset>'

    return HttpResponse(xml_cont, content_type="text/xml")


def handler404(request, exception):
    return render(request, 'site/404.html', status=404)


def handler500(request):
    return render(request, 'site/500.html', status=500)
