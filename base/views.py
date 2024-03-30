from django.shortcuts import render
from django.http import HttpResponse
from base.models import Paragraph, Word

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from base.serializers import UserSerializer


# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the base index.")

# Create a user
@api_view(["POST"])
@permission_classes([AllowAny])
def create_user(request):
    if request.method == "POST":
        serializer = UserSerializer(data=request.data) # create a user serializer
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
@api_view(["POST"])
def create_paras(request):
    paras = request.data["para"]  # get the paragraph from the request
    paras_list = paras.split("\n\n")  # split the paragraph into list of paragraphs

    # create paragraph and word objects
    for para in paras_list:
        p = Paragraph.objects.create(text=para, owner=request.user)
        words = para.split()
        for word in words:
            word = word.lower()
            w, create = Word.objects.get_or_create(
                text=word, para=p
            )  # get or create word object

    return Response(status=status.HTTP_201_CREATED)


# search for a word in the paragraphs
@permission_classes([IsAuthenticated])
@api_view(["GET"])
def search_para(request, word):
    word = word.lower()
    word_paras = (
        Word.objects.filter(text=word).values_list("para", flat=True).distinct()
    )  # get the paragraphs containing the word
    paras = Paragraph.objects.filter(id__in=word_paras)[
        :10
    ]  # get the first 10 paragraphs
    para_texts = {
        "Paragraph-" + str(val + 1): para.text for val, para in enumerate(paras)
    }  # create a dictionary of paragraph texts
    return Response({"paras": para_texts})
