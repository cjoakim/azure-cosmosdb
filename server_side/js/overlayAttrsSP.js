function overlayAttributes(pk, id, overlayAttributes) {
    var collection = getContext().getCollection();
    var selfLink = collection.getSelfLink();
    var sql = "SELECT * FROM root r where r.pk = '" + pk + "' and r.id = '" + id + "'";
    var response = getContext().getResponse();
    var responseObj = {};
    responseObj['pk'] = pk;
    responseObj['sql'] = sql;
    responseObj['result'] = undefined;

    var isAccepted = collection.queryDocuments(selfLink, sql,
        function (err, docs, options) {
            if (err) throw err;
            if (!docs || !docs.length) { 
                responseObj['message'] = 'document not found';
                response.setBody(JSON.stringify(responseObj));
            }
            else {
                var doc = docs[0];
                for (let key in overlayAttributes) {
                    if ((key == 'id') || (key == 'pk')) {
                        // don't overlay these attributes
                    }
                    else {
                        doc[key] = overlayAttributes[key];
                    }
                }
                var docLink = doc._self;
                responseObj['docLink'] = docLink;
                responseObj['updatedDoc'] = doc;

                var updated = collection.replaceDocument(docLink, doc, {},
                    function (err, result) { 
                        if (err) {
                            responseObj['message'] = 'error: ' + err.message;  
                        }
                        else {
                            responseObj['result'] = [result];
                        }
                    });  
                response.setBody(JSON.stringify(responseObj));
            }
        });
    if (!isAccepted) throw new Error('The query was not accepted by the server.');
}