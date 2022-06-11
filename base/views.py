from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.forms import ModelChoiceField, forms


from .models import Wybory, Kandydaci, TypWyborow, Uprawnieni


def home(request):
    q = request.GET.get('q')
    if q == None:
        q = ''

    if q != '':
        if request.user.is_authenticated:
            uprawnieni = Uprawnieni.objects.filter(id_wyborow__typ__typ=q, pesel=request.user)
        else:
            uprawnieni = Uprawnieni.objects.filter(id_wyborow__typ__typ=q)
    elif request.user.is_authenticated:
        uprawnieni = Uprawnieni.objects.filter(pesel=request.user)
    else:
        uprawnieni = Uprawnieni.objects.all()

    typy = TypWyborow.objects.all()

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

# def formularz_kandydatow(request):
#
#     context = {'form': form}
#     return render(request, 'base/wybory.html', context)