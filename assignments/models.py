from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from stories.models import UserStory
from django.core.validators import MinValueValidator, MaxValueValidator
from tasks.models import Task

class Assignment(models.Model):

    TYPE_CHOICES = [
        ('business', 'Business Analysis'),
        ('development', 'Development'),
        ('quality', 'QA'),
        ('bug-fixing', 'Bug fixing'),
        ('deployment', 'Deployment'),
    ]

    STATUS = [
        ('pending', 'Pending'),
        ('started', 'Started'),
        ('done', 'Done'),
    ]
    
    # this field can be used to store when actually the task was assigned 
    assigned_at = models.DateTimeField(auto_now_add=True)
    user_story = models.ForeignKey(UserStory, related_name='assignments', on_delete=models.SET_NULL, null=True, blank=True)
    # the following two properties are used to store the planned start date and end date
    planned_start_date = models.DateField(null=True, blank=True)
    planned_end_date = models.DateField(null=True, blank=True)
    # the following two properties are used to store the actual start date and end date
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    # storing who created the assignment (it should be set by default and not editable)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_assignments')
    # Storing when the assignment first created (should not be edited)
    created_at = models.DateTimeField(auto_now_add=True)
    # this field is used to decide the nature of the assignment
    assignment_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='business')
    # This field is used to store the percentage of completion for an assignment.
    completion = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)], help_text="Completion percentage (0–100%)")
    # This field is used for coloring the tasks bars inside gantt chart.
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    # List of assignees (Multiple users can be working on the same assigment)
    # it is set to blanl=True because it can be created as a draft before assigning it to anyone 
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assignments')
    # this field is used to sort the assignments based on the specified order
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order']  # This ensures consistent ordering

    def __str__(self):
        return f"{self.created_by.username} assigned "
    
    def can_be_started(self):
        """Return True if all previous assignments are done."""
        previous_assignments = Assignment.objects.filter(
            user_story=self.user_story,
            sort_order__lt=self.sort_order # when using __lt means search for records having a sort_order lowe than current which means the ones before the current.
        ).order_by('sort_order')
        return all(a.status == 'done' for a in previous_assignments)

    def clean(self):
        # Called on full_clean() or during form validation
        if self.status == 'started' and not self.can_be_started():
            raise ValidationError("Cannot start this assignment before completing previous ones.")

  

    def save(self, *args, **kwargs):
        '''
        Since assignments can be created using a form submission or Ajax call
        it is better to keep the logic of sorting the order of assignment in the save fuction of the assignment model.
        '''
        super().save(*args, **kwargs)  # Save first to ensure we have an ID

        # Reorder all assignments in the same user story
        assignments = Assignment.objects.filter(user_story=self.user_story).order_by('planned_start_date', 'id')
        for index, assignment in enumerate(assignments, start=1):
            if assignment.sort_order != index:
                Assignment.objects.filter(id=assignment.id).update(sort_order=index)
