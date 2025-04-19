<<<<<<< HEAD
import logging
from logging.config import fileConfig

from flask import current_app
=======
from __future__ import with_statement

from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
>>>>>>> c720ba8e45f7550d7a328ef6e0795df02c969ea0

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)
<<<<<<< HEAD
logger = logging.getLogger('alembic.env')


def get_engine():
    try:
        # this works with Flask-SQLAlchemy<3 and Alchemical
        return current_app.extensions['migrate'].db.get_engine()
    except (TypeError, AttributeError):
        # this works with Flask-SQLAlchemy>=3
        return current_app.extensions['migrate'].db.engine


def get_engine_url():
    try:
        return get_engine().url.render_as_string(hide_password=False).replace(
            '%', '%%')
    except AttributeError:
        return str(get_engine().url).replace('%', '%%')

=======
>>>>>>> c720ba8e45f7550d7a328ef6e0795df02c969ea0

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
<<<<<<< HEAD
config.set_main_option('sqlalchemy.url', get_engine_url())
target_db = current_app.extensions['migrate'].db
=======
from flask import current_app
config.set_main_option(
    'sqlalchemy.url',
    current_app.config.get('SQLALCHEMY_DATABASE_URI')
)
target_metadata = current_app.extensions['migrate'].db.metadata
>>>>>>> c720ba8e45f7550d7a328ef6e0795df02c969ea0

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


<<<<<<< HEAD
def get_metadata():
    if hasattr(target_db, 'metadatas'):
        return target_db.metadatas[None]
    return target_db.metadata


=======
>>>>>>> c720ba8e45f7550d7a328ef6e0795df02c969ea0
def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
<<<<<<< HEAD
        url=url, target_metadata=get_metadata(), literal_binds=True
=======
        url=url, target_metadata=target_metadata, literal_binds=True
>>>>>>> c720ba8e45f7550d7a328ef6e0795df02c969ea0
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
<<<<<<< HEAD

    # this callback is used to prevent an auto-migration from being generated
    # when there are no changes to the schema
    # reference: http://alembic.zzzcomputing.com/en/latest/cookbook.html
    def process_revision_directives(context, revision, directives):
        if getattr(config.cmd_opts, 'autogenerate', False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info('No changes in schema detected.')

    conf_args = current_app.extensions['migrate'].configure_args
    if conf_args.get("process_revision_directives") is None:
        conf_args["process_revision_directives"] = process_revision_directives

    connectable = get_engine()
=======
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
>>>>>>> c720ba8e45f7550d7a328ef6e0795df02c969ea0

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
<<<<<<< HEAD
            target_metadata=get_metadata(),
            **conf_args
=======
            target_metadata=target_metadata
>>>>>>> c720ba8e45f7550d7a328ef6e0795df02c969ea0
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
<<<<<<< HEAD
    run_migrations_online()
=======
    run_migrations_online() 
>>>>>>> c720ba8e45f7550d7a328ef6e0795df02c969ea0
