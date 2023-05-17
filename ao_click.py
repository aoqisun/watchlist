import click


@click.command()
@click.option('--count', default=2)
@click.option('--name', prompt='Your name', help='The person to greet.')
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo('Hello %s!' % name)


@click.command()
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True)
def input_password(password):
    click.echo('password: %s' % password)


if __name__ == '__main__':

    input_password()
    hello()

# if __name__ == '__main__':
#     input_password()
