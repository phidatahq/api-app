## Running Database Migrations

## Creating database revision using alembic

Run these commands locally to create a new database revision.

```bash
docker exec -it api-dev-container zsh

alembic -c db/alembic.ini revision --autogenerate -m "Initialize DB"
alembic -c db/alembic.ini upgrade head
```

Then set `UPGRADE_DB = True` which will run `alembic -c db/alembic.ini upgrade head` from the entrypoint script in production.

## How the migrations directory was created

> This has already been run to create the migrations directory

```bash
docker exec -it api-dev-container zsh

cd db
alembic init migration
```
