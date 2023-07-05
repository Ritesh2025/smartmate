from django.db import models
import random
from django.core.validators import FileExtensionValidator
from django.db import IntegrityError

# from shortuuid import ShortUUID
# from django.db import models
# from shortuuid.django_fields import ShortUUIDField

class DepartmentDetail(models.Model):
    did = models.BigAutoField(primary_key=True)
    dname = models.TextField(max_length=300)

    def __str__(self):
        return f"{self.did}"

    def save(self, *args, **kwargs):
        if not self.did:
            # Generate a 4 digit unique id
            self.did = self.generate_department_unique_id()

        try:
            super().save(*args, **kwargs)

        except IntegrityError:
            self.did = self.generate_department_unique_id()
            super().save(*args, **kwargs)


    @staticmethod
    def generate_department_unique_id():
        unique_id = str(random.randint(1000, 9999))
        while DepartmentDetail.objects.filter(did=unique_id).exists():
            unique_id = str(random.randint(1000, 9999))
        return unique_id


class FacultyDetail(models.Model):
    fid = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=30, null=True)
    email = models.EmailField()
    password = models.CharField(max_length=20)
    did_fk = models.ForeignKey(DepartmentDetail, null=True, on_delete=models.CASCADE)
    
    @property    #Accessing Data of above table
    def dept_name(self):
        return self.did_fk.dname


    def __str__(self):
        return str(self.fid)
        #return f"{self.fid} : {self.name}"
    
    def save(self, *args, **kwargs):
        if not self.fid:
            # Generate a 6 digit unique id
            self.fid = self.generate_faculty_unique_id()

        try:
            super().save(*args, **kwargs)

        except IntegrityError:
                # If a duplicate sid is generated, generate a new one and try again
            self.fid = self.generate_faculty_unique_id()
            super().save(*args, **kwargs)

    @staticmethod
    def generate_faculty_unique_id():
        prefix = '5000898'
        unique_id = prefix + str(random.randint(100000, 999999))
        while FacultyDetail.objects.filter(fid=unique_id).exists():
            unique_id = prefix + str(random.randint(100000, 999999))
        return unique_id
            


class CourseDetail(models.Model):
    cid = models.BigAutoField(primary_key=True)
    cname = models.TextField(max_length=300)
    did_fk = models.ForeignKey(DepartmentDetail, on_delete=models.CASCADE) # foreign key
    
    def __str__(self):
        return f"{self.cid}"

    def save(self, *args, **kwargs):
        if not self.cid:
            # Generate a 4 digit unique id
            self.cid = self.generate_unique_id()
        
        try:
            super().save(*args, **kwargs)

        except IntegrityError:
            self.cid = self.generate_unique_id()
            super().save(*args, **kwargs)

    @staticmethod
    def generate_unique_id():
        unique_id = str(random.randint(1000, 9999))
        while CourseDetail.objects.filter(cid=unique_id).exists():
            unique_id = str(random.randint(1000, 9999))
        return unique_id

    @property    # Accessing Data of above table
    def dept(self):
        return self.did_fk.dname


class StudentDetail(models.Model):
    sid = models.BigAutoField(primary_key=True)
    # sid = ShortUUIDField(primary_key=True, serialize=False, verbose_name='ID', max_length=6)
    name = models.CharField(max_length=30, null=True)
    email = models.EmailField()
    password = models.CharField(max_length=20)
    cid_fk = models.ForeignKey(CourseDetail,null=True, on_delete=models.CASCADE)

    access_stu = models.BooleanField(default=False)
    
    @property    #Accessing Data of above table
    def course_name(self):
        return self.cid_fk.cname
    

    def save(self, *args, **kwargs):
        if not self.sid:
            # Generate a 5 digit unique id
            self.sid = self.generate_student_unique_id()

        try:
            super().save(*args, **kwargs)

        except IntegrityError:
            # If a duplicate sid is generated, generate a new one and try again
            self.sid = self.generate_student_unique_id()
            super().save(*args, **kwargs)

    @staticmethod
    def generate_student_unique_id():
        unique_id = str(random.randint(10000, 99999))
        while StudentDetail.objects.filter(sid=unique_id).exists():
            unique_id = str(random.randint(10000, 99999))
        return unique_id
    
    
class Subject(models.Model):
    sub_id = models.BigAutoField(primary_key=True)
    sub_name = models.TextField(max_length=500)
    did_fk = models.ForeignKey(DepartmentDetail, on_delete=models.CASCADE) #foreign key
    cid_fk = models.ForeignKey(CourseDetail, on_delete=models.CASCADE) #foreign key
    fid_fk = models.ForeignKey(FacultyDetail, on_delete=models.CASCADE) #foreign key

    def __str__(self):
        return str(self.sub_id)
        #return f"{self.sub_id}: {self.sub_name}"

    def save(self, *args, **kwargs):
        if not self.sub_id:
            # Generate a 4 digit unique id
            self.sub_id = self.generate_unique_id()

        try:
            super().save(*args, **kwargs)

        except IntegrityError:
            self.sub_id = self.generate_unique_id()
            super().save(*args, **kwargs)


    @staticmethod
    def generate_unique_id():
        unique_id = str(random.randint(1000, 9999))
        while Subject.objects.filter(sub_id=unique_id).exists():
            unique_id = str(random.randint(1000, 9999))
        return unique_id
    
    
    @property    #Accessing Data of above table
    def dept(self):
        return self.did_fk.did
    
    @property    #Accessing Data of above table
    def course(self):
        return self.cid_fk.cid
    
    @property    #Accessing Data of above table
    def faculty(self):
        return self.fid_fk.fid
    
    # def name(self):
    #     return self.fid_fk.fname

class Note(models.Model):
    note_id = models.BigAutoField(primary_key=True)
    # title = models.CharField(max_length=100)
    # description = models.TextField(max_length=1000)
    note_text = models.TextField(max_length=500)
    file = models.FileField(upload_to='notes/', max_length=300, null=True, validators=[
        FileExtensionValidator(allowed_extensions=['pdf'])])
    sub_id_fk = models.ForeignKey(Subject, on_delete=models.CASCADE) #foreign key
    fid_fk = models.ForeignKey(FacultyDetail, on_delete=models.CASCADE) #foreign key
    cid_fk = models.ForeignKey(CourseDetail, null=True,on_delete=models.CASCADE)
    
    @property    #Accessing Data of above table
    def course_name(self):
        return self.cid_fk.cname

    def save(self, *args, **kwargs):
        if not self.note_id:
            # Generate a 4 digit unique id
            self.note_id = self.generate_note_unique_id()
        try:
            super().save(*args, **kwargs)

        except IntegrityError:
            self.note_id = self.generate_note_unique_id()
            super().save(*args, **kwargs)

    @staticmethod
    def generate_note_unique_id():
        unique_id = str(random.randint(1000, 9999))
        while Note.objects.filter(note_id=unique_id).exists():
            unique_id = str(random.randint(1000, 9999))
        return unique_id
    
    @property    #Accessing Data of above table
    def faculty(self):
        return self.fid_fk.fid
        # return self.fid_fk_id

    @property    #Accessing Data of above table
    def subject(self):
        return self.sub_id_fk.sub_id
        # return self.sub_id_fk_id

class Flashcard(models.Model):
    card_id = models.BigAutoField(primary_key=True)
    # title = models.CharField(max_length=100)
    # description = models.TextField(max_length=1000)
    set_title = models.TextField(max_length=100)
    sub_id_fk = models.ForeignKey(Subject, on_delete=models.CASCADE) #foreign key
    sid_fk = models.ForeignKey(StudentDetail, on_delete=models.CASCADE) #foreign key
    cid_fk = models.ForeignKey(CourseDetail, null=True,on_delete=models.CASCADE)#foreign key
    term = models.TextField(max_length=100)
    desc = models.TextField(max_length=100)


  
    @property    #Accessing Data of above table
    def course_name(self):
        return self.cid_fk.cname



    def save(self, *args, **kwargs):
        if not self.card_id:
            # Generate a 4 digit unique id
            self.card_id = self.generate_card_unique_id()
        try:
            super().save(*args, **kwargs)

        except IntegrityError:
            self.card_id = self.generate_card_unique_id()
            super().save(*args, **kwargs)

    @staticmethod
    def generate_card_unique_id():
        unique_id = str(random.randint(1000, 9999))
        while Flashcard.objects.filter(card_id=unique_id).exists():
            unique_id = str(random.randint(1000, 9999))
        return unique_id
    
    def __str__(self):
        return str(self.card_id)
    
    @property    #Accessing Data of above table
    def student(self):
        return str(self.sid_fk.name)
        # return self.sid_fk_id

    @property    #Accessing Data of above table
    def subject(self):
        return self.sub_id_fk.sub_id
        # return self.sub_id_fk_id


class Announcement(models.Model):
    ann_id = models.BigAutoField(primary_key=True)
    # title = models.CharField(max_length=100)
    # description = models.TextField(max_length=1000)
    title = models.TextField(max_length=100)
    desc = models.TextField(max_length=500)
    sub_id_fk = models.ForeignKey(Subject, on_delete=models.CASCADE) #foreign key
    fid_fk = models.ForeignKey(FacultyDetail, on_delete=models.CASCADE) #foreign key
    cid_fk = models.ForeignKey(CourseDetail, null=True,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    @property    #Accessing Data of above table
    def course_name(self):
        return self.cid_fk.cname



    def save(self, *args, **kwargs):
        if not self.ann_id:
            # Generate a 4 digit unique id
            self.ann_id = self.generate_ann_unique_id()
        try:
            super().save(*args, **kwargs)

        except IntegrityError:
            self.ann_id = self.generate_ann_unique_id()
            super().save(*args, **kwargs)

    @staticmethod
    def generate_ann_unique_id():
        unique_id = str(random.randint(1000, 9999))
        while Announcement.objects.filter(ann_id=unique_id).exists():
            unique_id = str(random.randint(1000, 9999))
        return unique_id
    
    @property    #Accessing Data of above table
    def faculty(self):
        return self.fid_fk.fid
        # return self.fid_fk_id

    @property    #Accessing Data of above table
    def subject(self):
        return self.sub_id_fk.sub_id
        # return self.sub_id_fk_id

class Forum(models.Model):
    forum_id = models.BigAutoField(primary_key=True)
    name=models.CharField(max_length=200,default="anonymous")
    topic= models.CharField(max_length=300)
    description = models.CharField(max_length=1000,blank=True)
    date_created=models.DateTimeField(auto_now_add=True,null=True)
    created_by = models.CharField(max_length=200, null= True, default="anonymous")

    def __str__(self):
        return str(self.topic)
    
    def save(self, *args, **kwargs):
        if not self.forum_id:
            # Generate a 4 digit unique id
            self.forum_id = self.generate_forum_unique_id()
        try:
            super().save(*args, **kwargs)

        except IntegrityError:
            self.forum_id = self.generate_forum_unique_id()
            super().save(*args, **kwargs)

    @staticmethod
    def generate_forum_unique_id():
        unique_id = str(random.randint(1000, 9999))
        while Forum.objects.filter(forum_id=unique_id).exists():
            unique_id = str(random.randint(1000, 9999))
        return unique_id
    
class Discussion(models.Model):
    dis_id = models.BigAutoField(primary_key=True)
    forum = models.ForeignKey(Forum,null=True, on_delete=models.CASCADE)
    discuss = models.CharField(max_length=1000)
    date_created=models.DateTimeField(auto_now_add=True,null=True)
    created_by = models.CharField(max_length=200,null= True, default="anonymous")

    @property    #Accessing Data of above table
    def get_forum_id(self):
        return self.forum.forum_id

    def __str__(self):
        return str(self.forum)
    

    def save(self, *args, **kwargs):
        if not self.dis_id:
            # Generate a 4 digit unique id
            self.dis_id = self.generate_disc_unique_id()
        try:
            super().save(*args, **kwargs)

        except IntegrityError:
            self.dis_id = self.generate_disc_unique_id()
            super().save(*args, **kwargs)

    @staticmethod
    def generate_disc_unique_id():
        unique_id = str(random.randint(1000, 9999))
        while Discussion.objects.filter(dis_id=unique_id).exists():
            unique_id = str(random.randint(1000, 9999))
        return unique_id