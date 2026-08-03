import csv

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице
    stations_list = []

    with open('data-398-2018-08-30.csv', newline='', encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            station_info = {
                'name': row['Name'] if 'Name' in row else row['name'],
                'street': row['Street'],
                'district': row['District']
            }
            stations_list.append(station_info)

    page_number = request.GET.get('page', 1)

    paginator = Paginator(stations_list, 10)

    page_obj = paginator.get_page(page_number)

    context = {
        # Передаем не весь список, а только объекты текущей страницы
        'bus_stations': page_obj.object_list,

        # Объект page удобен для вывода кнопок "Вперед", "Назад" и номеров страниц в шаблоне
        'page': page_obj,
    }
    return render(request, 'stations/index.html', context)
