from django import forms

from catalog.models import Post, Product, Version

INCORRECT_WORDS = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UpdateProductForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Product
        fields = ('title', 'description', 'image', 'category', 'price')

    def clean_title(self):
        cleaned_data = self.cleaned_data['title']
        if cleaned_data in INCORRECT_WORDS:
            raise forms.ValidationError('Некорректное название товара')
        return cleaned_data


class CreateProductForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Product
        fields = ('title', 'description', 'image', 'category', 'price')

    def clean_title(self):
        cleaned_data = self.cleaned_data['title']
        if cleaned_data in INCORRECT_WORDS:
            raise forms.ValidationError('Некорректное название')
        return cleaned_data


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'preview', 'is_published')


class VersionForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = ('name_version', 'number_version', 'is_active')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['is_active'].widget.attrs['class'] = 'form-choice'