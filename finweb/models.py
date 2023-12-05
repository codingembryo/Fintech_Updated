from django.db import models

# Create your models here.

# import the models module from django.db
from django.db import models

# define a model called Category that has a name and a subcategory field
class Category(models.Model):
# name is a CharField with a maximum length of 100 characters
    name = models.CharField(max_length=100)
# subcategory is a ForeignKey that references another model called Subcategory
# on_delete=models.CASCADE means that if a Category is deleted, all its related Subcategories are also deleted
    subcategory = models.ForeignKey('Subcategory', on_delete=models.CASCADE)

# define a string representation of the model
    def __str__(self):
        return self.name

# define a model called Subcategory that has a name and an image field
class Subcategory(models.Model):
# name is a CharField with a maximum length of 100 characters
    name = models.CharField(max_length=100)
    # image is an ImageField that stores the path to an image file
    # upload_to specifies the directory where the images are saved
    image = models.ImageField(upload_to='images/')

    # define a string representation of the model
    def __str__(self):
        return self.name