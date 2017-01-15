from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, Http404
from PIL import Image as PILImg
from PIL import ImageEnhance as PILImageEnhance
from imgscaler.forms import UserForm
from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from imgscaler.meta import get_session
from imgscaler.models import Image
from imgscaler.services import ImageService
import uuid
import os

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def images(request):
    images = ImageService.all()
    template = "images.html"
    data = {}
    data.update(img_list=images)
    return render(request, template, data)

def image(request, image_id):
    entry = ImageService.by_id(image_id)
    if not entry:
        raise Http404("No Image found")
    template = "image.html"
    data = {}
    data.update(image=entry)
    data.update(MEDIA_ROOT=settings.MEDIA_URL)
    return render(request, template, data)
 
def upload(request):
    template = "upload.html"
    data = {}
 
    if request.POST:
        userform = UserForm(request.POST, request.FILES)
 
        if userform.is_valid():
            origin_form = userform.cleaned_data["user_file"]
            origin_name = origin_form.name
            filename, file_extension = os.path.splitext(origin_name)
            new_name = str(uuid.uuid4())+file_extension
            original_file = os.path.join(settings.STATIC_DIR, new_name)
 
            if os.path.isfile(original_file):
                os.remove(original_file)
 
            with open(original_file, 'wb+') as f:
                f.write(origin_form.read())
 
            origin_form.seek(0)

            try:
                image = PILImg.open(origin_form)
            except IOError:
                data.update(error_format='This is not image')
                return render(request, template, data)

            entry = Image()
            entry.orig_name = origin_name
            entry.orig_content = new_name
            dbsession = get_session()
            dbsession.add(entry)
            dbsession.commit()
            dbsession.close()
            data.update(MEDIA_ROOT=settings.MEDIA_URL)
            data.update(origin_name=new_name)
 
            userform = UserForm()
 
    else:
 
        userform = UserForm()
 
    data.update(userform=userform)
 
    return render(request, template, data)