import media
import index

# Provide movie info and links as arguments to the Movie class in media.py
# to assign attributes to each instance of a movie.
# Movie instances are stored in descriptive variables.
anchorman = media.Movie(
    "Anchorman",
    "Ron Burgundy is San Diego's top-rated newsman in the male-dominated \
    broadcasting of the 1970s, but that's all about to change for Ron and \
    his cronies when an ambitious woman is hired as a new anchor.",
    "https://upload.wikimedia.org/wikipedia/en/6/64/Movie_poster_Anchorman_The_Legend_of_Ron_Burgundy.jpg",  # noqa
    "https://www.youtube.com/watch?v=Ip6GolC7Mk0")

step_brothers = media.Movie(
    "Step Brothers",
    "Two aimless middle-aged losers still living at home are forced \
    against their will to become roommates when their parents marry.",
    "https://upload.wikimedia.org/wikipedia/en/thumb/d/d9/StepbrothersMP08.jpg/220px-StepbrothersMP08.jpg",  # noqa
    "https://www.youtube.com/watch?v=ANjenc4W1_Q")

old_school = media.Movie(
    "Old School",
    "Three friends attempt to recapture their glory days by \
    opening up a fraternity near their alma mater.",
    "https://upload.wikimedia.org/wikipedia/en/2/21/Old_s_poster.jpg",
    "https://www.youtube.com/watch?v=ybNn__9pnms")

talladega_nights = media.Movie(
    "Talladega Nights",
    "#1 NASCAR driver Ricky Bobby stays atop the heap thanks to a \
    pact with his best friend and teammate, Cal Naughton, Jr. \
    But when a French Formula One driver, makes his way up the ladder, \
    Ricky Bobby's talent and devotion are put to the test.",
    "https://upload.wikimedia.org/wikipedia/en/e/e7/Talladega_nights.jpg",
    "https://www.youtube.com/watch?v=myKtVl8N7jU")

semi_pro = media.Movie(
    "Semi Pro",
    "Jackie Moon, the owner-coach-player of the American Basketball \
    Association's Flint Michigan Tropics, rallies his teammates to \
    make their NBA dreams come true",
    "https://upload.wikimedia.org/wikipedia/en/2/24/Poster-premiere-semi-pro.jpg",  # noqa
    "https://www.youtube.com/watch?v=tNGqlzoHrrI")

wedding_crashers = media.Movie(
    "Wedding Crashers",
    "John Beckwith and Jeremy Grey, a pair of committed womanizers \
    who sneak into weddings to take advantage of the romantic tinge \
    in the air, find themselves at odds with one another when John \
    meets and falls for Claire Cleary.",
    "https://upload.wikimedia.org/wikipedia/en/3/3e/Wedding_crashers_poster.jpg",  # noqa
    "https://www.youtube.com/watch?v=ZeUSo8voIXM")

# Create a movies list that contains the variables for each instance
movies = [
    anchorman, step_brothers, old_school,
    talladega_nights, semi_pro, wedding_crashers
    ]

# Provide movies list to "open_movies_page" function to create the HTML file
index.open_movies_page(movies)
