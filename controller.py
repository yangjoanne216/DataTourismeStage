class ApplicationController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def on_submit(self, code_postal, etiqutte, departement, file_name):
        for update_type, *args in self.model.write_to_csv(code_postal, etiqutte, departement, file_name):
            if update_type == 'progress':
                self.view.update_progress(*args)
            elif update_type == 'message':
                self.view.update_status_message(*args, process=True)

