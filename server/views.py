from django.shortcuts import render


def bad_request(request):
    return render(request, '../templates/400.html', status=400)


def page_not_found(request):
    return render(request, '../templates/404.html', status=404)
