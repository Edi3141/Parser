import csv
from peewee import *


db = PostgresqlDatabase(database='condos', user='user', password=1, host='localhost')


class Condos(Model):
    title = TextField()
    link = TextField()
    description = TextField()
    location = CharField()
    date_posted = CharField()
    price = CharField()

    class Meta:
        database = db


def main():
    db.connect()
    db.create_tables([Condos])

    with open('condos.csv', 'r', encoding='UTF-8') as csvfile:
        order = ['title', 'link', 'description', 'location', 'date_posted', 'price']
        reader = csv.DictReader(csvfile, fieldnames=order)

        # condos = list(reader)

        for row in reader:
            # print(row)
            condos = Condos(title=row['title'], link=row['link'], description=row['description'], location=row['location'], date_posted=row['date_posted'], price=row['price'])
            condos.save()
        # with db.atomic():
        #     for row in reader:
        #         Condos.create(**row)
        #     print(row)
#


if __name__ == '__main__':
    main()