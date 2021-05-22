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


class AutofillView(APIView):
    """
    Returns data about company (searched by INN)
    """

    # permission_classes = (IsAuthenticated,)

    def post(self, request):

        user = request.user
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


class SaveView(APIView):
    """
    Saves company data to the user's profile
    """

    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
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
        temp_data = {
            "okved": request.data['okved'],
            "osn_tass": request.data['osn_tass'],
            "dop_tass": request.data['dop_tass'],
            "attrs": request.data['attrs'],
            "otr": request.data['otr'],
            "region": request.data['region'],
            "forma": request.data['forma'],
            "kbk": request.data['kbk'],
            "inn": request.data['inn'],
            "ogrn": request.data['ogrn'],
        }

        # response = requests.post('http://ml:8000/predict', timeout=10000,
        #                          json={"file": base64.b64encode(request.FILES['file'].read()).decode('UTF-8')}).json()
        # answers = response['answers']
        # answers = self.pretty_json(answers)

        return Response(status.HTTP_200_OK)
