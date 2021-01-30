from cassandra.auth import PlainTextAuthProvider
import config as cfg
from cassandra.query import BatchStatement, SimpleStatement
from prettytable import PrettyTable
import time
import ssl
import cassandra
from cassandra.cluster import Cluster
from cassandra.policies import *
from ssl import PROTOCOL_TLSv1_2, SSLContext, CERT_NONE
from requests.utils import DEFAULT_CA_BUNDLE_PATH

def PrintTable(rows):
    t = PrettyTable(['UserID', 'Name', 'City'])
    for r in rows:
        t.add_row([r.user_id, r.user_name, r.user_bcity])
    print (t)

#<authenticateAndConnect>
ssl_context = SSLContext(PROTOCOL_TLSv1_2)
ssl_context.verify_mode = CERT_NONE
auth_provider = PlainTextAuthProvider(username=cfg.config['username'], password=cfg.config['password'])
cluster = Cluster([cfg.config['contactPoint']], port = cfg.config['port'], auth_provider=auth_provider,ssl_context=ssl_context)
session = cluster.connect()
#</authenticateAndConnect>

#<createKeyspace>
print ("\nCreating Keyspace")
session.execute('CREATE KEYSPACE IF NOT EXISTS uprofile WITH replication = {\'class\': \'NetworkTopologyStrategy\', \'datacenter\' : \'1\' }');
#</createKeyspace>

#<createTable>
print ("\nCreating Table")
session.execute('CREATE TABLE IF NOT EXISTS uprofile.user (user_id int PRIMARY KEY, user_name text, user_bcity text)');
#</createTable>

#<insertData>
session.execute("INSERT INTO  uprofile.user  (user_id, user_name , user_bcity) VALUES (%s,%s,%s)", [1,'Lybkov','Seattle'])
session.execute("INSERT INTO  uprofile.user  (user_id, user_name , user_bcity) VALUES (%s,%s,%s)", [2,'Doniv','Dubai'])
session.execute("INSERT INTO  uprofile.user  (user_id, user_name , user_bcity) VALUES (%s,%s,%s)", [3,'Keviv','Chennai'])
session.execute("INSERT INTO  uprofile.user  (user_id, user_name , user_bcity) VALUES (%s,%s,%s)", [4,'Ehtevs','Pune'])
session.execute("INSERT INTO  uprofile.user  (user_id, user_name , user_bcity) VALUES (%s,%s,%s)", [5,'Dnivog','Belgaum'])
session.execute("INSERT INTO  uprofile.user  (user_id, user_name , user_bcity) VALUES (%s,%s,%s)", [6,'Ateegk','Narewadi'])
session.execute("INSERT INTO  uprofile.user  (user_id, user_name , user_bcity) VALUES (%s,%s,%s)", [7,'KannabbuS','Yamkanmardi'])
#</insertData>

#<queryAllItems>
print ("\nSelecting All")
rows = session.execute('SELECT * FROM uprofile.user')
PrintTable(rows)
#</queryAllItems>

#<queryByID>
print ("\nSelecting Id=1")
rows = session.execute('SELECT * FROM uprofile.user where user_id=1')
PrintTable(rows)
#</queryByID>

cluster.shutdown()
