from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from django.http.response import JsonResponse
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from rest_framework.exceptions import APIException
from .models import Prices
from .serializers import PricesSerializer, PricesDetailSerializer
import requests
import csv


class PricesListView(generics.ListAPIView):
    serializer_class = PricesSerializer

    def get_queryset(self):
        q = Prices.objects.all()
        q.delete()
        print('All Prices objects deleted')
        name=self.kwargs['name']
        company_list = name.split(',')
        if len(company_list) == 0:
            return Response({"message": "Please add at least one company name"}, status=400)
        elif len(company_list) == 1:
            create_prices(self, name=company_list[0])
            queryset = Prices.objects.filter(company=company_list[0]).order_by('date')
            return queryset
        else:
            for i in company_list:
                create_prices(self, name=i)
            queryset = Prices.objects.all().order_by('company')
            return queryset


class PricesDetailView(generics.ListAPIView):
    serializer_class = PricesDetailSerializer

    def get_queryset(self):
        name = self.kwargs['name']
        queryset = Prices.objects.filter(company=name).order_by('date')
        return queryset


def create_prices(self, name):
    company = name
    # print('company=', company)
    url = "https://query1.finance.yahoo.com/v7/finance/download/" + company + "?" \
          "period1=-10000000000&period2=2000000000&interval=1d&events=history&includeAdjustedClose=true"
    headers = {'Host':'query1.finance.yahoo.com',
               'User-Agent': 'PostmanRuntime/7.26.8',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept': '*/*',
               'Connection': 'keep-alive',
               'Cache-Control':'no-cache'}
    r = requests.get( url, headers=headers)
    if r.status_code==200:
        reader = csv.reader(r.text.splitlines())
        prices_list = []
        for row in reader:
            if row[0]!='Date':
                p = Prices()
                p.company = company
                p.date = row[0]
                p.open = row[1]
                p.high = row[2]
                p.low = row[3]
                p.close = row[4]
                p.adj_close = row[5]
                p.volume = row[6]
                # plat.save()
                prices_list.append(p)
        Prices.objects.bulk_create([Prices(**{'company': p.company,
                                              'date': p.date,
                                              'open': p.open,
                                              'high': p.high,
                                              'low': p.low,
                                              'close': p.close,
                                              'adj_close': p.adj_close,
                                              'volume': p.volume})
                                  for p in prices_list])
        return Response({"message": "Elements added to Prices."}, status=201)
    else:
        print('Error. Wrong company name!!')
        response = JsonResponse({'message':'Something wrong. It seems that there is no such company'}, status=400)
        return response



def hello(self):
    return JsonResponse({'Description':"REST API, returns JSON which contains historical information"
     " about the value of shares of companies for the entire period of their existence, according to Yahoo. Finance.",

'USAGE. endpoint': "'/prices/Company_name1,Company_name2,...,Company_nameN'",

'returns': "JSON with the data of the listed companies."
   "The number of companies can be 1 or several.",

'Example1':
   "'http://127.0.0.1:8000/prices/ZM'",
'returns JSON':
    '[{"company":"ZM","date":"2019-04-18","open":65.0,"high":66.0,"low":60.320999,"close":62.0,"adj_close":62.0,"volume":25764700},'
    '{"company":"ZM","date":"2019-04-22","open":61.0,"high":68.900002,"low":59.939999,"close":65.699997,"adj_close":65.699997,"volume":9949700},...',
'Example2':
    "http://127.0.0.1:8000/prices/RUN,ZUO",
'returns Json':
    '[{"company":"RUN","date":"2019-07-19","open":20.09,"high":20.459999,"low":19.709999,"close":19.77,"adj_close":19.77,"volume":1668300},...'
'{"company":"ZUO","date":"2019-05-23","open":22.1,"high":22.17,"low":20.32,"close":20.799999,"adj_close":20.799999,"volume":3787300}]"'})