from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
import csv


def index(request):
    return redirect(reverse("bus_stations"))


def get_stations():
    with open(settings.BUS_STATION_CSV, "rt", encoding="utf8") as f:
        __result = []
        for line in csv.DictReader(f, delimiter=","):
            __result.append(line)
        return __result


def bus_stations(request):
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице
    page = int(request.GET.get("page", 1))
    page_limit = 10
    stations = get_stations()

    context = {
        "bus_stations": stations[
            page * page_limit - page_limit : page * page_limit
        ],
        "page": page,
    }
    return render(request, "stations/index.html", context)
