"""Final_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from Restaurant_menagment.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^main$', MainView.as_view()),
    url(r'^create/table$', TableCreateView.as_view()),
    url(r'^delete/table/(?P<pk>\d+)$', TableDeleteView.as_view()),
    url(r'^edit/table/(?P<pk>\d+)$', TableEditView.as_view()),
    url(r'^table_list$', TableListView.as_view(), name='table_list'),
    url(r'^table_details/(?P<number>\d+)$', TableDetailsView.as_view()),
    url(r'^add_order/(?P<tableNumber>\d+)$', AddOrderView.as_view()),
    url(r'^order/delete/(?P<pk>\d+)$', OrderDeleteView.as_view()),
    url(r'^order/edit/(?P<pk>\d+)', OrdersEditView.as_view()),
    url(r'^orders_colected$', KitchenOrdersView.as_view()),
    url(r'^order_details/(?P<id>\d+)$', OrderDetailsView.as_view()),
    url(r'^orders_to_serve$', OrdersToServeView.as_view(), name='toserve'),
    url(r'^orders_in_progres$', OrdersInProgresView.as_view(), name='inprogres'),
    url(r'^served/(?P<id>\d+)$', OrdersServed.as_view()),
    url(r'^add_meal_to_order/(?P<id>\d+)$', AddMealToOrder.as_view()),
    url(r'^bill/(?P<id>\d+)$', BillView.as_view()),
    url(r'^pdf/(?P<id>\d+)$', GenerateBillDocumentView.as_view()),
    url(r'^payed/(?P<id>\d+)', OrderPayedView.as_view()),
    url(r'^register$', RegisterView.as_view()),
    url(r'^$', LoginView.as_view()),
    url(r'^logout$', LogoutView.as_view())
]
