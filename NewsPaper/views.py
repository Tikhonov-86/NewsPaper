from django.http import HttpResponse
from django.views import View
from NewsPaper.tasks import hello, printer
from datetime import datetime, timedelta


class IndexView(View):
    def get(self, request):
        printer.delay(1)
        hello.delay()
        return HttpResponse('Hello!')