from django.db import models


class Student(models.Model):
    roll_no = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    fathers_name = models.CharField(max_length=255)
    college = models.ForeignKey('College')
    branch = models.ForeignKey('Branch')

    def __unicode__(self):
        return unicode(self.roll_no)

# code is being taken as a CharField instead of IntegerField
# because codes may start with a 0 which may be simply ignored
# by python or cause other problems.


class College(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, primary_key=True)

    def __unicode__(self):
        return self.name


class Branch(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, primary_key=True)

    def __unicode__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10)

    def __unicode__(self):
        return self.name


class Marks(models.Model):
    subject = models.ForeignKey('Subject')
    student = models.ForeignKey('Student')
    theory = models.IntegerField()
    practical = models.IntegerField()
    internal_theory = models.IntegerField()
    internal_practical = models.IntegerField()
    semester = models.IntegerField()
    credits = models.IntegerField()
    back = models.BooleanField()

    class Meta:
        unique_together = (('subject', 'student'),)

    def __unicode__(self):
        return unicode(self.theory)