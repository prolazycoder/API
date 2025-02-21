from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django.core.files.storage import default_storage
from .models import UploadedFile, ExtractedData
import pdfplumber
import pytesseract
from PIL import Image
import os
from rest_framework.generics import ListAPIView
from rest_framework import serializers

class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        uploaded_file = request.FILES['file']
        file_instance = UploadedFile.objects.create(file=uploaded_file)

        file_path = "C:\Users\ASUS\Downloads\SauLikh Assignment.pdf"
        extracted_text = ""

        if file_path.endswith(".pdf"):
            extracted_text = self.extract_pdf_text(file_path)
        elif file_path.endswith((".jpg", ".png", ".jpeg")):
            extracted_text = self.extract_image_text(file_path)

        ExtractedData.objects.create(file=file_instance, content=extracted_text)

        return Response({"message": "File processed", "text": extracted_text}, status=status.HTTP_201_CREATED)

    def extract_pdf_text(self, file_path):
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text.strip()

    def extract_image_text(self, file_path):
        image = Image.open(file_path)
        return pytesseract.image_to_string(image).strip()
    

class ExtractedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtractedData
        fields = '__all__'

class ExtractedDataView(ListAPIView):
    queryset = ExtractedData.objects.all()
    serializer_class = ExtractedDataSerializer
