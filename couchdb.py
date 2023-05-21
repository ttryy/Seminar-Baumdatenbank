import io
import os.path

import requests
import uuid  # CouchDB bietet auch unter /_uuids UUIDs an
import json
from PIL import Image

class CouchDB:

    def __init__(self):
        self.default = "http://admin:baumdb@127.0.0.1:5984/"

    def create_database(self, database):
        r = requests.put(f"{self.default}{database}")
        rdata = json.loads(r.content.decode("utf-8"))
        self.print_response(r)
        if r.status_code == 202 and rdata["ok"]:
            return True
        else:
            return False

    def insert(self, database, payload):
        r = requests.put(f"{self.default}{database}/{uuid.uuid4()}", json=payload)
        rdata = json.loads(r.content.decode("utf-8"))
        self.print_response(r)
        if r.status_code == 202 and rdata["ok"]:
            return Doc(id=rdata["id"], rev=rdata["rev"], database=database, content=payload)
        else:
            return None

    def update_id(self, database, id, rev, payload):
        r = requests.put(f"{self.default}{database}/{id}?rev={rev}", json=payload)
        rdata = json.loads(r.content.decode("utf-8"))
        self.print_response(r)
        if r.status_code == 201 and rdata["ok"]:
            return Doc(id=rdata["id"], rev=rdata["rev"], database=database, content=payload)
        else:
            return None

    def update_doc(self, document, payload):
        return self.update_id(document.database, document.id, document.rev, payload)

    def delete_id(self, database, id, rev):
        r = requests.delete(f"{self.default}{database}/{id}?rev={rev}")
        rdata = json.loads(r.content.decode("utf-8"))
        self.print_response(r)
        if r.status_code == 202 and rdata["ok"]:
            return None

    def delete(self, document):
        return self.delete_id(document.database, document.id, document.rev)

    def attachment(self, document, filepath):
        headers = {'Content-Type': 'image/jpeg'}
        if os.path.exists(filepath):
            with open(filepath, "rb") as file:
                r = requests.put(f"{self.default}{document.database}/{document.id}/image.jpg?rev={document.rev}",
                                 data=file, headers=headers)
                rdata = json.loads(r.content.decode("utf-8"))
                self.print_response(r)
                if r.status_code == 202 and rdata["ok"]:
                    document.rev = rdata["rev"]
                    return document
                else:
                    return document
        else:
            print("Datei nicht gefunden")

    def get_attachment(self, document):
        r = requests.get(f"{self.default}{document.database}/{document.id}/image.jpg")
        if r.status_code == 200:
            image = Image.open(io.BytesIO(r.content))
            return image
        else:
            return None

    def get_document_from_response(self, database, content):
        data = json.loads(content.decode("utf-8"))
        return self.get_document_from_json(database, data)

    def get_document_from_json(self, database, jsondata):
        _id = jsondata["_id"]
        _rev = jsondata["_rev"]
        del jsondata["_id"]
        del jsondata["_rev"]
        return Doc(_id, _rev, database, jsondata)

    def get_document_id(self, database, id, rev=None):
        url = f"{self.default}{database}/{id}"
        if rev is not None:
            url = f"{url}?rev={rev}"
        r = requests.get(url)
        self.print_response(r)
        if r.status_code == 200:
            return self.get_document_from_response(database, r.content)
        else:
            return None

    def get_document(self, document):
        return self.get_document_id(document.database, document.id, document.rev)

    def get_all_documents(self, database):
        r = requests.get(f"{self.default}{database}/_all_docs?include_docs=true")
        rdata = json.loads(r.content.decode("utf-8"))
        self.print_response(r)
        if r.status_code == 200:
            return [self.get_document_from_json(database, row['doc']) for row in rdata['rows']]

    def find_all_eq_documents(self, database, filter):
        # { "art": "Eiche" }, { "alter": "23" }, { "gesundheitszustand": "sehr gut" }, { "standort": "Park" }
        cleaned_filter = {}
        for key in filter:
            if not filter[key] == "":
                cleaned_filter[key] = filter[key]

        if len(cleaned_filter) == 0:
            return self.remove_design_documents(self.get_all_documents(database))

        filter_json = {"selector": {"$and": [cleaned_filter]}}
        r = requests.post(f"{self.default}{database}/_find", json=filter_json)
        rdata = json.loads(r.content.decode("utf-8"))
        self.print_response(r)
        if r.status_code == 200:
            return [self.get_document_from_json(database, doc) for doc in rdata['docs']]

    def remove_design_documents(self, documents):
        updated_documents = []
        for document in documents:
            if "_design" not in document.id:
                updated_documents.append(document)
        return updated_documents

    def get_view(self, database, design, view, group=False):
        r = requests.get(f"{self.default}{database}/_design/{design}/_view/{view}?group={group}")
        rdata = json.loads(r.content.decode("utf-8"))
        self.print_response(r)
        if r.status_code == 200:
            return rdata
        else:
            return None

    def print_response(self, res):
        print(res.url)
        print(res.content.decode("utf-8"))


class Doc:
    def __init__(self, id, rev, database, content):
        self.id = id
        self.rev = rev
        self.database = database
        self.content = content

    def __str__(self):
        return f"id: {self.id}, rev: {self.rev}, content: {self.content}"
