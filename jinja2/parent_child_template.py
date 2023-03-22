from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html', 'htm'])
)

template = env.get_template('child.html')
print(template.render(name="John"))