
from flask import Flask
from database import db_session, connection_url, init_db
from flask_graphql import GraphQLView
from schema import schema

app = Flask(__name__)
app.debug = True

app.config["SQLALCHEMY_DATABASE_URI"] = connection_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True
    )
)




if __name__ == "__main__":
    init_db()
    app.run()



# כדי להריץ:
# in the terminal
# docker compose down
# למחוק את כל מה שקיים כרגע בקודר דסקטופ:

# docker compose build
# docker compose up
# לגשת:
# http://127.0.0.1:5001/graphql
# לא משנה בפוסטמן או בדפדפן
# כדי לכבות:
# docker compose down