#!/bin/bash

DATABASE_NAME=catalog
USER=postgres
PASSWORD=yourpassword

psql -d $DATABASE_NAME -U $USER -f postgres/scripts/ddl.catalog.sql
psql -d $DATABASE_NAME -U $USER -f postgres/scripts/dml.catalog.sql
