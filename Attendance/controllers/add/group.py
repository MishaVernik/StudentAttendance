from django.shortcuts import render


def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """

    return render(
        request,
        'add_group.html')


def add_group(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    print(request.user)
    print(request.POST.get('semester'))
    print(request.POST.get('subject'))
    print(request.POST.get('group'))
    return render(
        request,
        'add_group.html')
