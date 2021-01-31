# Cosmos MongoDB

## Initial indexes after creation with az CLI

```
globaldb:PRIMARY> db.airports.getIndexKeys()
[ { "_id" : 1 } ]
```

```
globaldb:PRIMARY> db.airports.count()
globaldb:PRIMARY> db.airports.remove({timezone_num: "0"})
```