function hello(prefix) {
    var response = getContext().getResponse();
    response.setBody("Hello at " + new Date().toISOString());
}
