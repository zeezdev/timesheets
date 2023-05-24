from database import execute_statement


class ObjectsRollback:

    def __init__(self):
        self.objects_to_rollback = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for table, obj_id in self.objects_to_rollback:
            execute_statement(f'DELETE FROM {table} WHERE id=?', obj_id)

    def add_for_rollback(self, table, obj_id):
        self.objects_to_rollback.append((table, obj_id))
