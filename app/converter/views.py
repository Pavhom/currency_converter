from django.shortcuts import render
import requests
from django.conf import settings
# Create your views here.


def converter(request):
    response = requests.get(f'https://v6.exchangerate-api.com/v6/{settings.EXCHANGERATE_API}/latest/UAH')
    currencies = response.json().get('conversion_rates')

    if request.method == 'GET':
        context = {'currencies': currencies}
        return render(request, template_name='converter/index.html', context=context)

    if request.method == 'POST':
        form_data = request.POST
        pair_conversion = requests.get(f'https://v6.exchangerate-api.com/v6/{settings.EXCHANGERATE_API}/pair/{form_data["from_currency"]}/{form_data["to_currency"]}/{form_data["amount"]}').json()
        conversion_result = pair_conversion.get('conversion_result')
        context = {'currencies': currencies,
                   'conversion_result': round(conversion_result, 2),
                   'amount': form_data["amount"],
                   'from_currency': form_data["from_currency"],
                   'to_currency': form_data["to_currency"],
                   }

        return render(request, template_name='converter/index.html', context=context)
