from jinja2 import Environment, FileSystemLoader

env = Environment(
    loader=FileSystemLoader("templates"),
    lstrip_blocks=True
)

template = env.get_template("print_names_with_macro.txt")

names = [
    'Mohsen',
    'John',
    'Sara',
    'Ali',
    'Susan'    
]

print(template.render(names=names))