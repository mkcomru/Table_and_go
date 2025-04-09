@echo off
echo Waiting for PostgreSQL to start...
:loop
pg_isready -U postgres
if %ERRORLEVEL% NEQ 0 (
    timeout /t 1
    goto loop
)

echo Restoring database from backup...
pg_restore -U postgres -d table_and_go C:\docker-entrypoint-initdb.d\backup.dump

echo Database restored successfully!