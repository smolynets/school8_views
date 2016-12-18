
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from PIL import Image
from django.views.generic import UpdateView
from ..models import Biblioteka



#########################################################################
###adding


class form1(UpdateView):
  def podii_add(request):
    # was form posted?
    if request.method == "POST":
      # was form add button clicked?
      if request.POST.get('add_button') is not None:
        # errors collection
        errors = {}
        # data for student object
        data = {}
        # validate user input
        name = request.POST.get('name', '').strip()
        if not name:
          errors['name'] = u"Заголовок є обов'язковим"
        else:
          data['name'] = name
        text = request.POST.get('text', '').strip()
        if not text:
          errors['text'] = u"Текст є обов'язковим"
        else:
          data['text'] = text
      
        photo = request.FILES.get('photo')
        if photo:
          if photo.name.split(".")[-1].lower() not in ('jpg', 'jpeg', 'png', 'gif'):
             errors['photo'] = u"Файл має бути одного з наступних типів: jpg, jpeg, png, gif"
          else:
             try:
               Image.open(photo)
             except Exception:
               errors['photo'] = u"Завантажений файл не є файлом зображення або пошкоджений"
             else:
               if photo.size > 2 * 1024 * 1024:
                  errors['photo'] = u"Фото занадто велике (розмір файлу має бути менше 2Мб)"
               else:
                  data['photo'] = photo
           
        # save 
        if not errors:
          event = Biblioteka(**data)
          event.save()
          # redirect to podii list
          return HttpResponseRedirect( u'%s?status_message=Подія успішно додана'  % reverse('podii'))
        else:
          # render form with errors and previous user input
          return render(request, 'podii/podii_add_edit.html', {'errors': errors})
      elif request.POST.get('cancel_button') is not None:
        # redirect to home page on cancel button
        return HttpResponseRedirect( u'%s?status_message=Додавання події скасовано!' % reverse('podii'))
    else:
     # initial form render
     return render(request, 'podii/biblioteka_add_edit.html', {})