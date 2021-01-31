function docsInPk(pk) {
    var collection = getContext().getCollection();
    var selfLink = collection.getSelfLink();
    var sql = "SELECT * FROM root r where r.pk = '" + pk + "'";
    var response = getContext().getResponse();
    var responseObj = {};
    responseObj['pk'] = pk;
    responseObj['sql'] = sql;

    var isAccepted = collection.queryDocuments(selfLink, sql,
        function (err, docs, options) {
            if (err) throw err;
            if (!docs || !docs.length) {
                responseObj['docs'] = {};
                response.setBody(JSON.stringify(responseObj));
            }
            else {
                responseObj['docs'] = docs;
                response.setBody(JSON.stringify(responseObj));
            }
        });
    if (!isAccepted) throw new Error('The query was not accepted by the server.');
}