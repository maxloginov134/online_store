from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from catalog.service import send_email
from django.urls import reverse_lazy
from django.forms import inlineformset_factory
from django.http import HttpResponse, HttpResponseRedirect

from catalog.models import Product, Post, Contact, Version
from catalog.forms import PostForm, UpdateProductForm, CreateProductForm, VersionForm


class ProductList(ListView):
    model = Product
    extra_context = {
        'title': 'СберМаркетFast',
        'description': 'Как СберМаркет только быстрее, лучше и звонят сами когда заказ опаздывает на 3 дня.',
    }


class UpdateProduct(UpdateView):
    model = Product
    form_class = UpdateProductForm
    template_name = 'catalog/update_product.html'

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context['formset'] = VersionFormset(data=self.request.POST, instance=self.object)
        else:
            context['formset'] = VersionFormset(instance=self.object)
        return context

    def form_valid(self, form):
        form = CreateProductForm(data=self.request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = self.request.user
            product.save()
        return HttpResponseRedirect(reverse_lazy('catalog:home'))


class DetailProduct(DetailView):
    model = Product

    def get_object(self, queryset=None):
        object = Product.objects.get(pk=self.kwargs['pk'])
        return object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['version'] = Version.objects.filter(product_id=self.kwargs['pk'])
        for item in context['version']:
            if item.is_active == True:
                context['version'] = item
        return context


class DeleteProduct(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:home')


class ProductCreate(CreateView):
    model = Product
    form_class = CreateProductForm
    success_url = reverse_lazy('catalog:home')


class ContactList(ListView):
    model = Contact
    extra_context = {
        'title': 'Контакты'
    }


class PostList(ListView):
    model = Post
    extra_context = {
        'title': 'Список постов'
    }


class DetailPost(DetailView):
    model = Post

    def get_object(self, queryset=None):
        object = Post.objects.get(pk=self.kwargs['pk'])
        if object:
            object.count_views += 1
            object.save()
            if object.count_views == 100:
                send_email()
        return object


class PostCreate(CreateView):
    model = Post
    success_url = reverse_lazy('catalog:post_list')
    form_class = PostForm


class PostUpdate(UpdateView):
    model = Post
    template_name = 'catalog/update_post.html'
    form_class = PostForm

    def get_success_url(self):
        return reverse_lazy('catalog:post_detail', kwargs={'pk': self.kwargs['pk']})


class DeletePost(DeleteView):
    model = Post
    success_url = reverse_lazy('catalog:post_list')


def contacts(request):
    context = {
        'title': 'Напишите нам!',
        'description': 'Мы постараемся вам ответить как можно скорее и решим любой ваш вопрос!',
    }

    return render(request, 'catalog/contacts.html', context)
