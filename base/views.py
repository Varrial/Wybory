from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.forms import ModelChoiceField, forms


from .models import Wybory, Kandydaci, TypWyborow


def home(request):
    q = request.GET.get('q')

    if q != '':
        wybory = Wybory.objects.filter(typ__typ=q)
    else:
        wybory = Wybory.objects.all()
    typy = TypWyborow.objects.all()

    context = {
        'wybory': wybory,
        'typy': typy,
    }
    return render(request, 'base/home.html', context)

def wybory(request, pk):
    wybory = Wybory.objects.get(id=pk)
    kandydaci = Kandydaci.objects.filter(id_wyborow=pk)

    if request.method == 'POST':
        zaglosowany = request.POST.get('kandydat')
        item = kandydaci.get(pesel__username=zaglosowany)
        item.poparcie += 1
        item.save()
        print(item.poparcie)
        return redirect('home')

    context = {
        'wybory': wybory,
        'kandydaci': kandydaci,
    }
    return render(request, 'base/wybory.html', context)

# def formularz_kandydatow(request):
#
#     context = {'form': form}
#     return render(request, 'base/wybory.html', context)