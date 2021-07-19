from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from django.http.response import JsonResponse
from django.http import HttpResponseRedirect
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
