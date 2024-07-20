from Chatmate.Utility.auth_helpers import create_response
from Chatmate.Utility.processing_query import process_query
from Chatmate.models import Documents, Query
from Chatmate.serializers import DocumentSerializer, QuerySerializer
from rest_framework import viewsets, status
from rest_framework.decorators import action
from django.http import StreamingHttpResponse
from rest_framework.parsers import MultiPartParser
from rest_framework.parsers import FormParser


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Documents.objects.all()
    serializer_class = DocumentSerializer

    @action(detail=False, methods=['post'], parser_classes=[MultiPartParser, FormParser])
    def upload_file(self, request):
        file = request.data.get('file')
        if file:
            document = Documents.objects.create(file=file)
        return create_response(True, 'Document uploaded successfully', body=DocumentSerializer(document).data, status_code=status.HTTP_201_CREATED)

class QueryViewSet(viewsets.ModelViewSet):
    queryset = Query.objects.all()
    serializer_class = QuerySerializer

    @action(detail=False, methods=['post'])
    def process_chat(self, request):
        query = request.data.get('query')
        response = process_query(query)
        return StreamingHttpResponse(response, content_type="text/plain")