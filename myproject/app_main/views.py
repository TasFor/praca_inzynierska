from django.shortcuts import render

# Create your views here.
import yfinance as yf
from django.shortcuts import render
from .models import Stock
import matplotlib
matplotlib.use('Agg')

def fetch_stock_data(request):
    # Pobieranie danych dla akcji Apple
    data = yf.Ticker("AAPL").info
    stock, created = Stock.objects.update_or_create(
        symbol="AAPL",
        defaults={
            "name": data["shortName"],
            "price": data["currentPrice"],
        }
    )
    return render(request, "stock_data.html", {"stock": stock})

def home(request):
    return render(request, "home.html")

def introduction(request):
    return render(request, "introduction.html")

def stocks(request):
    return render(request, "stocks.html")

def technical_analysis(request):
    return render(request, "technical_analysis.html")

def real_estate(request):
    return render(request, "real_estate.html")

def login_panel(request):
    return render(request, "login_panel.html")


import yfinance as yf
from django.shortcuts import render

import yfinance as yf
from django.shortcuts import render


def stocks(request):

    # Mapowanie okresów
    period_map = {
        "15m": {"period": "1d", "interval": "15m"},  # Interwał 15 minut w ciągu 1 dnia
        "60m": {"period": "5d", "interval": "60m"},  # Interwał 1 godziny w ciągu 5 dni
        "1d": {"period": "1d", "interval": "1h"},   # 1 dzień
        "5d": {"period": "5d", "interval": "1d"},   # 5 dni
        "1mo": {"period": "1mo", "interval": "1d"}, # 1 miesiąc
        "3mo": {"period": "3mo", "interval": "1d"}, # 3 miesiące
        "6mo": {"period": "6mo", "interval": "1d"}, # 6 miesięcy
        "1y": {"period": "1y", "interval": "1d"},   # 1 rok
    }

    # Pobranie okresu od użytkownika (domyślnie 1 dzień)
    user_period = request.GET.get('period', '1d')
    selected_period = period_map.get(user_period, {"period": "1d", "interval": "1d"})

    # Lista symboli akcji (przykładowe 10 akcji, możesz rozszerzyć do 100)
    # symbols = [
    #     "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "NFLX", "ADBE", "ORCL",
    #     "INTC", "CSCO", "CMCSA", "AVGO", "QCOM", "TXN", "AMD", "AMAT", "MU", "ZM",
    #     "PYPL", "CRM", "BABA", "TWTR", "SHOP", "SQ", "DOCU", "SNAP", "ROKU", "UBER",
    #     "LYFT", "SPOT", "PLTR", "FSLY", "ETSY", "DDOG", "OKTA", "MDB", "ZS", "TEAM",
    #     "CLOU", "IBB", "ARKK", "QQQ", "SPY", "DIA", "V", "MA", "JPM", "BAC",
    #     "WFC", "GS", "MS", "C", "AXP", "BLK", "BRK-B", "VZ", "T", "TMUS",
    #     "DIS", "CMG", "MCD", "SBUX", "NKE", "HD", "LOW", "COST", "WMT", "AMGN",
    #     "BIIB", "REGN", "VRTX", "ISRG", "ILMN", "GILD", "ABBV", "JNJ", "PFE", "MRNA",
    #     "BNTX", "CVX", "XOM", "SLB", "OXY", "PSX", "VLO", "COP", "EOG", "BP",
    #     "TTE", "F", "GM", "TSLA", "NKLA", "RIVN", "LCID", "LI", "XPEV", "NIO"
    # ]

    symbols = [
        "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "NFLX", "ADBE", "ORCL"
    ]

    # Pobieranie danych o akcjach
    stocks_data = []
    for symbol in symbols:
        stock = yf.Ticker(symbol)

        try:
            # Pobieranie danych historycznych
            history = stock.history(period=selected_period["period"], interval=selected_period["interval"])

            # Pobranie cen
            #current_price = history['Close'].iloc[-1] if not history.empty else None
            # Pobieranie aktualnej ceny
            if user_period == "1d":  # Jeśli wybrano 1 dzień, używamy krótszego interwału
                current_data = stock.history(period="1d", interval="1m")
                current_price = current_data['Close'].iloc[-1] if not current_data.empty else None
            else:
                current_price = history['Close'].iloc[-1] if not history.empty else None

            past_price = history['Close'].iloc[0] if not history.empty else None

            # Obliczenie zmiany procentowej
            percent_change = None
            if current_price and past_price:
                percent_change = ((current_price - past_price) / past_price) * 100

            # Pobranie dodatkowych danych
            low_price = history['Low'].min() if not history.empty else None
            high_price = history['High'].max() if not history.empty else None
            volume = history['Volume'].sum() if not history.empty else None
            turnover = volume * current_price if volume and current_price else None
            num_transactions = len(history) if not history.empty else None

            # Dodanie danych do listy
            stocks_data.append({
                "symbol": symbol,
                "name": stock.info.get("shortName", "Brak danych"),
                "current_price": current_price,
                "past_price": past_price,
                "change": percent_change,
                "low_price": low_price,
                "high_price": high_price,
                "volume": volume,
                "turnover": turnover,
                "num_transactions": num_transactions,
            })
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            stocks_data.append({
                "symbol": symbol,
                "name": "Brak danych",
                "current_price": None,
                "past_price": None,
                "change": None,
                "low_price": None,
                "high_price": None,
                "volume": None,
                "turnover": None,
                "num_transactions": None,
            })

    # Przekazanie danych do szablonu
    return render(request, "stocks.html", {"stocks": stocks_data, "period": user_period})


import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
import base64
from django.shortcuts import render

def real_estate(request):
    # Dane dla różnych miast
    data_all = {
        'Polska': {
            'Rok': [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
            'Cena_ofertowa_pierwotny': [
                8525, 8115, 7893, 8098, 7860, 7827, 7734, 7814, 8680, 9808, 10703, 11839, 12834, 14364, 16353
            ],
            'Cena_transakcyjna_pierwotny': [
                7882, 7553, 6808, 7152, 7344, 7481, 7651, 7704, 8313, 9092, 9925, 10990, 12589, 13706, 15955
            ],
            'Cena_ofertowa_wtorny': [
                9860, 9485, 8954, 8604, 8644, 8595, 8717, 8986, 9646, 10718, 11696, 12736, 13605, 14927, 18112
            ],
            'Cena_transakcyjna_wtorny': [
                8518, 7911, 7402, 6929, 7314, 7373, 7414, 7831, 8452, 9374, 10162, 10710, 11789, 12569, 14752
            ],
        },
        'Bydgoszcz': {
            'Rok': [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
            'Cena_ofertowa_pierwotny': [
                3595, 5006, 4969, 4924, 4969, 4834, 4836, 5132, 5060, 5125, 5199, 5689, 6243, 6394, 7009
            ],
            'Cena_transakcyjna_pierwotny': [
                2737, 4039, 4735, 4827, 4735, 4642, 4581, 4774, 4706, 4726, 4868, 5106, 5465, 6092, 6471
            ],
            'Cena_ofertowa_wtorny': [
                2657, 3911, 4070, 4140, 4178, 4047, 3826, 3674, 3786, 3793, 3917, 4233, 4540, 5110, 5881
            ],
            'Cena_transakcyjna_wtorny': [
                2392, 3483, 3915, 3817, 3782, 3722, 3427, 3386, 3431, 3558, 3691, 3891, 4318, 4915, 5516
            ],
        },
        'Gdańsk': {
            'Rok': [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
            'Cena_ofertowa_pierwotny': [
                5710, 5769, 6399, 6456, 6171, 6517, 6576, 6984, 8343, 9145, 9759, 10237, 11566, 12225, 13838
            ],
            'Cena_transakcyjna_pierwotny': [
                5501, 5585, 5522, 5731, 5767, 5955, 6350, 6644, 7493, 8417, 8975, 10223, 11109, 11573, 12474
            ],
            'Cena_ofertowa_wtorny': [
                6434, 6456, 6302, 6143, 5977, 6014, 6298, 6979, 8473, 9652, 10423, 10987, 12065, 12866, 14165
            ],
            'Cena_transakcyjna_wtorny': [
                5716, 5480, 5145, 4908, 4961, 5209, 5513, 6053, 6942, 7826, 8655, 9469, 10865, 11249, 12196
            ],
        },
        'Lublin': {
            'Rok': [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
            'Cena_ofertowa_pierwotny': [
                5094, 5050, 5092, 5074, 4965, 5064, 5148, 5169, 5546, 5889, 6435, 7631, 8788, 10076, 11069
            ],
            'Cena_transakcyjna_pierwotny': [
                4668, 4875, 4851, 4797, 4843, 4958, 5055, 5096, 5571, 5965, 6292, 7331, 8653, 9304, 10334
            ],
            'Cena_ofertowa_wtorny': [
                5067, 5140, 5048, 4796, 4864, 4894, 4977, 5091, 5320, 5878, 6820, 7668, 8519, 8941, 10060
            ],
            'Cena_transakcyjna_wtorny': [
                4846, 5040, 4782, 4571, 4439, 4476, 4564, 4731, 4954, 5465, 6260, 7032, 7873, 8107, 9050
            ],
        },
        'Łódź': {
            'Rok': [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
            'Cena_ofertowa_pierwotny': [
                5310, 5102, 4935, 4814, 4884, 4870, 4919, 5151, 5548, 6027, 6653, 7597, 8688, 9662, 10856
            ],
            'Cena_transakcyjna_pierwotny': [
                4927, 4972, 4572, 4493, 4571, 4660, 4740, 4948, 5320, 5848, 6340, 7039, 8161, 8799, 9796
            ],
            'Cena_ofertowa_wtorny': [
                4457, 4265, 3922, 4007, 3925, 3878, 4020, 4227, 4649, 5191, 5521, 6317, 7090, 7719, 8766
            ],
            'Cena_transakcyjna_wtorny': [
                3894, 3830, 3498, 3413, 3434, 3375, 3331, 3661, 4176, 4698, 5348, 5867, 6534, 6675, 7549
            ],
        },
        'Katowice': {
            'Rok': [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
            'Cena_ofertowa_pierwotny': [
                6333, 5782, 5205, 5674, 5519, 5571, 5364, 5416, 5819, 6671, 7568, 8286, 9547, 10817, 11632
            ],
            'Cena_transakcyjna_pierwotny': [
                4950, 4762, 4953, 4884, 4857, 4936, 5027, 5175, 5504, 6610, 6989, 7960, 9172, 9718, 11092
            ],
            'Cena_ofertowa_wtorny': [
                4206, 4081, 4093, 3964, 3977, 3938, 3959, 3947, 4342, 5229, 5909, 6646, 7292, 7539, 8292
            ],
            'Cena_transakcyjna_wtorny': [
                3584, 3470, 3361, 3223, 3407, 3466, 3561, 3646, 4101, 4651, 5272, 5605, 6210, 6668, 7531
            ],
        },
        'Kraków': {
            'Rok': [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
            'Cena_ofertowa_pierwotny': [
                7561, 7207, 6965, 6205, 6403, 6617, 6608, 6805, 7054, 8032, 9513, 10339, 11512, 13497, 16192
            ],
            'Cena_transakcyjna_pierwotny': [
                6882, 6909, 6595, 5976, 5966, 6107, 6333, 6630, 6930, 7797, 8605, 9590, 11132, 12220, 14977
            ],
            'Cena_ofertowa_wtorny': [
                6932, 7098, 6691, 6564, 6735, 6938, 6833, 7162, 8075, 8905, 9638, 10540, 12170, 13752, 16617
            ],
            'Cena_transakcyjna_wtorny': [
                6219, 6366, 6178, 5831, 5858, 6097, 5849, 6160, 6521, 7033, 8011, 9157, 10644, 11499, 13972
            ],
        },
        'Poznań': {
            'Rok': [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
            'Cena_ofertowa_pierwotny': [
                6600, 6299, 6133, 6369, 6582, 6530, 6435, 6474, 6877, 7342, 7800, 8523, 10061, 11375, 12795
            ],
            'Cena_transakcyjna_pierwotny': [
                6491, 6294, 5782, 5982, 6127, 6245, 6261, 6321, 6758, 7157, 7476, 8130, 9473, 10461, 12100
            ],
            'Cena_ofertowa_wtorny': [
                6064, 5848, 5526, 5602, 5768, 5705, 6049, 6109, 6720, 7215, 7823, 8339, 9475, 10487, 11849
            ],
            'Cena_transakcyjna_wtorny': [
                5429, 5369, 5174, 4961, 4996, 5029, 5190, 5401, 5861, 6391, 6824, 7010, 7940, 8852, 10174
            ],
        },
        'Szczecin': {
            'Rok': [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
            'Cena_ofertowa_pierwotny': [
                5038, 5012, 4973, 4834, 4864, 4867, 4886, 5512, 5851, 6432, 7390, 8650, 10289, 11921, 12340
            ],
            'Cena_transakcyjna_pierwotny': [
                4825, 4892, 4706, 4579, 4744, 4739, 4846, 5181, 5578, 6475, 6988, 8241, 10206, 10782, 11738
            ],
            'Cena_ofertowa_wtorny': [
                4834, 4726, 4449, 4251, 4337, 4304, 4386, 4564, 4959, 5690, 6285, 7079, 8024, 8357, 9405
            ],
            'Cena_transakcyjna_wtorny': [
                4304, 4119, 3875, 3806, 3809, 3812, 3963, 4209, 4633, 5311, 5943, 6629, 7733, 8022, 8720
            ],
        },
        'Warszawa': {
            'Rok': [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
            'Cena_ofertowa_pierwotny': [
                8525, 8115, 7893, 8098, 7860, 7827, 7734, 7814, 8680, 9808, 10703, 11389, 12834, 14364, 16353
            ],
            'Cena_transakcyjna_pierwotny': [
                7882, 7553, 6808, 7152, 7344, 7481, 7651, 7704, 8313, 9092, 9925, 10990, 12589, 13706, 15955
            ],
            'Cena_ofertowa_wtorny': [
                9860, 9485, 8954, 8604, 8644, 8595, 8717, 8986, 9646, 10718, 11696, 12736, 13605, 14927, 18112
            ],
            'Cena_transakcyjna_wtorny': [
                8518, 7911, 7402, 6929, 7314, 7373, 7414, 7831, 8452, 9374, 10162, 10710, 11789, 12569, 14752
            ],
        },
        'Wrocław': {
            'Rok': [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
            'Cena_ofertowa_pierwotny': [
                6171, 6292, 6302, 5982, 6058, 6105, 6292, 6459, 7035, 7745, 8609, 9651, 10872, 12585, 13762
            ],
            'Cena_transakcyjna_pierwotny': [
                5729, 5918, 5632, 5583, 5811, 6052, 6134, 6318, 6704, 7441, 8184, 8850, 10335, 11680, 13188
            ],
            'Cena_ofertowa_wtorny': [
                6642, 6524, 6239, 6007, 5998, 5889, 6041, 6295, 6493, 7518, 8271, 9046, 10448, 11793, 13452
            ],
            'Cena_transakcyjna_wtorny': [
                6003, 5883, 5442, 5027, 5120, 5200, 5307, 5626, 6067, 6731, 7521, 8521, 9795, 10509, 12007
            ],
        },
    }

    # Pobranie miasta z parametru GET
    city = request.GET.get('city', 'Polska')  # Domyślnie 'Polska'

    # Wybranie odpowiednich danych
    data = data_all.get(city, data_all['Polska'])
    df = pd.DataFrame(data)

    # Tworzenie wykresów
    plt.figure(figsize=(12, 8))
    plt.plot(df['Rok'], df['Cena_ofertowa_pierwotny'], label='Pierwotny - ofertowe')
    plt.plot(df['Rok'], df['Cena_transakcyjna_pierwotny'], label='Pierwotny - transakcyjne', linestyle='--')
    plt.plot(df['Rok'], df['Cena_ofertowa_wtorny'], label='Wtórny - ofertowe')
    plt.plot(df['Rok'], df['Cena_transakcyjna_wtorny'], label='Wtórny - transakcyjne', linestyle='--')

    plt.title(f'Porównanie cen ofertowych i transakcyjnych ({city})')
    plt.xlabel('Rok')
    plt.ylabel('Cena za m² (PLN)')
    plt.legend()
    plt.grid(True)

    # Konwersja wykresu na obraz base64
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graph = base64.b64encode(image_png).decode('utf-8')

    # Przekazanie danych do szablonu
    return render(request, 'real_estate.html', {'graph': graph, 'table_data': df.to_dict(orient='records'), 'city': city})