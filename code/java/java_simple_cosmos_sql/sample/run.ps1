
# Execute the main Program via "mvn exec:java".
# Chris Joakim, Microsoft, 2021/03/22

mvn exec:java `
  -D"exec.mainClass"="org.cjoakim.azure.cosmos.sql.App" `
  -D"exec.args"="point_read dev airports SFO 895014e0-1d52-40f6-8ae2-f9dcb0119961"