from django.db import models
from django.contrib.auth.models import Permission, User
import django
import datetime

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	YEAR_IN_COLLEGE_CHOICES = (
		(1, '1st Year'),
		(2, '2nd Year'),
		(3, '3rd Year'),
		(4, '4th Year'),
	)
	full_name = models.CharField(max_length = 100)
	year = models.IntegerField(choices=YEAR_IN_COLLEGE_CHOICES, default=1)
	roll_no = models.CharField(max_length = 8, unique=True)
	created = models.DateField(editable=False, null=True)

	def __str__(self):
		return self.roll_no

	def save(self):
		if not self.id:
			self.roll_no = self.user.username
			self.created = datetime.date.today()
		super(UserProfile, self).save()

class Assignment(models.Model):
	YEAR_IN_COLLEGE_CHOICES = (
		(1, '1st Year'),
		(2, '2nd Year'),
		(3, '3rd Year'),
		(4, '4th Year'),
	)
	year = models.IntegerField(choices=YEAR_IN_COLLEGE_CHOICES, default=1)
	name = models.CharField(max_length = 200)
	questions = models.TextField(max_length = 1000)
	created = models.DateField(editable=False, null=True)
	updated = models.DateTimeField(editable=False, null=True)
	deadline = models.DateField()

	def __str__(self):
		return self.name

	def save(self):
		if not self.id:
			self.created = datetime.date.today()
		self.updated = datetime.datetime.today()
		super(Assignment, self).save()

class Solution(models.Model):
	assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
	student = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
	submission_date = models.DateField()
	file = models.FileField()

	def __str__(self):
		return self.file.url

	def save(self):
		self.submission_date = datetime.date.today()
		super(Solution, self).save()
