from django.contrib.auth import logout
from django.shortcuts import render, HttpResponse, redirect
from .models import *
# FacultyDetail,StudentDetail, Note, Subject, DepartmentDetail, CourseDetail, Flashcard, Announcement
from django.contrib import messages
from django.db.models import Q
import datetime
# Create your views here.

# def WelcomePage(request):
#     return render(request, 'welcome.html')

def HomePage(request):
    if "nm" not in request.session:
        return redirect('../login/1')

    if request.session['course'] == 'all':
        notes = Note.objects.all()
    else:
        cid = CourseDetail.objects.get(cid = request.session['course'])
        print(cid)
        notes = Note.objects.filter(cid_fk = cid)
        print(notes)

    context = {'notes':notes}
    return render(request, 'home.html', context)    

def SignUp(request):
    if request.method == 'POST':
        
        signup_type=request.POST.get('signup_type')
        name=request.POST.get('name')
        email=request.POST.get('email')
        pass1=request.POST.get('password')
        pass2=request.POST.get('password2')

        dep_id = request.POST.get('department')
        dep_id = DepartmentDetail.objects.get(did=dep_id)

        c_id = request.POST.get('course')
        c_id = CourseDetail.objects.get(cid=c_id)

        # Check if passwords match
        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

        if signup_type == 'faculty':
            try:
                faculty = FacultyDetail(name=name, email=email, password=pass1, did_fk=dep_id)
                faculty.save()
                messages.success(request, "Faculty account created successfully")
                
                return redirect('signup')
            except Exception:
                messages.error(request, "Error occurred while creating faculty account")
                return redirect('signup')
        elif signup_type == 'student':
            try:
                student = StudentDetail(name=name, email=email, password=pass1, cid_fk=c_id)
                student.save()
                messages.success(request, "Student account created successfully")
                return redirect('signup')
            except Exception:
                messages.error(request, "Error occurred while creating student account")
                return redirect('signup')
        else:
            messages.error(request, "Invalid signup type")
            return redirect('signup')
    return redirect('../login/0')

def Login(request,m=0):
    if request.method == 'POST':
        login_type = request.POST.get('login_type')
        name = request.POST.get('name')
        pass1 = request.POST.get('password')

        if login_type == 'faculty':
                try:
                    user = FacultyDetail.objects.get(name=name, password=pass1)
                    # Login the user and redirect to the home page
                    request.session["nm"] = user.name
                    request.session["pass1"] = user.password
                    request.session["course"] = 'all'
                    request.session["login_type"] = "faculty"
                    return redirect('/home/')
                except FacultyDetail.DoesNotExist:
                    return HttpResponse("Invalid username or password")
        else:
            # Handle student login
                try:
                    user = StudentDetail.objects.get(name=name, password=pass1)
                    # Login the user and redirect to the home page
                    request.session["nm"] = user.name
                    request.session["pass1"] = user.password
                    request.session["course"] = user.cid_fk.cid
                    print(user.cid_fk.cid)
                    request.session["login_type"] = "student"
                    return redirect('/home/')
                except StudentDetail.DoesNotExist:
                    return HttpResponse("Invalid username or password")
    else:
        if "nm" in request.session:
            return redirect('../home')
        
        dept = DepartmentDetail.objects.all()
        cours = CourseDetail.objects.all()

        return render(request, 'index.html',{'departments':dept,'courses':cours,'ms':m})
    

def logout(request):
    try:
        del request.session["nm"]
        del request.session['password']
        del request.session["course"]

    except KeyError:
        pass
    return redirect('../login/0')

def create_note(request):
    if "nm" not in request.session:
        return redirect('../login/1')
    if request.method == 'POST':
        note_text = request.POST.get('note_text')
        file = request.FILES.get('file')
        sub_id = request.POST.get('sub_id_fk')
        subject = Subject.objects.get(sub_id=sub_id)
        faculty_id = request.POST.get('fid_fk') # You can set the faculty ID as required
        course_id = request.POST.get('cid_fk')
        courses = CourseDetail.objects.get(cid = course_id)

        # Validate the uploaded file
        if file:
            ext = file.name.split('.')[-1]
            if ext.lower() not in ['pdf']:
                # raise ValidationError('File type not supported. Only PDF files are allowed.')
                return HttpResponse("Only .pdf")
            

        # Save the note to the database
        if FacultyDetail.objects.filter(fid=faculty_id).exists():
            faculty=FacultyDetail.objects.get(fid=faculty_id)
            note = Note(note_text=note_text, file=file, sub_id_fk=subject, fid_fk=faculty, cid_fk=courses)
            note.save()
        else:
            return HttpResponse("Invalid Try")
    
    # Get all the subjects for the subject dropdown
    subjects = Subject.objects.all()
    faculty = FacultyDetail.objects.all()
    course = CourseDetail.objects.all()

    return render(request, 'create_note.html', {'subjects': subjects, 'faculty': faculty, 'course': course})

def download_notes(request):
    # if "nm" not in request.session:
    #     return redirect('../login')

    # query = request.GET.get('q')
    # course = request.GET.get('c')
    # cid = None
    
    # if request.session['course'] == 'all':
    #     notes = Note.objects.all()
    # else:
    #     # cid = CourseDetail.objects.get(cid = request.session['course'])
    #     try:
    #         # cid = int(request.session['course'])
    #         cid = CourseDetail.objects.get(cid = request.session['course'])
    #     except ValueError:
    #         cid = None
    #     notes = Note.objects.filter(cid_fk = cid)
    
    # if query:
    #     # cid = CourseDetail.objects.get(cid=request.session['course'])
    #     try:
    #         # cid = int(request.session['course'])
    #         cid = CourseDetail.objects.get(cid = request.session['course'])
    #     except ValueError:
    #         cid = None
    #     notes = Note.objects.filter(note_text__icontains=query, cid_fk = cid )

    # elif course:
    #     try:
    #         # cid = int(request.session['course'])
    #         cid = CourseDetail.objects.get(cid = request.session['course'])
    #     except ValueError:
    #         cid = None
    #     notes = Note.objects.filter(Q(cid_fk__cname =course) | Q(cid_fk = cid))
    #     # print(type(notes))

    # try:
    #     t = StudentDetail.objects.get(name = request.session['nm'])
    #     t = t.access_stu
    # except StudentDetail.DoesNotExist:
    #     t=None

    # if course and request.session['login_type'] == 'faculty':
    #     notes = notes.filter(cid_fk__cname=course)

    # context = {'notes': notes,'trigger':t}
    # return render(request, 'download_note.html', context)

    if "nm" not in request.session:
        return redirect('../login')

    query = request.GET.get('q')
    course = request.GET.get('c')
    cid = None
    
    # if request.session['course'] == 'all':
    if course or request.session['course'] == 'all':
        notes = Note.objects.all()
    else:
        cid = request.session['course']
        notes = Note.objects.filter(cid_fk=cid)
    
    if query:
        notes = notes.filter(note_text__icontains=query)

    try:
        t = StudentDetail.objects.get(name=request.session['nm'])
        t = t.access_stu
    except StudentDetail.DoesNotExist:
        t = None

    if request.session['login_type']=='faculty':
        t = None


    if course:
        notes = notes.filter(cid_fk__cname=course)

    context = {'notes': notes, 'trigger': t}
    return render(request, 'download_note.html', context)

def view_student(request):
    if "nm" not in request.session:
        return redirect('../login')
    
    q1 = request.GET.get('s')
    if q1:
        student = StudentDetail.objects.filter(sid__icontains=q1)
    else:
        student = StudentDetail.objects.all()

    # if request.method == 'POST':
    #     student_ids = request.POST.getlist('selected_students') 
    #     print(student_ids,'FBD')
    #     chk = request.POST.get('selected_students')  
    #     print(chk,'MD')
    #     student=StudentDetail.objects.get(sid=chk)
    #     print(student.access_stu,'MD-2')
    #     checkbox_value = request.POST.get(f"selected_students{student_ids}")
    #     print(checkbox_value,'MD-3')

        # *******************************
    #     print(student_ids,"####")     
    #     for sid in student_ids:
    #         student = StudentDetail.objects.get(sid=sid)
    #         print(student, "*****")
    #         if request.POST.get('selected_students'):
    #             # student.access_stu = True
    #             student.access_stu  == True
    #         else:
    #             # student.access_stu = False
    #             student.access_stu  == False
    #         student.save()

    if request.method == 'POST':

        chk = request.POST.get("selected_students")
        print(chk,"******")
        student_ids = request.POST.get("id")
        print(student_ids,"#####")
        student = StudentDetail.objects.get(sid=student_ids)
        print(student, 'FBD')
        if chk:
            student.access_stu = True
            print("Hello MD")
        else:
            student.access_stu = False
            print("Hello FBD")
        student.save()
        # for chkval in chk:
        # for sid in student_ids:
        #         student = StudentDetail.objects.get(sid=sid)
        #         print(sid, chk)
        #         if chk:
        #             student.access_stu = True
        #             print("Hello MD")
        #         # else:
        #         #     student.access_stu = True
        #         #     print("Hello FBD")
        #             student.save()



        

        # for sid in student_ids:
        #     student = StudentDetail.objects.get(sid=sid)
        #     print(student,"mohnihs1")
        #     if chk:
        #         student.access_stu = True
        #         print(chk,'mohs2')
        #     else:
        #         student.access_stu = False
        #         print(chk,'mohs3')
        #     student.save()




            # student = StudentDetail.objects.get(sid=ids)
            # student.access_stu = selected_students == 'on'
            # student.save()




        # Add a success message to be displayed in the UI
        # messages.success(request, 'Access updated successfully.')
        
        # Redirect to the same page after updating the access field
        return redirect('view_students')
    
    context = {'students': student}
    return render(request, 'view_student.html', context)

def flashcard(request):
    if "nm" not in request.session:
        return redirect('../login/1')
    if request.method == 'POST':
        set_title = request.POST.get('set_title')
        sub_id = request.POST.get('sub_id_fk')
        subject = Subject.objects.get(sub_id=sub_id)
        student_id = request.POST.get('sid_fk') 
        course_id = request.POST.get('cid_fk')
        courses = CourseDetail.objects.get(cid = course_id)
        term = request.POST.get('term')
        desc = request.POST.get('desc')

        # Save the note to the database
        if StudentDetail.objects.filter(sid=student_id).exists():
            student=StudentDetail.objects.get(sid=student_id)
            flashcard = Flashcard(set_title=set_title, sub_id_fk=subject, sid_fk=student, cid_fk=courses,term=term,desc=desc)
            flashcard.save()
        else:
            return HttpResponse("Invalid Try")
    
    # Get all the subjects for the subject dropdown
    subjects = Subject.objects.all()
    student = StudentDetail.objects.all()
    course = CourseDetail.objects.all()

    return render(request, 'flashcard.html', {'subjects': subjects, 'student': student, 'course': course})

def announcement(request):
    if "nm" not in request.session:
        return redirect('../login/1')
    if request.method == 'POST':
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        sub_id = request.POST.get('sub_id_fk')
        subject = Subject.objects.get(sub_id=sub_id)
        faculty_id = request.POST.get('fid_fk') # You can set the faculty ID as required
        course_id = request.POST.get('cid_fk')
        courses = CourseDetail.objects.get(cid = course_id)
        date = datetime.datetime.now()

        # Save the note to the database
        if FacultyDetail.objects.filter(fid=faculty_id).exists():
            faculty=FacultyDetail.objects.get(fid=faculty_id)
            announcement = Announcement(title=title, desc=desc, sub_id_fk=subject, fid_fk=faculty, cid_fk=courses,date=date)
            announcement.save()
        else:
            return HttpResponse("Invalid Try")
    
    # Get all the subjects for the subject dropdown
    subjects = Subject.objects.all()
    faculty = FacultyDetail.objects.all()
    course = CourseDetail.objects.all()
    return render(request, 'announcement.html', {'subjects': subjects, 'faculty': faculty, 'course': course})

def view_flashcard(request):
    context = {}
    if request.session['login_type'] in ['faculty', 'student']:
        flashcard = Flashcard.objects.all().order_by('set_title')
        context = {'flashcards': flashcard}
    return render(request, 'view_flashcard.html',context)
         

def view_announcement(request):
    context = {}
    if request.session['login_type'] in ['faculty', 'student']:
        announcement = Announcement.objects.all().order_by('date')[::-1]
        context = {'announcements': announcement}
    return render(request, 'view_announcement.html',context)

def create_forum(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        topic = request.POST.get('topic')
        description = request.POST.get('description')
        created_by = request.POST.get('created_by')

        # Save the form data to the database
        forum1 = Forum(name=name, topic=topic, description=description, created_by = created_by)
        forum1.save()
        return redirect('addInForum')  # Redirect to the addInForum URL

    return render(request, 'addInForum.html')

# def addInDiscussion(request):
#     if request.method == 'POST':
#         discuss = request.POST.get('discuss')
#         forum_id = request.POST.get('forum_id')

#         # Get the corresponding forum object
#         forum2 = Forum.objects.get(forum_id=forum_id)

#         # Create a new discussion object
#         discussion = Discussion(discuss=discuss, forum=forum2)
#         discussion.save()

#         return redirect('addInDiscussion')  # Redirect to the discussionforum URL

#     # Fetch the forums to display in the form
#     forums = Forum.objects.all()
#     discussions = Discussion.objects.all()

#     return render(request, 'addInDiscussion.html', {'forums': forums, 'discussions': discussions})

def discussionforum(request):
    # forums = Forum.objects.all()
    # discussions = Discussion.objects.all()  

    # return render(request, 'discussionforum.html', {'forums': forums, 'discussions': discussions})

    # *****************
    if request.method == 'POST':
        discuss = request.POST.get('discuss')
        forum_id = request.POST.get('forum_id')
        created_by = request.POST.get('created_by')

        # Get the corresponding forum object
        forum2 = Forum.objects.get(forum_id=forum_id)

        # Create a new discussion object
        discussion = Discussion(discuss=discuss, forum=forum2, created_by=created_by)
        discussion.save()

        return redirect('discussionforum')  # Redirect to the discussionforum URL

    # Fetch the forums to display in the form
    forums = Forum.objects.all()
    discussions = Discussion.objects.all()

    return render(request, 'discussionforum.html', {'forums': forums, 'discussions': discussions})




    