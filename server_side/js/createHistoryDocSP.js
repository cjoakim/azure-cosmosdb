function createHistoryDoc(pk, id) {
    var collection = getContext().getCollection();
    var selfLink = collection.getSelfLink();
    var sql = "SELECT * FROM root r where r.pk = '" + pk + "' and r.id = '" + id + "'";
    var response = getContext().getResponse();
    var responseObj = {};
    responseObj['pk'] = pk;
    responseObj['sql'] = sql;

    var isAccepted = collection.queryDocuments(selfLink, sql,
        function (err, docs, options) {
            if (err) throw err;
            if (!docs || !docs.length) { 
                responseObj['message'] = 'document not found';
                response.setBody(JSON.stringify(responseObj));
            }
            else {
                var historyDoc = docs[0]; // prune and augment the found doc
                var date = new Date();
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
                historyDoc['Active'] = 0; 

                var created = collection.createDocument(selfLink, historyDoc,  
                    function (err, newDoc) { 
                        if (err) {
                            responseObj['message'] = 'error: ' + err.message;  
                        }  
                    });  
                responseObj['message'] = 'created: ' + created;
                response.setBody(JSON.stringify(responseObj));
            }
        });
    if (!isAccepted) throw new Error('The query was not accepted by the server.');
}

// select c.pk, c.id, c.doctype, c.Active, c.Version, c.doctype from c where c.pk = 'ANR'
