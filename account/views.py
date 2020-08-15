from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from account.models import item_request, subcategory, item_available
from math import ceil
import pgeocode

from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)
User = get_user_model()

from .forms import UserLoginForm, UserRegistrationForm, ItemRequestForm, searchForm, organizationSearchForm, ItemForm, searchForm2
from django.core.mail import send_mail
from django.db.models import Q
from .forms import emailForm

def pdistance(key, postal_code1, postal_code2):
    d = pgeocode.GeoDistance(key)
    return d.query_postal_code(postal_code1, postal_code2)

def homePage(request):
    return render(request, 'home.html', {'loggedin': request.user.is_authenticated})

@login_required(login_url='login')
def organizationSearch(request):
    form = organizationSearchForm()
    searched = False

    if request.POST:
        searched = True
        form = organizationSearchForm(request.POST)
        qs2 = User.objects.all()

        if form.is_valid():
            organization_name_search = form.cleaned_data['organization_name']
            organization_distance_search = form.cleaned_data['organization_distance']

            if organization_distance_search == "anywhere":
                pass
            elif organization_distance_search == "country":
                qs2 = qs2.filter(country=request.user.country)
            elif organization_distance_search == "postalcode":
                qs2 = qs2.filter(country=request.user.country).filter(postal_code=request.user.postal_code)
            else:
                qs2 = qs2.filter(country=request.user.country)
                numerical_distance = eval(str(organization_distance_search))
                nearby_requests=[]
                for r in qs2:
                    d = pdistance(str(request.user.country), r.postal_code, request.user.postal_code)
                    if (d <= numerical_distance):
                        nearby_requests.append(r.id)
                qs2 = qs2.filter (id__in=nearby_requests)

            if organization_name_search is not None:
                if organization_name_search != "":
                    qs2 = qs2.filter(organization_name__contains=organization_name_search)

    if searched:
        context = {'loggedin': request.user.is_authenticated, 'form': form, 'qs2': qs2}
    else:
        context = {'loggedin': request.user.is_authenticated, 'form': form}
    return render(request, 'organization_search.html', context)

@login_required(login_url='login')
def profilePage(request):
    context = {'user': request.user, 'loggedin': request.user.is_authenticated}
    return render(request, 'profilePage.html', context)

@login_required(login_url='login')
def discoverPage(request):
    products = item_request.objects.all()

    allProds=[]
    catprod=item_request.objects.values('item_category','id')
    cats ={item['item_category']for item in catprod}
    for cat in cats:
        prod=item_request.objects.filter(item_category=cat)
        n=len(products)
        nSlides = n//4 + ceil((n/4)-(n//4))
        allProds.append([prod,range(1,nSlides),nSlides])

    params= {'allProds':allProds, 'loggedin': request.user.is_authenticated}
    return render(request,'discoverPage.html',params)

@login_required(login_url='login')
def discoverPage2(request):
    products = item_available.objects.all()

    allProds=[]
    catprod=item_available.objects.values('item_category','id')
    cats ={item['item_category']for item in catprod}
    for cat in cats:
        prod=item_available.objects.filter(item_category=cat)
        n=len(products)
        nSlides = n//4 + ceil((n/4)-(n//4))
        allProds.append([prod,range(1,nSlides),nSlides])

    params= {'allProds':allProds, 'loggedin': request.user.is_authenticated}
    return render(request,'discoverPage2.html',params)

@login_required(login_url='login')
def organizationPage(request, pk):
    organization = User.objects.get(id=pk)
    context = {'organization': organization, 'loggedin': request.user.is_authenticated}

    return render (request, 'organization_details.html', context)

@login_required(login_url='login')
def itemPage(request, pk):
    item = item_available.objects.get(id=pk)
    context = {'item': item, 'sameuser': int(request.user.id) != int(item_available.objects.all().get(id=pk).item_organization.id), 'loggedin': request.user.is_authenticated}
    return render (request, 'item_details.html', context)

@login_required(login_url='login')
def itemRequestPage(request, pk):
    item = item_request.objects.get(id=pk)
    context = {'item': item, 'sameuser': int(request.user.id) != int(item_request.objects.all().get(id=pk).item_organization.id), 'loggedin': request.user.is_authenticated}
    return render (request, 'item_request_details.html', context)

@login_required(login_url='login')
def deleteItem2(request, pk):
    item = item_available.objects.get(id=pk)
    if item.item_organization != request.user:
        return redirect ('itemViewPage')

    if request.method == "POST":
        item.delete()
        return redirect('itemViewPage')
    context = {'item': item, 'loggedin': request.user.is_authenticated}
    return render (request, 'delete2.html', context)

@login_required(login_url='login')
def deleteItem(request, pk):
    item = item_request.objects.get(id=pk)
    if item.item_organization != request.user:
        return redirect ('viewitemrequests')

    if request.method == "POST":
        item.delete()
        return redirect('viewitemrequests')
    context = {'item': item, 'loggedin': request.user.is_authenticated}
    return render (request, 'delete.html', context)

@login_required(login_url='login')
def itemRequestViewPage(request):
    qs = item_request.objects.all()
    qs = qs.filter(item_organization=request.user)
    context = {
        'queryset': qs, 'loggedin': request.user.is_authenticated
    }
    return render(request, "view_item_requests.html", context)

@login_required(login_url='login')
def itemViewPage(request):
    qs = item_available.objects.all()
    qs = qs.filter(item_organization=request.user)
    context = {
        'queryset': qs, 'loggedin': request.user.is_authenticated
    }
    return render(request, "view_items.html", context)

@login_required(login_url='login')
def itemRequestSearch(request):
    form = searchForm()
    searched = False

    if request.method == "POST":
        form = searchForm(request.POST)
        searched = True
        qs = item_request.objects.all()
        qs2 = User.objects.all()

        if form.is_valid():
            item_name_search = form.cleaned_data['item_request_name']
            item_organization_search = form.cleaned_data['item_organization_name']
            item_start_date_search = form.cleaned_data['item_start_date']
            item_end_date_search = form.cleaned_data['item_end_date']
            item_distance_search = form.cleaned_data['item_distance']
            item_category_search = form.cleaned_data['item_category']
            item_subcategory_search = form.cleaned_data['item_subcategory']

            if item_distance_search == "anywhere":
                pass
            elif item_distance_search == "country":
                qs2 = qs2.filter(country=request.user.country)
                qs = qs.filter(item_organization__in=qs2)
            elif item_distance_search == "postalcode":
                qs2 = qs2.filter(country=request.user.country).filter(postal_code=request.user.postal_code)
                qs = qs.filter(item_organization__in=qs2)
            else:
                qs2 = qs2.filter(country=request.user.country)
                qs = qs.filter(item_organization__in=qs2)
                numerical_distance = eval(str(item_distance_search))
                nearby_requests=[]
                for r in qs:
                    d = pdistance(str(request.user.country), r.item_organization.postal_code, request.user.postal_code)
                    if (d <= numerical_distance):
                        nearby_requests.append(r.id)
                qs = qs.filter (id__in=nearby_requests)

            if item_category_search is not None:
                qs = qs.filter(item_category=item_category_search)

            if item_subcategory_search is not None:
                qs = qs.filter(item_subcategory=item_subcategory_search)

            if item_start_date_search is not None:
                qs = qs.filter(Q (item_start_date__lt = item_start_date_search) | Q(item_start_date=item_start_date_search)).filter(Q(item_end_date__gt = item_start_date_search)| Q(item_end_date=item_end_date_search))

            if item_end_date_search is not None:
                qs = qs.filter(Q(item_end_date__gt = item_end_date_search)|Q(item_end_date=item_end_date_search)).filter(Q(item_start_date__lt = item_end_date_search)|Q(item_start_date=item_end_date_search))

            if item_name_search is not None:
                if item_name_search != "":
                    qs = qs.filter(item_name__contains=item_name_search)

            if item_organization_search is not None:
                qs2 = qs2.filter(organization_name__contains=item_organization_search)
                qs = qs.filter(item_organization__in=qs2)

    if searched:
        context = {'organization_name': request.user, 'queryset': qs, 'searchform': form, 'loggedin': request.user.is_authenticated}
    else:
        context = {'organization_name': request.user, 'searchform': form, 'loggedin': request.user.is_authenticated}

    return render(request, "item_request_search.html", context)

@login_required(login_url='login')
def itemSearch(request):
    form = searchForm2()
    searched = False

    if request.method == "POST":
        form = searchForm2(request.POST)
        searched = True
        qs = item_available.objects.all()
        qs2 = User.objects.all()

        if form.is_valid():
            item_name_search = form.cleaned_data['item_request_name']
            item_organization_search = form.cleaned_data['item_organization_name']
            item_distance_search = form.cleaned_data['item_distance']
            item_category_search = form.cleaned_data['item_category']
            item_subcategory_search = form.cleaned_data['item_subcategory']

            if item_distance_search == "anywhere":
                pass
            elif item_distance_search == "country":
                qs2 = qs2.filter(country=request.user.country)
                qs = qs.filter(item_organization__in=qs2)
            elif item_distance_search == "postalcode":
                qs2 = qs2.filter(country=request.user.country).filter(postal_code=request.user.postal_code)
                qs = qs.filter(item_organization__in=qs2)
            else:
                qs2 = qs2.filter(country=request.user.country)
                qs = qs.filter(item_organization__in=qs2)
                numerical_distance = eval(str(item_distance_search))
                nearby_requests=[]
                for r in qs:
                    d = pdistance(str(request.user.country), r.item_organization.postal_code, request.user.postal_code)
                    if (d <= numerical_distance):
                        nearby_requests.append(r.id)
                qs = qs.filter (id__in=nearby_requests)

            if item_category_search is not None:
                qs = qs.filter(item_category=item_category_search)

            if item_subcategory_search is not None:
                qs = qs.filter(item_subcategory=item_subcategory_search)

            if item_name_search is not None:
                if item_name_search != "":
                    qs = qs.filter(item_name__contains=item_name_search)

            if item_organization_search is not None:
                qs2 = qs2.filter(organization_name__contains=item_organization_search)
                qs = qs.filter(item_organization__in=qs2)

    if searched:
        context = {'organization_name': request.user, 'queryset': qs, 'searchform': form, 'loggedin': request.user.is_authenticated}
    else:
        context = {'organization_name': request.user, 'searchform': form, 'loggedin': request.user.is_authenticated}

    return render(request, "item_search.html", context)

# Create your views here.
@login_required(login_url='login')
def submitRequestPage(request):
    form = ItemRequestForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        itemrequest = form.save(commit=False)
        itemrequest.item_organization = request.user
        itemrequest.save()
        return redirect ('viewitemrequests')
    context = {
        'form': form,
        'organization_name': request.user, 'loggedin': request.user.is_authenticated
    }
    return render(request, "submitRequestPage.html", context)

@login_required(login_url='login')
def submitItemPage(request):
    form = ItemForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        itemrequest = form.save(commit=False)
        itemrequest.item_organization = request.user
        itemrequest.save()
        return redirect ('itemViewPage') #change
    context = {
        'form': form,
        'organization_name': request.user, 'loggedin': request.user.is_authenticated
    }
    return render(request, "submitItemPage.html", context)

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('discoverPage')

    next = request.GET.get('next')
    form = UserRegistrationForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(email=user.email, password=password)
        login(request, new_user)
        if next:
            return redirect(next)
        return redirect('discoverPage')

    context = {
        'form': form, 'loggedin': request.user.is_authenticated
    }
    return render(request, "register.html", context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('discoverPage')

    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)

    if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('discoverPage')

    context = {
        'form': form, 'loggedin': request.user.is_authenticated
    }
    return render(request, "login.html", context)


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def load_subcategories(request):
    category_id = request.GET.get('item_category')
    subcategories = subcategory.objects.filter(category_id=category_id)
    return render(request, 'hr/item_subcategory_dropdown_list_options.html', {'subcategories': subcategories, 'loggedin': request.user.is_authenticated})

@login_required(login_url='login')
def sendEmail(request, pk, pk2):
    if item_request.objects.all().get(id=pk2).item_organization != User.objects.all().get(id=pk):
        return redirect('discoverPage')

    if int(request.user.id) == int(pk):
        return redirect('discoverPage')

    form = emailForm ()
    form.fields['message_name'].initial = request.user.organization_name + " @ UConnect: Response to your " + item_request.objects.all().get(id=pk2).item_name + " request"
    form.fields['message_email_to'].initial = User.objects.all().get(id=pk).email

    if request.method == "POST":
        form = emailForm(request.POST)

        if form.is_valid():
            message_name = form.cleaned_data.get('message_name')
            message_email_to = form.cleaned_data.get('message_email_to')
            message = form.cleaned_data.get('message')
        send_mail(
            message_name,
            message,
            'hackforafrica@gmail.com',
            [message_email_to],
        )
        return redirect('discoverPage')
    else:
        return render (request, 'email.html', {'form': form, 'loggedin': request.user.is_authenticated, 'pk': pk, 'pk2': pk2})

@login_required(login_url='login')
def sendEmail2(request, pk, pk2):
    if item_available.objects.all().get(id=pk2).item_organization != User.objects.all().get(id=pk):
        return redirect('discoverPage')

    if int(request.user.id) == int(pk):
        return redirect('discoverPage')

    form = emailForm ()
    form.fields['message_name'].initial = request.user.organization_name + " @ UConnect: Request for your " + item_available.objects.all().get(id=pk2).item_name + " posting"
    form.fields['message_email_to'].initial = User.objects.all().get(id=pk).email

    if request.method == "POST":
        form = emailForm(request.POST)

        if form.is_valid():
            message_name = form.cleaned_data.get('message_name')
            message_email_to = form.cleaned_data.get('message_email_to')
            message = form.cleaned_data.get('message')
        send_mail(
            message_name,
            message,
            'hackforafrica@gmail.com',
            [message_email_to],
        )
        return redirect('discoverPage')
    else:
        return render (request, 'email.html', {'form': form, 'loggedin': request.user.is_authenticated, 'pk': pk, 'pk2': pk2})