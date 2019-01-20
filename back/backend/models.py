from django.db import models
from django.contrib.auth.models import User

class Report(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    date_created = models.DateTimeField('date created')
    date_submitted = models.DateTimeField('date submitted')
    submitted = models.BooleanField()

class Section(models.Model):
    report_id = models.ForeignKey(Report, on_delete=models.CASCADE)
    completed = models.BooleanField()
    title = models.CharField(max_length=256)
    html_description = models.TextField()
    number = models.IntegerField()

class Field(models.Model):
    section_id = models.ForeignKey(Section, on_delete=models.CASCADE)
    label = models.CharField(max_length=256)
    number = models.IntegerField()
    type = models.CharField(max_length=128)
    completed = models.BooleanField()

class DataBool(models.Model):
    field_id = models.ForeignKey(Field, on_delete=models.CASCADE)
    data = models.BooleanField()

class DataDecimal(models.Model):
    field_id = models.ForeignKey(Field, on_delete=models.CASCADE)
    data = models.DecimalField(max_digits=9,decimal_places=2)

class DataDate(models.Model):
    field_id = models.ForeignKey(Field, on_delete=models.CASCADE)
    data = models.DateField()

class DataFile(models.Model):
    field_id = models.ForeignKey(Field, on_delete=models.CASCADE)
    data = models.FileField()

class DataString(models.Model):
    field_id = models.ForeignKey(Field, on_delete=models.CASCADE)
    data = models.TextField()

class DataInteger(models.Model):
    field_id = models.ForeignKey(Field, on_delete=models.CASCADE)
    data = models.IntegerField()
