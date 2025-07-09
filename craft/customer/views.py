from django.shortcuts import render,redirect
from django.views.generic import ListView,DetailView
from account.models import *
from django.db.models import Avg
from django.shortcuts import get_object_or_404
# from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import *
from django.core.mail import send_mail
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.core.mail import EmailMultiAlternatives
from django.utils.html import format_html


def signin_required(fn):
    def inner(request, *args, **kw):
        if request.user.is_authenticated:
            return fn(request, *args, **kw)
        else:
            messages.error(request, 'Please login First!!')
            return redirect('login')
    return inner

decorators = [signin_required, never_cache]


class ShopView(ListView):
    template_name='shop.html'
    queryset=Productss.objects.all()
    context_object_name='products'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_products = Productss.objects.all().order_by('-created_at')[:8]
        context['latest_products'] = latest_products

        
        return context
    

class ProductListView(ListView):
    model = Productss
    template_name = 'productlist.html'
    context_object_name = 'products'

    def get_queryset(self):
        cat = self.kwargs.get('cat')
        self.request.session['category'] = cat
        
        sort_option = self.request.GET.get('sortby')
        queryset = Productss.objects.filter(category=cat)
        if sort_option == 'price_asc':
            queryset = queryset.order_by('offerprice')
        elif sort_option == 'price_desc':
            queryset = queryset.order_by('-offerprice')
        elif sort_option == 'newest':
            queryset = queryset.order_by('-created_at')
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.kwargs.get('cat')
        context['category'] = category
        
        context['sortby'] = self.request.GET.get('sortby', '')
        return context



class ProductDetailView(DetailView):
    template_name = 'productdetail.html'
    queryset = Productss.objects.all()
    context_object_name = 'product'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()

        related_products = Productss.objects.filter(category=product.category).exclude(id=product.id)[:4]
    
        context['related_products'] = related_products

        return context


def product_detail(request, id):
    product = get_object_or_404(Productss, pk=id)
    
    return render(request, 'productdetail.html', {
        'product': product,
        'form': form,
        'category': product.category, 
    })


       
        # if 'reply_to_review' in request.POST:
        #     review_id = request.POST.get('reply_to_review')
        #     review = get_object_or_404(ProductReview, id=review_id)
            
        #     existing_reply = ReviewReply.objects.filter(review=review).first()
        #     if existing_reply:
        #         messages.error(request, "A reply already exists for this review.")
        #         return redirect('view_reviews', pk=pk)

            # reply_form = ReviewReplyForm(request.POST)
            # if reply_form.is_valid() and request.user.is_superuser:
            #     reply = reply_form.save(commit=False)
            #     reply.review = review
            #     reply.admin = request.user
            #     reply.save()
            #     return redirect('view_reviews', pk=pk)

    return render(request, 'view_reviews.html', {
        'product': product,
        
        # 'reply_form': reply_form,
    })



@signin_required
def addToCart(request,*args,**kwargs):
    try:
        pid=kwargs.get('id')
        product=Productss.objects.get(id=pid)
        user=request.user
        cartcheck=Cart.objects.filter(product=product,user=user).exists()
        if cartcheck:
            cartitem=Cart.objects.get(product=product,user=user)
            cartitem.quantity+=1
            cartitem.save()
            return redirect('cartlist')
        else:
            Cart.objects.create(product=product,user=user)
            return redirect('cartlist')
    except Exception as e:
        print(f"Error in addToCart: {e}")
        return redirect('cartlist')
    
@method_decorator(decorator=decorators, name='dispatch')
class CartListView(ListView):
    template_name = 'cart.html'
    queryset = Cart.objects.all()
    context_object_name = 'carts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        carts = self.get_queryset()

        subtotal = sum(cart.total for cart in carts)
        if subtotal > 5000:
            shipping_fee = 0
        else:
            shipping_fee = sum(
                (int(cart.product.ShippingFee) if cart.product.ShippingFee.isdigit() else 0) * cart.quantity
                for cart in carts
            )

        context['subtotal'] = subtotal
        context['shipping_fee'] = shipping_fee
        context['grand_total'] = subtotal + shipping_fee

        return context



def IncreaseQuantity(request, *args, **kwargs):
    try:
        cid = kwargs.get('id')
        cart = Cart.objects.get(id=cid)
        cart.quantity += 1
        cart.save()
        return redirect('cartlist')
    except:
        return redirect('cartlist')


def decreaseQuantity(request, *args, **kwargs):
    try:
        cid = kwargs.get('id')
        cart = Cart.objects.get(id=cid)
        if cart.quantity == 1:
            cart.delete()
        else:
            cart.quantity -= 1
            cart.save()
        return redirect('cartlist')
    except:
        return redirect('cartlist')


def deleteCartItem(request, **kwargs):
    try:
        cid = kwargs.get('id')
        cart = Cart.objects.get(id=cid)
        cart.delete()
        return redirect('cartlist')
    except:
        return redirect('cartlist')
    
@signin_required
def add_to_wishlist(request, product_id):
    product = Productss.objects.get(id=product_id)
    Wishlist.objects.get_or_create(user=request.user, product=product)
    return redirect('shop')


def remove_from_wishlist(request, product_id):
    product = Productss.objects.get(id=product_id)
    Wishlist.objects.filter(user=request.user, product=product).delete()
    return redirect('wishlist_view')


@signin_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

@signin_required
def placeorder(request):
    try:
        cart_items = Cart.objects.filter(user=request.user)

        if not cart_items.exists():
            return redirect('cartlist')

        for cart in cart_items:
            product = cart.product
            if product.stock > 0:
                product.stock -= cart.quantity
                product.save()
                Orders.objects.create(
                    product=cart.product,
                    user=request.user,
                    quantity=cart.quantity,
                    total=cart.total,
                )
            else:
                messages.error(request, f"Sorry, {cart.product.title} is out of stock!")
                return redirect('cartlist')

            cart.delete()
            subject = 'Craft.io Order Confirmation'
            html_content = format_html(
                f"""
                <p>Hi <strong>{request.user.username}</strong>,</p>
                <p>Your order has been successfully placed.</p>
                <p>
                    <strong>Product:</strong> {cart.product.title} <br>
                    <strong>Quantity:</strong> {cart.quantity} <br>
                    <strong>Total Price:</strong> ₹{cart.total}
                </p>
                <p>Thank you for shopping with us!</p>
                """
            )
            email = EmailMultiAlternatives(subject, '', to=[request.user.email])
            email.attach_alternative(html_content, "text/html")
            email.send()

        messages.success(request, 'Your order has been successfully placed! Thank you for shopping with us!')
        return redirect('orderlist')

    except Exception as e:
        return redirect('cartlist')


@method_decorator(decorator=decorators, name='dispatch')
class OrderListView(ListView):
    template_name = 'orderlist.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Orders.objects.filter(user=self.request.user)

@signin_required
def CancelOrder(request, **kwargs):
    try:
        oid = kwargs.get('id')
        if not oid:
            return redirect('orderlist')

        order = get_object_or_404(Orders, id=oid)

        if order.status == 'Delivered':
            messages.error(request, "Delivered orders cannot be canceled.")
            return redirect('orderlist')
        product = order.product
        product.stock += order.quantity
        product.save()

        order.delete()

        messages.success(request, 'Your order has been canceled.')
        return redirect('orderlist')

    except Exception as e:
        return redirect('orderlist')




def searchproduct(request):
    keyword = request.POST.get('searchkey', '')
    cat = request.session.get('category', '')
    if keyword:
        products = Productss.objects.filter(title__icontains=keyword, category=cat)
        return render(request, 'productlist.html', {'products': products})
    else:
        return redirect('products', cat=cat)
    
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        full_message = f"Message from {name} ({email}):\n\n{message}"

        try:
            send_mail(
                subject,
                full_message,
                'tcsahla@gmail.com',
                [request.user.email],
            )
            messages.success(request, 'Your message has been sent successfully!')
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")

        return redirect('contact')

    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')



@signin_required
def add_delivery_address(request):
    if request.method == 'POST':
        form = DeliveryAddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('placeorder') 
    else:
        form = DeliveryAddressForm()

    return render(request, 'delivery_address_form.html', {'form': form})

