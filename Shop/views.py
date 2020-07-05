from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.db.models import Q
from .models import Brand, Product
from django.contrib import messages
from .forms import ProductForm, LoginForm
from django.contrib.auth import login
from django.views.generic import View
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib.auth.decorators import login_required
import requests

# Create your views here.

@login_required
def home(request):
    latest_products_list = Product.objects.all().order_by('-created_at')
    first_product = latest_products_list[0]
    second_product = latest_products_list[1]
    paginator = Paginator(latest_products_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    template = loader.get_template('Shop/home.html')
    context = {
        'page_obj': page_obj,
        'first_product': first_product,
        'second_product': second_product,
    }
    return HttpResponse(template.render(context, request))


@login_required
def product_detail(request, id):
    template = 'Shop/product_detail.html'
    try:
        product = Product.objects.get(id=id)
    except:

        return render(request, template)

    context = {
        'product': product,
    }

    return render(request, template, context)

@login_required
def brand_detail(request, name):
    product = Product.objects.filter(brand__Name=name)

    paginator = Paginator(product, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    template = 'Shop/brand_detail.html'

    return render(request, template, context)

@login_required
def search(request):
    if request.method == 'POST':
        srch = request.POST['search']

        if srch:
            match = Product.objects.filter(
                Q(title__icontains=srch)).order_by('-created_at')

            if match:
                return render(request, 'Shop/search.html', {'products_list': match})
            else:
                match = Product.objects.filter(
                    brand__Name=srch).order_by('-created_at')
                if match:
                    return render(request, 'Shop/search.html', {'products_list': match})
                else:
                    messages.error(request, 'no request found')
        else:
            return HttpResponseRedirect('/search')
    return render(request, 'Shop/search.html')

@login_required
def product_create_view(request):
    form = ProductForm()

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/home')
        else:
            return render(request, 'Shop/product_form.html', {'error': "Thông tin sản phẩm không hợp lệ", 'form': form, 
                            'title': "Đăng tải sản phẩm mới", "button": "Đăng sản phẩm"})
    return render(request, 'Shop/product_form.html', {'form': form, 'title': "Đăng tải sản phẩm mới", "button": "Đăng sản phẩm"})

@login_required
def product_update_view(request, pk):
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/home')
        else:
            return render(request, 'Shop/product_form.html', {'error': "Thông tin sản phẩm không hợp lệ", 'form': form, 
                            'title': "Cập nhật thông tin sản phẩm", "button": "Cập nhật"})
    return render(request, 'Shop/product_form.html', {'form': form, 'title': "Cập nhật thông tin sản phẩm", "button": "Cập nhật"})


def autocomplete(request):
    if 'term' in request.GET:
        products_list = Product.objects.filter(title__icontains=request.GET.get('term')).order_by("-created_at")
        brands_list = Brand.objects.filter(Name__icontains=request.GET.get('term'))
        res = list()
        if (brands_list):
            for brand in brands_list:
                p_list = Product.objects.filter(brand=brand).order_by("-created_at")
                for p in p_list:
                    res.append(p.title)
                res.append(brand.Name)
        else:
            for product in products_list:
                res.append(product.title)
        
        return JsonResponse(res, safe=False)    
    return HttpResponseRedirect('/')


class DeleteProduct(View):
    def get(self, request):
        id = request.GET.get('id', None)
        print(id)
        Product.objects.get(id=id).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/home")
    form = LoginForm(request.POST or None)
    error = ""
    if request.POST and form.is_valid():
        user = form.login(request)
        remember_me = form.cleaned_data['remember_me']
        print(remember_me)
        if user:
            ''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            ''' End reCAPTCHA validation '''
            if result['success']:
                login(request, user)
                if remember_me == False:
                    request.session.set_expiry(0)
                return HttpResponseRedirect("/home")
                        
    
    return render(request, 'registration/login.html', {'form': form, 'err': error })


