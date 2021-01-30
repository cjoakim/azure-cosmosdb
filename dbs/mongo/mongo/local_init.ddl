// MongoDB "DDL" initialize the dev database with airports collection.
// Chris Joakim, Microsoft, 2020/04/04

use dev

db.airports.drop()
db.createCollection("airports")
db.airports.ensureIndex({"iata_code" : 1}, {"unique" : false})
db.airports.ensureIndex({"name" : 1}, {"unique" : false})
db.airports.ensureIndex({"timezone_num" : 1}, {"unique" : false})
db.airports.getIndexKeys()

db.postal_codes.drop()
db.createCollection("postal_codes")
db.postal_codes.ensureIndex({""postal_cd"" : 1}, {"unique" : true})
db.postal_codes.ensureIndex({"city_name" : 1}, {"unique" : false})
db.postal_codes.ensureIndex({"state_abbrv" : 1}, {"unique" : false})
db.postal_codes.getIndexKeys()

show collections
db.airports.count()
db.postal_codes.count()
 