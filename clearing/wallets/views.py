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
@login_required
def fund_list(request: HttpRequest, wallet_id: UUID) -> HttpResponse:

    wallet, funds, search = _search_funds(request, wallet_id)
    context = {"wallet": wallet, "funds": funds, "search": search}

    return TemplateResponse(
        request,
        "wallets/fund_list.html",
        context,
    )


@require_http_methods(["GET"])
@login_required
def fund_list_search(request: HttpRequest, wallet_id: UUID) -> HttpResponse:

    wallet, funds, search = _search_funds(request, wallet_id)
    context = {"wallet": wallet, "funds": funds, "search": search}

    return TemplateResponse(
        request,
        "wallets/_fund_list.html",
        context,
    )


def _search_funds(request, wallet_id):

    search = request.GET.get("search")
    page = request.GET.get("page")
    wallet = Wallet.objects.get(id=wallet_id)
    funds = wallet.funds.filter(Q(type='INCOMING')|Q(type='OUTGOING')).order_by('-created_at').all()
    if search:
        funds = funds.filter(
            Q(amount__icontains=request.GET.get('search')) |
            Q(payment_number__icontains=request.GET.get('search')) |
            Q(comment__icontains=request.GET.get('search'))
        )

    paginator = Paginator(funds, 20)
    try:
        funds = paginator.page(page)
    except PageNotAnInteger:
        funds = paginator.page(1)
    except EmptyPage:
        funds = paginator.page(paginator.num_pages)

    return wallet, funds, search or ""


@require_http_methods(["GET", "POST"])
@login_required
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

        return HttpResponseClientRedirect(reverse("fund_list", kwargs={"wallet_id": wallet.id}))

    return TemplateResponse(request, "wallets/_fund_form.html", {"form": form, "wallet": wallet, "fund_type": fund_type})