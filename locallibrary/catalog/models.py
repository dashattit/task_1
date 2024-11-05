from django.db import models
from django.urls import reverse

# Create your models here.
# определение модели
class MyModelName(models.Model):
    """Типичный класс модели, производный от класса Model."""

    # Поля
    my_field_name = models.CharField(max_length=20, help_text='Введите описание поля')
    # …

    # Метаданные
    class Meta:
        ordering = ['-my_field_name']

    # Methods
    def get_absolute_url(self):
        """Возвращает URL-адрес для доступа к определенному экземпляру MyModelName."""
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        """Строка для представления объекта MyModelName (например, в административной панели и т.д.)."""
        return self.my_field_name


# модель жанра
class Genre(models.Model):
    # Модель, представляющая книжный жанр (например, научную фантастику, нон-фикшн).
    name = models.CharField(max_length=200, help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)")

    def __str__(self):
        # Строка для представления объекта модели (на сайте администратора и т.д.)
        return self.name


# модель книги
class Book(models.Model):

    # Модель, представляющая книгу (но не конкретную копию книги).
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    # Внешний ключ используется потому, что у книги может быть только один автор, но у авторов может быть несколько книг
    #  Author в виде строки, а не объекта, поскольку он еще не был объявлен в файле.
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField('ISBN',max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
    # Поле ManyToManyField используется потому, что жанр может содержать много книг. Книги могут охватывать множество жанров.
    # Класс жанра уже определен, поэтому мы можем указать объект, указанный выше.

    def __str__(self):
        # Строка для представления модельного объекта.
        return self.title


    def get_absolute_url(self):
        # Возвращает URL-адрес для доступа к определенному экземпляру книги.
        return reverse('book-detail', args=[str(self.id)])


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