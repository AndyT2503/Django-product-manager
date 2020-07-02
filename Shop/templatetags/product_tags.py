from django import template 
from ..models import Product, Brand

register = template.Library() 

@register.simple_tag
def total_posts():
    return Product.objects.count()


@register.inclusion_tag('Shop/show_brands.html')
def show_brands():
    brand_list = Brand.objects.all()
    return {'brand_list': brand_list}
