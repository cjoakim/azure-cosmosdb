function southEastUsa(pk) {
    return ["ATL", "CAE", "CLT", "GSP", "MIA", "MCO", "JAX", "RDU", "TPA"].includes(pk);
}

// Use: 
// SELECT c.pk, c.City, c.Name FROM c WHERE udf.southEastUsa(c.pk)