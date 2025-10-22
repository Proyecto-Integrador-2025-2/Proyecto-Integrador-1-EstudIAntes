from django.db import models
from django.utils.text import slugify

class TimeStamped(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class Tag(models.Model):
    name = models.CharField(max_length=40, unique=True)
    def __str__(self): return self.name

class Challenge(TimeStamped):
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    summary = models.TextField()
    body = models.TextField()
    is_published = models.BooleanField(default=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:140]
        super().save(*args, **kwargs)

    def __str__(self): return self.title

    class Meta:
        indexes = [
            models.Index(fields=["is_published", "-created_at"]),
        ]

class Story(TimeStamped):
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    teaser = models.TextField(help_text="Resumen corto o primeros párrafos")
    body = models.TextField()
    is_published = models.BooleanField(default=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:140]
        super().save(*args, **kwargs)

    def __str__(self): return self.title

    class Meta:
        indexes = [
            models.Index(fields=["is_published", "-created_at"]),
        ]
