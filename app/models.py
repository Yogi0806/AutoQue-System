from django.db import models

class QuestionType(models.TextChoices):
    Six_Six_Five_EndSem = "Six_Six_Five_EndSem", "6-6-6, 6-6-5"
    Nine_Eight_EndSem = 'Nine_Eight_EndSem', "9-9, 9-8"
    Six_Five_Four_Midsem = 'Six_Five_Four_Midsem', "6-5-4"
    Five_Five_Five_Midsem = 'Five_Five_Five_Midsem', "5-5-5"


# Create your models here.
class Subject_data(models.Model):
    college_name = models.CharField(null=True, blank=True, max_length=50)
    branch_name = models.CharField(null=True, blank=True, max_length=50)
    semester = models.CharField(null=True, blank=True, max_length=50)
    subject_name = models.CharField(null=True, blank=True, max_length=50)
    year = models.CharField(null=True, blank=True, max_length=50)
    faculty = models.CharField(null=True, blank=True, max_length=50)
    paper_format = models.CharField(max_length=40,blank=True, null=True)
    number_of_sets = models.IntegerField(default=1)
    qb = models.FileField()
    date = models.DateField(blank=True, null=True)
    marks_format = models.CharField(max_length=120, choices=QuestionType.choices, 
                    blank=True, null=True)
    def __str__(self):
        return self.branch_name + " - " + self.semester + " - " + self.subject_name + " - "+str(self.id)


class MidSemPaperSet(models.Model):
    paper = models.ForeignKey(Subject_data, on_delete=models.CASCADE,
                                        related_name='midsem_paper')
    q1 = models.CharField(null=True, blank=True, max_length=700)
    q2 = models.CharField(null=True, blank=True, max_length=700)
    q3 = models.CharField(null=True, blank=True, max_length=700)
    q4 = models.CharField(null=True, blank=True, max_length=700)
    q5 = models.CharField(null=True, blank=True, max_length=700)
    q6 = models.CharField(null=True, blank=True, max_length=700)
    q7 = models.CharField(null=True, blank=True, max_length=700)
    q8 = models.CharField(null=True, blank=True, max_length=700)
    q9 = models.CharField(null=True, blank=True, max_length=700)
    q10 = models.CharField(null=True, blank=True, max_length=700)
    q11 = models.CharField(null=True, blank=True, max_length=700)
    q12 = models.CharField(null=True, blank=True, max_length=700)
    bl1 = models.CharField(null=True, blank=True, max_length=500)
    bl2 = models.CharField(null=True, blank=True, max_length=500)
    bl3 = models.CharField(null=True, blank=True, max_length=500)
    bl4 = models.CharField(null=True, blank=True, max_length=500)
    bl5 = models.CharField(null=True, blank=True, max_length=500)
    bl6 = models.CharField(null=True, blank=True, max_length=500)
    bl7 = models.CharField(null=True, blank=True, max_length=500)
    bl8 = models.CharField(null=True, blank=True, max_length=500)
    bl9 = models.CharField(null=True, blank=True, max_length=500)
    bl10 = models.CharField(null=True, blank=True, max_length=500)
    bl11 = models.CharField(null=True, blank=True, max_length=500)
    bl12 = models.CharField(null=True, blank=True, max_length=500)

    


class SemesterPaperSet(models.Model):
    paper = models.ForeignKey(Subject_data, on_delete=models.CASCADE,
                                        related_name='semester_paper')
    q1 = models.CharField(null=True, blank=True, max_length=700)
    q2 = models.CharField(null=True, blank=True, max_length=700)
    q3 = models.CharField(null=True, blank=True, max_length=700)    
    q4 = models.CharField(null=True, blank=True, max_length=700)
    q5 = models.CharField(null=True, blank=True, max_length=700)
    q6 = models.CharField(null=True, blank=True, max_length=700)
    q7 = models.CharField(null=True, blank=True, max_length=700)
    q8 = models.CharField(null=True, blank=True, max_length=700)
    q9 = models.CharField(null=True, blank=True, max_length=700)
    q10 = models.CharField(null=True, blank=True, max_length=700)
    q11 = models.CharField(null=True, blank=True, max_length=700)
    q12 = models.CharField(null=True, blank=True, max_length=700)
    q13 = models.CharField(null=True, blank=True, max_length=700)
    q14 = models.CharField(null=True, blank=True, max_length=700)
    q15 = models.CharField(null=True, blank=True, max_length=700)
    q16 = models.CharField(null=True, blank=True, max_length=700)
    q17 = models.CharField(null=True, blank=True, max_length=700)
    q18 = models.CharField(null=True, blank=True, max_length=700)
    q19 = models.CharField(null=True, blank=True, max_length=700)
    q20 = models.CharField(null=True, blank=True, max_length=700)
    q21 = models.CharField(null=True, blank=True, max_length=700)
    q22 = models.CharField(null=True, blank=True, max_length=700)
    q23 = models.CharField(null=True, blank=True, max_length=700)
    q24 = models.CharField(null=True, blank=True, max_length=700)
    bl1 = models.CharField(null=True, blank=True, max_length=500)
    bl2 = models.CharField(null=True, blank=True, max_length=500)
    bl3 = models.CharField(null=True, blank=True, max_length=500)
    bl4 = models.CharField(null=True, blank=True, max_length=500)
    bl5 = models.CharField(null=True, blank=True, max_length=500)
    bl6 = models.CharField(null=True, blank=True, max_length=500)
    bl7 = models.CharField(null=True, blank=True, max_length=500)
    bl8 = models.CharField(null=True, blank=True, max_length=500)
    bl9 = models.CharField(null=True, blank=True, max_length=500)
    bl10 = models.CharField(null=True, blank=True, max_length=500)
    bl11 = models.CharField(null=True, blank=True, max_length=500)
    bl12 = models.CharField(null=True, blank=True, max_length=500)
    bl13 = models.CharField(null=True, blank=True, max_length=500)
    bl14 = models.CharField(null=True, blank=True, max_length=500)
    bl15 = models.CharField(null=True, blank=True, max_length=500)
    bl16 = models.CharField(null=True, blank=True, max_length=500)
    bl17 = models.CharField(null=True, blank=True, max_length=500)
    bl18 = models.CharField(null=True, blank=True, max_length=500)
    bl19 = models.CharField(null=True, blank=True, max_length=500)
    bl20 = models.CharField(null=True, blank=True, max_length=500)
    bl21 = models.CharField(null=True, blank=True, max_length=500)
    bl22 = models.CharField(null=True, blank=True, max_length=500)
    bl23 = models.CharField(null=True, blank=True, max_length=500)
    bl24 = models.CharField(null=True, blank=True, max_length=500)


    

