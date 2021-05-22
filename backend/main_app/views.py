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
        # print('ok')
        # print(user.company)
        data = json.loads(user.company)
        # print(type(data))

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


class GetSubsidyView(APIView):
    """
    Returns selected subsidy
    """

    def post(self, request):
        id = request.data['id']
        dfs = pd.read_excel(r'main_app/data_main.xlsx')
        dfs = dfs.loc[dfs['\"ID\"'] == int(id)]
        print(dfs)
        max_i = 0
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

        return Response({
            'status': status.HTTP_200_OK,
            'data': data
        })


class PredictView(APIView):
    """
    Predicts the most relevant subsidies
    """

    def fuzz_me(self, purpose):
        dfs = pd.read_excel(r'main_app/data_main.xlsx')
        max = 0
        max_i = 0
        temp_i = 0
        for value in dfs['\"SMALL_NAME\"']:
            temp = fuzz.ratio(purpose, str(value))
            if max < temp:
                max = temp
                max_i = temp_i
            temp_i += 1

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

    def post(self, request):
        # temp_data = {
        #     'status': 200,
        #     'data': {
        #         "okved": request.data['okved'],
        #         "osn_tass": request.data['osn_tass'],
        #         "dop_tass": request.data['dop_tass'],
        #         "attrs": request.data['attrs'],
        #         "otr": request.data['otr'],
        #         "region": request.data['region'],
        #         "forma": request.data['forma'],
        #         # "kbk": request.data['kbk'],
        #         "inn": request.data['inn'],
        #         "ogrn": request.data['ogrn'],
        #     }
        # }

        temp_data = request.data['temp_data']

        # req_data = {
        #     "status": 200,
        #     "data": {
        #         "inn": "5908002499",
        #         "ogrn": "1025901607841",
        #         "okved": [
        #             "Производство лекарственных препаратов [27408]"
        #         ],
        #         "osn_tass": "Производство лекарственных препаратов [27408]",
        #         "dop_tass": [
        #             "Перевозка грузов неспециализированными автотранспортными средствами [28152]",
        #             "Деятельность вспомогательная прочая, связанная с перевозками [28284]",
        #             "Торговля оптовая фармацевтической продукцией [28508]",
        #             "Торговля оптовая изделиями, применяемыми в медицинских целях [28510]",
        #             "Торговля оптовая неспециализированная [28603]",
        #             "Торговля розничная лекарственными средствами в специализированных магазинах (аптеках) [28724]",
        #             "Торговля розничная изделиями, применяемыми в медицинских целях, ортопедическими изделиями в специализированных магазинах [28725]",
        #             "Предоставление прочих финансовых услуг, кроме услуг по страхованию и пенсионному обеспечению, не включенных в другие группировки [28887]",
        #             "Деятельность в области права [28950]",
        #             "Консультирование по вопросам коммерческой деятельности и управления [28963]",
        #             "Деятельность по техническому контролю, испытаниям и анализу прочая [29011]",
        #             "Научные исследования и разработки в области биотехнологии [29014]",
        #             "Научные исследования и разработки в области естественных и технических наук прочие [29015]",
        #             "Научные исследования и разработки в области общественных и гуманитарных наук [29020]",
        #             "Деятельность рекламных агентств [29025]",
        #             "Исследование конъюнктуры рынка и изучение общественного мнения [29028]",
        #             "Деятельность по изучению общественного мнения [29030]",
        #             "Аренда и лизинг легковых автомобилей и легких автотранспортных средств [29120]",
        #             "Аренда и лизинг прочих сухопутных транспортных средств и оборудования [29139]",
        #             "Общая врачебная практика [29233]"
        #         ],
        #         "otr": [
        #             "Фармацевтическая промышленность [266]"
        #         ],
        #         "attrs": [
        #             "С государственной поддержкой [9153213]"
        #         ],
        #         "region": "Пермский край [3516]",
        #         "form": "НЕПУБЛИЧНЫЕ АКЦИОНЕРНЫЕ ОБЩЕСТВА [7026704]"
        #     }
        # }

        # data = requests.post('http://ml:5000/predict', timeout=10000, json=temp_data).json()
        data = requests.post('http://localhost:5000/predict', timeout=10000, json=temp_data).json()

        data = [(key, value) for key, value in data['probs'].items()]
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

        return Response({
            'status': status.HTTP_200_OK,
            'data': res_list
        })
