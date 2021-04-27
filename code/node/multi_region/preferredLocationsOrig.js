const { CosmosClient } = require("@azure/cosmos");

const key = "REDACTED";

const eastUSClient = new CosmosClient({
  endpoint: "https://stfaul-sql.documents.azure.com:443/",
  connectionPolicy: {
    preferredLocations: ["East US"],
  },
  key,
  plugins: [
    {
      on: "request",
      plugin: async (context, next) => {
        console.log("East US Client", context.endpoint);
        const response = await next(context);
        return response;
      },
    },
  ],
});

const northCentralUSClient = new CosmosClient({
  endpoint: "https://stfaul-sql.documents.azure.com:443/",
  connectionPolicy: {
    preferredLocations: ["North Central US"],
  },
  key,
  plugins: [
    {
      on: "request",
      plugin: async (context, next) => {
        console.log("North Central Client", context.endpoint);
        const response = await next(context);
        return response;
      },
    },
  ],
});

async function main() {
  console.log(await (await eastUSClient.getDatabaseAccount()).resource);
  console.log(await (await northCentralUSClient.getDatabaseAccount()).resource);
  await eastUSClient
    .database("test")
    .container("test")
    .items.readAll()
    .fetchAll();
  await northCentralUSClient
    .database("test")
    .container("test")
    .items.readAll()
    .fetchAll();
}

main().catch((e) => {
  console.log(e);
  process.exit(1);
});
