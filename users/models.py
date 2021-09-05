from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	# on_delete will decide what to do with Profile if
	# User is deleted
	city = models.CharField(max_length=50)
	image = models.ImageField(default='default.jpg', upload_to='profile_pics')


	def __str__(self):
		return f"{self.user.username} from {self.city}"

	# we override exisitng `save()`
	'''
	save() must be commented out if S3 is used
	for storage otherwise it'll give errors
	'''
	def save(self, *args, **kwargs):

		super().save(*args, **kwargs)

		img = Image.open(self.image.path)

		if img.height > 300 or img.width > 300:
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save(self.image.path)
