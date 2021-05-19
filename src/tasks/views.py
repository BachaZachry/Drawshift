
from django.shortcuts import render,get_object_or_404,redirect
from .models import task
from django.urls import reverse
from django.views.generic import CreateView,DetailView,UpdateView,DeleteView,ListView
from .forms import taskForm ,RawtaskForm
from .serializers import taskSerializer


from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse

# Create your views here.
@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'List':'/task-list/',
        
    }
    return Response("fdvfv")
    
class taskCreateView(CreateView):
    template_name='task/task_create.html'
    form_class = taskForm
    queryset  = task.objects.all()
    def form_valid(self,form):
        print(form.cleaned_data)
        return super().form_valid(form)
        


class taskUpdateView(UpdateView):
    template_name='task/task_create.html'
    form_class = taskForm
    queryset  = task.objects.all()
    def get_object(self):
        id = self.kwargs.get("id")
        return get_object_or_404(task,id=id)


    def form_valid(self,form):
        print(form.cleaned_data)
        return super().form_valid(form)
        

class taskListView(ListView):
    template_name='task/task_list.html'
    queryset  = task.objects.all()

class taskDeleteView(DeleteView):
    template_name='task/taskdelete.html'
    queryset  = task.objects.all()
    def get_object(self):
        id = self.kwargs.get("id")
        return get_object_or_404(task,id=id)

    def get_success_url(self):
        return reverse('tasks:taskList')

class taskDetailView(DetailView):
    template_name='task/taskdetail.html'
    queryset  = task.objects.all()
    
    def get_object(self):
        id = self.kwargs.get("id")
        return get_object_or_404(task,id=id)


def task_create_view(request):
    my_form=taskForm(request.POST or None)
    if my_form.is_valid():
        my_form.save()
        my_form=taskForm()
    else:
            print(my_form.errors)
    context={
            "form":my_form
        }
    return render(request,"task/task_create.html",context)
 
def task_detail_view(request):
    obj=task.objects.get(id=1)
    context={
        'title':obj.title,
        'description':obj.description
    }
    return render(request,"task/taskdetail.html",context)

def dynamic_lookup_view(request,id):
    obj = get_object_or_404(task,id=id)
    context={
        "object":obj
    }
    return render(request,"task/taskdetail.html",context)

def dynamic_delete_view(request,id):
    obj = get_object_or_404(task,id=id)
    if request.method == "POST":
       obj.delete()
    context={
        "object":obj
    }
    return render(request,"task/taskdelete.html",context)    

def task_list_view(request):
    queryset= task.objects.all()
    context={
        "object_list":queryset
    }
    return render (request,"task/task_list.html",context)



@api_view(['GET'])
def task_list_view1(request):
    queryset= task.objects.all()
    serializer=taskSerializer(queryset,many=True)

    return Response(serializer.data)
@api_view(['GET'])
def task_detail_view1(request,pk):
    queryset=task.objects.get(id=pk)
    serializer=taskSerializer(queryset,many=False)

  
    return Response(serializer.data)


@api_view(['POST'])
def task_create_view1(request):
    serializer=taskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
  
    return Response(serializer.data)

@api_view(['POST'])
def task_update_view1(request,pk):
    queryset=task.objects.get(id=pk)

    serializer=taskSerializer(instance=queryset,data=request.data)
    if serializer.is_valid():
        serializer.save()
  
    return Response(serializer.data)




@api_view(['DELETE'])
def task_delete_view1(request,pk):
    queryset=task.objects.get(id=pk)
    queryset.delete()
    return Response("Task is deleted Succesfully")