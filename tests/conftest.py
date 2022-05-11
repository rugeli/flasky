import pytest
from app import create_app
from app import db
from flask.signals import request_finished
from app.models.cats import Cat

@pytest.fixture
def app():
    app = create_app({"TESTING": True})

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    #set up database, return app
    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def seven_cats(app):
    jazz = Cat(id=1, name="Jazz", color="black", age=8)
    cosmo = Cat(id=2, name="Cosmo", color="tuxedo",age=8)
    lily = Cat(id=3, name="Lily", color="brown and black",age=6)
    ellis = Cat(id=4, name="Ellis", color="orange",age=2)
    monster = Cat(id=5, name="Monster", color="grey",age=14)
    simba = Cat(id=6, name="Simba", color="orange",age=8)
    jenkins = Cat(id=7, name="Jenkins", color="tuxedo",age=4)

    db.session.add(jazz)
    db.session.add(cosmo)
    db.session.add(lily)
    db.session.add(ellis)
    db.session.add(monster)
    db.session.add(simba)
    db.session.add(jenkins)
    
    db.session.commit()