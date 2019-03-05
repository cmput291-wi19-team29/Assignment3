rm -f database.db
sqlite3 database.db < tables.sql
sqlite3 database.db < modded_data.sql
