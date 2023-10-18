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

from .forms import CompanyForm, BankAccountForm
from .models import Company, Info
from clearing.wallets.models import Wallet
from clearing.core.models import Counter

COMPANIES_PER_PAGE = 20


@require_http_methods(["GET"])
def home(request: HttpRequest) -> HttpResponse:

    return TemplateResponse(request, "home.html")


@require_http_methods(["GET"])
def history(request: HttpRequest) -> HttpResponse:

    return TemplateResponse(request, "history.html")


@require_http_methods(["GET"])
@login_required
def company_list(request: HttpRequest) -> HttpResponse:

    companies, search = _search_companies(request)
    context = {"companies": companies, "search": search}

    return TemplateResponse(
        request,
        "companies/company_list.html",
        context,
    )


@require_http_methods(["GET"])
@login_required
def company_list_search(request: HttpRequest) -> HttpResponse:

    companies, search = _search_companies(request)
    context = {"companies": companies, "search": search}

    return TemplateResponse(
        request,
        "companies/_company_list.html",
        context,
    )


def _search_companies(request):

    search = request.GET.get("search")
    page = request.GET.get("page")
    companies = Company.objects.all()
    if search:
        companies = companies.filter(
            Q(name__icontains=request.GET.get('search')) |
            Q(bin__icontains=request.GET.get('search'))
        )

    paginator = Paginator(companies, COMPANIES_PER_PAGE)
    try:
        companies = paginator.page(page)
    except PageNotAnInteger:
        companies = paginator.page(1)
    except EmptyPage:
        companies = paginator.page(paginator.num_pages)

    return companies, search or ""


@require_http_methods(["GET", "POST"])
@login_required
def create_company(request: HttpRequest) -> HttpResponse:

    if (counter := Counter.objects.filter(type='MAIN_WALLET').first()) is None:
        return HttpResponseClientRedirect(reverse("company_list"))

    if request.method == "GET":
        return TemplateResponse(
            request,
            "companies/company_form.html",
            {"form": CompanyForm()},
        )

    if (form := CompanyForm(request.POST)).is_valid():
        company = form.save(commit=False)
        company.save()

        country = Info.objects.create(type='COUNTRY', value=form.cleaned_data.get('country'))
        country.save()

        postal_code = Info.objects.create(type='POSTAL_CODE', value=form.cleaned_data.get('postal_code'))
        postal_code.save()

        address = Info.objects.create(type='ADDRESS', value=form.cleaned_data.get('address'))
        address.save()

        email = Info.objects.create(type='EMAIL', value=form.cleaned_data.get('email'))
        email.save()

        phone = Info.objects.create(type='PHONE', value=form.cleaned_data.get('phone'))
        phone.save()

        person = Info.objects.create(type='PERSON', value=form.cleaned_data.get('person'))
        person.save()

        company.info.add(country)
        company.info.add(postal_code)
        company.info.add(address)
        company.info.add(email)
        company.info.add(phone)
        company.info.add(person)

        wallet = Wallet.objects.create(
            trader=company, 
            account_number='ACC-' + str(counter.value + 1).zfill(5),
            contract_number=form.cleaned_data.get('contract_number'),
        )
        wallet.save()

        counter.value += 1
        counter.save()

        return HttpResponseClientRedirect(reverse("company_detail", kwargs={"company_id": company.id}))

    return TemplateResponse(request, "companies/_company_form.html", {"form": form})


@require_http_methods(["GET", "POST"])
@login_required
def edit_company(request: HttpRequest, company_id: UUID) -> HttpResponse:

    company = get_object_or_404(Company, pk=company_id)

    country = company.info.filter(type='COUNTRY').first()
    postal_code = company.info.filter(type='POSTAL_CODE').first()
    address = company.info.filter(type='ADDRESS').first()
    email = company.info.filter(type='EMAIL').first()
    phone = company.info.filter(type='PHONE').first()
    person = company.info.filter(type='PERSON').first()

    if request.method == "GET":

        return TemplateResponse(
            request,
            "companies/company_form.html",
            {
                "form": CompanyForm(instance=company, initial={
                    'country': country.value if country else '',
                    'postal_code': postal_code.value if postal_code else '',
                    'address': address.value if address else '',
                    'email': email.value if email else '',
                    'phone': phone.value if phone else '',
                    'person': person.value if person else '',
                    'contract_number': company.wallet.contract_number,
                }),
                "company": company,
            },
        )

    if (form := CompanyForm(request.POST, instance=company)).is_valid():
        form.save()

        company.wallet.contract_number = form.cleaned_data.get('contract_number')
        company.wallet.save()

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

        return HttpResponseClientRedirect(reverse("company_detail", kwargs={"company_id": company_id}))

    return TemplateResponse(
        request,
        "companies/_company_form.html",
        {
            "form": form,
            "company": company,
        },
    )


@require_http_methods(["GET"])
@login_required
def company_detail(request: HttpRequest, company_id: UUID) -> HttpResponse:

    company = get_object_or_404(Company, pk=company_id)
    bank_accounts = company.bank_accounts.all()
    context = {"company": company, "bank_accounts": bank_accounts}
    return TemplateResponse(request, "companies/company.html", context)


@require_http_methods(["GET"])
@login_required
def invert_company_status(request: HttpRequest, company_id: int) -> HttpResponse:

    company = get_object_or_404(Company, pk=company_id)

    if company.status == 'ACTIVE':
        company.status = 'BLOCKED'
    else:
        company.status = 'ACTIVE'

    company.save()

    return TemplateResponse(request, "companies/_company.html", {"company": company})


@require_http_methods(["GET", "POST"])
@login_required
def create_bank_accounts(request: HttpRequest, company_id: UUID) -> HttpResponse:

    company = get_object_or_404(Company, pk=company_id)

    if request.method == "GET":
        return TemplateResponse(
            request,
            "companies/bank_account_form.html",
            {"company": company, "form": BankAccountForm()},
        )

    if (form := BankAccountForm(request.POST)).is_valid():
        bank_account = form.save(commit=False)
        bank_account.save()

        company.bank_accounts.add(bank_account)

        return HttpResponseClientRedirect(reverse("company_detail", kwargs={"company_id": company_id}))

    return TemplateResponse(request, "companies/_bank_account_form.html", {"form": form})

