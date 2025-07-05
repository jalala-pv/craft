from account.models import Cart,Wishlist,Orders

def item_count(request):
    if request.user.is_authenticated:
        cart_count=Cart.objects.filter(user=request.user).count()
        wishlist_count=Wishlist.objects.filter(user=request.user).count()
        order_count=Orders.objects.filter(user=request.user).count()
        return {'cart':cart_count,'wishlist':wishlist_count,'order':order_count}
    else:
        return {"cart":0,'wishlist':0,"order":0}
    

