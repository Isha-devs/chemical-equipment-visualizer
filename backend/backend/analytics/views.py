from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Dataset
from .utils import analyze_csv

class UploadCSVView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        file = request.FILES.get('file')

        if not file:
            return Response({"error": "No file uploaded"}, status=400)
        
        summary_data = analyze_csv(file)

        dataset = Dataset.objects.create(file=file,
                                         filename = file.name,
                                         summary = summary_data)


        old_datasets = Dataset.objects.order_by('-uploaded_at')[5:]
        Dataset.objects.filter(id__in = old_datasets.values_list('id', flat = True)).delete()


        

        return Response({
            "message": "File uploaded successfully",
            "summary": summary_data
        })
    


class UploadHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        datasets = Dataset.objects.order_by('-uploaded_at')[:5]

        return Response([
            {
                "filename": d.filename,
                "uploaded_at": d.uploaded_at,
                "summary": d.summary
            }
            for d in datasets
        ])
