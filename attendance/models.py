from django.db import models


def student_directory_path(instance, filename):
    name, ext = filename.split(".")
    name = instance.registration_id
    filename = name + '.' + ext
    return 'Student_Images/{}/{}/{}/{}'.format(instance.branch, instance.year, instance.section, filename)


class Student(models.Model):
    BRANCH = (
        ('Computing', 'Computing'),
        ('Networking', 'Networking'),
        ('Multimedia', 'Multimedia'),
        ('AI', 'AI'),
    )
    YEAR = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
    )
    SECTION = (
        ('C1', 'C1'),
        ('C2', 'C2'),
        ('C3', 'C3'),
        ('C4', 'C4'),
        ('C5', 'C5'),
        ('C6', 'C6'),
        ('C7', 'C7'),
        ('C8', 'C8'),
        ('C9', 'C9'),
        ('C10', 'C10'),
        ('C11', 'C11'),
        ('C12', 'C12'),
        ('C13', 'C12'),
        ('C14', 'C14'),
        ('C15', 'C15'),
    )

    firstname = models.CharField(max_length=200, null=True, blank=True)
    lastname = models.CharField(max_length=200, null=True, blank=True)
    registration_id = models.CharField(max_length=200, null=True)
    branch = models.CharField(max_length=100, null=True, choices=BRANCH)
    year = models.CharField(max_length=100, null=True, choices=YEAR)
    section = models.CharField(max_length=100, null=True, choices=SECTION)
    profile_pic = models.ImageField(upload_to=student_directory_path, null=True, blank=True)

    objects = models.Manager()

    def __str__(self):
        return str(self.registration_id)


class Attendance(models.Model):
    Faculty_Name = models.CharField(max_length=200, null=True, blank=True)
    Student_ID = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateField(auto_now_add=True, null=True)
    time = models.TimeField(auto_now_add=True, null=True)
    branch = models.CharField(max_length=200, null=True)
    year = models.CharField(max_length=200, null=True)
    section = models.CharField(max_length=200, null=True)
    period = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=200, null=True, default='Absent')

    objects = models.Manager()

    def __str__(self):
        return f'{self.Student_ID}_{self.date}_{self.period}'
