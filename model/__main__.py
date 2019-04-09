import click
from .db_model import Base, engine, Session, Region


@click.group(chain=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        click.echo('please use a command!')


@cli.command()
def init_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    Region.insert_regions()


if __name__ == "__main__":
    cli()  # pylint: disable=no-value-for-parameter
