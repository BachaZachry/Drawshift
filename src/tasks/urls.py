from django.urls import path,include
from .views import task_delete_view1,task_update_view1,task_list_view1,apiOverview, taskListView,taskDetailView,taskCreateView,taskUpdateView,taskDeleteView,task_detail_view1,task_create_view1


app_name='tasks'
urlpatterns=[
         path('', apiOverview, name="api-overview"),
         path('task_list/', task_list_view1, name="task-list"),
         path('task_list/<str:pk>', task_detail_view1, name="task-detail"),
         path('create/', task_create_view1, name="task-create"),
         path('update/<str:pk>', task_update_view1, name="task-update"),
         path('delete/<str:pk>', task_delete_view1, name="task-delete"),

    # path('', taskListView.as_view(), name="taskList"),
    # path('<int:id>/', taskDetailView.as_view(), name="taskDetail"),
    
    # path("create/", taskCreateView.as_view(), name="taskCreate"),
    # path('<int:id>/update/', taskUpdateView.as_view(), name="taskUpdate"),
    # path('<int:id>/delete/', taskDeleteView.as_view(), name="taskDelete"),
    #     path('api/', include('rest_framework.urls'))

]