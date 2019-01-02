from datetime import datetime

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, UpdateView, CreateView, DeleteView

from Restaurant_menagment.forms import *
from .functions import render_to_pdf
from .models import *


class MainView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'Restaurant_menagment/base.html')


class TableCreateView(CreateView):
    model = Table
    fields = '__all__'
    success_url = reverse_lazy("table_list")


class TableDeleteView(DeleteView):
    model = Table
    success_url = reverse_lazy("table_list")


class TableEditView(UpdateView):
    model = Table
    fields = '__all__'
    success_url = reverse_lazy("table_list")


class TableListView(ListView):
    model = Table
    ordering = ['number']


class TableDetailsView(View):

    def get(self, request, number):
        table = Table.objects.get(number=number)
        return render(request, "Restaurant_menagment/table_details.html", {'table': table})


class AddOrderView(View):

    def get(self, request, tableNumber):
        table = Table.objects.get(number=tableNumber)
        order = Orders.objects.create(status=1, table=table)
        return redirect('/add_meal_to_order/%s' % order.id)


class OrdersEditView(UpdateView):
    model = Orders
    fields = '__all__'
    success_url = reverse_lazy("table_list")


class OrderDeleteView(DeleteView):
    model = Orders
    success_url = reverse_lazy("table_list")


class AddMealToOrder(View):

    def get(self, request, id):
        order = Orders.objects.get(pk=id)
        dishes = Dish.objects.all()
        comments = order.comments_set.all()
        categories = Category.objects.all()
        ctx = {'order': order,
               'dishes': dishes,
               'comments': comments,
               'categories': categories}
        return render(request, 'Restaurant_menagment/add_meal_to_order.html', ctx)

    def post(self, request, id):

        order = Orders.objects.get(pk=id)
        if request.POST.get("dish"):
            dish = Dish.objects.get(pk=request.POST.get("dish"))
            order.dish_set.add(dish)
        if request.POST.get("comment"):
            Comments.objects.create(comment=request.POST.get("comment"), order=order)

        return redirect('/add_meal_to_order/%s' % order.id)


class KitchenOrdersView(View):

    def get(self, request):
        orders = Orders.objects.filter(status=1)
        return render(request, 'Restaurant_menagment/kitchen_order_list.html', {'orders': orders})

    def post(self, request):
        order = Orders.objects.get(pk=request.POST.get("id"))
        order.status = 2
        order.save()
        return redirect('/order_details/%s' % order.id)


class OrderDetailsView(View):
    def get(self, request, id):
        order = Orders.objects.get(pk=id)
        return render(request, 'Restaurant_menagment/order_details.html', {'order': order})

    def post(self, request, id):
        order = Orders.objects.get(pk=id)
        order.status = 3
        order.save()
        return redirect('/orders_to_serve')


class OrdersInProgresView(View):

    def get(self, request):
        orders = Orders.objects.filter(status=2)
        return render(request, 'Restaurant_menagment/order_in_progres.html', {'orders': orders})


class OrdersToServeView(View):

    def get(self, request):
        orders = Orders.objects.filter(status=3)
        return render(request, 'Restaurant_menagment/order_to_serve.html', {'orders': orders})


class OrdersServed(View):

    def get(self, request, id):
        order = Orders.objects.get(pk=id)
        order.status = 4
        order.save()
        return redirect('toserve')


class BillView(View):

    def get(self, request, id):
        table = Table.objects.get(pk=id)
        orders = table.orders_set.filter(archive=False)
        partSume = {}
        for order in orders:
            partSume.setdefault(order.id, []).append(order.dish_set.all())

        for order in orders:
            for dishSet in partSume[order.id]:
                price = 0
                for dish in dishSet:
                    price += dish.price
                partSume[order.id] = price

        ctx = {'table': table,
               'orders': orders,
               'partSume': partSume,
               }
        return render(request, 'Restaurant_menagment/bill.html', ctx)


class GenerateBillDocumentView(View):

    def get(self, request, id):
        order = Orders.objects.get(pk=id)
        dishes = order.dish_set.all()
        amount = 0
        for dish in dishes:
            amount += dish.price

        ctx = {'order_id': id,
               'now': datetime.now(),
               'dishes': dishes,
               'amount': amount,
               }
        pdf = render_to_pdf('Restaurant_menagment/invoice.html', ctx)
        return pdf


class OrderPayedView(View):

    def post(self, request, id):
        order = Orders.objects.get(pk=id)
        table_id = order.table.id
        order.archive = True
        order.save()
        return redirect('/bill/%s' % table_id)


class RegisterView(PermissionRequiredMixin, View):
    permission_required = 'auth.add_user'

    def get(self, request):
        form = RegisterForm()
        return render(request, 'Restaurant_menagment/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data.get('username'),
                                            password=form.cleaned_data.get('password'),
                                            email=form.cleaned_data.get('email'),
                                            first_name=form.cleaned_data.get('first_name'),
                                            last_name=form.cleaned_data.get('last_name'),
                                            )
            print(form.cleaned_data.get('groups'))
            user.groups.set(form.cleaned_data.get('groups'))
            return HttpResponse("OK")
        else:
            return render(request, 'Restaurant_menagment/register.html', {'form': form})


class LoginView(View):

    def get(self, request):
        form = LogInForm()
        return render(request, 'Restaurant_menagment/login.html', {'form': form})

    def post(self, request):
        form = LogInForm(request.POST)
        if form.is_valid():
            loginn = form.cleaned_data.get("login")
            password = form.cleaned_data.get("password")
            user = authenticate(username=loginn, password=password)

            if user:
                login(request, user)
                next = request.GET.get("next")
                if next is not None:
                    return redirect(next)
                return redirect('/main')
            else:
                return HttpResponse("Nie ma takiego użytkownika")

        return redirect('/')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/')
