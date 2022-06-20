import datetime
import io

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect
from django.forms import ModelChoiceField, forms
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from .forms import newWybory
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
        if q != '':
            uprawnieni = uprawnieni.filter(typ__typ=q)

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
        glosujacy = uprawnieni.get(id_wyborow=wybory, pesel=request.user)
        glosujacy.CzyZaglosowal = True  # zmiana na zagłosowane
        glosujacy.save()

        zaglosowany = request.POST.get('kandydat')
        if zaglosowany == 'Null':
            return redirect('home')

        item = kandydaci.get(id=zaglosowany)
        item.poparcie += 1  # zwiekszenie poparcia
        item.save()

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

    uprawnieni = Uprawnieni.objects.filter(id_wyborow=pk)
    ilosc_uprawnionych = uprawnieni.count()

    ilosc_oddanych_glosow = 0
    ilosc_oddanych_glosow_procent = 0
    ilosc_nieoddanych_glosow = 0
    ilosc_nieoddanych_glosow_procent = 0

    if ilosc_uprawnionych > 0:
        uprawnieni = uprawnieni.filter(CzyZaglosowal=1)
        ilosc_oddanych_glosow = uprawnieni.count()
        ilosc_oddanych_glosow_procent = ilosc_oddanych_glosow / ilosc_uprawnionych * 100
        ilosc_nieoddanych_glosow = ilosc_uprawnionych - ilosc_oddanych_glosow
        ilosc_nieoddanych_glosow_procent = ilosc_nieoddanych_glosow / ilosc_uprawnionych * 100

    context = {
        'kandydaci': kandydaci,
        'nazwa_wyborow': nazwa_wyborow,
        'ilosc_uprawnionych': ilosc_uprawnionych,
        'ilosc_oddanych_glosow': ilosc_oddanych_glosow,
        'ilosc_oddanych_glosow_procent': int(ilosc_oddanych_glosow_procent),
        'ilosc_nieoddanych_glosow': ilosc_nieoddanych_glosow,
        'ilosc_nieoddanych_glosow_procent': int(ilosc_nieoddanych_glosow_procent),
        'pk': pk,
    }

    return render(request, 'base/konkretne_wyniki.html', context)


def konkretne_wyniki_pdf(request, pk):
    kandydaci = Kandydaci.objects.filter(id_wyborow=pk)
    nazwa_wyborow = Wybory.objects.get(id=pk)

    uprawnieni = Uprawnieni.objects.filter(id_wyborow=pk)
    ilosc_uprawnionych = uprawnieni.count()

    ilosc_oddanych_glosow = 0
    ilosc_oddanych_glosow_procent = 0
    ilosc_nieoddanych_glosow = 0
    ilosc_nieoddanych_glosow_procent = 0

    if ilosc_uprawnionych > 0:
        uprawnieni = uprawnieni.filter(CzyZaglosowal=1)
        ilosc_oddanych_glosow = uprawnieni.count()
        ilosc_oddanych_glosow_procent = ilosc_oddanych_glosow / ilosc_uprawnionych * 100
        ilosc_nieoddanych_glosow = ilosc_uprawnionych - ilosc_oddanych_glosow
        ilosc_nieoddanych_glosow_procent = ilosc_nieoddanych_glosow / ilosc_uprawnionych * 100

    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    pdfmetrics.registerFont(TTFont('Verdana', 'Verdana.ttf'))
    textob.setFont("Verdana", 16)
    textob.textLine(f'{nazwa_wyborow.nazwa} - podumowanie')
    textob.setFont("Verdana", 11)

    for kandydat in kandydaci:
        textob.textLine("")
        dane = (str(kandydat.pesel.first_name) + " " + str(kandydat.pesel.last_name)).ljust(30)
        textob.textLine(f'{dane} Ilość głosów: {kandydat.poparcie}')
        print(f'{dane} Ilość głosów: {kandydat.poparcie}')

    textob.textLine("")
    textob.textLine("")
    textob.setFont("Verdana", 13)
    textob.textLine("Frekwencja: ")
    textob.setFont("Verdana", 11)

    textob.textLine("")
    textob.textLine(f'Ilość osób uprawnionych: {ilosc_uprawnionych}')
    textob.textLine("")
    textob.textLine(f'Ilość oddanych głosów: {ilosc_oddanych_glosow} ({ilosc_oddanych_glosow_procent}%)')
    textob.textLine("")
    textob.textLine(f'Ilość nieoddanych głosów: {ilosc_nieoddanych_glosow} ({ilosc_nieoddanych_glosow_procent}%)')


    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename=f'Raport - {nazwa_wyborow.nazwa}.pdf')


@staff_member_required
def zarzadzaj_kandydatami(request):
    q = request.GET.get('q')

    if q == None:
        q = ''

    wybory = Wybory.objects.filter(data_rozpoczecia__gte=datetime.datetime.now())
    typy = TypWyborow.objects.all()

    if q != '':
        wybory = wybory.filter(typ__typ=q)  # filtrowanie po przyciskach

    context = {
        'wybory': wybory,
        'typy': typy,
        'wybrany': q,
    }

    return render(request, 'base/zarzadzaj_kandydatami.html', context)

@staff_member_required
def zarzadzaj_kandydatami_users(request, pk):
    wybory = Wybory.objects.get(id=pk)
    users = User.objects.all()
    kandydaci = Kandydaci.objects.filter(id_wyborow=pk).values_list('pesel')

    if request.method == 'POST':
        nowi = request.POST.getlist('user')
        Kandydaci.objects.filter(id_wyborow=pk).delete()
        for nowy in nowi:
            new = Kandydaci(
                id_wyborow=Wybory.objects.get(id=pk),
                pesel=User.objects.get(id=nowy),
                poparcie=0,
            )
            new.save()
        return redirect('home')

    context = {
        'wybory': wybory,
        'users': users,
        'kandydaci': kandydaci,
    }


    return render(request, 'base/zarzadzaj_kandydatami_users.html', context)

@staff_member_required
def zarzadzaj_uprawnionymi(request):
    q = request.GET.get('q')

    if q == None:
        q = ''

    wybory = Wybory.objects.filter(data_rozpoczecia__gte=datetime.datetime.now())
    typy = TypWyborow.objects.all()

    if q != '':
        wybory = wybory.filter(typ__typ=q)  # filtrowanie po przyciskach

    context = {
        'wybory': wybory,
        'typy': typy,
        'wybrany': q,
    }

    return render(request, 'base/zarzadzaj_uprawnionymi.html', context)

@staff_member_required
def zarzadzaj_uprawnionymi_users(request, pk):
    wybory = Wybory.objects.get(id=pk)
    users = User.objects.all()
    uprawnieni = Uprawnieni.objects.filter(id_wyborow=pk).values_list('pesel')

    if request.method == 'POST':
        nowi = request.POST.getlist('user')
        Uprawnieni.objects.filter(id_wyborow=pk).delete()
        for nowy in nowi:
            new = Uprawnieni(
                id_wyborow=Wybory.objects.get(id=pk),
                pesel=User.objects.get(id=nowy),
                CzyZaglosowal=False,
            )
            new.save()
        return redirect('home')

    context = {
        'wybory': wybory,
        'users': users,
        'uprawnieni': uprawnieni,
    }


    return render(request, 'base/zarzadzaj_uprawnionymi_users.html', context)

@staff_member_required
def dodaj_wybory(request):
    new_wybory = newWybory()

    if request.method == 'POST':
        new = newWybory(request.POST)
        new.save()
        return redirect('zarzadzaj_wyborami')

    contex = {
        'form': new_wybory
    }

    return render(request, 'base/dodaj_wybory.html', contex)

@staff_member_required
def zarzadzaj_wyborami(request):
    q = request.GET.get('q')

    if q == None:
        q = ''

    wybory = Wybory.objects.filter(data_zakonczenia__lte=datetime.datetime.now())
    wybory = Wybory.objects.all()
    typy = TypWyborow.objects.all()

    if q != '':
        wybory = wybory.filter(typ__typ=q)  # filtrowanie po przyciskach

    context = {
        'wybory': wybory,
        'typy': typy,
        'wybrany': q,
    }

    return render(request, 'base/zarzadzaj_wyborami.html', context)

@staff_member_required
def usun_wybory(request):
    q = request.GET.get('q')
    Wybory.objects.get(id=q).delete()
    return redirect('zarzadzaj_wyborami')

@staff_member_required
def edytuj_wybory(request, pk ):
    wybor = Wybory.objects.get(id=pk)
    form = newWybory(instance=wybor)

    if request.method == 'POST':
        form = newWybory(request.POST, instance=wybor)
        form.save()
        return redirect('zarzadzaj_wyborami')


    contex = {
        'form': form
    }
    return render(request, 'base/dodaj_wybory.html', contex)