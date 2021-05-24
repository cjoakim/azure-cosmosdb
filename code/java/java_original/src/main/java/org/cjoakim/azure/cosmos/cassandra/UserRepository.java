package org.cjoakim.azure.cosmos.cassandra;

import java.util.List; 
import com.datastax.driver.core.BoundStatement; 
import com.datastax.driver.core.PreparedStatement; 
import com.datastax.driver.core.Row; 
import com.datastax.driver.core.Session; 
import org.slf4j.Logger; 
import org.slf4j.LoggerFactory; 

/** 
 * Create a Cassandra session 
 */ 
public class UserRepository { 

    private static final Logger LOGGER = LoggerFactory.getLogger(UserRepository.class); 
    private Session session; 
    public UserRepository(Session session) { 
        this.session = session; 
    } 

    /** 
    * Create keyspace uprofile in cassandra DB 
     */ 

    public void createKeyspace() { 
         final String query = "CREATE KEYSPACE IF NOT EXISTS uprofile WITH REPLICATION = { 'class' : 'NetworkTopologyStrategy', 'datacenter1' : 1 }"; 
        session.execute(query); 
        LOGGER.info("Created keyspace 'uprofile'"); 
    } 

    /** 
     * Create user table in cassandra DB 
     */ 

    public void createTable() { 
        final String query = "CREATE TABLE IF NOT EXISTS uprofile.user (user_id int PRIMARY KEY, user_name text, user_bcity text)"; 
        session.execute(query); 
        LOGGER.info("Created table 'user'"); 
    } 
}
