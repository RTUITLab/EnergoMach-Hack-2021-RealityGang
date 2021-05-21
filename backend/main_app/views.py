from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
# from .serializers import *
from .models import *
from rest_framework import status
import requests
import base64
import json


class CompareView(APIView):
    """
    Returns two selected subsidies
    """

    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        # subsidy_1 = Subsidy.objects.get(pk=request.data['subsidy_1'])
        # subsidy_2 = Subsidy.objects.get(pk=request.data['subsidy_2'])
        # return Response({
        #     'status': status.HTTP_200_OK,
        #     'data': {
        #         'subsidy_1': subsidy_1,
        #         'subsidy_2': subsidy_2
        #     }
        # })
        return Response(status.HTTP_200_OK)


class PredictView(APIView):
    """
    Predicts the most relevant subsidies
    """

    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        return Response(status.HTTP_200_OK)
