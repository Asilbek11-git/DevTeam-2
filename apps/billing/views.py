"""
Billing views for plans, subscriptions, checkout, and invoice templates.
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from apps.core.responses import success_response
from apps.core.permissions import IsWorkspaceOwner
from .models import Plan, Subscription, Invoice, Coupon
from .serializers import PlanSerializer, SubscriptionSerializer, InvoiceSerializer

class PlanViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Plan.objects.filter(is_active=True).order_by('monthly_price')
    serializer_class = PlanSerializer
    permission_classes = [AllowAny]

class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated, IsWorkspaceOwner]

    def get_queryset(self):
        workspace = getattr(self.request, 'current_workspace', None)
        if workspace:
            return Subscription.objects.filter(workspace=workspace)
        return Subscription.objects.none()

def pricing_plans_view(request):
    """Render public or workspace pricing comparison table."""
    plans = Plan.objects.filter(is_active=True).order_by('monthly_price')
    workspace = getattr(request, 'current_workspace', None)
    current_sub = None
    if workspace:
        current_sub = Subscription.objects.filter(workspace=workspace).first()
        
    return render(request, 'billing/plans.html', {
        'plans': plans,
        'current_subscription': current_sub,
        'page_title': 'Pricing & Subscription Plans'
    })

@login_required(login_url='login')
def invoices_view(request):
    """Render workspace billing invoices & payment methods."""
    workspace = getattr(request, 'current_workspace', None)
    invoices = []
    if workspace:
        invoices = Invoice.objects.filter(workspace=workspace).order_by('-created_at')
    return render(request, 'billing/invoices.html', {
        'invoices': invoices,
        'page_title': 'Invoices & Billing History'
    })
