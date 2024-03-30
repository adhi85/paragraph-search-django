from django.core.exceptions import ValidationError
from django.http import HttpResponse
from base.models import Paragraph, Word

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from base.serializers import UserSerializer
from django.db import transaction
from django.utils.html import escape


# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the base index.")


# Create a user
@api_view(["POST"])
@permission_classes([AllowAny])
def create_user(request):
    try:
        if request.method == "POST":
            with transaction.atomic():
                serializer = UserSerializer(data=request.data)  # create a user serializer
                if serializer.is_valid():
                    user = serializer.save()
                    return Response({"message": "User created successfully", "user": serializer.data}, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@permission_classes([IsAuthenticated])
@api_view(["POST"])
def create_paras(request):
    try:
        paras = request.data.get("para")  # get the paragraph from the request
        if not paras or not isinstance(paras, str):
            return Response(
                {"error": "Invalid input. 'para' field is missing or not a string."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        paras_list = paras.split("\n\n")  # split the paragraph into list of paragraphs

        # create paragraphs and words in a transaction to ensure atomicity
        with transaction.atomic():
            for para in paras_list:
                p = Paragraph.objects.create(text=para, owner=request.user)
                words = para.split()
                for word in words:
                    word = word.lower()
                    _, created = Word.objects.get_or_create(
                        text=word, para=p
                    )  # get or create word object

        return Response(
            {"message": "Paragraphs created successfully."},
            status=status.HTTP_201_CREATED,
        )

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# search for a word in the paragraphs
@permission_classes([IsAuthenticated])
@api_view(["GET"])
def search_para(request, word):
    try:
        word = escape(word.strip().lower())

        # Search for paragraphs containing the word
        word_paras = (
            Word.objects.filter(text=word).values_list("para", flat=True).distinct()
        )

        # Paginate the results
        paras = Paragraph.objects.filter(id__in=word_paras)[:10]

        # Create a dictionary of paragraph texts
        para_texts = {
            f"Paragraph {index + 1}": para.text for index, para in enumerate(paras)
        }

        return Response({"paras": para_texts})

    except ValidationError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
