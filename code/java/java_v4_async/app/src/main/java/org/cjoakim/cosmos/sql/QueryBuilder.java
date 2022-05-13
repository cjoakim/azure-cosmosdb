package org.cjoakim.cosmos.sql;


import org.cjoakim.cosmos.AppConstants;

/**
 * Instances of this class build SQL String values to be executed by CosmosSqlUtil.
 *
 * Chris Joakim, Microsoft
 */

public class QueryBuilder implements AppConstants {

    public QueryBuilder() {

        super();
    }

    public String countDocumentsQuery() {

        return "select count(1) as count from c";  // alternatively: "select count(1) from c";
    }

    public String countDocumentsInPkQuery(String pk) {

        return "select count(1) as count from c where c.pk = '" + pk + "'";
    }

    public String allDocumentsQuery() {

        return "select * from c";
    }

    public String allDocumentsInPkQuery(String pk) {

        return selectBufferWithPk(pk).toString();
    }

    public String lookupPeopleInPk(String pk) {

        StringBuffer sb = selectBufferWithPk(pk);
        sb.append("' and c.doctype = 'person'");
        return sb.toString();
    }

    private StringBuffer selectBufferWithPk(String pk) {

        StringBuffer sb = new StringBuffer();
        sb.append("select * from c where ");
        sb.append("c.pk = '" + pk + "' ");
        return sb;
    }
}

