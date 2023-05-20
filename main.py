import couchdb
from menu import Menu

couch = couchdb.CouchDB()

# docs = couch.find_all_eq_documents("trees", {"art": "Eiche"})
# [print(doc) for doc in docs]

Menu()