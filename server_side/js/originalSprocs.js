'use strict';

// const DocumentBase = require('documentdb').DocumentBase;
// const TriggerType  = DocumentBase.TriggerType;
// const TriggerOperation = DocumentBase.TriggerOperation;

// This file contains CosmosDB Stored Procedures.
// See https://azure.github.io/azure-cosmosdb-js-server/ for server-side API.
// Chris Joakim, Microsoft, 2019/07/11

var helloWorld = {
    id: "helloWorld",
    serverScript: function () {
        var context = getContext();
        var response = context.getResponse();
        response.setBody("Hello, World");
    }
}

var lookupDoc = {
    id: "lookupDoc",
    serverScript: function (id, pk) {
        var collection = getContext().getCollection();
        var selfLink = collection.getSelfLink();
        var sql = "SELECT * FROM root r where r.pk = '" + pk + "' and r.id = '" + id + "'";
        var isAccepted = collection.queryDocuments(selfLink, sql,
            function (err, docs, options) {
                if (err) throw err;
                if (!docs || !docs.length) {
                    var response = getContext().getResponse();
                    response.setBody('no docs found');
                }
                else {
                    var response = getContext().getResponse();
                    var body = { id: id, pk: pk, doc: docs[0] };
                    response.setBody(JSON.stringify(body));
                }
            });
        if (!isAccepted) throw new Error('The query was not accepted by the server.');
    }
}

var upsertAirportDoc = {
    id: "upsertAirportDoc",
    serverScript: function (givendoc) { 

        function upsertCallback(err, doc, options) {
            if (err) throw err;
            getContext().getResponse().setBody(doc);
        }

        function omit_field(key) {
            if (key.startsWith('_')) {
                return true;
            }
            if (key === 'location') {
                return true;
            }
            return false;
        }

        if (givendoc != undefined) {
            var collection = getContext().getCollection();
            var selfLink   = collection.getSelfLink();
            var pk   = givendoc['pk'];
            var iata = givendoc['iata_code'];
            var sql  = "SELECT * FROM root r where r.pk = '" + pk + "' and r.iata_code = '" + iata + "' ";

            var queryAccepted = collection.queryDocuments(selfLink, sql,
                function (err, query_result_docs, options) {
                    if (err) throw err;
                    if (!query_result_docs || !query_result_docs.length) {
                        // insert the doc, there are no diffs
                        var epoch = new Date().getTime();
                        givendoc['__sp_created_at'] = epoch;
                        givendoc['__sp_updated_at'] = epoch;
                        givendoc['__sp_diff'] = 0;
                        givendoc['__sp_diffs'] = [];
                        collection.createDocument(selfLink, givendoc, upsertCallback);
                    }
                    else {
                        // update/overlay the original doc in the DB from the givendoc, and detect diffs
                        var dbdoc = query_result_docs[0];
                        var diffs = [];
                        dbdoc['__sp_diff'] = 0;  // reset these two field for this upsert
                        dbdoc['__sp_diffs'] = [];

                        var keys = Object.keys(givendoc);
                        var len = keys.length;
                        for (var i = 0; i < len; i++) {
                            var key = keys[i];
                            if (omit_field(key)) {
                                // don't do diff logic for this key/attribute
                            }
                            else {
                                var newval = givendoc[key];
                                if (dbdoc.hasOwnProperty(key)) {
                                    var oldval = dbdoc[key];
                                    // detect changes in current vs new values for each attribute
                                    if (newval != oldval) {
                                        diffs.push('chg; ' + key + ': ' + oldval + ' -> ' + newval);
                                    }
                                }
                                else {
                                    // detect a new attribute in the doc
                                    diffs.push('add; ' + key + ': ' + newval);
                                }
                                dbdoc[key] = newval;
                            }
                        }
                        
                        if (diffs.length > 0) {
                            dbdoc['__sp_diff'] = 1; 
                            dbdoc['__sp_diffs'] = diffs;
                        }

                        // Update the Document only if there are differences
                        if (dbdoc['__sp_diff'] > 0) {
                            dbdoc['__sp_updated_at'] = new Date().getTime();
                            collection.upsertDocument(selfLink, dbdoc, upsertCallback);
                        }
                        else {
                            getContext().getResponse().setBody(dbdoc);
                        }
                    }
                });
            if (!queryAccepted) throw new Error('The query was not accepted by the server; ' + sql);
        }
        else {
            response.setBody('no newdoc');
        }
    }
}

var createHistoryDoc = {
    id: "createHistoryDoc",
    serverScript: function (id, pk) {
        var collection = getContext().getCollection();
        var selfLink = collection.getSelfLink();
        var sql = "SELECT * FROM root r where r.pk = '" + pk + "' and r.id = '" + id + "'";
        var isAccepted = collection.queryDocuments(selfLink, sql,
            function (err, docs, options) {
                if (err) throw err;
                if (!docs || !docs.length) {
                    var response = getContext().getResponse();
                    response.setBody('no docs found');
                }
                else {
                    var historyDoc = docs[0]; // prune and augment the found doc
                    var date = new Date();
                    var respBody = {};
                    respBody['id'] = id;
                    respBody['pk'] = pk;
                    delete historyDoc['id'];
                    delete historyDoc['_attachments'];
                    delete historyDoc['_etag'];
                    delete historyDoc['_lsn'];
                    delete historyDoc['_rid'];
                    delete historyDoc['_self'];
                    delete historyDoc['_ts']; 
                    historyDoc['doctype'] = historyDoc['doctype'] + '_history';
                    historyDoc['history_id_pk'] = '' + id + '|' + pk;
                    historyDoc['history_date'] = date;
                    historyDoc['history_epoc'] = date.getTime(); 
                    historyDoc['history_method'] = 'createHistoryDoc';

                    var created = collection.createDocument(selfLink, historyDoc,  
                        function (err, newDoc) { 
                            respBody['err'] = err;
                            respBody['newDoc'] = newDoc;
                            if (err) {
                                respBody['err_msg'] = err.message;  
                            }  
                        });  
                    respBody['created'] = created;
                    var response = getContext().getResponse();
                    response.setBody(JSON.stringify(respBody));
                }
            });
        if (!isAccepted) throw new Error('The query was not accepted by the server.');
    }
}

var bulkImport = {
    id: "bulkImport",
    serverScript: function (docs) {
        if (!docs) throw new Error("The arg array is undefined or null.");
        var index = 0;
        var docsLength = docs.length;
        var collection = getContext().getCollection();
        var collectionLink = collection.getSelfLink();
        var context = getContext();
        var response = context.getResponse();

        if (docsLength == 0) {
            response.setBody(0);
        }
        else {
            createDoc(docs[index], callback);
        }

        function createDoc(doc, callback) {
            doc['bulk_import_date'] = new Date();

            var isAccepted = collection.createDocument(collectionLink, doc, callback);
            // If the request was accepted, callback will be called.
            // Otherwise report current count back to the client, 
            // which will call the script again with remaining set of docs.
            if (!isAccepted) getContext().getResponse().setBody(index);
        }

        function callback(err, doc, options) {
            if (err) throw err;
            index++;

            if (index >= docsLength) {
                getContext().getResponse().setBody(index);
            }
            else {
                createDoc(docs[index], callback);
            }
        }
    }
}

// Note: this stored proc is a work-in-progress at this time; it isn't working yet.
var bulkDelete = {
    id: "bulkDelete",
    serverScript: function (docs) {  // Version: 2018/09/16 09:00 
        if (!docs) throw new Error("The arg array is undefined or null.");
        var index = 0;
        var docsLength = docs.length;
        var collection = getContext().getCollection();
        var collectionLink = collection.getSelfLink();
        var context = getContext();
        var response = context.getResponse();

        if (docsLength == 0) {
            response.setBody(0);
        }
        else {
            deleteDoc(docs[index], callback);
        }

        // See https://docs.microsoft.com/en-us/rest/api/cosmos-db/cosmosdb-resource-uri-syntax-for-rest
        // Collection: 'https://{databaseaccount}.documents.azure.com/dbs/{db}/colls/{coll}'
        // Document:   'https://{databaseaccount}.documents.azure.com/dbs/{db}/colls/{coll}/docs/{doc}'
        function deleteDoc(doc, callback) {
            var documentLink = collectionLink + '/docs/' + doc['id'];
            var isAccepted = collection.deleteDocument(documentLink, {}, callback);
            // If the request was accepted, callback will be called.
            // Otherwise report current count back to the client, 
            // which will call the script again with remaining set of docs.
            if (!isAccepted) getContext().getResponse().setBody(index);
        }

        function callback(err, doc, options) {
            if (err) throw err;
            index++;

            if (index >= docsLength) {
                getContext().getResponse().setBody(index);
            }
            else {
                deleteDoc(docs[index], callback);
            }
        }
    }
}

module.exports.helloWorld       = helloWorld;
module.exports.lookupDoc        = lookupDoc;
module.exports.upsertAirportDoc = upsertAirportDoc;
module.exports.createHistoryDoc = createHistoryDoc;
module.exports.bulkImport       = bulkImport;
module.exports.bulkDelete       = bulkDelete;
