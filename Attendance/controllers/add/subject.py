from django.shortcuts import render


def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    return render(
        request,
        'add_group.html')


def add_subject(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    return render(
        request,
        'add_group.html')
