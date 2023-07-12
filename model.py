import json
import pandas as pd
import csv
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse

class DataProcessor:
    def __init__(self, root_dir, output_filename):
        self.root_dir = root_dir
        self.output_filename = output_filename
        self.data = []
        self.view = None

    def set_view(self,view):
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

    def find_depth(self, key, depth, class_hierarchy, visited=None):
        if visited is None:
            visited = set()  # 使用集合存储已访问过的键，避免重复访问
        if key in visited:  # 如果键已经访问过，直接返回当前深度，停止递归
            return depth
        visited.add(key)
        parent = class_hierarchy.get(key)  # 使用get方法，当键不存在时返回None
        if parent is None:
            return depth
        else:
            return self.find_depth(parent, depth + 1, class_hierarchy, visited)

    def formaliserEtiquette(self, csv_file_in, csv_file_out):
        with open("ressource/classes.html", 'r', encoding='utf-8') as f:
            html = f.read()
        soup = BeautifulSoup(html, 'html.parser')
        class_hierarchy = {}

        for div in soup.find_all('div', {'class': 'entity'}):
            if 'id' in div.attrs:  # 判断 'id' 是否在 div 的属性中
                class_name = div['id']
                if urlparse(class_name).path:
                    class_name = urlparse(class_name).path.split('/')[-1]
                superclass = None
                description = div.find('dl', {'class': 'description'})
                if description:
                    dd_tag = description.find('dd')
                    if dd_tag:
                        superclass_tag = dd_tag.find('a')
                        if superclass_tag:
                            superclass_url = superclass_tag.get('href')
                            if superclass_url:
                                if superclass_url.startswith('#'):
                                    superclass = superclass_url.replace('#', '')  # 去掉超类中的 '#'
                                else:
                                    superclass = urlparse(superclass_url).path.split('/')[-1]  # 提取超类 URL 的最后一个部分
                class_hierarchy[class_name] = superclass

        # 创建一个空的 set 来存储层次为3，4，5和6的类
        desired_classes3 = set()
        desired_classes4 = set()
        desired_classes5 = set()
        desired_classes6 = set()

        # 遍历类层次字典
        for key in class_hierarchy.keys():
            # 对每一个键执行 find_depth 函数
            depth = self.find_depth(key, 1, class_hierarchy)
            # 如果返回的层次深度为5或6，则将该键添加到 set 中
            if depth == 3:
                desired_classes3.add(key)
            if depth == 4:
                desired_classes4.add(key)
            if depth == 5:
                desired_classes5.add(key)
            if depth == 6:
                desired_classes6.add(key)

        with open(csv_file_in, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)

        # 处理每一行
        for row in rows:
            if len(row) < 17:  # 如果行的长度小于17
                row.extend([''] * (17 - len(row)))
                # 分割第一列为项目列表
            items = row[1].split(", ")
            # 保留在 set 中的项目
            items5 = [item for item in items if item in desired_classes5]
            # 重新组合项目为一个字符串
            #row.append(", ".join(items5))
            row[15] = (", ".join(items5))
            items6 = [item for item in items if item in desired_classes6]
            #row.append(", ".join(items6))
            row[16] = (", ".join(items6))

            if row[15] is None or row[15] == '':
                items4 = [item for item in items if item in desired_classes4]
                row[15] = (", ".join(items4))
                row[16] = (", ".join(items5))

            if row[15] is None or row[15] == '' and row[16] is None or row[16] == '':
                items3 = [item for item in items if item in desired_classes3]
                row[15] = (", ".join(items3))
                row[16] = (", ".join(items4))
        with open(csv_file_out, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            fieldnames = [
                "Afficher le nom", "Étiquettes", "Rue 1", "Rue 2", "Ville",
                "État", "Pays", "Code postal", "Téléphone", "Mobile", "Email", "Site web", "Description", "Createur",
                "Publieur", "Etiquette générale", "Etiquette spécialiste"
            ]  # 列名列表
            dict_writer = csv.DictWriter(f, fieldnames=fieldnames)  # 使用列名列表创建DictWriter对象
            dict_writer.writeheader()  # 写入列名
            writer.writerows(rows)

    def count_instance(self,file_json):
        with open(file_json, 'r') as f:
            # 读取JSON数据
            data = json.load(f)
        # 打印实例的数量
        return len(data)

    def write_to_csv(self, code, etiquettes, departements,file_name):
        root_dir = 'flux/objects'
        total_files = self.count_instance('flux/index.json')
        processed_files = 0
        with open('outputCSV/'+file_name+".csv", 'w', newline='', encoding='utf-8') as f:
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
                        print("Extraction des données en cours : "+str(processed_files)+"/"+str(total_files))

        print("Fin de l'impression de toutes les données")
        #yield 'message', "Fin de l'impression de toutes les données"  # yield a status messag
        self.view.update_status_message(
            f"Fin de l'impression de toutes les données,{str(total_files)} fichiers traités", True)
        data = pd.read_csv('outputCSV/'+file_name+".csv")
        data.to_excel('outputExcel/'+file_name+".xlsx")

 #       self.formaliserEtiquette('outputCSV/outputCSV.csv', 'outputCSV/outputCSV.csv')

    def filter_data(self, filters):
        pass

