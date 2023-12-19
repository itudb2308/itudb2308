from dto.Transaction import Transaction
from .UserForm import UserForm


class AddUserForm(UserForm):
    def __init__(self, service, transaction: Transaction, *args, **kwargs):
        super(AddUserForm, self).__init__(service, transaction, *args, **kwargs)
        self.submit.label.text = "Add User"
