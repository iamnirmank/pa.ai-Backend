from Chatmate.Utility.auth_helpers import create_response
from Chatmate.Utility.processing_documents import update_combined_chunks
from Chatmate.Utility.processing_query import process_query
from Chatmate.models import CombinedChunk, Documents, Query
from Chatmate.serializers import CombinedChunkSerializer, DocumentSerializer, QuerySerializer
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
        update_combined_chunks()
        return create_response(True, 'Document uploaded successfully', body=DocumentSerializer(document).data, status_code=status.HTTP_201_CREATED)

    @action(detail=True, methods=['put'], parser_classes=[MultiPartParser, FormParser])
    def update_document(self, request, pk=None):
        document = self.get_object()
        file = request.data.get('file')
        if file:
            document.file = file
            document.save()
        update_combined_chunks()
        return create_response(True, 'Document updated successfully', body=DocumentSerializer(document).data, status_code=status.HTTP_200_OK)
    
    @action(detail=True, methods=['delete'])
    def delete_document(self, request, pk=None):
        document = self.get_object()
        if document.file:
            document.file.delete()
        document.delete()
        update_combined_chunks()
        return create_response(True, 'Document deleted successfully', status_code=status.HTTP_200_OK)

    @action(detail=False, methods=['delete'])
    def delete_all_documents(self, request):
        documents = Documents.objects.all()
        for document in documents:
            if document.file:
                document.file.delete()
            document.delete()
        update_combined_chunks()
        return create_response(True, 'All documents deleted successfully', status_code=status.HTTP_200_OK)

class QueryViewSet(viewsets.ModelViewSet):
    queryset = Query.objects.all()
    serializer_class = QuerySerializer

    @action(detail=False, methods=['post'])
    def process_chat(self, request):
        query = request.data.get('query')
        response = process_query(query)
        return StreamingHttpResponse(response, content_type="text/plain")
    
class CombinedChunkViewSet(viewsets.ModelViewSet):
    queryset = CombinedChunk.objects.all()
    serializer_class = CombinedChunkSerializer
    