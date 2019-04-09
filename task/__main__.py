import click
from model.db_model import Region
from .spider import get_projects


@click.group(chain=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        click.echo('please use a command!')


@cli.command()
@click.argument('region', nargs=1)
def sync_project(region):
    if not Region.region_map.get(region):
        click.echo(f'region({region}) code not found!')
        return
    get_projects(region)
    click.echo(f'sync {Region.region_map.get(region)}({region}) successful!')


if __name__ == "__main__":
    cli()  # pylint: disable=no-value-for-parameter
