from django import forms
from .models import Creation, Author

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit


class CreationFormView(forms.ModelForm):
    created_date = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date'}
        ), label='Бичигдсэн огноо'
    )

    class Meta:
        model = Creation
        fields = '__all__'

    new_author = forms.CharField(max_length=30, required=False, label="Шинэ зохиолч")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['author'].required = False

        self.helper = FormHelper()
        self.helper.layout = Layout(
            ButtonHolder(
                'new_author',
                'author', 'title', 'co_authors', 'type',
                'category', 'subclass', 'overview', 'keyword',
                'created_date', 'language', 'file', 'price', 'num_of_page',
                Submit('create', 'Үүсгэх')
            )
        )

    def clean(self):
        author = self.cleaned_data.get('author')
        new_author = self.cleaned_data.get('new_author')

        if not author and not new_author:
            raise forms.ValidationError('Зохиолч сонгох эсвэл шинээр үүсгэнэ үү!')
        elif not author:
            author, created = Author.objects.get_or_create(last_name=new_author)
            self.cleaned_data['author'] = author

            return super(CreationFormView, self).clean()


class ReportForm(forms.Form):
    year_choices = (
        ('Бүгд', 'Бүгд'),
        ('2018', '2018'),
        ('2017', '2017'),
        ('2016', '2016')
    )

    month_choices = (
        ('Бүгд', 'Бүгд'),
        (12, '12 сар'), (11, '11 сар'),
        (10, '10 сар'), (9, '9 сар'),
        (8, '8 сар'), (7, '7 сар'),
        (6, '6 сар'), (5, '5 сар'),
        (4, '4 сар'), (3, '3 сар'),
        (2, '2 сар'), (1, '1 сар'),
    )

    year = forms.ChoiceField(label='Он сонгоно уу', choices=year_choices)
    month = forms.ChoiceField(label='Сар сонгоно уу', choices=month_choices)

    def __init__(self, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'year', 'month',
            ButtonHolder(
                Submit('download', 'Татах')
            )
        )
