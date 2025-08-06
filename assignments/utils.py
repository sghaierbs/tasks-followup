



def update_user_story_status(user_story):
    assignments = user_story.assignments.all().order_by('sort_order')
    current_assignment = None
    if not assignments.exists():
        user_story.status = 'Pending'
    else:
        if assignments.filter(status='done').count() == assignments.count():
            current_assignment = assignments.last()
            # since all the assignments are marked as done, we can mark the user story to completed
            user_story.status = 'Completed' #current_assignment.get_assignment_type_display()
            print("---------1---------------")
        else:
            started = assignments.filter(status='started').last()
            if started:
                print("---------2---------------")
                current_assignment = started 
                user_story.status = current_assignment.get_assignment_type_display()
            elif assignments.filter(status='done').count() > 0:
                current_assignment = assignments.filter(status='done').last() 
                user_story.status = current_assignment.get_assignment_type_display()
                print("---------3---------------")
            else:
                print(f"---------4---------------first {assignments.first().get_assignment_type_display()} sor_order: {assignments.first().sort_order}")
                print(f"---------4---------------last {assignments.last().get_assignment_type_display()} sor_order: {assignments.last().sort_order}")
                current_assignment = assignments.first() 
                user_story.status = current_assignment.get_assignment_type_display()
    if current_assignment and current_assignment.assignee:
        user_story.assignee = current_assignment.assignee 
    else:
        user_story.assignee = None
    user_story.save()