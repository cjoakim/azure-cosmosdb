#!/bin/bash


echo 'count_documents...'
dotnet run query compidx coll1 count_documents > tmp/count_documents_coll1.txt 
dotnet run query compidx coll2 count_documents > tmp/count_documents_coll2.txt 

echo 'select_two...'
dotnet run query compidx coll1 select_two > tmp/select_two_coll1.txt
dotnet run query compidx coll2 select_two > tmp/select_two_coll2.txt

echo 'select_four...'
dotnet run query compidx coll1 select_four > tmp/select_four_coll1.txt
dotnet run query compidx coll2 select_four > tmp/select_four_coll2.txt

echo 'select_four_ordered_two...'
dotnet run query compidx coll2 select_four_ordered_two > tmp/select_four_ordered_two_coll2.txt

echo 'davidson_geo...'
dotnet run query compidx coll1 davidson_geo > tmp/davidson_geo_coll1.txt
dotnet run query compidx coll2 davidson_geo > tmp/davidson_geo_coll2.txt

echo 'done'
