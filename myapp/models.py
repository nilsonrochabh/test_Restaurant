from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone

# Tabela de restaurantes
class Restaurant(models.Model):
    name = models.CharField('Nome', max_length=100)
    description = models.TextField('Descrição')
    address = models.CharField('Endereço', max_length=200)
    phone = models.CharField('Telefone', max_length=20)
    opening_time = models.TimeField('Horário de Abertura')
    closing_time = models.TimeField('Horário de Fechamento')
    image = models.ImageField('Imagem', upload_to='restaurants/', null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Proprietário')
    created_at = models.DateTimeField('Criado em', default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '1 - Restaurante'
        verbose_name_plural = '1 - Restaurantes'
        ordering = ['name']

# Tabela de mesas (vinculada a restaurantes)
class Table(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, verbose_name='Restaurante')
    number = models.IntegerField('Número da Mesa')
    capacity = models.IntegerField('Capacidade', validators=[MinValueValidator(1)])

    class Meta:
        verbose_name = '2 - Mesa'
        verbose_name_plural = '2 - Mesas'
        unique_together = ['restaurant', 'number']

    def __str__(self):
        return f'Mesa {self.number} - {self.restaurant.name}'


class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    ordem = models.IntegerField(default=0)  # Para ordenar no menu
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['ordem', 'nome']
    
    def __str__(self):
        return self.nome

class Produto(models.Model):
    UNIDADE_CHOICES = [
        ('UN', 'Unidade'),
        ('KG', 'Quilograma'),
        ('LT', 'Litro'),
        ('CX', 'Caixa'),
        ('PC', 'Pacote'),
        ('SC', 'Saco'),
    ]
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, verbose_name='Restaurante')
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    unidade_medida = models.CharField(max_length=2, choices=UNIDADE_CHOICES)
    quantidade_estoque = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    quantidade_minima = models.DecimalField(max_digits=10, decimal_places=3, default=1)
    preco_custo = models.DecimalField(max_digits=10, decimal_places=2)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2)
    codigo_barras = models.CharField(max_length=50, blank=True, unique=True)
    ativo = models.BooleanField(default=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['categoria', 'nome']
    
    def __str__(self):
        return f"{self.nome} ({self.categoria})"
    
    @property
    def situacao_estoque(self):
        """Verifica se estoque está baixo"""
        if self.quantidade_estoque <= 0:
            return 'ESGOTADO'
        elif self.quantidade_estoque <= self.quantidade_minima:
            return 'BAIXO'
        return 'NORMAL'
    
    @property
    def margem_lucro(self):
        """Calcula margem de lucro"""
        if self.preco_custo > 0:
            return round(((self.preco_venda - self.preco_custo) / self.preco_custo) * 100, 2)
        return 0

class MovimentacaoEstoque(models.Model):
    TIPO_CHOICES = [
        ('E', 'Entrada'),
        ('S', 'Saída'),
    ]
    
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    quantidade = models.DecimalField(max_digits=10, decimal_places=3)
    observacao = models.TextField(blank=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    data_movimentacao = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Movimentação de Estoque'
        verbose_name_plural = 'Movimentações de Estoque'
        ordering = ['-data_movimentacao']
# Cardápio e Itens do Cardápio (vinculado a restaurantes)
class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('entrada', 'Entrada'),
        ('prato_principal', 'Prato Principal'),
        ('sobremesa', 'Sobremesa'),
        ('bebida', 'Bebida'),
    ]

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, verbose_name='Restaurante')
    name = models.CharField('Nome', max_length=100)
    description = models.TextField('Descrição')
    price = models.DecimalField('Preço', max_digits=10, decimal_places=2)
    category = models.CharField('Categoria', max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField('Imagem', upload_to='menu_items/', null=True, blank=True)
    available = models.BooleanField('Disponível', default=True)

    def __str__(self):
        return f'{self.name} - {self.restaurant.name}'

    class Meta:
        verbose_name = '3 - Item do Cardápio'
        verbose_name_plural = '3 - Itens do Cardápio'
        ordering = ['category', 'name']

# Tabela de reservas (vinculada a usuários, restaurantes e mesas)
class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
        ('concluida', 'Concluída'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Cliente')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, verbose_name='Restaurante')
    table = models.ForeignKey(Table, on_delete=models.CASCADE, verbose_name='Mesa')
    date = models.DateField('Data')
    time = models.TimeField('Horário')
    guests = models.IntegerField('Número de Pessoas', validators=[MinValueValidator(1)])
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='pendente')
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    notes = models.TextField('Observações', blank=True, null=True)

    def __str__(self):
        return f'Reserva de {self.user.get_full_name()} - {self.restaurant.name}'

    class Meta:
        verbose_name = '4 - Reserva'
        verbose_name_plural = '4 - Reservas'
        ordering = ['-date', '-time']

# Tabela de pedidos (vinculada a usuários, restaurantes, reservas e itens do cardápio)
class Order(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('preparando', 'Preparando'),
        ('pronto', 'Pronto'),
        ('entregue', 'Entregue'),
        ('cancelado', 'Cancelado'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Cliente')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, verbose_name='Restaurante')
    reservation = models.ForeignKey(Reservation, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Reserva')
    items = models.ManyToManyField(MenuItem, through='OrderItem', verbose_name='Itens')
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='pendente')
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    total = models.DecimalField('Total', max_digits=10, decimal_places=2, default=0)
    notes = models.TextField('Observações', blank=True, null=True)

    def __str__(self):
        return f'Pedido #{self.id} - {self.user.get_full_name()}'

    class Meta:
        verbose_name = '5 - Pedido'
        verbose_name_plural = '5 - Pedidos' 
        ordering = ['-created_at']


# Tabela intermediária para itens do pedido
# Permite armazenar quantidade e preço no momento do pedido (para histórico e pagamento)
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Pedido')
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, verbose_name='Item')
    quantity = models.IntegerField('Quantidade', validators=[MinValueValidator(1)])
    price = models.DecimalField('Preço', max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        # Sempre atualiza o preço baseado no item e quantidade
        if self.item:
            self.price = self.item.price * self.quantity
        
        # Salva o item
        super().save(*args, **kwargs)
        
        # Atualiza o total do pedido
        if self.order:
            total = sum(item.price for item in self.order.orderitem_set.all())
            self.order.total = total
            self.order.save()

    def __str__(self):
        return f'{self.quantity}x {self.item.name}'

    class Meta:
        verbose_name = 'Item do Pedido'
        verbose_name_plural = 'Itens do Pedido'
        ordering = ['order']