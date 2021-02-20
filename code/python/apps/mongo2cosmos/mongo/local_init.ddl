// MongoDB "DDL" initialize the "migrate" database and its collections.
// Chris Joakim, Microsoft, 2021/02/20

use migrate

db.name_basics.drop()
db.createCollection("name_basics")
db.name_basics.ensureIndex({"pk" : 1}, {"unique" : false})
db.name_basics.ensureIndex({"doctype" : 1}, {"unique" : false})
db.name_basics.ensureIndex({"primaryName" : 1}, {"unique" : false})
db.name_basics.ensureIndex({"birthYear" : 1}, {"unique" : false})
db.name_basics.getIndexKeys()
db.name_basics.getIndexes()

db.title_basics.drop()
db.createCollection("title_basics")
db.title_basics.ensureIndex({"pk" : 1}, {"unique" : false})
db.title_basics.ensureIndex({"doctype" : 1}, {"unique" : false})
db.title_basics.ensureIndex({"titleType" : 1}, {"unique" : false})
db.title_basics.ensureIndex({"primaryTitle" : 1}, {"unique" : false})
db.title_basics.ensureIndex({"startYear" : 1}, {"unique" : false})
db.title_basics.getIndexKeys()
db.title_basics.getIndexes()

show collections
