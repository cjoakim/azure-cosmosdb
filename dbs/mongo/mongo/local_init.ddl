// MongoDB "DDL" initialize the dev database with airports collection.
// Chris Joakim, Microsoft, 2021/01/31

use dev

db.airports.drop()
db.createCollection("airports")
db.airports.ensureIndex({"pk" : 1}, {"unique" : false})
db.airports.ensureIndex({"iata_code" : 1}, {"unique" : false})
db.airports.ensureIndex({"name" : 1}, {"unique" : false})
db.airports.ensureIndex({"timezone_num" : 1}, {"unique" : false})
db.airports.getIndexKeys()
db.airports.getIndexes()

show collections
db.airports.count()
 