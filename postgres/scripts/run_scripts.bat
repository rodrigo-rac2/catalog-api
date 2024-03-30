@echo off
SET DATABASE_NAME=catalog
SET USER=postgres
SET PASSWORD=yourpassword

psql -d %DATABASE_NAME% -U %USER% -f postgres/scripts/ddl.catalog.sql
psql -d %DATABASE_NAME% -U %USER% -f postgres/scripts/dml.catalog.sql
