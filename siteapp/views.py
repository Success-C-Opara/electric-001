from django.shortcuts import render

# Create your views here.

def fan(request):
    return render(request, 'siteapp/index.html')

def about(request):
    return render(request, 'siteapp/about.html')

def services(request):
    return render(request, 'siteapp/services.html')

def testimonial(request):
    return render(request, 'siteapp/testimonial.html')