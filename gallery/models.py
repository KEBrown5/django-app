from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

class Posts(models.Model):
    # Django model's automatically have an id associated with it, meaning I don't need to define it here
    author = models.ForeignKey(User, on_delete = models.CASCADE)

    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='blogImages/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Automatically creates a join table between Posts and tags. Related name is how the other model refers to this one
    tags = models.ManyToManyField('Tag', related_name = 'posts', blank = True)

    def __str__(self):
        return self.title

    # Im pretty sure this code is redundant 
    # def edit(self, title, content, image): Not currently in use
    #     self.title = title
    #     self.content = content
    #     self.image = image
    #     self.save()


    def short_description(self):
        # Split the description into words
        words = self.content.split()
        if len(words) > 50:
            # Join the first 50 words and add "..." at the end
            return ' '.join(words[:30]) + '...'
        else:
            # If the description is already less than 50 words, return it as is
            return self.content
       
class Tag(models.Model):
    name = models.CharField(max_length = 50, unique = True) # Keep tags unique so we don't repeat the same things  

    def __str__(self):
        return self.name
