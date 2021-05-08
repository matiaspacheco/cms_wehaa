from django.db import models

# Wehaa Portal 
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone

from taggit.managers import TaggableManager
from tinymce.models import HTMLField

from core.utils import count_words, read_time

class Category(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    slug = models.SlugField()
    description = HTMLField('Content')
    #description = models.TextField(max_length=240, default="")
    image = models.FileField(default='category-default.jpg',
                              upload_to='category_images')
    approved = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('name',)
        verbose_name = "Categoría"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('articles:category_detail', kwargs={'category_name': self.slug})

class Article(models.Model):

    # Article status constants
    DRAFTED = "DRAFTED"
    PUBLISHED = "PUBLISHED"

    # CHOICES
    STATUS_CHOICES = (
        (DRAFTED, 'Draft'),
        (PUBLISHED, 'Publish'),
    )
    COMMENT_STATUS = (
        ('o', 'Abierto'),
        ('c', 'Cerrado'),
    )

    # BLOG MODEL FIELDS
    id = models.AutoField(primary_key=True)

    title = models.CharField(max_length=250, null=False, blank=False)
    slug = models.SlugField()
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='articles')

    image = models.FileField(default='article-default.jpg',
                              upload_to='article_images')
    image_credit = models.CharField(max_length=250, null=True, blank=True)
    body = HTMLField('Content')

    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='articles')
    tags = TaggableManager()
    comment_status = models.CharField(max_length=1, choices=COMMENT_STATUS, default='o')

    # Destacado
    featured = models.BooleanField()
    article_order = models.IntegerField('Orden', blank=False, null=False, default=0)

    date_published = models.DateTimeField(null=True, blank=True,
                                          default=timezone.now)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,
                              default='DRAFT')
    views = models.PositiveIntegerField(default=0)
    count_words = models.CharField(max_length=50, default=0)
    read_time = models.CharField(max_length=50, default=0)
    deleted = models.BooleanField(default=False)

    class Meta:
        unique_together = ("title",)
        ordering = ('-date_published',)
        verbose_name = "Artículo"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        self.count_words = count_words(self.body)
        self.read_time = read_time(self.body)
        super(Article, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('articles:article_detail', kwargs={'username': self.author.username.lower(), 'slug': self.slug})