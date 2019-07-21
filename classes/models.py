from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Classroom(models.Model):
	name = models.CharField(max_length=120)
	subject = models.CharField(max_length=120)
	year = models.IntegerField()
	teacher= models.ForeignKey(User, on_delete=models.CASCADE)

	def get_absolute_url(self):
		return reverse('classroom-detail', kwargs={'classroom_id':self.id})
class Student(models.Model):
	name= models.CharField(max_length=120)
	date_of_birth= models.DateField (null=True)
	MALE = "male"
	FEMALE= "female"
	GENDER_CHOICES= (
		(MALE, MALE),
		(FEMALE, FEMALE),
		)
	gender = models.CharField (max_length=6, choices= GENDER_CHOICES)
	exam_grade = models.IntegerField(default=0)
	classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
