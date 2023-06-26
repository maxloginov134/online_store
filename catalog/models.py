from django.db import models
from transliterate import translit

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):

    title = models.CharField(max_length=150, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('id',)


class Product(models.Model):

    title = models.CharField(max_length=200, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='media/images/', verbose_name='Превью', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.FloatField(verbose_name='Цена')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    last_change_date = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')

    def __str__(self):
        return f"Наименование товара:{self.title}. " \
               f"Категория: {self.category}. " \
               f"Цена:{self.price}. " \
               f"Дата создания: {self.create_date}"

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('id',)


class Contact(models.Model):
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField()
    site = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return f'{self.phone} | {self.email}'

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'


class Post(models.Model):
    title = models.CharField(max_length=20, verbose_name='Заголовок')
    slug = models.CharField(max_length=30, verbose_name='Слаг')
    content = models.TextField(verbose_name='Контент')
    preview = models.ImageField(upload_to='media/image/', verbose_name='Изображение', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')
    count_views = models.IntegerField(default=0, verbose_name='Количество просмотров')

    def save(self, *args, **kwargs):
        self.slug = translit(self.title, language_code='ru', reversed=True)
        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        self.is_published = False
        self.save()

    def __str__(self):
        return f'{self.title} | {self.content[:30]}'

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class Version(models.Model):
    product = models.ForeignKey(Product, related_name='versions', on_delete=models.CASCADE, max_length=200, verbose_name='Продукт')
    number_version = models.FloatField(verbose_name='Номер версии')
    name_version = models.CharField(max_length=200, verbose_name='Название версии')
    is_active = models.BooleanField(default=False, verbose_name='Активная')

    def save(self, *args, **kwargs):
        versions = Version.objects.filter(product_id=self.product.id)
        for version in versions:
            if version.is_active == True:
                raise ValueError('У продукта уже есть активная версия')
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.product.title} {self.name_version}'

    class Meta:
        verbose_name = 'Версия'
        verbose_name_plural = 'Версия'

