from django.db import models

from django.contrib.auth.models import User

class Author(models.Model):
    name = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Song(models.Model):
    name = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Record(models.Model):
    name = models.TextField()
    songs = models.ManyToManyField(Song)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Search(models.Model):
    q = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def results(self):
        return {
            'songs': Song.objects.filter(name__icontains=self.q),
            'records': Record.objects.filter(name__icontains=self.q),
            'authors': Author.objects.filter(name__icontains=self.q),

        }



