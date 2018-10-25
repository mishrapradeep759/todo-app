


def make_super_user(user):
    user.is_super_user = True


def make_domain_name(email_id):
    domain_name = email_id.split("@")
    return domain_name[-1]

def assign_task(assignee, user):
    pass


def delete_task():
    pass

def complete_task(user):
    pass
