from django.shortcuts import render

def homescreen_view(request):
	context = {}
	return render(request, "home.html", context)