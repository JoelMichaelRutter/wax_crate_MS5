"""
1 - Importing models (default)
2 - Importing slugify to slugify title on save when
adding records from web interface.
"""

from django.db import models
from django.utils.text import slugify


class Genre(models.Model):
    """
    This is the Genre model, to add a record to the store
    where the genre doesnt already exist, the admin will
    need to add the genre first prior to adding the record.
    """
    genre = models.CharField(max_length=254, unique=True)

    def __str__(self):
        return str(self.genre)


class Record(models.Model):
    """
    This is the record model, it sets the db table according to
    the data required to show a new record in the store.
    """
    CONDITION_CHOICES = (
        ('M', 'mint'),
        ('NM', 'near_mint'),
        ('VG', 'very_good'),
        ('G', 'good'),
        ('F', 'fair'),
        ('P', 'poor'),
    )
    genre = models.ForeignKey(
        'Genre', null=True, blank=False, on_delete=models.SET_NULL
        )
    image = models.ImageField(null=True, blank=True)
    title = models.CharField(
        max_length=254, null=False, unique=True, blank=False
    )
    slug = models.SlugField(
        max_length=254, null=False, unique=True, blank=False
    )
    artist = models.CharField(max_length=254, null=False, blank=False)
    record_label = models.CharField(max_length=254, null=False, blank=False)
    release_year = models.CharField(max_length=4, null=False, blank=False)
    hot_pick = models.BooleanField(default=False)
    condition = models.CharField(
        max_length=9, choices=CONDITION_CHOICES,
        default='mint', blank=False, null=False
    )
    price = models.DecimalField(max_digits=6, decimal_places=2)
    tracklist = models.TextField()
    description = models.TextField()
    has_link = models.BooleanField(default=False)
    link_to_music = models.URLField(max_length=1024, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super(Record, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.title)
