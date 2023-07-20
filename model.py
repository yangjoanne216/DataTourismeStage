import json
import pandas as pd
import csv
import os
import ast

class DataProcessor:
    def __init__(self, root_dir, output_filename):
        self.root_dir = root_dir
        self.output_filename = output_filename
        self.data = []
        self.view = None

    def set_view(self, view):
        self.view = view

    def read_json_file(self, json_file):
        with open(json_file, 'r') as f:
            data = json.load(f)
        return data

    def extract_addresses(self, data):
        addresses = data.get("isLocatedAt", [{}])[0].get("schema:address", [{}])[0].get("schema:streetAddress", [])
        address_1 = addresses[0] if len(addresses) > 0 else None
        address_2 = addresses[1] if len(addresses) > 1 else None
        return address_1, address_2

    def extract_description(self, data):
        # Simplified version, you may want to adjust according to your requirements
        description = data.get("rdfs:comment", {}).get("fr", [None])[0]
        if description is None:
            description = data.get("hasDescription", [{}])[0].get("dc:description", {}).get("fr", [None])[0]
        return description

    def extract_telephones(self, data):
        telephones = data.get("hasContact", [{}])[0].get("schema:telephone", [])
        telephone1 = telephones[0] if len(telephones) > 0 else None
        telephone2 = telephones[1] if len(telephones) > 1 else None
        return telephone1, telephone2

    def extract_info(self, json_file):
        try:
            data = self.read_json_file(json_file)
            address_1, address_2 = self.extract_addresses(data)
            telephone1, telephone2 = self.extract_telephones(data)
            description = self.extract_description(data)

            company_info = {
                "Afficher le nom": data["rdfs:label"]["fr"][0],
                "Étiquettes": ", ".join(data["@type"]),
                "Rue 1": address_1,
                "Rue 2": address_2,
                "Ville": data["isLocatedAt"][0]["schema:address"][0]["hasAddressCity"]["rdfs:label"]["fr"][0],
                "État":
                    data["isLocatedAt"][0]["schema:address"][0]["hasAddressCity"]["isPartOfDepartment"]["rdfs:label"][
                        "fr"][
                        0],
                "Pays":
                    data["isLocatedAt"][0]["schema:address"][0]["hasAddressCity"]["isPartOfDepartment"][
                        "isPartOfRegion"][
                        "isPartOfCountry"]["rdfs:label"]["fr"][0],
                "Code postal": data["isLocatedAt"][0]["schema:address"][0]["schema:postalCode"],
                "Téléphone": telephone1,
                "Mobile": telephone2,
                "Email": data["hasContact"][0]["schema:email"][0] if "hasContact" in data and "schema:email" in
                                                                     data["hasContact"][0] else None,
                "Site web": data["hasContact"][0]["foaf:homepage"][0] if "hasContact" in data and "foaf:homepage" in
                                                                         data["hasContact"][0] else None,
                "Description": description,
                "Createur": data["hasBeenCreatedBy"][
                    "schema:legalName"] if "hasBeenCreatedBy" in data and "schema:legalName" in data[
                    "hasBeenCreatedBy"] else None,
                "Publieur": data["hasBeenPublishedBy"][0][
                    "schema:legalName"] if "hasBeenPublishedBy" in data and "schema:legalName" in
                                           data["hasBeenPublishedBy"][0] else None

            }
            return company_info
        except Exception as e:
            print(f"处理文件 {json_file} 时发生错误： {str(e)}")
            print(f"error line:{e.__traceback__.tb_lineno}")
            if "@id" in data:
                print(f"错误发生在 {data['@id']}")
            return None

    def dfs(self, class_dict, start_class, depth=0, max_depth=float('inf')):
        level_dict = {}
        stack = [(start_class, depth)]
        while stack:
            node, level = stack.pop()
            if int(level) < max_depth:
                if level not in level_dict:
                    level_dict[level] = [node]
                else:
                    level_dict[level].append(node)
                # print(f'Class: {node}, Level: {level}')
                # for key, value in class_dict.items():
                # value ==stack.pop()
                for key, value in class_dict.items():
                    if value == node:
                        stack.append((key, level + 1))

        for level in sorted(level_dict.keys()):
            print(f'Level {level}:')
            for class_name in level_dict[level]:
                print(f'    {class_name}')
        return level_dict

    def translate_to_french(slef,english_str,translation_dict,j):
        print("En cours " +str(j) + "ème traduction de l'anglais vers le français: "+english_str+"\n")
        j=j+1
        # 检查字典中是否有对应的法语翻译
        if english_str in translation_dict:
            return j,translation_dict[english_str]
        else:
            print("can't find"+english_str)
            return j,english_str

    def formaliserEtiquette(self, csv_file_in, csv_file_out, level_dict):
        level_classes = [level_dict.get(i, []) for i in range(5)]
        with open(csv_file_in, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)

        # 处理表头
        headers = rows[0]
        for i in range(5):
            headers.append(f"étiquette niveau {i}")
        rows[0] = headers

        with open("ressource/Anglais_Francais_dict.txt", 'r') as file:
            dict_str = file.read()
            translation_dict = ast.literal_eval(dict_str)
        j = 0
        for row in rows[1:]:
            items = row[1].split(", ")
            for i, level_class in enumerate(level_classes):
                # Filter items based on the class level
                filtered_items = [item for item in items if item in level_class]
                filtered_items_translate=[]
                for filtered_item in filtered_items:
                    j,filtered_item_translate = self.translate_to_french(filtered_item,translation_dict,j)
                    filtered_items_translate.append(filtered_item_translate)
                row.append(", ".join(filtered_items_translate))
                if row[15 + i] is None or row[15 + i] == '':
                    row[15 + i] = ", ".join(filtered_items_translate)
        print("fini tranlated")
        with open(csv_file_out, 'w', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerows(rows)

    def count_instance(self, file_json):
        with open(file_json, 'r') as f:
            # 读取JSON数据
            data = json.load(f)
        # 打印实例的数量
        return len(data)

    def write_to_csv(self, code, etiquettes, departements, file_name):
        root_dir = 'flux/objects'
        total_files = self.count_instance('flux/index.json')
        processed_files = 0
        with open('outputCSV/' + file_name + ".csv", 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                "Afficher le nom", "Étiquettes", "Rue 1", "Rue 2", "Ville",
                "État", "Pays", "Code postal", "Téléphone", "Mobile", "Email", "Site web", "Description", "Createur",
                "Publieur"
            ])
            writer.writeheader()
            print("Extraction des données en cours, un total de " + str(total_files) + " fichiers à traiter")
            self.view.update_status_message(
                f"Extraction des données en cours, un total de {str(total_files)} fichiers à traiter", True)

            for subdir, dirs, files in os.walk(root_dir):
                for file in files:
                    if file.endswith('.json'):
                        processed_files += 1
                        yield 'progress', processed_files, total_files  # yield a progress update
                        json_file = os.path.join(subdir, file)
                        company_info = self.extract_info(json_file)

                        # Convert the Étiquettes to list
                        company_etiquettes = company_info["Étiquettes"].split(', ')

                        # If 'all' is not selected and the "État" field does not match any departement in the departements list, skip the record
                        if 'all' not in departements and company_info["État"] not in departements:
                            continue

                        # When both code and etiquettes are not empty, perform filtering
                        if code and etiquettes and not ('all' in etiquettes):
                            if company_info["Code postal"] == code and (
                                    any(e in company_etiquettes for e in etiquettes)):
                                writer.writerow(company_info)
                        # When code is not empty and etiquettes are empty, only filter based on code
                        elif code:
                            if company_info["Code postal"] == code:
                                writer.writerow(company_info)
                        # When code is empty and etiquettes are not empty, only filter based on etiquettes
                        elif etiquettes and not ('all' in etiquettes):
                            if any(e in company_etiquettes for e in etiquettes):
                                writer.writerow(company_info)
                        # When both code and etiquettes are empty or 'all' is selected, no filtering is performed
                        else:
                            writer.writerow(company_info)
                        print("Extraction des données en cours : " + str(processed_files) + "/" + str(total_files))
        # yield 'message', "Fin de l'impression de toutes les données"  # yield a status messag
        self.view.update_status_message(
            f"Les données ont été lues avec succès.,{str(total_files)} fichiers traités", True)
        print("*****************************\nFin de l'impression de toutes les données\n*****************************\n")

        with open("ressource/class_hierarchy.txt", 'r') as file:
            dict_str = file.read()
            class_hierarchy = ast.literal_eval(dict_str)
        level_dict = self.dfs(class_hierarchy, 'PointOfInterest', max_depth=6)
        self.formaliserEtiquette('outputCSV/' + file_name + ".csv", 'outputCSV/' + file_name + ".csv", level_dict)
        data = pd.read_csv('outputCSV/' + file_name + ".csv")
        self.view.update_status_message(
            f"La sortie du fichier CSV se termine.,{str(total_files)} fichiers traités", True)
        print("*****************************\nLa sortie du fichier csv se termine.\n*****************************\n")
        data.to_excel('outputExcel/' + file_name + ".xlsx")
        self.view.update_status_message(
            f"La sortie du fichier Excel se termine.\nLe processus se termine.\nVous pouvez resélectionner le fichier suivant à sortir.\n", True)
        print("*****************************\nLa sortie du fichier Excel se termine.\nLe processus se termine.\nVous pouvez resélectionner le fichier suivant à sortir.\n*****************************\n")

    def filter_data(self, filters):
        pass
