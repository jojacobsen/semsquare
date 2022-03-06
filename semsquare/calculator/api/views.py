import pandas as pd
import json
from rest_framework import status
from rest_framework import views
from rest_framework.response import Response
from .serializers import PlspmSerializer, LatentVariableSerializer
from ..functions import run_pls

class PostView(views.APIView):
    def post(self, request):
        if request.method == "POST":
            serializer = LatentVariableSerializer(data=request.data)

            if serializer.is_valid():
                # run_pls(input_json, dataset)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            #dataset = pd.read_json(input_json["data"])
            #run_pls(input_json, dataset)
