from django.db import models
from django.conf import settings
import datetime
import ntpath

class Report(models.Model):
    """
    This model represents an expense report that can be
    created, updated and submitted by a user.
    """
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    date_created = models.DateTimeField('date created', default=datetime.date.today)
    date_submitted = models.DateTimeField('date submitted', default=datetime.date.today)
    submitted = models.BooleanField(default=False)

    def __str__(self):
        """
        For debugging and display in admin view.
        """
        return self.title

class Section(models.Model):
    """
    This model represents a logical division of a report,
    containing its own fields and rules that apply to those
    fields.
    """
    report_id = models.ForeignKey(Report, on_delete=models.CASCADE)
    auto_submit = models.BooleanField(default=False)
    required = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    title = models.CharField(max_length=256)
    html_description = models.TextField()
    number = models.IntegerField()
    approved = models.BooleanField(default=False)

    def __str__(self):
        """
        For debugging and display in admin view.
        """
        return "{0}(#{1})".format(self.title, self.number)

class Field(models.Model):
    """
    This model contains a piece of data entered by the user.
    Depending on the type of the data ( boolean, decimal,
    date, file, string or integer), different table columns
    will be used to store the data.
    """
    section_id = models.ForeignKey(Section, on_delete=models.CASCADE)
    field_name = models.CharField(max_length=512, default="field")
    label = models.CharField(max_length=512)
    number = models.IntegerField(default=0)
    field_type = models.CharField(max_length=128)
    completed = models.BooleanField(default=False)
    data_bool = models.BooleanField(default=False)
    data_decimal = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    data_date = models.DateField(null=True, blank=True)
    data_file = models.FileField(upload_to='uploads/%Y/%m/%d/', max_length=512, null=True, blank=True)
    data_string = models.TextField(default='', blank=True)
    data_integer = models.IntegerField(default=0, blank=True)

    def __str__(self):
        """
        For debugging and display in the admin view.
        """
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
        return "Invalid type"

    def get_datatype(self):
        """
        Returns the data corresponding to the type of the
        field.
        """
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

    def path_leaf(self, path):
        """
        Function accommodating path with slash at end.
        """
        dir_path, name = ntpath.split(path)
        return name or ntpath.basename(dir_path)
