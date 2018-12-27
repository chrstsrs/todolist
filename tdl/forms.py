from django import forms
from .models import Task


class NewTaskForm(forms.ModelForm):
    name = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Write here a short task name', 'size': 40, 'rows': 1}),
                           max_length=40, help_text='The Maximium Length is 40'
                           )
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Write here the new task.', 'size': 4000}), max_length=4000,
                                  help_text='The Maximium Length is 4000'
                                  )

    class Meta:
        model = Task
        fields = ['name', 'description', ]
