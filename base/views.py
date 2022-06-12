import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.forms import ModelChoiceField, forms


from .models import Wybory, Kandydaci, TypWyborow, Uprawnieni


def home(request):
    q = request.GET.get('q')

    if q == None:
        q = ''

    # Filtrowanie tylko po aktywnych
    uprawnieni = Uprawnieni.objects.filter(id_wyborow__data_rozpoczecia__lte=datetime.datetime.now(),
                                           id_wyborow__data_zakonczenia__gte=datetime.datetime.now(),
                                           id_wyborow__czy_aktywne=True)

    if q != '':
        uprawnieni = uprawnieni.filter(id_wyborow__typ__typ=q)  # filtrowanie po przyciskach

    if request.user.is_authenticated:
        uprawnieni = uprawnieni.filter(pesel=request.user)  # zalogowany dostaje tylko te w ktorych moze wziać udział

    if not request.user.is_authenticated:   # niezalogowany dostaje wszystkie możliwe wybory z aktywnych
        uprawnieni = Wybory.objects.filter(data_rozpoczecia__lte=datetime.datetime.now(),
                                           data_zakonczenia__gte=datetime.datetime.now(),
                                           czy_aktywne=True)

    typy = TypWyborow.objects.filter()

    context = {
        'wybory': uprawnieni,
        'typy': typy,
        'wybrany': q,
    }
    return render(request, 'base/home.html', context)

@login_required
def wybory(request, pk):
    wybory = Wybory.objects.get(id=pk)
    kandydaci = Kandydaci.objects.filter(id_wyborow=pk)
    uprawnieni = Uprawnieni.objects.filter(id_wyborow=wybory)

    if not request.user.is_authenticated:   # jeżeli jest niezalogowany
        valid = False
    elif uprawnieni.filter(pesel=request.user).exists() and not uprawnieni.get(pesel=request.user).CzyZaglosowal:
        # zalogowany jest uprawniony do wyborów i nie głosował
        valid = True
    else:
        valid = False


    valid = valid
    if request.method == 'POST':
        zaglosowany = request.POST.get('kandydat')
        item = kandydaci.get(pesel__username=zaglosowany)
        item.poparcie += 1  # zwiekszenie poparcia
        item.save()
        glosujacy = uprawnieni.get(id_wyborow=wybory, pesel=request.user)
        glosujacy.CzyZaglosowal = True  # zmiana na zagłosowane
        glosujacy.save()
        print(item.poparcie)
        return redirect('home')

    context = {
        'wybory': wybory,
        'kandydaci': kandydaci,
        'valid': valid,
    }
    return render(request, 'base/wybory.html', context)

def wyniki(request):
    q = request.GET.get('q')

    if q == None:
        q = ''

    # Filtrowanie tylko po aktywnych
    wybory = Wybory.objects.filter(data_zakonczenia__lte=datetime.datetime.now())

    if q != '':
        wybory = wybory.filter(typ__typ=q)  # filtrowanie po przyciskach


    typy = TypWyborow.objects.all()

    context = {
        'wybory': wybory,
        'typy': typy,
        'wybrany': q,
    }

    return render(request, 'base/wyniki.html', context)

def konkretne_wyniki(request, pk):
    kandydaci = Kandydaci.objects.filter(id_wyborow=pk)
    nazwa_wyborow = Wybory.objects.get(id=pk)

    context = {
        'kandydaci': kandydaci,
        'nazwa_wyborow': nazwa_wyborow,
    }

    return render(request, 'base/konkretne_wyniki.html', context)