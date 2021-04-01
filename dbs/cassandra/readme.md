# CosmosDB w/Cassandra API


---

## Quick Starts 

### CQL Shell 

```
export SSL_VERSION=TLSv1_2
export SSL_VALIDATE=false

cqlsh.py cjoakimcosmoscass.cassandra.cosmos.azure.com 10350 -u cjoakimcosmoscass -p ...password... --ssl
```

### Java

```
SSLContext sc = SSLContext.getInstance("TLSv1.2");
sc.init(kmf.getKeyManagers(), tmf.getTrustManagers(), null);

JdkSSLOptions sslOptions = RemoteEndpointAwareJdkSSLOptions.builder()
    .withSSLContext(sc)
    .build();

Cluster cluster = Cluster.builder()
            .addContactPoint("cjoakimcosmoscass.cassandra.cosmos.azure.com")
            .withPort(10350)
            .withCredentials("cjoakimcosmoscass", "...password...")
            .withSSL(sslOptions)
            .build();

Session session = cluster.connect("<your-keyspace>");
```

- https://docs.microsoft.com/en-us/azure/cosmos-db/create-cassandra-api-account-java
- https://github.com/Azure-Samples/azure-cosmos-db-cassandra-java-getting-started


### Python

```
pip install cassandra-driver


from cassandra.cluster import Cluster
from ssl import PROTOCOL_TLSv2, CERT_REQUIRED

ssl_opts = {
    'ca_certs': '<path-to-your-.pem-file>',
    'ssl_version': PROTOCOL_TLSv2,
    'cert_reqs': CERT_REQUIRED  # Certificates are required and validated
}

auth_provider = PlainTextAuthProvider(username="cjoakimcosmoscass", password="...password...")
cluster = Cluster("cjoakimcosmoscass.cassandra.cosmos.azure.com", port = 10350, auth_provider=auth_provider, ssl_options=ssl_opts)
session = cluster.connect("<your-keyspace>")
```

- https://github.com/Azure-Samples/azure-cosmos-db-cassandra-python-getting-started


### .Net

```
Install-Package CassandraCSharpDriver


let options = new Cassandra.SSLOptions(SslProtocols.Tls12, true, ValidateServerCertificate);
options.SetHostNameResolver((ipAddress) => "cjoakimcosmoscass.cassandra.cosmos.azure.com");
Cluster cluster = Cluster.Builder()
    .WithCredentials("cjoakimcosmoscass", "...password...")
    .WithPort(10350)
    .AddContactPoint("cjoakimcosmoscass.cassandra.cosmos.azure.com")
    .WithSSL(options)
    .Build();

ISession session = cluster.Connect("<your-keyspace>");
```

- https://github.com/Azure-Samples/azure-cosmos-db-cassandra-dotnet-getting-started


### Node.js

```
npm install cassandra-driver


process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0";

let cassandra = require('cassandra-driver');
let authProvider = new cassandra.auth.PlainTextAuthProvider('cjoakimcosmoscass', '...password...');
let client = new cassandra.Client({
    contactPoints: ['cjoakimcosmoscass.cassandra.cosmos.azure.com:10350'], 
    keyspace: '<your-keyspace>', 
    authProvider: authProvider
});
```

- https://github.com/Azure-Samples/azure-cosmos-db-cassandra-nodejs-getting-started
