from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from .models import Produto, Restaurant


class ProdutoForm(forms.ModelForm):
    
    class Meta:
        model = Produto
        fields = ['restaurant', 'nome', 'descricao', 'categoria', 'unidade_medida', 
                  'quantidade_estoque', 'quantidade_minima', 
                  'preco_custo', 'preco_venda', 'codigo_barras', 'ativo']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
            'quantidade_estoque': forms.NumberInput(attrs={'step': '0.001'}),
            'quantidade_minima': forms.NumberInput(attrs={'step': '0.001'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            # Filtra apenas restaurants do usuário
            self.fields['restaurant'].queryset = Restaurant.objects.filter(
                proprietario=user
            )
            
            # Se tiver apenas um restaurante, seleciona automaticamente
            restaurantes = Restaurant.objects.filter(proprietario=user)
            if restaurantes.count() == 1:
                self.fields['restaurant'].initial = restaurantes.first()
                self.fields['restaurant'].widget.attrs['readonly'] = True
    def __init__(self, *args, **kwargs):
        # Recebe o restaurante do usuário via kwargs
        self.restaurant = kwargs.pop('restaurant', None)
        super().__init__(*args, **kwargs)
        
        if self.restaurant:
            # Define o valor inicial do campo oculto
            self.fields['restaurant'].initial = self.restaurant
    
    
class UserRegistrationForm(UserCreationForm):   
    email = forms.EmailField(required=False, label="Endereço de Email")
    phone_number = forms.CharField(required=False, label="Número de Telefone")
    first_name = forms.CharField(required=True, label="Primeiro Nome")
    last_name = forms.CharField(required=True, label="Sobrenome")

    
    class Meta:
        model = User
        fields = ('username',  'phone_number', 'first_name', 'last_name', 'email', 'password1','password2')
        labels = {
            'username': 'Nome de Usuário',
            'password1': 'Senha',
            'password2': 'Confirme a Senha',
        }
        
        
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None


        self.helper = FormHelper()
        self.helper.form_method = 'post' 
        self.helper.enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='col-md-6'),
                Column('email', css_class='col-md-6'),
            ),
            Row(
                Column('first_name', css_class='col-md-6'),
                Column('last_name', css_class='col-md-6'),
            ), 
            Row(
                Column('password1', css_class='col-md-6'),
                Column('password2', css_class='col-md-6'),
            ),
            Row(
                Column('phone_number', css_class='col-md-6'),
            ),
            Submit('submit', 'Registrar', css_class='btn btn-primary w-100'),
        ) 