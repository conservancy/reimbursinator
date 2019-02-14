from django.db import models
from django.conf import settings
import datetime
import ntpath

class Report(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    date_created = models.DateTimeField('date created', default=datetime.date.today)
    date_submitted = models.DateTimeField('date submitted', default=datetime.date.today)
    submitted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Section(models.Model):
    report_id = models.ForeignKey(Report, on_delete=models.CASCADE)
    auto_submit = models.BooleanField()
    required = models.BooleanField()
    completed = models.BooleanField()
    title = models.CharField(max_length=256)
    html_description = models.TextField()
    number = models.IntegerField()

    def __str__(self):
        return "{0}(#{1})".format(self.title, self.number)

class Field(models.Model):
    section_id = models.ForeignKey(Section, on_delete=models.CASCADE)
    field_name = models.CharField(max_length=512, default="field")
    label = models.CharField(max_length=512)
    number = models.IntegerField()
    field_type = models.CharField(max_length=128)
    completed = models.BooleanField(default=False)
    data_bool = models.BooleanField(default=False)
    data_decimal = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    data_date = models.DateField(null=True, blank=True)
    data_file = models.FileField(upload_to='uploads/%Y/%m/%d/', max_length=512, null=True, blank=True)
    data_string = models.TextField(default='', blank=True)
    data_integer = models.IntegerField(default=0, blank=True)

    # function that prints the string representation
    # on the api?
    def __str__(self):
        if self.field_type == "boolean":
            if self.data_bool:
                return "True"
            else:
                return "False"
        elif self.field_type == "decimal":
            return "{}".format(self.data_decimal)
        elif self.field_type == "date":
            return "{}".format(self.data_date)
        elif self.field_type == "file":
            return "{}".format(self.data_file)
        elif self.field_type == "string":
            return "{}".format(self.data_string)
        elif self.field_type == "integer":
            return "{}".format(self.data_integer)


    # function that gets corresponding
    # data type
    def get_datatype(self):
        if self.field_type == "boolean":
            if self.data_bool:
                return True
            else:
                return False
        elif self.field_type == "decimal":
            return self.data_decimal
        elif self.field_type == "date":
            return "{}".format(self.data_date)
        elif self.field_type == "file":
            file_name = self.path_leaf(str(self.data_file))
            return "{}".format(file_name)
        elif self.field_type == "string":
            return "{}".format(self.data_string)
        elif self.field_type == "integer":
            return self.data_integer

    # function that accommodates if
    # path has slash at end
    def path_leaf(self, path):
        dir_path, name = ntpath.split(path)
        return name or ntpath.basename(dir_path)
