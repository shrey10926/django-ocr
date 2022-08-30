from django.shortcuts import render, redirect
from app1.forms import UserUploadForm
from app1.models import UserUploadModel
from app1.convert import convert_file
from app1.transfer import move_dir
import os
from project1 import settings
from django.contrib.auth.decorators import login_required


# Create your views here.

# path = settings.MEDIA_ROOT
# print(path)
# i = os.listdir(path + '/converted_files')
# print(i)



@login_required
def home(request):
    
    if request.method == 'POST':
        form = UserUploadForm(request.POST, request.FILES)
        
        if form.is_valid():
            f = form.save()
            f.user = request.user
            f.save()
          
            ff = request.FILES.getlist('file')
            
            #type is weird
            # ff = request.FILES['file']
            #type is str
            # file_name = form.cleaned_data['file'].name
            #abs path and type is str
            # file_path = f.file.path
            
            #not the full path and type is weird
            # p = f.file
            
            f_list = []
            
            for i in ff:
                file_instance = UserUploadModel(file = i)
                file_instance.save()
                f_list.append(file_instance.file.path)
            
            [convert_file(j) for j in f_list]
            

            src_dir = os.getcwd()
            dest_dir = os.path.join(src_dir, 'media/converted_files')            
            move_dir(src_dir, dest_dir, '*.png')
            
            return redirect('app1-display')
        
    else:
        
        form = UserUploadForm()
    
    return render(request, 'app1/home.html', {'form' : form})

@login_required
def display(request):
    
    return render(request, 'app1/display.html')


















