from django.db import models
from django.conf import settings

class Report(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    date_created = models.DateTimeField('date created')
    date_submitted = models.DateTimeField('date submitted', null=True, blank=True)
    submitted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Section(models.Model):
    report_id = models.ForeignKey(Report, on_delete=models.CASCADE)
    completed = models.BooleanField()
    title = models.CharField(max_length=256)
    html_description = models.TextField()
    number = models.IntegerField()

    def __str__(self):
        return "{0}(#{1})".format(self.title, self.number)

class Field(models.Model):
    section_id = models.ForeignKey(Section, on_delete=models.CASCADE)
    label = models.CharField(max_length=256)
    number = models.IntegerField()
    type = models.CharField(max_length=128)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return "{0}(#{1})".format(self.label, self.number)

class DataBool(models.Model):
    field_id = models.ForeignKey(Field, on_delete=models.CASCADE)
    data = models.BooleanField(default=False)

    def __str__(self):
        if self.data:
            return "True"
        else:
            return "False"

class DataDecimal(models.Model):
    field_id = models.ForeignKey(Field, on_delete=models.CASCADE)
    data = models.DecimalField(max_digits=9,decimal_places=2, null=True, blank=True)

    def __str__(self):
        return "{0}".format(self.data)

class DataDate(models.Model):
    field_id = models.ForeignKey(Field, on_delete=models.CASCADE)
    data = models.DateField(null=True, blank=True)

    def __str__(self):
        return "{0}".format(self.data)

class DataFile(models.Model):
    field_id = models.ForeignKey(Field, on_delete=models.CASCADE)
    data = models.FileField(upload_to='uploads/%Y/%m/%d/', max_length=512, null=True, blank=True)
    
    def __str__(self):
        return "{0}".format(self.data)

class DataString(models.Model):
    field_id = models.ForeignKey(Field, on_delete=models.CASCADE)
    data = models.TextField(default='')

    def __str__(self):
        return "{0}".format(self.data)

class DataInteger(models.Model):
    field_id = models.ForeignKey(Field, on_delete=models.CASCADE)
    data = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return "{0}".format(self.data)
