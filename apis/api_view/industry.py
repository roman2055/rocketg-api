from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apis.api_view.utility import getIndustryData
from apis.models import Industry_locales


@api_view(['GET'])
def industryGet(request):
    token = request.headers.get('access-token')
    client = request.headers.get('client')
    uid = request.headers.get('uid')
    lang = request.headers.get('lang')

    if lang is None or lang == '':
        lang = 'en'

    if request.method == 'GET':
        industryList = None
        try:
            industryList = Industry_locales.objects.filter(Q(language=lang)).order_by('industry_id')
        except Industry_locales.DoesNotExist:
            return Response(data={'success': False, 'error': ['Error in getting industry.']}, status=status.HTTP_200_OK)

        industryData = getIndustryData(industryList)
        return Response(data={'success': True, 'data': industryData}, status=status.HTTP_200_OK)