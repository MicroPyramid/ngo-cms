from django.shortcuts import render
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as signin
from django.http.response import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
import os
# from django.core.context_processors import csrf
from blog.models import Category, Gal_Image, Post, Menu, Page, Image_File, Banner
from blog.forms import CategoryForm, PostForm, MenuForm, PageForm, bannerForm, PasswordForm
from events.forms import EventForm
from events.models import Event
from PIL import Image
from django.core.files.base import File as fle
from django.core.files.storage import default_storage
from django.db.models import Max


@csrf_exempt
def upload_photos(request):
    '''
    takes all the images coming from the redactor editor and
    stores it in the database and returns all the files'''

    if request.FILES.get("upload"):
        f = request.FILES.get("upload")
        obj = Image_File.objects.create(upload=f, is_image=True)
        size = (128, 128)
        x = f.name
        z = 'thumb' + f.name
        y = open(x, 'w')
        for i in f.chunks():
            y.write(i)
        y.close()
        im = Image.open(x)
        im.thumbnail(size)
        im.save(z)
        imdata = open(z)
        obj.thumbnail.save(z, fle(imdata))
        imdata.close()
        # obj.thumbnail = imdata
        os.remove(x)
        os.remove(z)
        upurl = default_storage.url(obj.upload.url)
    upurl = upurl
    return HttpResponse("""
    <script type='text/javascript'>
        window.parent.CKEDITOR.tools.callFunction({0}, '{1}');
    </script>""".format(request.GET['CKEditorFuncNum'], upurl))


@csrf_exempt
def recent_photos(request):
    ''' returns all the images from the data base '''
    imgs = []
    for obj in Image_File.objects.filter(is_image=True).order_by("-date_created"):
        upurl = default_storage.url(obj.upload.url)
        thumburl = default_storage.url(obj.thumbnail.url)
        imgs.append({'src': upurl, 'thumb': thumburl, 'is_image': True})
    return render_to_response('admin/browse.html', {'files': imgs})


def login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            posts = Post.objects.all().count()
            categoryies = Category.objects.all().count()
            menus = Menu.objects.all().count()
            pages = Page.objects.all().count()
            events = Event.objects.all().count()
            return render_to_response("admin/index.html",
                                      {'posts': posts,
                                       'categoryies': categoryies,
                                       'menus': menus,
                                       'pages': pages,
                                       'events': events})
        return HttpResponseRedirect("/")

    if request.method == "POST":
        user = authenticate(email=request.POST.get("email"),
                            password=request.POST.get("password"))
        if user is not None:
            if user.is_superuser and user.is_active:
                signin(request, user)
                data = {"error": False}
                return JsonResponse(data)

            data = {"error": True,
                    "message": "Your account is not yet activated!"}
            return JsonResponse(data)

        data = {"error": True,
                "message": "Username and password were incorrect."}
        return JsonResponse(data)

    return render(request, "admin/login.html")


@login_required
def category_list(request):
    category_list = Category.objects.all()
    return render_to_response('admin/category-list.html',
                              {'category_list': category_list})


@login_required
def post_list(request):
    post_list = Post.objects.all().order_by('id')
    return render_to_response('admin/post-list.html', {'post_list': post_list})


@login_required
def event_list(request):
    event_list = Event.objects.all().order_by('id')
    return render_to_response('admin/event-list.html',
                              {'event_list': event_list})


@login_required
def menu_list(request):
    menu_list = Menu.objects.filter(parent=None)
    return render_to_response('admin/menu-list.html', {'menu_list': menu_list})


@login_required
def page_list(request):
    page_list = Page.objects.all()
    return render_to_response('admin/page-list.html', {'page_list': page_list})


@login_required
def banner_list(request):
    banner_list = Banner.objects.all()
    return render_to_response('admin/banner-list.html',
                              {'banner_list': banner_list})


@login_required
def add_category(request):

    if request.method == 'GET':
        category_list = Category.objects.all()
        return render(request, 'admin/category-add.html',
                      {'category_list': category_list})

    validate_category = CategoryForm(request.POST)
    errors = {}
    if validate_category.is_valid():
        new_category = validate_category.save()
        if request.FILES['image']:
            new_category.image = request.FILES['image']
        new_category.save()
        data = {"data": 'Category created successfully', "error": False}
        return JsonResponse(data)

    for k in validate_category.errors:
        errors[k] = validate_category.errors[k][0]
    return JsonResponse(errors)


@login_required
def add_post(request):

    if request.method == 'GET':
        category_list = Category.objects.all()
        post_list = Post.objects.all()
        return render(request, 'admin/post-add.html',
                      {'category_list': category_list, 'post_list': post_list})

    validate_post = PostForm(request.POST)
    errors = {}
    if validate_post.is_valid():
        new_post = validate_post.save(commit=False)

        if 'image' not in request.FILES:
            errors['image'] = 'Please upload Image'
            return JsonResponse(errors)

        if request.FILES['image']:
            new_post.image = request.FILES['image']
            new_post.save()

        photos = request.FILES.getlist('photos')
        for p in photos:
            img = Gal_Image.objects.create(image=p)
            new_post.photos.add(img)
        data = {"data": 'Post created successfully', "error": False}
        return JsonResponse(data)

    if 'image' not in request.FILES:
        validate_post.errors['image'] = 'Please upload Image'
    return JsonResponse(validate_post.errors)


@login_required
def add_event(request):

    if request.method == 'GET':
        event_list = Event.objects.all()
        return render(request, 'admin/event-add.html',
                      {'event_list': event_list})

    validate_event = EventForm(request.POST)
    errors = {}
    if validate_event.is_valid():
        if validate_event.cleaned_data['end_date'] and validate_event.cleaned_data['start_date']:
            if validate_event.cleaned_data['start_date'] > validate_event.cleaned_data['end_date']:
                errors['date_err'] = 'Start Date should not greater than End Date'
                return JsonResponse(errors)

        if 'image' not in request.FILES:
            errors['image'] = 'Please upload Image'
            return JsonResponse(errors)

        new_event = validate_event.save(commit=False)
        new_event.image = request.FILES['image']
        new_event.save()
        data = {"data": 'event created successfully', "error": False}
        return JsonResponse(data) 
    
    for k in validate_event.errors:
        errors[k] = validate_event.errors[k][0]
    if 'image' not in request.FILES:
        errors['image'] = 'Please upload Image'

    return JsonResponse(errors)


@login_required
def delete_category(request, pk):
    category = Category.objects.get(pk=pk)
    category.delete()
    return HttpResponseRedirect('/admin/category/list/')


@login_required
def delete_post(request, pk):
    post = Post.objects.get(pk=pk)
    image_path = post.image.url

    for img in post.photos.all():
        photo_path = img.image.url
        try:
            os.remove(photo_path)
        except FileNotFoundError:
            pass
    try:
        os.remove(image_path)
    except FileNotFoundError:
        pass
    post.delete()
    return HttpResponseRedirect('/admin/article/list/')


@login_required
def edit_category(request, pk):
    if request.method == "GET":
        category = Category.objects.get(pk=pk)
        category_list = Category.objects.all()
        return render(request, 'admin/category-edit.html',
                      {'category_list': category_list, 'category': category})

    c = Category.objects.get(pk=pk)
    validate_category = CategoryForm(request.POST, instance=c)
    errors = {}

    if validate_category.is_valid():
        new_category = validate_category.save()
        if request.FILES['image']:
            new_category.image = request.FILES['image']
            new_category.save()
        data = {"data": 'Category edited successfully', "error": False}
        return JsonResponse(data)

    for k in validate_category.errors:
        errors[k] = validate_category.errors[k][0]
    return JsonResponse(errors)


@login_required
def edit_post(request, pk):
    if request.method == "GET":
        post = Post.objects.get(pk=pk)
        category_list = Category.objects.all()
        post_list = Post.objects.all()
        return render(request, 'admin/post-edit.html',
                      {'post': post, 'post_list': post_list,
                       'category_list': category_list})
    
    p = Post.objects.get(pk=pk)
    validate_post = PostForm(request.POST, instance=p)
    errors = {}
    if validate_post.is_valid():
        new_post = validate_post.save(commit=False)

        if 'image' in request.FILES:
            image_path = p.image.url
            try:
                os.remove(image_path)
            except Exception:
                pass
            new_post.image = request.FILES['image']
        new_post.save()

        photos = request.FILES.getlist('photos')
        for p in photos:
            img = Gal_Image.objects.create(image=p)
            new_post.photos.add(img)
        return JsonResponse({"data": 'Post edited successfully', "error": False})

    for k in validate_post.errors:
        errors[k] = validate_post.errors[k][0]
    return JsonResponse(errors)


@login_required
def edit_event(request, pk):
    if request.method == "GET":
        event = Event.objects.get(pk=pk)
        event_list = Event.objects.all()
        return render(request, 'admin/event-edit.html',
                      {'event': event, 'event_list': event_list})

    e = Event.objects.get(pk=pk)
    validate_event = EventForm(request.POST, instance=e)
    errors = {}
    if validate_event.is_valid():
        if validate_event.cleaned_data['end_date'] and validate_event.cleaned_data['start_date']:
            if validate_event.cleaned_data['start_date'] > validate_event.cleaned_data['end_date']:
                errors['date_err'] = 'Start Date should not greater than End Date'
                return JsonResponse(errors)

        new_event = validate_event.save(commit=False)
        if 'image' in request.FILES:
            image_path = e.image.url
            try:
                os.remove(image_path)
            except FileNotFoundError:
                pass
            new_event.image = request.FILES['image']
        new_event.save()
        return JsonResponse({"data": 'event edited successfully', "error": False})

    for k in validate_event.errors:
        errors[k] = validate_event.errors[k][0]
    return JsonResponse(errors)


@login_required
def delete_event(request, pk):
    event = Event.objects.get(pk=pk)
    image_path = event.image.url
    try:
        os.remove(image_path)
    except FileNotFoundError:
        pass
    event.delete()
    return HttpResponseRedirect('/admin/event/list/')


def admin_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required
def add_menu(request):
    if request.method == 'GET':
        menu_list = Menu.objects.filter(parent=None)
        return render(request, 'admin/menu-add.html', {'menu_list': menu_list})
    validate_menu = MenuForm(request.POST)
    errors = {}
    if request.POST['slug'] == "":
        errors['slug'] = 'This field is required'
    if request.POST['name'] == "":
        errors['name'] = 'This field is required'

    # if len(errors)>0:
    #     return HttpResponse(json.dumps(errors))
    if validate_menu.is_valid():
        new_menu = validate_menu.save(commit=False)
        lvl_count = Menu.objects.filter(parent=new_menu.parent).count()
        new_menu.lvl = lvl_count + 1
        new_menu.save()
        return JsonResponse({"data": 'Menu created successfully', "error": False})

    for e in validate_menu.errors:
        errors[e] = validate_menu.errors[e][0]
    return JsonResponse(errors)


@login_required
def edit_menu(request, pk):
    if request.method == 'GET':
        menu = Menu.objects.get(pk=pk)
        menu_list = Menu.objects.filter(parent=None)
        return render(request, 'admin/menu-edit.html',
                      {'menu_list': menu_list, 'menu': menu})

    m = Menu.objects.get(pk=pk)
    old_parent = m.parent
    validate_menu = MenuForm(request.POST, instance=m)
    errors = {}
    if validate_menu.is_valid():
        menu = validate_menu.save(commit=False)
        if old_parent == menu.parent:
            menu.save()
        else:
            lvl_count = Menu.objects.filter(parent=menu.parent).count()
            menu.lvl = lvl_count + 1
            menu.save()
        return JsonResponse({"data": 'Menu Edited successfully', "error": False})

    for e in validate_menu.errors:
        errors[e] = validate_menu.errors[e][0]
    return JsonResponse(errors)


@login_required
def delete_menu(request, pk):
    curent_menu = Menu.objects.get(pk=pk)
    menu_parent = curent_menu.parent
    menu_lvl = curent_menu.lvl
    max_lvl = Menu.objects.filter(
        parent=menu_parent).aggregate(Max('lvl'))['lvl__max']
    Menu.objects.get(pk=pk).delete()
    if max_lvl != 1:
        for m in Menu.objects.filter(parent=menu_parent,
                                     lvl__gt=menu_lvl, lvl__lte=max_lvl):
            m.lvl -= 1
            m.save()

    return HttpResponseRedirect('/admin/menu/list/')


@login_required
def menu_state(request, pk):
    menu = Menu.objects.get(pk=pk)
    if menu.is_active is True:
        menu.is_active = False
        menu.save()
    else:
        menu.is_active = True
        menu.save()

    return HttpResponseRedirect('/admin/menu/list/')


@login_required
def menu_lvl_up(request, pk):
    m_parent = Menu.objects.get(pk=pk).parent
    curent_menu = Menu.objects.get(pk=pk)
    up_menu = Menu.objects.get(parent=m_parent, lvl=curent_menu.lvl - 1)
    curent_menu.lvl = curent_menu.lvl - 1
    up_menu.lvl = up_menu.lvl + 1
    curent_menu.save()
    up_menu.save()
    return HttpResponseRedirect('/admin/menu/list/')


@login_required
def menu_lvl_down(request, pk):
    m_parent = Menu.objects.get(pk=pk).parent
    curent_menu = Menu.objects.get(pk=pk)
    down_menu = Menu.objects.get(parent=m_parent, lvl=curent_menu.lvl + 1)
    curent_menu.lvl = curent_menu.lvl + 1
    down_menu.lvl = down_menu.lvl - 1
    curent_menu.save()
    down_menu.save()
    return HttpResponseRedirect('/admin/menu/list/')


@login_required
def post_state(request, pk):
    post = Post.objects.get(pk=pk)
    if post.is_active is True:
        post.is_active = False
        post.save()
    else:
        post.is_active = True
        post.save()

    return HttpResponseRedirect('/admin/article/list/')


@login_required
def event_state(request, pk):
    event = Event.objects.get(pk=pk)
    if event.is_active:
        event.is_active = False
        event.save()
    else:
        event.is_active = True
        event.save()
    return HttpResponseRedirect('/admin/event/list/')


@login_required
def delete_gal_image(request, pk, pid):
    img = Gal_Image.objects.get(pk=pk)
    image_path = img.image.url
    try:
        os.remove(image_path)
    except FileNotFoundError:
        pass
    img.delete()
    return HttpResponseRedirect('/admin/article/edit/' + pid)


@login_required
def delete_page_images(request, pk, pid):
    img = Gal_Image.objects.get(pk=pk)
    image_path = img.image.url
    try:
        os.remove(image_path)
    except FileNotFoundError:
        pass
    img.delete()
    return HttpResponseRedirect('/admin/page/edit/' + pid)


@login_required
def add_page(request):
    if request.method == 'GET':
        page_list = Page.objects.all()
        return render(request, 'admin/page-add.html', {'page_list': page_list})

    validate_page = PageForm(request.POST)
    errors = {}
    if validate_page.is_valid():
        new_page = validate_page.save()
        photos = request.FILES.getlist('photos')
        for p in photos:
            img = Gal_Image.objects.create(image=p)
            new_page.photos.add(img)
        new_page.save()
        return JsonResponse({'data': 'Page Created successfully', "error": False})

    for e in validate_page.errors:
        errors[e] = validate_page.errors[e][0]
    return JsonResponse(errors)


@login_required
def edit_page(request, pk):
    if request.method == 'GET':
        page = Page.objects.get(pk=pk)
        page_list = Page.objects.all()
        return render(request, 'admin/page-edit.html',
                      {'page': page, 'page_list': page_list})

    p = Page.objects.get(pk=pk)
    validate_page = PageForm(request.POST, instance=p)
    errors = {}
    if validate_page.is_valid():
        page = validate_page.save()
        photos = request.FILES.getlist('photos')
        for p in photos:
            img = Gal_Image.objects.create(image=p)
            page.photos.add(img)
        page.save()
        return JsonResponse({'data': 'Page edited successfully', "error": False})

    for e in validate_page.errors:
        errors[e] = validate_page.errors[e][0]
    return JsonResponse(errors)


@login_required
def delete_page(request, pk):
    page = Page.objects.get(pk=pk)
    page.delete()
    return HttpResponseRedirect('/admin/page/list/')


@login_required
def change_password(request):
    if request.method == 'GET':
        return render(request, 'admin/change-pwd.html')

    validate_password = PasswordForm(request.POST)
    errors = {}
    if validate_password.is_valid():
        pwd = validate_password.cleaned_data['old_password']
        if request.user.check_password(pwd):
            if validate_password.cleaned_data['new_password'] == validate_password.cleaned_data['re_password']:
                request.user.set_password(
                    validate_password.cleaned_data['new_password'])
                request.user.save()
                return JsonResponse({'data': 'password changed successfully',
                    'error': False})
            errors['repwd'] = 'New password and Re-enter password are not same'
            return JsonResponse(errors)
        errors['oldpwd'] = 'please enter correct password'
        return JsonResponse(errors)

    for e in validate_password.errors:
        errors[e] = validate_password.errors[e][0]
    return JsonResponse(errors)


def add_banner(request):
    if request.method == 'GET':
        return render(request, 'admin/banner-add.html')

    validate_banner = bannerForm(request.POST)
    errors = {}
    if validate_banner.is_valid():
        new_banner = validate_banner.save(commit=False)
        if 'image' not in request.FILES:
            errors['image'] = 'Please Upload Banner Image'
        if request.POST['title'] == "":
            errors['title'] = 'This field is required'
        if errors:
            return JsonResponse(errors)
        if request.FILES['image']:
            new_banner.image = request.FILES['image']
            new_banner.save()
            return JsonResponse({"data": 'Banner created successfully', "error": False})

    for k in validate_banner.errors:
        errors[k] = validate_banner.errors[k][0]
    return JsonResponse(errors)


def edit_banner(request, pk):
    if request.method == 'GET':
        banner = Banner.objects.get(pk=pk)
        return render(request, 'admin/banner-edit.html',
                      {'banner': banner})

    b = Banner.objects.get(pk=pk)
    validate_banner = bannerForm(request.POST, instance=b)
    errors = {}
    if validate_banner.is_valid():
        banner = validate_banner.save(commit=False)
        if 'image' in request.FILES:
            image_path = b.image.url
            try:
                os.remove(image_path)
            except Exception:
                pass
            banner.image = request.FILES['image']
        banner.save()
        return JsonResponse({'data': 'Banner edited successfully', 'error': False})

    for k in validate_banner.errors:
        errors[k] = validate_banner.errors[k][0]
    return JsonResponse(errors)


def delete_banner(request, pk):
    b = Banner.objects.get(pk=pk)
    img = b.image.url
    try:
        os.remove(img)
    except FileNotFoundError:
        pass
    b.delete()
    return HttpResponseRedirect('/admin/banner/list')
