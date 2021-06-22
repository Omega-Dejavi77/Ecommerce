from django.http.response import Http404
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, render

from .models import Product

class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = "products/list.html"

    def get_queryset(self, *args, **kwargs):
        return Product.objects.all();

class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    template_name = "products/detail.html"

    def get_queryset(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        return Product.objects.filter(pk);


class ProductFeaturedListView(ListView):
    template_name = "products/list.html"

    def get_queryset(self, *args, **kwargs):
        return Product.objects.all().featured()


class ProductFeaturedDetailView(ListView):
    queryset = Product.objects.all.featured()
    template_name = "products/featured-detail.html"


def product_list_view(request):
    context = {
        'object_list': Product.objects.all()
    }
    return render(request, "product/list.html", context)


# This function is equivalent to ProductDetailView class.
# The class handle with internally get_context_data:
#   - a context that already exists
#   - a default html that can be overriden (temaple_name)
#   - the search of a object based on the pk
#   - ...
def product_detail_view(request, pk=None, *args, **kwargs):
    qs = Product.objects.filter(id=pk)
    if qs.exists() and qs.count() == 1:
        instance = qs.first()
    else:
        raise Http404("Product does not exist")
    context = {
        'object': instance
    }
    return render(request, "products/detail.html", context)