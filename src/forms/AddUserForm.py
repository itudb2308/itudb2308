from .UserForm import UserForm

class AddUserForm(UserForm):
    def __init__(self, service, *args, **kwargs):
        super(AddUserForm, self).__init__(service, *args, **kwargs)
        self.submit.label.text = "Add User"
