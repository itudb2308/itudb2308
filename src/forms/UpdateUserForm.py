from dto.Transaction import Transaction
from .UserForm import UserForm


class UpdateUserForm(UserForm):
    def __init__(self, service, transaction: Transaction, *args, **kwargs):
        super(UpdateUserForm, self).__init__(service, transaction, *args, **kwargs)
        self.submit.label.text = "Update User"
