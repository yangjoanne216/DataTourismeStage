from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QListView, QLabel, QProgressBar
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt

class ApplicationView(QWidget):
    def __init__(self,submit_callback, etiquettes,departements):
        super().__init__()
        self.submit_callback = submit_callback
        self.etiquettes = etiquettes
        self.departements = departements
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # code postal input
        self.entry_code_postal = QLineEdit(self)
        self.entry_code_postal.setPlaceholderText("code postal(All par défault)")
        self.layout.addWidget(self.entry_code_postal)

        # Departement input
        self.layout.addWidget(QLabel('Département:'))  # Adding a label
        self.modelDepartement = QStandardItemModel(self)
        all_departement = QStandardItem('all')
        all_departement.setCheckable(True)
        self.modelDepartement.appendRow(all_departement)  # Adding 'all' checkbox
        for departement in self.departements:
            item = QStandardItem(departement)
            item.setCheckable(True)
            self.modelDepartement.appendRow(item)
        self.entry_departement = QListView(self)
        self.entry_departement.setModel(self.modelDepartement)
        self.layout.addWidget(self.entry_departement)

        # Etiquette input
        self.layout.addWidget(QLabel('Activité:'))  # Adding a label
        self.model = QStandardItemModel(self)
        all_etiquette = QStandardItem('all')
        all_etiquette.setCheckable(True)
        self.model.appendRow(all_etiquette)  # Adding 'all' checkbox
        for etiquette in self.etiquettes:
            item = QStandardItem(etiquette)
            item.setCheckable(True)
            self.model.appendRow(item)
        self.entry_etiqutte = QListView(self)
        self.entry_etiqutte.setModel(self.model)
        self.layout.addWidget(self.entry_etiqutte)

        # File name input
        self.entry_file_name = QLineEdit(self)
        self.entry_file_name.setPlaceholderText("Nom du fichier de sortie")
        self.layout.addWidget(self.entry_file_name)

        # Submit button
        self.submit_button = QPushButton('Soumettre', self)
        self.submit_button.clicked.connect(self.submit)
        self.layout.addWidget(self.submit_button)

        # Progress bar
        self.progress_bar = QProgressBar(self)
        self.layout.addWidget(self.progress_bar)

        # Status label for the total and processed files
        self.status_label = QLabel(self)
        self.layout.addWidget(self.status_label)

        # Status label for the process start and end
        self.process_label = QLabel(self)
        self.layout.addWidget(self.process_label)

    def submit(self):
        code_postal = self.entry_code_postal.text()
        file_name = self.entry_file_name.text()
        departement = [self.modelDepartement.item(i).text() for i in range(self.modelDepartement.rowCount()) if self.modelDepartement.item(i).checkState() == Qt.Checked]
        etiqutte = [self.model.item(i).text() for i in range(self.model.rowCount()) if self.model.item(i).checkState() == Qt.Checked]
        self.submit_callback(code_postal, etiqutte,departement,file_name)

    def update_status_message(self, message, process=False):
        if process:
            self.process_label.setText(message)
        else:
            self.status_label.setText(message)

    def update_progress(self, processed, total):
        self.progress_bar.setValue(int(processed / total * 100))
        progress_message = f'{processed}/{total}'
        self.update_status_message(progress_message)