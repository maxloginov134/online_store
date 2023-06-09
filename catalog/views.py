from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from catalog.service import send_email
from django.urls import reverse_lazy

from catalog.models import Product, Post, Contact
from catalog.forms import PostForm


class ProductList(ListView):
    model = Product
    extra_context = {
        'title': 'СберМаркетFast',
        'description': 'Как СберМаркет только быстрее, лучше и звонят сами когда заказ опаздывает на 3 дня.',
    }


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
