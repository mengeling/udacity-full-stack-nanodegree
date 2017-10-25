from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, User, Genre, Movie

# Connect to database
engine = create_engine('sqlite:///moviecatalog.db')
Base.metadata.bind = engine

# Create session
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create dummy user
user = User(name="Anonymous", email="anonymous@udacity.com",
    picture='https://static.independent.co.uk/s3fs-public/thumbnails/image/2016/05/19/11/man-1.jpg')  # noqa
session.add(user)
session.commit()

# Add movies for action genre
genre1 = Genre(name="Action", user_id=1)
session.add(genre1)
session.commit()

movie1 = Movie(
    name="Logan", user_id=1, rating=8.2, genre=genre1, description=(
        "In the near future, a weary Logan cares for an ailing Professor X, "
        "somewhere on the Mexican border. However, Logan's attempts to hide "
        "from the world, and his legacy, are upended when a young mutant "
        "arrives, pursued by dark forces."))
movie2 = Movie(
    name="Dunkirk", user_id=1, rating=8.4, genre=genre1, description=(
        "Allied soldiers from Belgium, the British Empire and France "
        "are surrounded by the German army and evacuated during a "
        "fierce battle in World War II."))
movie3 = Movie(
    name="Iron Man", user_id=1, rating=7.9, genre=genre1, description=(
        "After being held captive in an Afghan cave, billionaire engineer "
        "Tony Stark creates a unique weaponized suit of armor to fight evil."))
session.add_all([movie1, movie2, movie3])
session.commit()

# Add movies for comedy genre
genre2 = Genre(name="Comedy", user_id=1)
session.add(genre2)
session.commit()

movie1 = Movie(
    name="Anchorman", user_id=1, rating=7.2, genre=genre2, description=(
        "Ron Burgundy is San Diego's top-rated newsman in the male-dominated "
        "broadcasting of the 1970s, but that's all about to change for Ron "
        "and his cronies when an ambitious woman is hired as a new anchor."))
movie2 = Movie(
    name="Step Brothers", user_id=1, rating=6.9, genre=genre2, description=(
        "Two aimless middle-aged losers still living at home are forced "
        "against their will to become roommates when their parents marry."))
movie3 = Movie(
    name="Old School", user_id=1, rating=7.2, genre=genre2, description=(
        "Three friends attempt to recapture their glory days by opening up a "
        "fraternity near their alma mater."))
session.add_all([movie1, movie2, movie3])
session.commit()

# Add movies for documentary genre
genre3 = Genre(name="Documentary", user_id=1)
session.add(genre3)
session.commit()

movie1 = Movie(
    name="Blackfish", user_id=1, rating=8.1, genre=genre3, description=(
        "A documentary following the controversial captivity of killer "
        "whales, and its dangers for both humans and whales."))
movie2 = Movie(
    name="Inside Job", user_id=1, rating=8.3, genre=genre3, description=(
        "Takes a closer look at what brought about the "
        "2008 financial meltdown."))
movie3 = Movie(
    name="Hoop Dreams", user_id=1, rating=8.3, genre=genre3, description=(
        "A film following the lives of two inner-city Chicago boys "
        "who struggle to become college basketball players "
        "on the road to going professional."))
session.add_all([movie1, movie2, movie3])
session.commit()

# Add movies for drama genre
genre4 = Genre(name="Drama", user_id=1)
session.add(genre4)
session.commit()

movie1 = Movie(
    name="Moonlight", user_id=1, rating=7.5, genre=genre4, description=(
        "A chronicle of the childhood, adolescence and burgeoning adulthood "
        "of a young, African-American, gay man growing up in a rough "
        "neighborhood of Miami."))
movie2 = Movie(
    name="Spotlight", user_id=1, rating=8.1, genre=genre4, description=(
        "The true story of how the Boston Globe uncovered the massive scandal "
        "of child molestation and cover-up within the local Catholic "
        "Archdiocese, shaking the entire Catholic Church to its core."))
movie3 = Movie(
    name="Argo", user_id=1, rating=7.7, genre=genre4, description=(
        "Acting under the cover of a Hollywood producer scouting a location "
        "for a science fiction film, a CIA agent launches a dangerous "
        "operation to rescue six Americans in Tehran during the U.S. "
        "hostage crisis in Iran in 1980."))
session.add_all([movie1, movie2, movie3])
session.commit()

# Add movies for horror genre
genre5 = Genre(name="Horror", user_id=1)
session.add(genre5)
session.commit()

movie1 = Movie(
    name="Get Out", user_id=1, rating=7.8, genre=genre5, description=(
        "It's time for a young African American to meet with his white "
        "girlfriend's parents for a weekend in their secluded estate "
        "in the woods, but before long, the friendly and polite ambience "
        "will give way to a nightmare."))
movie2 = Movie(
    name="Halloween", user_id=1, rating=7.8, genre=genre5, description=(
        "Fifteen years after murdering his sister on Halloween night 1963, "
        "Michael Myers escapes from a mental hospital and returns to the "
        "small town of Haddonfield to kill again."))
movie3 = Movie(
    name="The Shining", user_id=1, rating=8.4, genre=genre5, description=(
        "A family heads to an isolated hotel for the winter where an evil "
        "and spiritual presence influences the father into violence, "
        "while his psychic son sees horrific forebodings from the past "
        "and of the future."))
session.add_all([movie1, movie2, movie3])
session.commit()

# Add movies for science fiction genre
genre6 = Genre(name="Science Fiction", user_id=1)
session.add(genre6)
session.commit()

movie1 = Movie(
    name="Arrival", user_id=1, rating=8.0, genre=genre6, description=(
        "When twelve mysterious spacecraft appear around the world, "
        "linguistics professor Louise Banks is tasked with interpreting "
        "the language of the apparent alien visitors."))
movie2 = Movie(
    name="Ex Machina", user_id=1, rating=7.7, genre=genre6, description=(
        "A young programmer is selected to participate in a ground-breaking "
        "experiment in synthetic intelligence by evaluating the human "
        "qualities of a breath-taking humanoid A.I."))
movie3 = Movie(
    name="Blade Runner", user_id=1, rating=8.2, genre=genre6, description=(
        "A blade runner must pursue and try to terminate four replicants "
        "who stole a ship in space and have returned to Earth "
        "to find their creator."))
session.add_all([movie1, movie2, movie3])
session.commit()


print("\nAdded the Following Movie Genres:\n")
genres = session.query(Genre).all()
for genre in genres:
    movieCount = session.query(Movie).filter_by(genre_id=genre.id).count()
    print(genre.name + ", " + str(movieCount) + " Movies")
print("")
