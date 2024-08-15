from django.shortcuts import render, redirect, get_object_or_404
from courses.models import Course
from .models import Cart, CartItem
from discounts.utils import calculate_discount
from django.core.mail import send_mail
from .forms import CheckoutForm
from django.conf import settings


def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    discounted_total, discount_percentage = calculate_discount(cart)
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        course = get_object_or_404(Course, id=course_id)
        quantity = int(request.POST.get('quantity', 1))
        cart_item, created = CartItem.objects.get_or_create(cart=cart, course=course)
        if not created:
            cart_item.quantity += quantity
        cart_item.save()
        return redirect('cart_view')

    context = {
        'cart': cart,
    }
    return render(request, 'cart/cart.html', {
        'cart': cart,
        'discounted_total': discounted_total,
        'discount_percentage': discount_percentage,
    })


def add_to_cart(request, course_id):
    cart, created = Cart.objects.get_or_create(user=request.user)
    course = get_object_or_404(Course, id=course_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, course=course)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('cart_view')


def update_cart(request):
    if request.method == 'POST':
        cart = Cart.objects.get(user=request.user)
        for item in cart.items.all():
            quantity = request.POST.get(f'quantity_{item.id}')
            if quantity:
                item.quantity = int(quantity)
                item.save()
        return redirect('cart_detail')


def remove_from_cart(request, item_id):
    cart = Cart.objects.get(user=request.user)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    item.delete()
    return redirect('cart_detail')


def checkout_view(request):
    cart = Cart.objects.get(user=request.user)
    discounted_total, discount_percentage = calculate_discount(cart)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Збираємо інформацію про замовлення
            order_details = []
            for item in cart.items.all():
                order_details.append(
                    f"Курс: {item.course.title}, Кількість: {item.quantity}, Вартість: {item.get_cost()} грн")

            order_details = "\n".join(order_details)
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']

            # Формування повідомлення
            message = f"""
            Нова заявка на замовлення:

            Ім'я: {full_name}
            Email: {email}
            Телефон: {phone}

            Замовлення:
            {order_details}

            Загальна вартість замовлення (з урахуванням знижки): {discounted_total} грн
            """

            # Відправка листа на електронну пошту компанії
            send_mail(
                subject='Нове замовлення',
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.COMPANY_EMAIL],
            )

            # Очищення кошика після успішної оплати
            cart.items.all().delete()

            return redirect('checkout_success')  # Перенаправлення на сторінку успішного оформлення замовлення
    else:
        form = CheckoutForm()

    context = {
        'cart': cart,
        'discounted_total': discounted_total,
        'discount_percentage': discount_percentage,
        'form': form,
    }
    return render(request, 'cart/checkout.html', context)


def checkout_success_view(request):
    return render(request, 'cart/checkout_success.html')