from django.shortcuts import render
from django.http import HttpResponse

from .models import Stance, Confidence, Expressivity
# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def quotes_simple_example(request):
    if request.method == 'POST': 
        Stance.objects.get(name=request.POST['stance'])
        print(request.POST)
        
        s = Stance.objects.get(name=request.POST['stance'])
        c = Confidence.objects.get(name=request.POST['confidence'])
        e = Expressivity.objects.get(
            type=request.POST['expressivity_type'],
            value = request.POST['expressivity_value'],
            evidence = request.POST['evidence']
        )
        print(s.id)
        print(c.id)
        print(e.id)
    return render(request, 'analisis/Quotes_Simple_example.html')

def replies_simple_example(request):
    return render(request, 'analisis/Replies_Simple_example.html')
