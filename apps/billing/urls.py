from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import PlanViewSet, SubscriptionViewSet, pricing_plans_view, invoices_view

router = DefaultRouter()
router.register(r'api/plans', PlanViewSet, basename='plans-api')
router.register(r'api/subscriptions', SubscriptionViewSet, basename='subscriptions-api')

urlpatterns = [
    path('', pricing_plans_view, name='billing-plans'),
    path('plans/', pricing_plans_view, name='billing-plans-direct'),
    path('invoices/', invoices_view, name='billing-invoices'),
] + router.urls
