from invoke.context import Context
from invoke.tasks import task


@task(name="create_migration", aliases=["cm"])
def create_migration(
    c: Context,
    message: str = "migration",
    alembic_ini: str = "alembic.ini",
):
    """
    Creates a new database migration using Alembic.
    The message parameter
    is used as the message for the migration, and is passed to the -m flag.

    :param message: The message for the migration (default: "migration")
    :param alembic_ini:
    The path to the Alembic configuration file (default: "alembic.ini")
    :type message: str
    :type alembic_ini: str
    """
    c.run(f'alembic -c "{alembic_ini}" revision --autogenerate -m "{message}"')


@task(name="migrate up", aliases=["mu", "migup"])
def migrate_up(
    c: Context,
    alembic_ini: str = "alembic.ini",
):
    """
    Runs database migrations up using Alembic.

    :param alembic_ini:
    The path to the Alembic configuration file. Defaults to "alembic.ini".
    """
    c.run(f"alembic -c {alembic_ini} upgrade head")


@task(name="migrate down", aliases=["md", "migdown"])
def migrate_down(
    c: Context,
    alembic_ini: str = "alembic.ini",
    number: int = 1,
):
    """
    Runs database migrations down using Alembic.

    :param alembic_ini: The path to the Alembic configuration file.
    Defaults to "alembic.ini".
    """
    c.run(f"alembic -c {alembic_ini} downgrade -n {number}")


@task(name="tests", aliases=["t"])
def run_tests(c: Context, module: str = "tests/operations") -> None:
    """
    runs tests for a specific module
    :param module: the module to run tests for.
    Defaults to "tests/operations"
    """
    c.run(f"pytest {module}")
