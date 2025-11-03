from django.shortcuts import render
from django.http import HttpResponse
from .models import Product

def home(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'home.html', context=context)

def contacts(request):
    if request.method == 'POST':
        # Получение данных из формы
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        # Обработка данных (например, сохранение в БД, отправка email и т. д.)
        # Здесь мы просто возвращаем простой ответ
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено и ваш номер телефона {phone} записан.")
    return render(request, 'contacts.html')

def product_card(request, pk):
    product = Product.objects.get(id=pk)
    context = {'product': product}
    return render(request, 'product_card.html', context=context)