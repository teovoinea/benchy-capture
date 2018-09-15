import click
import requests

INFO_VERBOSITY = 1
DEBUG_VERBOSITY = 2

API_URL = 'https://benchy.azurewebsites.net/api/benchmark'

@click.command()
@click.option('-v', '--verbose', count=True)
@click.argument('language', type=click.Choice(['python']))
@click.argument('framework', type=click.Choice(['performance']))
@click.argument('location', type=click.Path(exists=True, resolve_path=True))
def capture(verbose, language, framework, location):
    debug_print(verbose, 'Verbosity: %s' % verbose)
    debug_print(verbose, 'Language: %s' % language)
    debug_print(verbose, 'Framework: %s' % framework)
    debug_print(verbose, 'Location: %s' % location)

    with open(location, 'rb') as benchmark_file:
        info_print(verbose, "Reading benchmark data...")
        benchmark_data = benchmark_file.read()

    body = {
        'language': language,
        'framework': framework,
        'data': benchmark_data
    }

    info_print(verbose, "Posting data...")
    debug_print(verbose, "Post body: %s" % body)
    request = requests.post(API_URL, json=body)

    # If the request failed, raise an error
    request.raise_for_status()

    click.echo("Benchy succeeded")

def info_print(verbosity, msg):
    if verbosity >= INFO_VERBOSITY:
        click.echo(msg)

def debug_print(verbosity, msg):
    if verbosity >= DEBUG_VERBOSITY:
        click.echo(msg)

if __name__ == "__main__":
    capture()