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

from .forms import FundForm
from .models import Wallet


@require_http_methods(["GET"])
# @login_required
def fund_list(request: HttpRequest) -> HttpResponse:

    companies, search = _search_companies(request)
    context = {"companies": companies, "search": search}

    return TemplateResponse(
        request,
        "companies/company_list.html",
        context,
    )

# Create your views here.
@require_http_methods(["GET", "POST"])
# @login_required
def create_fund(request: HttpRequest, wallet_id: UUID, fund_type: str) -> HttpResponse:

    wallet = get_object_or_404(Wallet, pk=wallet_id)

    if request.method == "GET":
        return TemplateResponse(
            request,
            "wallets/fund_form.html",
            {"form": FundForm(), "wallet": wallet, "fund_type": fund_type},
        )

    if (form := FundForm(request.POST)).is_valid():
        fund = form.save(commit=False)
        fund.type = fund_type
        fund.save()

        wallet.funds.add(fund)
        wallet.calculate()

        return HttpResponseClientRedirect(reverse("company_detail", kwargs={"company_id": wallet.trader.id}))

    return TemplateResponse(request, "wallets/_fund_form.html", {"form": form, "wallet": wallet, "fund_type": fund_type})