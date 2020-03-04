from django.db import models


class Machine(models.Model):
    ip = models.GenericIPAddressField(protocol='IPv4')
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.ip


class Line(models.Model):
    machine = models.ForeignKey('Machine', related_name='lines', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{} ({})'.format(self.name, self.machine.ip)


class Data(models.Model):
    line = models.ForeignKey('Line', on_delete=models.CASCADE)
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} ({})'.format(self.line, self.timestamp)
