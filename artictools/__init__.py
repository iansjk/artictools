from flask import Flask, url_for

from artictools.wordlists.corpus import consonants, arpabet_to_ipa

app = Flask(__name__)
app.config["MINIMUM_PICTOGRAM_QUERY_LENGTH"] = 3
app.config["S3_PICTOGRAM_URL"] = "https://images.artic.tools/pictograms"

from views import general
from views import pictograms
from views import wordlists

app.register_blueprint(general.bp)
app.register_blueprint(pictograms.bp)
app.register_blueprint(wordlists.bp)


@app.context_processor
def inject_constants():
    return {
        "project_name": "ArticTools",
        "active_page": "Home",
        "navigation": (
            ("Home", "general.index"),
            ("Pictograms", url_for("pictograms.index")),
            ("Wordlists", (
                ("By Syllable Count", url_for("wordlists.syllables")),
                ("By Sounds", url_for("wordlists.sounds")),
                ("Minimal Pairs", url_for("wordlists.minimal_pairs")),
            )),
            ("Grid Builder", url_for("general.grid_builder")),
            ("About", url_for("general.about")),
        ),
        "consonants": consonants,
        "arpabet_to_ipa": arpabet_to_ipa
    }


@app.after_request
def add_cache_header(response):
    response.cache_control.max_age = 300
    response.cache_control.public = True
    return response
