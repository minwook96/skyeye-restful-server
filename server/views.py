from django.shortcuts import render


def custom_page_not_found_view(request, exception):
    return render(request, "../templates/404.html", {})


def custom_error_view(request, exception=None):
    return render(request, "../templates/500.html", {})


def custom_permission_denied_view(request, exception=None):
    return render(request, "../templates/403.html", {})


def custom_bad_request_view(request, exception=None):
    return render(request, "../templates/400.html", {})
