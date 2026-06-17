from .models import Task
from rest_framework import viewsets
from .Taskserializer import TaskSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from datetime import timedelta
from django.utils import timezone
from django.views.generic import TemplateView


class TaskViewSet(viewsets.ModelViewSet):

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        qs = Task.objects.filter(user=self.request.user)

        search = self.request.GET.get('q')
        due_within = self.request.GET.get('due_within')

        if search:
            search_words = search.split()
            

            for word in search_words:
                qs = qs.filter(
                    Q(title__icontains=word) | 
                    Q(description__icontains=word)
                )
            
        if due_within:
            try:
                days = int(due_within)

                today = timezone.localdate()
                limit_date = today + timedelta(days=days)

                qs = qs.filter(
                    due_date__gte=today,
                    due_date__lte=limit_date,
                )
            
            except ValueError:
                pass

        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskListView(TemplateView):
    template_name = 'task/task_list.html'


class TaskDetailView(TemplateView):
    template_name = 'task/task_detail.html'