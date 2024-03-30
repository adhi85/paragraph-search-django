from django.shortcuts import render
from django.http import HttpResponse
from base.models import Paragraph,Word

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the base index.")

@api_view(['POST'])
def create_paras(request):
    paras = request.data['para']
    paras_list = paras.split('\n\n')

    for para in paras_list:
        p = Paragraph.objects.create(text=para)
        words = para.split()
        for word in words:
            word = word.lower()
            w,create = Word.objects.get_or_create(text=word,para=p)

    return Response(status=status.HTTP_201_CREATED)

@api_view(['GET'])
def search_para(request,word):
    word = word.lower()
    word_paras = Word.objects.filter(text=word).values_list('para', flat=True).distinct()
    paras = Paragraph.objects.filter(id__in=word_paras)[:10]
    para_texts = [para.text for para in paras]
    return Response({"paras":para_texts})