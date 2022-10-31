#from django.http import HttpResponse
#from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import render, redirect
from listings.models import Spot
from django.template import loader
from listings.forms import RegistrationForm, ContactUsForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

from .forms import *

def hello(request):
    return HttpResponse('<h1>Hello Django!</h1>')

def home(request):
    """home page"""
    try:
        plages = Spot.objects.all()
        context = {'plages': plages}

        if plages:
            context['plages'] = plages
        else:
            raise Exception()
    except:
        context['no_plages'] = 'Aucune plage trouvé'

    return render(request, 'pages/index.html', context)


def plage(request, plage_name):
    """Product page"""
    name = plage_name
    try:
        plage = Spot.objects.get(name__iexact=name)
        context = {'plage': plage}
        print("plage.photo:", plage.photo)
        if plage.photo == "0":
            print("ça marche:", plage.photo)
            context = {'plage': plage}

    except Spot.DoesNotExist:
        context = {'error' : 'pas de données pour cette plage.'}

    """
    else:
        try:
            alternatives = Product.objects.filter(nutriscore__lt=product.nutriscore,
                                                  category=product.category
                                                  ).order_by('nutrigrade', 'name')
            if request.user.is_authenticated:
                saved = Alternative.objects.filter(user=request.user).values('product')
                alternatives = alternatives.exclude(pk__in=saved)
            if alternatives:
                context['alternatives'] = alternatives
            else:
                raise Exception()
        except:
            context['no_alternatives'] = 'Aucun meilleur produit trouvé'
    """

    return render(request, 'pages/plage.html', context)



def search(request):
    """Research page :
    if 1 product match the research, display it with it's alternative
    if no product match the research, try to find result containing research
    if 1 product match the new research, display it with it's alternative
    if several product match the new research, display them all
    if no product match the new research, display no product found
    """
    try:
        search = request.GET['name']
        plage = Spot.objects.get(name__iexact=search)
        context = {'plage': plage}
    except Spot.DoesNotExist:
        plages = Spot.objects.filter(name__icontains=search)
        if not plages:
            context = {'error': 'Aucune plage correspondant'}
        elif len(plages) == 1:
            context = {'plage': plages[0]}
        else:
            context = {'plages': plages}
    except:
        context = {'error': 'Aucune plage correspondant'}
    """if we got only one product, let's find his alternative products"""
    try:
        plage = context['plage']
    except:
        pass
    else:
        try:
            if request.user.is_authenticated:
                saved = Alternative.objects.filter(user=request.user).values('product')
                alternatives = alternatives.exclude(pk__in=saved)
            else:
                raise Exception()
        except:
            context['no_alternatives'] = 'Aucun meilleur produit trouvé'
    return render(request, 'pages/search.html', context)

def registration(request):
    """Page to create an account"""
    print("ça marche")
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            print(username, password)
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = RegistrationForm()
    context = {'form': form}
    return render(request, 'pages/registration.html', context)


def connection(request):
    """page to log in"""
    context = {}

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        print(form.is_valid())
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        print(username, password)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            context['error'] = 'Mauvais mot de passe ou pseudo.'

    else:
        form = AuthenticationForm()
    context['form'] = form
    return render(request, 'pages/connexion.html', context)


def disconnection(request):
    """Please, the name is clear enough"""
    logout(request)
    return redirect('home')

def mentions(request):
    """Legales mentions page"""
    return render(request, 'pages/mentions.html')

def contactsite(request):
    """page with contact information"""
    return render(request, 'pages/contact.html')

def handler404(request, exception):
    """Error page 404"""
    return render(request, 'errors/error404.html', status=404)

def handler500(request):
    """Error page 500"""
    return render(request, 'errors/error500.html')


def image_view(request, plage_name):

    name = plage_name
    plage = Spot.objects.get(name__iexact=name)

    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)  #(request.POST, request.FILES)
        form.fields["name"].initial = "blabla"

        if form.is_valid():
            print("it's valide")
            #plage.name = form.cleaned_data['name']
            plage.photo = form.cleaned_data['photo']
            plage.save()
            return redirect('success')
    else:
        form = PhotoForm()
        form.fields["name"].initial = "blabla" #plage.name
    return render(request, 'pages/hotel_image_form.html', {'form' : form})
  
  
def success(request):
    return HttpResponse('successfully uploaded')


def contact(request, plage_name):

    name = plage_name
    plage = Spot.objects.get(name__iexact=name)
    context = {'plage': plage}

    if request.method == 'POST':
        print("ça marche")
        form = ContactUsForm(request.POST, request.FILES)  # ajout d’un nouveau formulaire ici
    
        if form.is_valid():
            print("it's valide")
            plage.photo = form.cleaned_data['photo']
            plage.save()
            
            #return redirect('plage/<path:name>')
            return render(request, 'pages/plage.html', context)

    else:
        form = ContactUsForm()

    return render(request,
            'pages/Testform.html',
            {'form': form})  # passe ce formulaire au gabarit