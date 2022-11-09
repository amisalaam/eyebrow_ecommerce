from django.shortcuts import render,redirect
# from django.contrib import messages

# from home.views import home
# from .models import Account
# # from .forms import StudentRegistration
# from django.contrib.auth.models import User
# from django.contrib.auth.decorators import user_passes_test
# from django.contrib.auth.decorators import login_required




# # Create your views here.
# @user_passes_test(lambda u: u.is_superuser,login_url=home)
# @login_required(login_url='signin')
# def add_show(request):

#     stud = User.objects.all()
#     return render(request, 'crud/addandshow.html', {'stu': stud})
    

# @user_passes_test(lambda u: u.is_superuser,login_url=home)
# @login_required(login_url='signin')
# def delete_data(request, id):
#     if request.method == 'POST':
#         pi = User.objects.get(pk = id)
#         pi.delete()
#         messages.info(request, 'Deleted Succefully')
#     return redirect('addandshow')

# @user_passes_test(lambda u: u.is_superuser,login_url=home)
# @login_required(login_url='signin')
# def update_data(request, id):
#     if request.method == 'POST':
#         pi = User.objects.get(pk=id)
        
#         fm = StudentRegistration(request.POST, instance=pi)
        
#         if fm.is_valid():
#             fm.save()
#             messages.info(request, 'Edited Succefully')
        
#     else:
#         pi = User.objects.get(pk = id)
#         fm = StudentRegistration(instance=pi)
        
#     return render(request, 'crud/updatestudent.html', {'form' : fm})


# @user_passes_test(lambda u: u.is_superuser,login_url=home)
# @login_required(login_url='signin')
# def search_username(request):
#     searched = request.GET['search']
#     searchnames = User.objects.filter(username__contains = searched)
#     return render(request, 'crud/addandshow.html', {'stu' : searchnames})

    