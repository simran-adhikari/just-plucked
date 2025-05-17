from django.views.generic import ListView, DetailView
from .models import Farmer
from products.models import Product

class FarmerListView(ListView):
    model = Farmer
    template_name = 'website/farmer/farmer_list.html'
    context_object_name = 'farmers'
    paginate_by = 16  # default, can override with GET

    def get_queryset(self):
        queryset = super().get_queryset()
        per_page = self.request.GET.get('per_page')
        if per_page == 'all':
            self.paginate_by = None
        elif per_page and per_page.isdigit():
            self.paginate_by = int(per_page)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['per_page_options'] = [5, 8, 13, 16]
        return context

# View to display Farmer Details along with Products
class FarmerDetailView(DetailView):
    model = Farmer
    template_name = 'website/farmer/farmer_detail.html'
    context_object_name = 'farmer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        farmer = self.get_object()
        context['products'] = Product.objects.filter(farmer=farmer)
        return context
