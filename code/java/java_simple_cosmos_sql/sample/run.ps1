
# Execute the main Program via "mvn exec:java".
# Chris Joakim, Microsoft, 2021/06/28


mvn exec:java `
  -D"exec.mainClass"="org.cjoakim.azure.cosmos.sql.App" `
  -D"exec.args"="select_distinct dev airports"