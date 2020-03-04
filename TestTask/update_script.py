from pylogix import PLC
from socket import timeout
from time import sleep
from random import random
import requests

DELAY = 5


def save_data(line, value):
    requests.post('http://127.0.0.1:8000/send_data/', data={'line': line, 'value': value})
    print(line, value)
    pass


def data_generator(ip, lines):
    variables_dict = {}
    with PLC() as comm:
        comm.Micro800 = True
        comm.IPAddress = ip
        while True:
            for line in lines:
                try:
                    variable = line['name']
                    value = comm.Read(variable)
                    # value = random() # For tests
                    if variables_dict.get(variable, None) != value:
                        save_data(line['id'], value)
                except timeout:
                    save_data(line['id'], None)
            yield 1


update_array = []

response = requests.get('http://127.0.0.1:8000/machines/')
machines = response.json()

for machine in machines:
    ip = machine.get('ip', '')
    lines = machine.get('lines', [])
    if lines:
        update_array.append(data_generator(ip, lines))

while True:
    for el in update_array:
        el.__next__()
    sleep(DELAY)

