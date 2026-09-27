from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    biography = models.TextField(blank=True)
    date_of_birth = models.DateField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        indexes = [
            models.Index(fields=['last_name', 'first_name']),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Publisher(models.Model):
    name = models.CharField(max_length=200, unique=True)
    address = models.TextField(blank=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'

    def __str__(self):
        return self.name


class Book(models.Model):

    GENRE_CHOICES = [
        ('FIC', 'Fiction'),
        ('NF', 'Non-Fiction'),
        ('SCI', 'Science'),
        ('TECH', 'Technology'),
        ('HIST', 'History'),
        ('BIO', 'Biography'),
        ('MYS', 'Mystery'),
        ('ROM', 'Romance'),
        ('FAN', 'Fantasy'),
        ('OTH', 'Other'),
    ]

    title = models.CharField(max_length=200)

    isbn = models.CharField(
        max_length=13,
        unique=True
    )

    authors = models.ManyToManyField(
        Author,
        through='BookAuthor',
        related_name='books'
    )

    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='books'
    )

    genres = models.ManyToManyField(
        Genre,
        related_name='books',
        blank=True
    )

    genre = models.CharField(
        max_length=10,
        choices=GENRE_CHOICES,
        default='OTH'
    )

    publication_date = models.DateField()

    pages = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    summary = models.TextField(blank=True)

    is_available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['isbn']),
            models.Index(fields=['publication_date']),
        ]

    def __str__(self):
        return self.title

    def is_recent(self):
        if not self.publication_date:
            return False

        current_year = timezone.now().year
        return self.publication_date.year >= current_year - 5

    @property
    def author_names(self):
        return ", ".join(
            author.full_name for author in self.authors.all()
        )


class BookAuthor(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='book_authors'
    )

    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='book_authors'
    )

    role = models.CharField(
        max_length=50,
        default='Author'
    )

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        constraints = [
            models.UniqueConstraint(
                fields=['book', 'author'],
                name='unique_book_author'
            )
        ]

    def __str__(self):
        return f"{self.author} - {self.book}"


class BookCopy(models.Model):
    STATUS_CHOICES = [
        ('AVAILABLE', 'Available'),
        ('BORROWED', 'Borrowed'),
        ('LOST', 'Lost'),
        ('DAMAGED', 'Damaged'),
        ('RESERVED', 'Reserved'),
    ]

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='copies'
    )

    copy_number = models.PositiveIntegerField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='AVAILABLE'
    )

    acquisition_date = models.DateField(
        default=timezone.now
    )

    condition = models.CharField(
        max_length=100,
        default='Good'
    )

    class Meta:
        ordering = ['book', 'copy_number']
        constraints = [
            models.UniqueConstraint(
                fields=['book', 'copy_number'],
                name='unique_book_copy'
            )
        ]

    def __str__(self):
        return f"{self.book.title} - Copy {self.copy_number}"

    @property
    def is_available(self):
        return self.status == 'AVAILABLE'


class Review(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    reviewer_name = models.CharField(max_length=100)

    rating = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )

    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['book', '-created_at']),
        ]

    def __str__(self):
        return f"{self.book.title} - {self.rating}/5"