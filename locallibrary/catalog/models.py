from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
import uuid # Требуется для уникальных экземпляров книг
from django.contrib.auth.models import User
from datetime import date

# определение модели
class MyModelName(models.Model):
    # Типичный класс модели, производный от класса Model

    # Поля
    my_field_name = models.CharField(max_length=20, help_text='Введите описание поля')
    # …

    # Метаданные
    class Meta:
        ordering = ['-my_field_name']

    # Методы
    def get_absolute_url(self):
        # Возвращает URL-адрес для доступа к определенному экземпляру MyModelName
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        """Строка для представления объекта MyModelName (например, в административной панели и т.д.)."""
        return self.my_field_name


# модель жанра
class Genre(models.Model):
    # Модель, представляющая книжный жанр
    name = models.CharField(max_length=200, help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)")

    def __str__(self):
        # Строка для представления объекта модели (на сайте администратора и т.д.)
        return self.name


# модель книги
class Book(models.Model):
    # Модель, представляющая книгу (но не конкретную копию книги)
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    # Внешний ключ используется потому, что у книги может быть только один автор, но у авторов может быть несколько книг
    # Author в виде строки, а не объекта, поскольку он еще не был объявлен в файле
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField('ISBN',max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField('Genre', help_text="Select a genre for this book")
    # Поле ManyToManyField используется потому, что жанр может содержать много книг. Книги могут охватывать множество жанров
    # Класс жанра уже определен, поэтому мы можем указать объект, указанный выше

    def __str__(self):
        # Строка для представления модельного объекта.
        return self.title

    def get_absolute_url(self):
        # Возвращает URL-адрес для доступа к определенному экземпляру книги.
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):

        # Создает строку для жанра. Это необходимо для отображения жанра в Admin.

        return ', '.join([genre.name for genre in self.genre.all()[:3]])
    display_genre.short_description = 'Genre'


# модель экземпляра книги
class BookInstance(models.Model):
    # Модель, представляющая конкретный экземпляр книги (т.е. ту, которую можно взять напрокат в библиотеке)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book availability')

    class Meta:
        ordering = ["due_back"]
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):

        # Строка для представления модельного объекта

        return f'Книга: {self.book.title}, Статус: {self.get_status_display()}, Дата возврата: {self.due_back}, ID: {self.id}'

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

# модель автора
class Author(models.Model):
    # Модель, представляющая автора.
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    def get_absolute_url(self):
        # Возвращает URL-адрес для доступа к конкретному экземпляру author
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        # Строка для представления модельного объекта
        return '%s, %s' % (self.last_name, self.first_name)

    def clean(self):
        # проверка на минимальный возраст 20 лет
        if self.date_of_birth:
            age = date.today().year - self.date_of_birth.year
            if (date.today().month, date.today().day) < (self.date_of_birth.month, self.date_of_birth.day):
                age -= 1
            if age < 20:
                raise ValidationError('Возраст автора должен быть не меньше 20 лет')

        # проверка на дату смерти
        if self.date_of_death and self.date_of_birth >= self.date_of_death:
                raise ValidationError('Дата смерти не может быть раньше даты рождения')



    class Meta:
        ordering = ['last_name']


