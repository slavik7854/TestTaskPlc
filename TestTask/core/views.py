import json

from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView

from .models import Data, Machine, Line

import matplotlib.pyplot as plt
import io

from .serializers import DataSerializer, MachineSerializer


class DataView(CreateAPIView):
    queryset = Data.objects.all()
    serializer_class = DataSerializer


class MachineView(ListAPIView):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer


def generate_chart(request):
    if request.method == "POST":
        params = json.loads(request.body)
        lines = params['line']
        time_start = params['datefrom']
        time_end = params['dateto']

        line_arr = []
        for line in lines:
            d = Data.objects.filter(line=line, timestamp__gte=time_start, timestamp__lte=time_end)
            line_arr.append(d)
        plt.xticks(rotation=45, ha='right')
        plt.subplots_adjust(bottom=0.15)

        for data in line_arr:
            plt.plot([d.timestamp for d in data], [d.value for d in data], label=data[0].line)
        plt.legend()

        chart_IObytes = io.BytesIO()
        plt.savefig(chart_IObytes, format='png')
        plt.clf()
        chart_IObytes.seek(0)

        html_content = '<b>Generated chart</b>'
        msg = EmailMultiAlternatives('Generated chart', html_content, 'sender@test.test', ['to_mail@test.test'])
        msg.attach('test.png', content=chart_IObytes.read())
        msg.send()

    lines_list = []
    lines = Line.objects.filter(active=True).values_list('id', 'name')
    if lines:
        lines_list.extend([(line[0], line[1]) for line in lines])

    return render(request, 'core/generate_chart.html', {'lines': lines_list})
