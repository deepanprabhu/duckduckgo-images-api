import click
import json
import duckduckgo_images_api.api as api


@click.command()
@click.option('--max_results', default=10)
@click.argument('keywords', nargs=-1)
def search(keywords, max_results):
    print(json.dumps(api.search(' '.join(keywords), max_results)))


if __name__ == '__main__':
    from click.testing import CliRunner
    runner = CliRunner()
    result = runner.invoke(search, ['red','bus'])
    assert result.exit_code == 0
    assert len(json.loads(result.output)) == 10
