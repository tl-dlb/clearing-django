from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django_htmx.http import HttpResponseClientRedirect
from uuid import UUID

from .forms import ClientForm, BankAccountForm
from .models import Client, Info

CLIENTS_PER_PAGE = 20


@require_http_methods(["GET"])
def home(request: HttpRequest) -> HttpResponse:

    return TemplateResponse(request, "home.html")


@require_http_methods(["GET"])
def history(request: HttpRequest) -> HttpResponse:

    return TemplateResponse(request, "history.html")


@require_http_methods(["GET"])
# @login_required
def client_list(request: HttpRequest) -> HttpResponse:

    clients, search = _search_clients(request)
    context = {"clients": clients, "search": search}

    return TemplateResponse(
        request,
        "clients/client_list.html",
        context,
    )


@require_http_methods(["GET"])
# @login_required
def client_list_search(request: HttpRequest) -> HttpResponse:

    clients, search = _search_clients(request)
    context = {"clients": clients, "search": search}

    return TemplateResponse(
        request,
        "clients/_client_list.html",
        context,
    )


def _search_clients(request):

    search = request.GET.get("search")
    page = request.GET.get("page")
    clients = Client.objects.all()
    if search:
        clients = clients.filter(
            Q(name__icontains=request.GET.get('search')) |
            Q(bin__icontains=request.GET.get('search'))
        )

    paginator = Paginator(clients, CLIENTS_PER_PAGE)
    try:
        clients = paginator.page(page)
    except PageNotAnInteger:
        clients = paginator.page(1)
    except EmptyPage:
        clients = paginator.page(paginator.num_pages)

    return clients, search or ""


@require_http_methods(["GET", "POST"])
# @login_required
def create_client(request: HttpRequest) -> HttpResponse:

    if request.method == "GET":
        return TemplateResponse(
            request,
            "clients/client_form.html",
            {"form": ClientForm()},
        )

    if (form := ClientForm(request.POST)).is_valid():
        client = form.save(commit=False)
        client.save()

        country = Info.objects.create(
            type='COUNTRY', value=form.cleaned_data.get('country'))
        country.save()

        postal_code = Info.objects.create(
            type='POSTAL_CODE', value=form.cleaned_data.get('postal_code'))
        postal_code.save()

        address = Info.objects.create(
            type='ADDRESS', value=form.cleaned_data.get('address'))
        address.save()

        email = Info.objects.create(
            type='EMAIL', value=form.cleaned_data.get('email'))
        email.save()

        phone = Info.objects.create(
            type='PHONE', value=form.cleaned_data.get('phone'))
        phone.save()

        person = Info.objects.create(
            type='PERSON', value=form.cleaned_data.get('person'))
        person.save()

        client.info.add(country)
        client.info.add(postal_code)
        client.info.add(address)
        client.info.add(email)
        client.info.add(phone)
        client.info.add(person)

        return HttpResponseClientRedirect(reverse("client_detail", kwargs={"client_id": client.id}))

    return TemplateResponse(request, "clients/_client_form.html", {"form": form})


@require_http_methods(["GET", "POST"])
# @login_required
def edit_client(request: HttpRequest, client_id: UUID) -> HttpResponse:

    client = get_object_or_404(Client, pk=client_id)

    country = client.info.filter(type='COUNTRY').first()
    postal_code = client.info.filter(type='POSTAL_CODE').first()
    address = client.info.filter(type='ADDRESS').first()
    email = client.info.filter(type='EMAIL').first()
    phone = client.info.filter(type='PHONE').first()
    person = client.info.filter(type='PERSON').first()

    if request.method == "GET":

        return TemplateResponse(
            request,
            "clients/client_form.html",
            {
                "form": ClientForm(instance=client, initial={
                    'country': country.value if country else '',
                    'postal_code': postal_code.value if postal_code else '',
                    'address': address.value if address else '',
                    'email': email.value if email else '',
                    'phone': phone.value if phone else '',
                    'person': person.value if person else '',
                }),
                "client": client,
            },
        )

    if (form := ClientForm(request.POST, instance=client)).is_valid():
        form.save()

        country.value = form.cleaned_data.get('country')
        country.save()

        postal_code.value = form.cleaned_data.get('postal_code')
        postal_code.save()

        address.value = form.cleaned_data.get('address')
        address.save()

        email.value = form.cleaned_data.get('email')
        email.save()

        phone.value = form.cleaned_data.get('phone')
        phone.save()

        person.value = form.cleaned_data.get('person')
        person.save()

        return HttpResponseClientRedirect(reverse("client_detail", kwargs={"client_id": client_id}))

    return TemplateResponse(
        request,
        "clients/_client_form.html",
        {
            "form": form,
            "client": client,
        },
    )


@require_http_methods(["GET"])
# @login_required
def client_detail(request: HttpRequest, client_id: UUID) -> HttpResponse:

    client = get_object_or_404(Client, pk=client_id)
    bank_accounts = client.bank_accounts.all()
    context = {"client": client, "bank_accounts": bank_accounts}
    return TemplateResponse(request, "clients/client.html", context)


@require_http_methods(["GET"])
# @login_required
def activate_client(request: HttpRequest, client_id: int) -> HttpResponse:

    client = get_object_or_404(Client, pk=client_id)

    if client.status == 'ACTIVE':
        client.status = 'BLOCKED'
    else:
        client.status = 'ACTIVE'

    client.save()

    return TemplateResponse(request, "clients/_client.html", {"client": client})


@require_http_methods(["GET", "POST"])
# @login_required
def create_bank_accounts(request: HttpRequest, client_id: UUID) -> HttpResponse:

    client = get_object_or_404(Client, pk=client_id)

    if request.method == "GET":
        return TemplateResponse(
            request,
            "clients/bank_account_form.html",
            {"client": client, "form": BankAccountForm()},
        )

    if (form := BankAccountForm(request.POST)).is_valid():
        bank_account = form.save(commit=False)
        bank_account.save()

        client.bank_accounts.add(bank_account)

        return HttpResponseClientRedirect(reverse("client_detail", kwargs={"client_id": client_id}))

    return TemplateResponse(request, "clients/_bank_account_form.html", {"form": form})
