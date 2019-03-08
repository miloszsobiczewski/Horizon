from django.shortcuts import render
from .morizon import Morizon
from .forms import PropertiesForm
from .models import Property
import pandas as pd
import pdb
import os
from miloszsobiczewski.settings import BASE_DIR
import json


def test(request):
    return render(request, 'horizon/portal.html')


def load(request):
    return render(request, 'horizon/load.html')


def tables(request):
    log = ''
    properties = Property.objects.all().order_by('unit_price')

    config_path = os.path.join(BASE_DIR, 'horizon/static/horizon/morizon.json')
    with open(config_path) as f:
        data = json.load(f)
    fltr = data['exclude']
    villages_in = data['places']
    villages_out = data['exclude']
    PW = data['password']
    TO = data['recipients']

    if request.method == 'POST':

        get_done = request.POST.get('Done', None)
        get_done2 = request.POST.get('Run', None)
        get_send = request.POST.get('Send', None)
        get_results = request.POST.get('Results', None)
        get_refresh = request.POST.get('Refresh', None)
        get_logs = request.POST.get('Logs', None)
        get_like = request.POST.get('Like', None)
        get_test = request.POST.get('Test', None)

        # check if it is a run request

        if get_done is not None or get_done2 is not None:

            propertiesform = PropertiesForm(request.POST)
            if propertiesform.is_valid():
                if len(propertiesform.cleaned_data['min_size']) == 0:
                    propertiesform.min_size = 950
                if len(propertiesform.cleaned_data['max_price']) == 0:
                    propertiesform.max_price = 200000

                # run = request.POST.get('Run', None)
                # log = '[running...]'
                horizon = Morizon()

                try:

                    horizon.set(propertiesform.min_size, propertiesform.max_price)
                    df = horizon.search()

                    # clean df as of config file
                    df2 = horizon.clean(df, fltr)

                    dim = df2.shape[0]
                    new_cnt = 0
                    for i in range(dim):
                        link = df2.iloc[i, 4]
                        exist = properties.filter(link=link)
                        if exist:
                            pass
                        else:
                            new_cnt = new_cnt + 1
                            new_properties = Property()
                            new_properties.location = df2.iloc[i, 0]
                            # new_properties.price = df2.iloc[i, 1]
                            new_properties.size = int(df2.iloc[i, 7])
                            new_properties.total_price = df2.iloc[i, 6]
                            new_properties.link = link
                            new_properties.unit_price = float(df2.iloc[i, 5])

                            new_properties.type = df2.iloc[i, 8]
                            # new_properies.phone = df2.iloc[i, 1]
                            new_properties.save()
                            print(new_properties.location)
                    # log = 'Run finished.'
                    log = str(new_cnt) + ' new properties were added.'
                    horizon.close()
                except:
                    horizon.close()

        elif get_send is not None:
            #pdb.set_trace()
            horizon = Morizon()
            df = pd.DataFrame(properties.values_list())
            msg = horizon.mail_prep(df)
            res = horizon.send(TO, msg, PW)
            if res:
                log = 'Report Sent'
            else:
                log = 'Error while sending report'

        # check if it is a retrieve results request
        elif get_results is not None:
            log = 'Tables Filtered'
        elif get_logs is not None:
            log = 'Redirecting to log page'
        elif get_refresh is not None:
            log = 'Page Refreshed'
            propertiesform = PropertiesForm()
        elif get_like is not None:
            status = list(map(lambda t: t[-1], properties.filter(pk=get_like).values_list()))[0]
            # pdb.set_trace()
            if status:
                properties.filter(pk=get_like).update(like=False)
                log = 'You disliked #' + str(get_like)
            else:
                properties.filter(pk=get_like).update(like=True)
                log = 'You liked #' + str(get_like)

        elif get_test is not None:
            log = 'Test: ' + str(get_test)
        else:
            log = 'No operation was recognized.'
    else:
        propertiesform = PropertiesForm()
    return render(request, 'horizon/tables.html',
                  {'log': log, 'propertiesform': propertiesform, 'properties': properties, 'villages_in': villages_in,
                   'villages_out': villages_out})


def horizon(request):
    log = ''
    propertiesform = ''
    properties = Property.objects.all().order_by('price')
    if request.method == 'POST':

        # check if it is a run request

        # run = request.POST.get('Run', None)
        log = '[running...]'
        horizon = Morizon()
        min_size = 950
        max_price = 200000
        horizon.set(min_size, max_price)
        df = horizon.search()

        config_path = os.path.join(BASE_DIR, 'horizon/static/horizon/morizon.json')

        # clean df as of config file
        df2 = horizon.clean(df, config_path)
        pdb.set_trace()

        dim = df2.shape[0]
        for i in range(dim):

            new_properties = Property()
            new_properties.location = df2.iloc[i, 0]
            # new_properties.price = df2.iloc[i, 1]
            new_properties.size = int(df2.iloc[i, 7])
            new_properties.total_price = int(df2.iloc[i, 6])
            new_properties.link = df2.iloc[i, 4]
            new_properties.unit_price = float(df2.iloc[i, 5])

            new_properties.type = df2.iloc[i, 8]
            #new_properies.phone = df.iloc[i, 1]
            new_properties.save()
            print(new_properties.location)

        # pdb.set_trace()

        # check if it is a retrieve results request

    else:
        propertiesform = PropertiesForm()
    return render(request, 'horizon/tables.html',
                  {'log': log, 'propertiesform': propertiesform, 'properties': properties})



