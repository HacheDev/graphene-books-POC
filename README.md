# Books GraphQL POC using Django-Graphene

## Installation
Clone the directory and go to projects root directory.
Create virtualenv and activate it:
```
pyenv virtualenv 3.10 graphql_books
pyenv local graphql_books
```
Install dependencies:
```
pip install -r requirements.txt
```
Run migrations:
```
python manage.py makemigrations
python manage.py migrate
```
Populate sqlite database with data from a json file.
```
python manage.py populate <PATH/TO/JSON/FILE>
```
You can use books.json file by replacing <PATH/TO/JSON/FILE> with graphql_books/books/books.json, or you can use your own JSON file. However, if you use a JSON file with a different structure, you might need to change or add your own custom command to populate it.\
This command is defined in graphql_books/books/management/commands/populate.py .

## Playground
To use the playground, run:
```
python manage.py runserver
```
And navigate to http://localhost:8000/graphql