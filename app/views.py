from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from app.verify import authentication, form_varification
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from sklearn.feature_extraction.text import CountVectorizer
from .form import question_paper_form
from app.models import *
import pandas as pd
import pickle
import numpy as np
import csv
from io import StringIO
import random

# # Load the model from a file
with open("dataset/blooms_level.pkl", "rb") as f:
    blooms_model = pickle.load(f)
with open("dataset/blooms_vector.pkl", "rb") as f:
    blooms_vector = pickle.load(f)

# # Create your views here.
def index(request):
    # return HttpResponse("This is Home page")    
    return render(request, "index.html")

def log_in(request):
    if request.method == "POST":
        # return HttpResponse("This is Home page")  
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username = username, password = password)

        if user is not None:
            login(request, user)
            messages.success(request, "Log In Successful...!")
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid User...!")
            return redirect("log_in")
    # return HttpResponse("This is Home page")    
    return render(request, "log_in.html")

def register(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']
        password = request.POST['password']
        password1 = request.POST['password1']
        # print(fname, contact_no, ussername)
        verify = authentication(fname, lname, password, password1)
        if verify == "success":
            user = User.objects.create_user(username, password, password1)          #create_user
            user.first_name = fname
            user.last_name = lname
            user.save()
            messages.success(request, "Your Account has been Created.")
            return redirect("/")
            
        else:
            messages.error(request, verify)
            return redirect("register")
    # return HttpResponse("This is Home page")    
    return render(request, "register.html")


@login_required(login_url="log_in")
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def log_out(request):
    logout(request)
    messages.success(request, "Log out Successfuly...!")
    return redirect("/")


def create_sets(data, n):
    sets = []
    for _ in range(n):
        unique_strings = set(random.sample(data, 13))
        length = len(unique_strings)
        if length < 13:
            remain = 13-length
            unique_strings = list(unique_strings)+list(set(random.sample(data, remain)))
        sets.append(unique_strings)
    return sets

def create_semester_sets(data, n):
    sets = []
    for _ in range(n):
        unique_strings = set(random.sample(data, 26))
        length = len(unique_strings)
        if length < 25:
            remain = 25-length
            unique_strings = list(unique_strings)+list(set(random.sample(data, remain)))
            print(unique_strings,len(unique_strings))
        sets.append(unique_strings)
    return sets

@login_required(login_url="log_in")
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def dashboard(request):
    context = {
        'fname': request.user.first_name, 
        'form' : question_paper_form(),
        }
    if request.method == "POST":
        form = question_paper_form(request.POST, request.FILES)
        try:
            if form.is_valid():
                college_name = form.cleaned_data['college_name']
                branch_name = form.cleaned_data['branch_name']
                semester = form.cleaned_data['semester']
                subject_name = form.cleaned_data['subject_name']
                year = form.cleaned_data['year']
                faculty = form.cleaned_data['faculty']
                date = form.cleaned_data['date']
                qb = form.cleaned_data['qb']
                paper_format = form.cleaned_data['paper_format']
                number_of_sets = form.cleaned_data['number_of_sets']
                number_of_sets = int(number_of_sets)
                marks_format = request.POST.get('marks_format')
                print(marks_format)
                verify_from = form_varification(faculty)
                if verify_from == "Success":
                    # Load the saved model
                    data = []
                    csv_data = qb.read().decode('utf-8', errors='replace')
                    csv_reader = csv.reader(StringIO(csv_data))
                    for row in csv_reader:
                        data.append(row[0])
                    data.pop(0)
                    if paper_format == '30 Marks':
                        sets = create_sets(data, number_of_sets)
                        subject_data = Subject_data.objects.create(
                            college_name = college_name, 
                            branch_name = branch_name, 
                            semester = semester, 
                            subject_name = subject_name,
                            year = year, faculty = faculty,
                            qb = qb, date=date,
                            paper_format = paper_format,
                            number_of_sets = int(number_of_sets),
                            marks_format = marks_format
                            )
                        subject_data.save()
                        for paper_set in sets:
                            paper_set = list(paper_set)
                            X_new = blooms_vector.transform(paper_set)
                            # Make predictions using the loaded model
                            y_new_pred = blooms_model.predict(X_new)
                            # Add the predicted Bloom's level to the questions
                            questions_with_blooms = pd.DataFrame({'question': paper_set, 
                            'blooms_level': y_new_pred})
                            # Print the questions with their Bloom's level
                            print(questions_with_blooms)
                            que_blooms = questions_with_blooms['blooms_level']
                            obj = MidSemPaperSet.objects.create(paper=subject_data,
                            q1 = paper_set[0],q2 = paper_set[1],
                            q3 = paper_set[2],q4 = paper_set[3],
                            q5 = paper_set[4],q6 = paper_set[5],
                            q7 = paper_set[6],q8 = paper_set[7],
                            q9 = paper_set[8],q10 = paper_set[9],
                            q11 = paper_set[10],q12 = paper_set[11],
                            bl1 = que_blooms[0],bl2 = que_blooms[1],
                            bl3 = que_blooms[2],bl4 = que_blooms[3],
                            bl5 = que_blooms[4],bl6= que_blooms[5],
                            bl7 = que_blooms[6],bl8 = que_blooms[7],
                            bl9 = que_blooms[8],bl10 = que_blooms[9],
                            bl11 = que_blooms[10], bl12 = que_blooms[11]
                            )
                    elif paper_format == '70 Marks':
                        sets = create_semester_sets(data, number_of_sets)
                        subject_data = Subject_data.objects.create(
                            college_name = college_name, 
                            branch_name = branch_name, 
                            semester = semester, 
                            subject_name = subject_name,
                            year = year, faculty = faculty,
                            qb = qb, date=date,
                            paper_format = paper_format,
                            number_of_sets = int(number_of_sets),
                            marks_format = marks_format
                            )
                        subject_data.save()
                        for paper_set in sets:
                            paper_set = list(paper_set)
                            X_new = blooms_vector.transform(paper_set)
                            y_new_pred = blooms_model.predict(X_new)
                            questions_with_blooms = pd.DataFrame({'question': paper_set, 
                            'blooms_level': y_new_pred})
                            print(questions_with_blooms)
                            que_blooms = questions_with_blooms['blooms_level']
                            obj = SemesterPaperSet.objects.create(paper=subject_data,
                                q1 = paper_set[0], q2 = paper_set[1],
                                q3 = paper_set[2], q4 = paper_set[3],
                                q5 = paper_set[4], q6 = paper_set[5],
                                q7 = paper_set[6], q8 = paper_set[7],
                                q9 = paper_set[8], q10 = paper_set[9],
                                q11 = paper_set[10], q12 = paper_set[11],
                                q13 = paper_set[12], q14 =paper_set[13],
                                q15 = paper_set[14], q16 =paper_set[15],
                                q17 = paper_set[16], q18 =paper_set[17],
                                bl1 = que_blooms[0],bl2 = que_blooms[1],
                                bl3 = que_blooms[2],bl4 = que_blooms[3],
                                bl5 = que_blooms[4],bl6= que_blooms[5],
                                bl7 = que_blooms[6],bl8 = que_blooms[7],
                                bl9 = que_blooms[8],bl10 = que_blooms[9],
                                bl11 = que_blooms[10], bl12 = que_blooms[11],
                                bl13 = que_blooms[12], bl14 = que_blooms[13],
                                bl15 = que_blooms[14], bl16 = que_blooms[15],
                                bl17 = que_blooms[16], bl18 = que_blooms[17])

                            if marks_format == "Six_Six_Five_EndSem":
                                obj.q19 = paper_set[18]
                                obj.q20 = paper_set[19]
                                obj.q21 = paper_set[20]
                                obj.q22 = paper_set[21]
                                obj.q23 = paper_set[22]
                                obj.q24 = paper_set[23]
                                obj.bl19 = que_blooms[18]
                                obj.bl20 = que_blooms[19]
                                obj.bl21 = que_blooms[20]
                                obj.bl22 = que_blooms[21]
                                obj.bl23 = que_blooms[22]
                                obj.bl24 = que_blooms[23]
                                obj.save()
                    return redirect("result")
                    ### Backup Code
                else:
                    messages.error(request, verify_from)
                    return redirect("dashboard")
            else:
                messages.error(request, "Invalid Date")
                return redirect("dashboard")
        except Exception as e:
            print(str(e))
            print(e)
            messages.error(request, "Uploaded Questions are Not Appropriate!!!")
            return redirect("dashboard")
    return render(request, "dashboard.html",context)

@login_required(login_url="log_in")
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def result(request):
    subject_data = Subject_data.objects.last()
    context = {
        'fname': request.user.first_name, 
        'subject_data' : subject_data,
        }
    if subject_data.paper_format == '30 Marks':
        context['midsem_papers'] = subject_data.midsem_paper.all()
        return render(request, "midsem.html",context)
    elif subject_data.paper_format == '70 Marks':
        context['semester_papers'] = subject_data.semester_paper.all()
        print(subject_data.semester_paper.all())
        return render(request, "semester.html",context)
    if request.method == "POST":
        return redirect("print")
    return render(request, "midsem.html",context)
