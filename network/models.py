from django.core.exceptions import ValidationError
from django.db import models

NULLABLE = {'null': True, 'blank': True}


def validate_provider_not_self(value):
    if isinstance(value, int):
        if value == NetworkElement.objects.get(pk=value).provider.pk:
            raise ValidationError('Поставщик не может поставлять товар сам себе.')
    elif isinstance(value, NetworkElement) and value.provider:
        if value.pk == value.provider.pk:
            raise ValidationError('Поставщик не может поставлять товар сам себе.')


# Create your models here.

class Contact(models.Model):
    """
    Model representing contact information.

    Fields:
    - email (EmailField): The email address.
    - country (CharField): The country.
    - city (CharField): The city.
    - street (CharField): The street.
    - building_num (PositiveSmallIntegerField): The building number.
    """
    email = models.EmailField(verbose_name='Почта', unique=True)
    country = models.CharField(max_length=100, verbose_name='Страна')
    city = models.CharField(max_length=100, verbose_name='Город')
    street = models.CharField(max_length=100, verbose_name='Улица')
    building_num = models.PositiveSmallIntegerField(verbose_name='Номер дома')


class Product(models.Model):
    """
    Model representing a product.

    Fields:
    - name (CharField): The name of the product.
    - model (CharField): The model of the product.
    - launch_date (DateField): The date when the product was launched on the market.
    """
    name = models.CharField(max_length=100, verbose_name='Название')
    model = models.CharField(max_length=100, verbose_name='Модель')
    launch_date = models.DateField(verbose_name='Дата выхода продукта на рынок')


class NetworkElement(models.Model):
    """
    Model representing a network element.

    Fields:
    - name (CharField): The name of the network element.
    - contacts (ForeignKey to Contact): Contact information of the network element.
    - products (ManyToManyField to Product): Products associated with the network element.
    - provider (ForeignKey to self): The provider network element (previous network object in hierarchy).
    - debt (DecimalField): Debt to the supplier in monetary terms accurate to penny.
    - created_at (DateTimeField): The timestamp when the network element was created (auto-generated).
    - level (CharField with choices): The level of the network element.
    """

    LEVEL = [
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
    ]

    name = models.CharField(max_length=100, verbose_name='Название')
    contacts = models.ForeignKey('Contact', on_delete=models.CASCADE, verbose_name='Контакт')
    products = models.ManyToManyField('Product', verbose_name='Продукты', **NULLABLE)
    provider = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='Поставщик',
                                 validators=[validate_provider_not_self], **NULLABLE)
    debt = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Задолженность')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    level = models.CharField(max_length=50, choices=LEVEL, **NULLABLE)
