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
from openpyxl import load_workbook
from datetime import datetime
import pandas as pd
import numpy as np


class AutofillView(APIView):
    """
    Returns data about company (searched by INN)
    """

    def post(self, request):
        inn = request.data['inn']
        types = {'h': np.int64,
                 'i': np.int64,
                 'j': np.int64}
        dfs = pd.read_excel(r'main_app/data.xlsx', dtype=types)
        try:
            temp_str = dfs.iloc[np.int64(dfs['ИНН']) == int(inn)].index[0]

            data = {
                "inn": inn,
                "ogrn": dfs['ОГРН'][temp_str],
                "okved": dfs['ОКВЭД2'][temp_str].split(' / '),
                "osn_tass": dfs['Вид деятельности, основной ТАСС'][temp_str],
                "dop_tass": dfs['Вид деятельности, дополнительный ТАСС'][temp_str].split(' / '),
                "otr": dfs['Отрасль'][temp_str].split(' / '),
                "attrs": dfs['Атрибуты предприятия'][temp_str].split(' / '),
                "region": dfs['Регион'][temp_str],
                "form": dfs['Организационно правовая форма'][temp_str],
            }
            return Response({
                'status': status.HTTP_200_OK,
                'data': data
            })
        except:
            return Response({'status': status.HTTP_404_NOT_FOUND})

        # wb = load_workbook('data.xlsx')
        # sheet = wb['сводная информация']
        # print(sheet[1].value)

        # birthdays = []
        #
        # for i in range(35):
        #     index_name = 'B' + str(i + 2)
        #     index_birth = 'C' + str(i + 2)
        #     temp_dict = {
        #         'name': sheet[index_name].value,
        #         'birth': sheet[index_birth].value,
        #     }
        #     birthdays.append(temp_dict)
        #
        # i = 0
        # print('\nBirthdays in the current month:')
        # for el in sorted(birthdays, key=lambda x: x['birth'].day, reverse=False):
        #     i += 1
        #     if el['birth']:
        #         if el['birth'].month == CURRENT_MONTH:
        #             print(el['birth'].day, '\t', el['name'])
        #
        # i = 0
        # print('\nBirthdays in the next month:')
        # for el in sorted(birthdays, key=lambda x: x['birth'].day, reverse=False):
        #     i += 1
        #     if el['birth']:
        #         if el['birth'].month == NEXT_MONTH:
        #             print(el['birth'].day, '\t', el['name'])
        return Response(status.HTTP_200_OK)


class SaveView(APIView):
    """
    Saves company data to the user's profile
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        # user = request.user
        return Response(status.HTTP_200_OK)


class CompareView(APIView):
    """
    Returns two selected subsidies
    """

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
