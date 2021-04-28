// Copied/modified version of original sample from Steve Faulkner,
// Principal Software Eng Manager, CosmosDB team.

// Use:
// $ node preferredLocations.js             (doesn't display query FeedReponse)
// $ node preferredLocations.js --verbose   (displays query FeedReponse - headers and resources)

// libraries:
const CosmosClient = require("@azure/cosmos").CosmosClient;
const format = require('string-format')

// configuration, use environment variables:
const uri     = process.env.AZURE_COSMOSDB_SQLDB_URI;
const key     = process.env.AZURE_COSMOSDB_SQLDB_KEY;
const db      = process.env.AZURE_COSMOSDB_SQLDB_DBNAME;
const coll    = process.env.AZURE_COSMOSDB_SQLDB_COLLNAME;
const regions = process.env.AZURE_COSMOSDB_SQLDB_PREF_REGIONS;  // comma-delim list 'eastus,australiacentral'
// const region1 = "eastus";
// const region2 = "australiacentral";
const region1 = regions.split(',')[0];
const region2 = regions.split(',')[1];

console.log(format('uri:     {}', uri));
console.log(format('key:     {}...', key.substring(0, 20)));
console.log(format('db:      {}', db));
console.log(format('coll:    {}', coll));
console.log(format('regions: {}', regions));
console.log(format('regions: {}', regions.split(',')));

const querySpec = {
  query: "SELECT c from c where c.pk = 'SUE'"
};
// SUE = Door County Cherryland Airport, Sturgeon Bay

const client1 = new CosmosClient({
  endpoint: uri,
  connectionPolicy: {
    preferredLocations: [region1, region2],
  },
  key,
  plugins: [
    {
      on: "request",
      plugin: async (context, next) => {
        console.log(format('client1 endpoint: {}', context.endpoint));
        const response = await next(context);
        return response;
      },
    },
  ],
});

const client2 = new CosmosClient({
  endpoint: uri,
  connectionPolicy: {
    preferredLocations: [region2, region1],
  },
  key,
  plugins: [
    {
      on: "request",
      plugin: async (context, next) => {
        console.log(format('client2 endpoint: {}', context.endpoint));
        //console.log("client2", context);
        const response = await next(context);
        return response;
      },
    },
  ],
});

async function main() {
  var verbose = false;
  process.argv.forEach((val, index) => {
    if (val == '--verbose') { verbose = true };
  })

  console.log(await (await client1.getDatabaseAccount()).resource);
  console.log(await (await client2.getDatabaseAccount()).resource);

  display_response("client1", verbose, await client1
    .database(db)
    .container(coll)
    .items.query(querySpec)
    .fetchAll());

  display_response("client2", verbose, await client2
    .database(db)
    .container(coll)
    .items.query(querySpec)
    .fetchAll());
}

function display_response(client_name, verbose, feed_response) {
  if (verbose) {
    console.log(format("display_response: {}\n{}\n{}",
      client_name,
      JSON.stringify(feed_response['headers']),
      JSON.stringify(feed_response['resources'])));
  }
}

main().catch((e) => {
  console.log(e);
  process.exit(1);
});
