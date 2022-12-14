from django import forms
from store.models import Product,Variation,MultipleImages 
from users.models import Banner,BrandAd


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['product_name', 'description', 'price', 'images',
                   'category', 'stock', 'is_available']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

        self.fields['is_available'].widget.attrs['class'] = 'ml-2 mt-1 form-check-input'


class VariationForm(forms.ModelForm):

    class Meta:
        model = Variation
        fields = ['product', 'variation_category',
                  'variation_value', 'is_active']

    def __init__(self, *args, **kwargs):
        super(VariationForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

        self.fields['is_active'].widget.attrs['class'] = 'ml-2 mt-1 form-check-input'


class BannerForm(forms.ModelForm):

    class Meta:
        model = Banner
        fields = ['img', 'alt_text','caption','brandslogan','Brandname']

    def __init__(self, *args, **kwargs):
        super(BannerForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class BrandAdForm(forms.ModelForm):

    class Meta:
        model = BrandAd
        fields = ['img', 'alt_text','caption','Brandname']

    def __init__(self, *args, **kwargs):
        super(BrandAdForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class MultipleImagesForm (forms.ModelForm):

    class Meta:
        model = MultipleImages
        fields = ['image','product']

    def __init__(self, *args, **kwargs):
        super(MultipleImagesForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


