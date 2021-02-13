// MongoDB "DDL" initialize the imdb database with names collection.
// Chris Joakim, Microsoft, 2021/02/13

use imdb

db.names.drop()
db.airports.drop()
db.createCollection("names")
db.names.ensureIndex({"pk" : 1}, {"unique" : false})
db.names.ensureIndex({"nconst" : 1}, {"unique" : false})
db.names.ensureIndex({"primaryName" : 1}, {"unique" : false})
db.names.getIndexKeys()
db.names.getIndexes()

show collections
db.names.count()
