from django.shortcuts import render
import requests
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# eia key ba035c7b1423526c800b51c7a1cd3fc2
# wunderground key 78bda23fc1bc1907

def index(request):
    consumption = {}
    consumption['renewable'] = requests.get('http://api.eia.gov/series/?api_key=ba035c7b1423526c800b51c7a1cd3fc2&series_id=TOTAL.RETCBUS.A').json()
    consumption['coal'] = requests.get('http://api.eia.gov/series/?api_key=ba035c7b1423526c800b51c7a1cd3fc2&series_id=TOTAL.CLTCBUS.A').json()
    consumption['geothermal'] = requests.get('http://api.eia.gov/series/?api_key=ba035c7b1423526c800b51c7a1cd3fc2&series_id=TOTAL.GETCBUS.A').json()
    consumption['hydroelectric'] = requests.get('http://api.eia.gov/series/?api_key=ba035c7b1423526c800b51c7a1cd3fc2&series_id=TOTAL.HVTCBUS.A').json()
    consumption['gas'] = requests.get('http://api.eia.gov/series/?api_key=ba035c7b1423526c800b51c7a1cd3fc2&series_id=TOTAL.NNTCBUS.A').json()
    consumption['nuclear'] = requests.get('http://api.eia.gov/series/?api_key=ba035c7b1423526c800b51c7a1cd3fc2&series_id=TOTAL.NUETBUS.A').json()
    consumption['petroleum'] = requests.get('http://api.eia.gov/series/?api_key=ba035c7b1423526c800b51c7a1cd3fc2&series_id=TOTAL.PMTCBUS.A').json()
    consumption['solar'] = requests.get('http://api.eia.gov/series/?api_key=ba035c7b1423526c800b51c7a1cd3fc2&series_id=TOTAL.SOTCBUS.A').json()
    consumption['biomass'] = requests.get('http://api.eia.gov/series/?api_key=ba035c7b1423526c800b51c7a1cd3fc2&series_id=TOTAL.BMTCBUS.A').json()
    consumption['fossil_fuels'] = requests.get('http://api.eia.gov/series/?api_key=ba035c7b1423526c800b51c7a1cd3fc2&series_id=TOTAL.FFTCBUS.A').json()
    consumption['primary'] = requests.get('http://api.eia.gov/series/?api_key=ba035c7b1423526c800b51c7a1cd3fc2&series_id=TOTAL.TETCBUS.A').json()
    consumption['wind'] = requests.get('http://api.eia.gov/series/?api_key=ba035c7b1423526c800b51c7a1cd3fc2&series_id=TOTAL.WYTCBUS.A').json()

    for source in consumption:
        xval = []
        yval = []
        for key, value in consumption[source]['series'][0]['data']:
            xval.append(key)
            if isinstance(value, float) or isinstance(value, int):
                yval.append(value)
            else:
                yval.append('0')
        plt.plot(xval, yval, label=source)
    plt.ylabel(consumption['renewable']['series'][0]['units'])
    plt.legend()
    plt.savefig('apps/dashboard/static/dashboard/images/all.png')
    plt.clf()

    pallet = ['#00D0E5','#1BBBCB','#37A6B2','#539298','#6F7D7F','#8A6865','#A6544C','#C23F32','#DE2A19','#FA1600']

    weather = {}
    # weather['San Francisco - 10 Day'] = requests.get('http://api.wunderground.com/api/78bda23fc1bc1907/hourly10day/q/CA/San_Francisco.json').json()
    weather['San Francisco'] = requests.get('http://api.wunderground.com/api/78bda23fc1bc1907/hourly/q/CA/San_Francisco.json').json()
    weather['Dallas'] = requests.get('http://api.wunderground.com/api/78bda23fc1bc1907/hourly/q/TX/Dallas.json').json()
    weather['Greenville'] = requests.get('http://api.wunderground.com/api/78bda23fc1bc1907/hourly/q/SC/Greenville.json').json()

    for location in weather:
        xval = []
        yval = []
        area = []
        time = int(weather[location]['hourly_forecast'][0]['FCTTIME']['hour'])
        for each in weather[location]['hourly_forecast']:  # 0, 1, 2, 3 ... array index
            # xval.append(each['FCTTIME']['hour'])
            xval.append(time)
            time = time + 1
            yval.append(int(each['temp']['english']))
            area.append(int(1.1**int(each['humidity'])))

        max_temp = max(yval)
        min_temp = min(yval)

        colors = [pallet[int(round((n - min_temp) * 9 / (max_temp - min_temp )))] for n in yval]

        plt.scatter(xval, yval, c=colors, s=area, alpha=0.5)

        plt.title("Hourly Weather Forecast for {}".format(location))
        plt.ylabel("Temperature (F)")
        plt.xlabel("Hour")

        # plt.ylim(40,100)
        # plt.yticks([])
        # plt.axis([0,time,0,100])

        plt.savefig('apps/dashboard/static/dashboard/images/hourly_forecast_'+location+'.png')
        plt.clf()

    request.session['plots'] = []

    rootdir = '/Users/wildcard/Documents/Python/Django/energy/apps/dashboard/static/dashboard/images/'
    request.session['plots'] = []
    for file in os.listdir(rootdir):
        request.session['plots'].append(file)

    return render(request, 'dashboard/index.html')
