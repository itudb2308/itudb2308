from psycopg2._psycopg import connection

from dto.Transaction import Transaction


class TransactionService:
    def __init__(self, connection: connection):
        self._connection = connection

    def transactional(self):
        transaction = self._createNewTransaction()
        def decorator(func):
            def wrapper(*args, **kwargs):
                kwargs['transaction'] = transaction
                result = None
                try:
                    result = func(*args, **kwargs)
                except Exception as e:
                    print(e.args[0])
                    kwargs["transaction"].rollback()
                    raise e
                finally:
                    kwargs["transaction"].commit()
                return result

            # Ensure that the wrapper function retains the original function's attributes
            wrapper.__name__ = func.__name__
            wrapper.__doc__ = func.__doc__

            return wrapper
        return decorator

    def _createNewTransaction(self):
        return Transaction(self._connection)
