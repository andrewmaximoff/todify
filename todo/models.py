from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from django.db import models


class Tag(models.Model):
    name = models.TextField(max_length=32, unique=True)
    slug = models.SlugField(unique=True)

    def _get_slug(self):
        return slugify(self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_slug()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=128, blank=False)
    body = models.TextField(max_length=2048, blank=True)
    created_date = models.DateField(default=timezone.now)
    modified_date = models.DateField()
    due_date = models.DateField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    completed_date = models.DateField(blank=True, null=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='task_owner',
        on_delete=models.CASCADE
    )
    tags = models.ManyToManyField(Tag, blank=True)

    priority = models.PositiveIntegerField(default=9999)

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        # If task completed, sets the completion date
        if self.completed and self.completed_date is None:
            self.completed_date = timezone.now()

        if not self.id:
            self.created_date = timezone.now()
        self.modified_date = timezone.now()
        super().save(*args, **kwargs)

    def overdue_status(self):
        """ Return True if the task's time has expired """
        if self.due_date and timezone.now() > self.due_date:
            return True

    def get_absolute_url(self):
        return reverse('todo:task-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title
