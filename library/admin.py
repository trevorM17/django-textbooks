
from django.contrib import admin
from .models import (
    Author, Publisher, Genre, Book, BookAuthor,
    BookCopy, Review, UserProfile, Comment,
    Librarian, AvailableBook, UserPreferences
)


class BookAuthorInline(admin.TabularInline):
    model = BookAuthor
    extra = 1


class BookCopyInline(admin.TabularInline):
    model = BookCopy
    extra = 0


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'email', 'birth_date')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('last_name', 'first_name')
    inlines = [BookAuthorInline]


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'country', 'established')
    search_fields = ('name', 'city', 'country')
    list_filter = ('country',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)
    list_filter = ('parent',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'author_list', 'publisher', 'genre',
        'publication_date', 'is_available', 'rating'
    )
    list_filter = ('genre', 'is_available', 'publication_date', 'rating')
    search_fields = (
        'title', 'subtitle', 'isbn',
        'authors__first_name', 'authors__last_name'
    )
    ordering = ('title',)
    date_hierarchy = 'publication_date'
    readonly_fields = ('created_at', 'updated_at', 'age')
    inlines = [BookAuthorInline, BookCopyInline]
    autocomplete_fields = ['publisher', 'genre']

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'subtitle', 'isbn', 'publisher', 'genre')
        }),
        ('Publication', {
            'fields': (
                'publication_date', 'pages',
                'language', 'summary', 'cover_image'
            )
        }),
        ('Library Status', {
            'fields': ('is_available', 'borrowed_count', 'rating')
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at', 'age'),
        }),
    )

    actions = ['mark_available', 'mark_unavailable']

    @admin.display(description='Authors')
    def author_list(self, obj):
        return ', '.join(str(a) for a in obj.authors.all())

    @admin.action(description='Mark selected books as available')
    def mark_available(self, request, queryset):
        count = queryset.update(is_available=True)
        self.message_user(request, f'{count} book(s) marked available.')

    @admin.action(description='Mark selected books as unavailable')
    def mark_unavailable(self, request, queryset):
        count = queryset.update(is_available=False)
        self.message_user(request, f'{count} book(s) marked unavailable.')


@admin.register(BookAuthor)
class BookAuthorAdmin(admin.ModelAdmin):
    list_display = ('book', 'author', 'contribution_type', 'contribution_order')
    list_filter = ('contribution_type',)
    search_fields = ('book__title', 'author__first_name', 'author__last_name')


@admin.register(BookCopy)
class BookCopyAdmin(admin.ModelAdmin):
    list_display = (
        'book', 'copy_number', 'condition',
        'is_borrowed', 'borrowed_by', 'due_date'
    )
    list_filter = ('condition', 'is_borrowed')
    search_fields = ('book__title', 'borrowed_by__username')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('book__title', 'user__username')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'birth_date')
    search_fields = ('user__username', 'user__email', 'location')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'content_type', 'object_id', 'created_at')
    list_filter = ('content_type',)


@admin.register(Librarian)
class LibrarianAdmin(admin.ModelAdmin):
    list_display = ('employee_number', 'first_name', 'last_name', 'department')
    search_fields = ('employee_number', 'first_name', 'last_name')


@admin.register(AvailableBook)
class AvailableBookAdmin(admin.ModelAdmin):
    list_display = ('title', 'rating', 'is_available', 'publication_date')
    list_filter = ('is_available', 'rating')


@admin.register(UserPreferences)
class UserPreferencesAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')
    search_fields = ('user__username',)
# Register your models here.
