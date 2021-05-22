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
from fuzzywuzzy import fuzz


class AutofillOGRNView(APIView):
    """
    Returns data about company (searched by OGRN)
    """

    def post(self, request):
        ogrn = request.data['ogrn']
        # if request.data['type']=='inn':
        #     inn = request.data['inn']
        # elif request.data['type']=='ogrn':
        #     ogrn = request.data['ogrn']
        types = {'h': np.int64,
                 'i': np.int64,
                 'j': np.int64}
        dfs = pd.read_excel(r'main_app/data.xlsx', dtype=types)
        try:
            temp_str = dfs.iloc[np.int64(dfs['ОГРН']) == int(ogrn)].index[0]

            data = {
                "inn": str(int(dfs['ИНН'][temp_str])),
                "ogrn": ogrn,
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


class AutofillINNView(APIView):
    """
    Returns data about company (searched by INN)
    """

    def post(self, request):
        inn = request.data['inn']
        # if request.data['type']=='inn':
        #     inn = request.data['inn']
        # elif request.data['type']=='ogrn':
        #     ogrn = request.data['ogrn']
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


class SaveView(APIView):
    """
    Saves company data to the user's profile
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        data = json.loads(user.company)

        return Response({
            'status': status.HTTP_200_OK,
            'data': data
        })

    def post(self, request):
        user = request.user
        user.company = request.data['company']
        user.save()
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


class FillDBView(APIView):
    """
    Fills db from json
    """

    def fuzz_me(self, purpose):
        dfs = pd.read_excel(r'main_app/data_main.xlsx')
        # dfs = dfs.astype({
        #     '\"ID\"': 'str',
        #     '\"GUARANTEE_COST\"': 'str',
        #     '\"DATE_NPA\"': 'str',
        #     '\"IS_NOT_ACTIVE\"': 'str',
        #     '\"IS_SOFINANCE\"': 'str',
        # })
        max = 0
        max_i = 0
        temp_i = 0
        for value in dfs['\"SMALL_NAME\"']:
            temp = fuzz.ratio(purpose, str(value))
            if max < temp:
                max = temp
                max_i = temp_i
            # print(max, '\t', max_i, '\t', temp, '\t', str(value)[0:20])
            temp_i += 1

        # df = dfs.iloc[max_i].to_dict()
        # print(dfs.dtypes)
        # print(df)

        data = {
            'ID': str(dfs['\"ID\"'][max_i]),
            'URL': str(dfs['\"URL\"'][max_i]),
            'SMALL_NAME': str(dfs['\"SMALL_NAME\"'][max_i]),
            'FULL_NAME': str(dfs['\"FULL_NAME\"'][max_i]),
            'NUMBER_NPA': str(dfs['\"NUMBER_NPA\"'][max_i]),
            'DATE_NPA': str(dfs['\"DATE_NPA\"'][max_i]),
            'DESCRIPTION': str(dfs['\"DESCRIPTION\"'][max_i]),
            'PURPOSE': str(dfs['\"PURPOSE\"'][max_i]),
            'OBJECTIVE': str(dfs['\"OBJECTIVE\"'][max_i]),
            'TYPE_MERA': str(dfs['\"TYPE_MERA\"'][max_i]),
            'TYPE_FORMAT_SUPPORT': str(dfs['\"TYPE_FORMAT_SUPPORT\"'][max_i]),
            'SROK_VOZVRATA': str(dfs['\"SROK_VOZVRATA\"'][max_i]),
            'PROCENT_VOZVRATA': str(dfs['\"PROCENT_VOZVRATA\"'][max_i]),
            'GUARANTE_PERIODE': str(dfs['\"GUARANTE_PERIODE\"'][max_i]),
            'GUARANTEE_COST': str(dfs['\"GUARANTEE_COST\"'][max_i]),
            'APPLIANCE_ID': str(dfs['\"APPLIANCE_ID\"'][max_i]),
            'OKVED2': str(dfs['\"OKVED2\"'][max_i]),
            'COMPLEXITY': str(dfs['\"COMPLEXITY\"'][max_i]),
            'AMOUNT_OF_SUPPORT': str(dfs['\"AMOUNT_OF_SUPPORT\"'][max_i]),
            'REGULARITY_SELECT': str(dfs['\"REGULARITY_SELECT\"'][max_i]),
            'PERIOD': str(dfs['\"PERIOD\"'][max_i]),
            'DOGOVOR': str(dfs['\"DOGOVOR\"'][max_i]),
            'GOS_PROGRAM': str(dfs['\"GOS_PROGRAM\"'][max_i]),
            'EVENT': str(dfs['\"EVENT\"'][max_i]),
            'DOP_INFO': str(dfs['\"DOP_INFO\"'][max_i]),
            'IS_NOT_ACTIVE': str(dfs['\"IS_NOT_ACTIVE\"'][max_i]),
            'PRICHINA_NOT_ACT': str(dfs['\"PRICHINA_NOT_ACT\"'][max_i]),
            'REQ_ZAYAVITEL': str(dfs['\"REQ_ZAYAVITEL\"'][max_i]),
            'REQUEST_PROJECT': str(dfs['\"REQUEST_PROJECT\"'][max_i]),
            'IS_SOFINANCE': str(dfs['\"IS_SOFINANCE\"'][max_i]),
            'DOLYA_ISOFINANCE': str(dfs['\"DOLYA_ISOFINANCE\"'][max_i]),
            'BUDGET_PROJECT': str(dfs['\"BUDGET_PROJECT\"'][max_i]),
            'POKAZATEL_RESULT': str(dfs['\"POKAZATEL_RESULT\"'][max_i]),
            'TERRITORIAL_LEVEL': str(dfs['\"TERRITORIAL_LEVEL\"'][max_i]),
            'REGION_ID': str(dfs['\"REGION_ID\"'][max_i]),
            'RESPONS_STRUCTURE': str(dfs['\"RESPONS_STRUCTURE\"'][max_i]),
            'ORG_ID': str(dfs['\"ORG_ID\"'][max_i]),
        }

        return data

    def get(self, request):
        res = {
            "probs": {
                "02004111950168580812": 0.2,
                "02004121610168733811": 0.1,
                "02004121616713810242": 0.3,
                "020060516101626750811": 0.0001,
                "02006051610166750811": 0.4,
                "020060516101667350811": 0.001,
            }
        }
        data = [(key, value) for key, value in res['probs'].items()]
        data.sort(key=lambda val: val[1], reverse=True)
        data = [(key, value) for key, value in data if value > 0.05]

        for el in data:
            print(el)

        with open('main_app/subsidy.json', 'r', encoding="utf8") as f:
            subsidies = json.load(f)

        res_list = []
        for el in data:
            temp_kbk = el[0]
            temp_purpose = subsidies[temp_kbk]['purpose']
            df = self.fuzz_me(temp_purpose)
            res_list.append(df)

        # for el in res_list

        # res_json = json.dumps(res_list)

        # with open('main_app/subsidy_all_fields.json', 'r', encoding="utf8") as f:
        #     data = json.load(f)
        #
        # purpose = 'Субсидии российским организациям на финансовое обеспечение части затрат на создание научно-технического задела по разработке базовых технологий производства приоритетных электронных компонентов и радиоэлектронной аппаратуры'
        # print(self.fuzz_me(purpose))
        # dfs = pd.read_excel(r'main_app/data_main.xlsx')
        # print(dfs['\"SMALL_NAME\"'][1897])

        return Response({
            'status': status.HTTP_200_OK,
            'data': res_list
        })
