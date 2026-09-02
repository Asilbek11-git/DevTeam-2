"""
Billing views for plans, subscriptions, checkout, and invoice templates.
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from apps.core.responses import success_response
from apps.core.permissions import IsWorkspaceOwner, get_active_workspace
from django.db.models import Q
from apps.workspaces.models import Client
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
    """Render workspace billing invoices & payment methods with strict role isolation."""
    workspace, role = get_active_workspace(request)
    invoices = []
    
    if not workspace:
        messages.warning(request, "Please create or select a workspace.")
        return redirect('workspace-list')
        
    if role in ['OWNER', 'ADMIN'] or request.user.is_superuser:
        invoices = Invoice.objects.filter(workspace=workspace).order_by('-created_at')
    elif role == 'CLIENT':
        # Client can only see invoices linked to their client profile
        client_obj = Client.objects.filter(
            Q(workspace=workspace) & (
                Q(user=request.user) | Q(email__iexact=request.user.email) | Q(owner=request.user)
            )
        ).first()
        if client_obj:
            invoices = Invoice.objects.filter(workspace=workspace, client=client_obj).order_by('-created_at')
        else:
            invoices = Invoice.objects.none()
    else:
        # Team members (DEVELOPER, etc.) cannot view financial billing invoices
        messages.error(request, "Access restricted. You do not have permission to view billing invoices.")
        return redirect('dashboard')
        
    return render(request, 'billing/invoices.html', {
        'invoices': invoices,
        'page_title': 'Invoices & Billing History'
    })
