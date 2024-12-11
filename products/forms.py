"""Forms for Products App."""

from django import forms

from products.models import Category, Brand, Deal, CategoryTree, Publication, Comment, BookAuthor
from utils.tailwind_classes import form_select, form_number


class CategoriesForm(forms.Form):
    """Base form for categories filter."""

    def __init__(self, *args , descendant_categories = None ,  **kwargs):
        super().__init__(*args, **kwargs)

        # print("form descendant categories", descendant_categories)
        if descendant_categories:
            self.fields['category'].queryset = descendant_categories
        # else:
        #     self.fields['category'].queryset = descendant_categories

    category = forms.ModelChoiceField(
        queryset=CategoryTree.objects.all(),
        required=False,
        empty_label="All Categories",
        widget=forms.Select(attrs=form_select()),
    )
    brand = forms.ModelChoiceField(
        queryset=Brand.objects.all(),
        required=False,
        empty_label="All Brands",
        widget=forms.Select(attrs=form_select()),
    )
    publications = forms.ModelChoiceField(
        queryset=Publication.objects.all(),
        required=False,
        empty_label="All Publications",
        widget=forms.Select(attrs=form_select()),
    )
    deal = forms.ModelChoiceField(
        queryset=Deal.objects.all(),
        required=False,
        empty_label="All Deals",
        widget=forms.Select(attrs=form_select()),
    )
    authors = forms.ModelChoiceField(
        queryset=BookAuthor.objects.all(),
        required=False,
        empty_label="All Authors",
        widget=forms.Select(attrs=form_select()),
    )
    min_price = forms.DecimalField(
        required=False,
        min_value=1,
        max_value=10000,
        widget=forms.NumberInput(attrs=form_number("Min Price")),
    )
    max_price = forms.DecimalField(
        required=False,
        min_value=1,
        max_value=10000,
        widget=forms.NumberInput(attrs=form_number("Max Price")),
    )



class FiltersForm(forms.Form):
    """Base form for categories filter."""

    category = forms.ModelChoiceField(
        queryset=CategoryTree.objects.all(),
        required=False,
        empty_label="All Categories",
        widget=forms.Select(attrs=form_select()),
    )
    brand = forms.ModelChoiceField(
        queryset=Brand.objects.all(),
        required=False,
        empty_label="All Brands",
        widget=forms.Select(attrs=form_select()),
    )
    deal = forms.ModelChoiceField(
        queryset=Deal.objects.all(),
        required=False,
        empty_label="All Deals",
        widget=forms.Select(attrs=form_select()),
    )
    authors = forms.ModelChoiceField(
        queryset=BookAuthor.objects.all(),
        required=False,
        empty_label="All Authors",
        widget=forms.Select(attrs=form_select()),
    )
    min_price = forms.DecimalField(
        required=False,
        min_value=1,
        max_value=10000,
        widget=forms.NumberInput(attrs=form_number("Min Price")),
    )
    max_price = forms.DecimalField(
        required=False,
        min_value=1,
        max_value=10000,
        widget=forms.NumberInput(attrs=form_number("Max Price")),
    )




class ReviewForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['rate', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'placeholder': 'Write your review here...', 'rows': 4}),
            'rate': forms.HiddenInput()  # We will handle this with JavaScript
        }
