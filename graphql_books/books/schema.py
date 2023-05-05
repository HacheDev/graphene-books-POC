import graphene
import json

import graphene
from graphene import Mutation, Boolean, ID, List, Field, String
from graphene_django import DjangoObjectType
from .models import Book, Author, Editorial


class AuthorType(DjangoObjectType):
    class Meta:
        model = Author
        fields = "__all__"

    books = graphene.List(lambda: BookType)


class EditorialType(DjangoObjectType):
    class Meta:
        model = Editorial
        fields = "__all__"

    books = graphene.List(lambda: BookType)


class BookType(DjangoObjectType):
    class Meta:
        model = Book
        fields = "__all__"

    author = graphene.Field(AuthorType)
    editorials = graphene.List(EditorialType)

    def resolve_editorials(parent, info):
        return parent.editorials.all()


class Query(graphene.ObjectType):
    # Retrieve all books
    all_books = graphene.List(BookType)

    def resolve_all_books(root, info):
        return Book.objects.all()

    # Retrieve all authors
    all_authors = graphene.List(AuthorType)

    def resolve_all_authors(root, info):
        return Author.objects.all()

    # Retrieve all editorials
    all_editorials = graphene.List(EditorialType)

    def resolve_all_editorials(root, info):
        return Editorial.objects.all()

    # Retrieve a book by its name
    books_by_title = List(BookType, title=String(required=True))

    def resolve_books_by_title(root, info, title):
        return Book.objects.filter(title__icontains=title)

    # Retrieve an author by their name
    authors_by_name = List(AuthorType, name=String(required=True))

    def resolve_authors_by_name(root, info, name):
        return Author.objects.filter(name__icontains=name)

    # Retrieve an editorial by its name
    editorials_by_name = List(EditorialType, name=String(required=True))

    def resolve_editorials_by_name(root, info, name):
        return Editorial.objects.filter(name__icontains=name)

    # Retrieve a book by its ID
    book_by_id = Field(BookType, id=ID(required=True))

    def resolve_book_by_id(root, info, id):
        return Book.objects.get(id=id)

    # Retrieve an author by their ID
    author_by_id = Field(AuthorType, id=ID(required=True))

    def resolve_author_by_id(root, info, id):
        return Author.objects.get(id=id)

    # Retrieve an editorial by its ID
    editorial_by_id = Field(EditorialType, id=ID(required=True))

    def resolve_editorial_by_id(root, info, id):
        return Editorial.objects.get(id=id)


class CreateBook(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        author_id = graphene.ID(required=True)
        editorial_id = graphene.ID(required=True)

    book = graphene.Field(BookType)

    def mutate(root, info, title, author_id, editorial_id):
        author = Author.objects.get(pk=author_id)
        editorial = Editorial.objects.get(pk=editorial_id)
        book = Book.objects.create(title=title, author=author, editorial=editorial, )
        return CreateBook(book=book)


class DeleteBook(Mutation):
    class Arguments:
        id = ID(required=True)

    ok = Boolean()

    def mutate(root, info, id):
        book = Book.objects.get(id=id)
        book.delete()
        return DeleteBook(ok=True)


class DeleteAuthor(Mutation):
    class Arguments:
        id = ID(required=True)

    ok = Boolean()

    def mutate(root, info, id):
        author = Author.objects.get(id=id)
        author.delete()
        return DeleteAuthor(ok=True)


class Mutation(graphene.ObjectType):
    create_book = CreateBook.Field()
    delete_book = DeleteBook.Field()
    delete_author = DeleteAuthor.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

# class AudioVisualType(graphene.Enum):
#     SERIES = "series"
#     MOVIE = "movie"
#
#
# class AudioVisual(graphene.ObjectType):
#     comingSoon = graphene.Boolean(required=False)
#     title = graphene.String(required=True)
#     year = graphene.String(required=True)
#     rated = graphene.String(required=False)
#     released = graphene.String(required=False)
#     runtime = graphene.String(required=False)
#     director = graphene.String(required=False)
#     writer = graphene.String(required=True)
#     actors = graphene.String(required=True)
#     plot = graphene.String(required=True)
#     language = graphene.String(required=True)
#     country = graphene.String(required=True)
#     awards = graphene.String(required=False)
#     poster = graphene.String(required=True)
#     metaScore = graphene.String(required=False)
#     imdbRating = graphene.Decimal(required=False)
#     imdbVotes = graphene.Int(required=False)
#     imdbID = graphene.String(required=True)
#     type = graphene.Field(AudioVisualType, required=True)
#     totalSeasons = graphene.Int(required=True)
#     response = graphene.Boolean(required=True)
#
#
# class Actor(graphene.ObjectType):
#     name = graphene.String(required=True)
#     birthDate = graphene.Date(required=False)
#     movies = graphene.List(AudioVisual, required=True)
#
#
# class Query(graphene.ObjectType):
#     getAudioVisualByName = graphene.Field(AudioVisual, name=graphene.String())
#     getActorByName = graphene.Field(Actor, name=graphene.String())
#     getAudioVisuals = graphene.List(AudioVisual)
#     getActors = graphene.List(Actor)
#
#     def resolve_movies(root, info):
#         with open("movies.json") as file:
#             data = json.load(file)
#
#         movies = [AudioVisual(
#             comingSoon=p['comingSoon'],
#             title=p['title'],
#             year=p['year'],
#             rated=p['rated'],
#             released=p['released'],
#             runtime=p['runtime'],
#             director=p['director'],
#             writer=p['writer'],
#             actors=p['actors'],
#             plot=p['plot'],
#             language=p['language'],
#             country=p['country'],
#             awards=p['awards'],
#             poster=p['poster'],
#             metaScore=p['metaScore'],
#             imdbRating=p['imdbRating'],
#             imdbVotes=p['imdbVotes'],
#             imdbID=p['imdbID'],
#             type=p['type'],
#             totalSeasons=p['totalSeasons'],
#             response=p['response'],
#         ) for p in data]
#
#         return movies
