from django.test import TestCase
from ..forms import NewTaskForm


class NewTaskFormTests(TestCase):
    def test_edit_task_field_name(self):
        form = NewTaskForm()
        self.assertTrue(form.fields['name'].label == None or form.fields['name'].label == 'name')

    def test_edit_task_field_description(self):
        form = NewTaskForm()
        self.assertTrue(form.fields['description'].label ==
                        None or form.fields['description'].label == 'description')

    def test_edit_task_field_name_help_text(self):
        form = NewTaskForm()
        self.assertEqual(form.fields['name'].help_text,  'The Maximium Length is 40')

    def test_edit_task_field_description_help_text(self):
        form = NewTaskForm()
        self.assertEqual(form.fields['description'].help_text, 'The Maximium Length is 4000')

    def test_edit_task_field_name_max_length(self):
        form = NewTaskForm()
        self.assertEqual(form.fields['name'].max_length,  40)

    def test_edit_task_field_description_max_length(self):
        form = NewTaskForm()
        self.assertEqual(form.fields['description'].max_length,  4000)

    def test_edit_task_field_name_placeholder(self):
        form = NewTaskForm()
        self.assertEqual(form.fields['name'].widget.attrs['placeholder'],
                         'Write here a short task name')

    def test_edit_task_field_description_placeholder(self):
        form = NewTaskForm()
        self.assertEqual(form.fields['description'].widget.attrs['placeholder'],
                         'Write here the new task.')

    def test_edit_task_field_name_size(self):
        form = NewTaskForm()
        self.assertEqual(form.fields['name'].widget.attrs['size'], 40)

    def test_edit_task_field_description_size(self):
        form = NewTaskForm()
        self.assertEqual(form.fields['description'].widget.attrs['size'], 4000)

    def test_edit_task_field_name_rows(self):
        form = NewTaskForm()
        self.assertEqual(form.fields['name'].widget.attrs['rows'], 1)
