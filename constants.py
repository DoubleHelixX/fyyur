
# !!!                                    THIS PAGE CONTAINS CONSTANT VARIABLES THAT ARE VERY IMPORTANT


import os
SECRET_KEY = os.urandom(32)

#  Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))


# ----------------------------------------------------------------------------#
#                ! Future implementation - do not touch
# *              Constants for Authlib.integrations implementation
# ----------------------------------------------------------------------------#
#  AUTH0_CLIENT_ID = 'AUTH0_CLIENT_ID'
#  AUTH0_CLIENT_SECRET = 'AUTH0_CLIENT_SECRET'
#  AUTH0_CALLBACK_URL = 'AUTH0_CALLBACK_URL'
#  AUTH0_DOMAIN = 'AUTH0_DOMAIN'
#  AUTH0_AUDIENCE = 'AUTH0_AUDIENCE'
#  PROFILE_KEY = 'profile'
#  SECRET_KEY = 'ThisIsTheSecretKey'
#  JWT_PAYLOAD = 'jwt_payload'


# ----------------------------------------------------------------------------#
# *              Constants for Storing auth configuration
# ----------------------------------------------------------------------------#
auth0_config = {
    "AUTH0_DOMAIN": 'double-helixx.us.auth0.com',
    "ALGORITHMS": ["RS256"],
    "API_AUDIENCE": "image"
}


# ----------------------------------------------------------------------------#
# *              Constants for Storing the bearer tokens
# ----------------------------------------------------------------------------#
bearer_tokens = {
    "store_manager":  " Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjJpZzd3T0p6dEo1MnZDMzFBN2FyNyJ9.eyJpc3MiOiJodHRwczovL2RvdWJsZS1oZWxpeHgudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmMGNmMTI2MmViMzAzMDAxOWM4NzFkYyIsImF1ZCI6ImltYWdlIiwiaWF0IjoxNTk3ODk1NzgzLCJleHAiOjE1OTc5ODIxODMsImF6cCI6Imw2eW5nNUxGdEtaSUZaNkk1NmZnUHlKcWJmSjN5ZzhVIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJjcmVhdGU6YmF5cyIsImRlbGV0ZTpiYXlzIiwiZGVsZXRlOmRyaW5rcyIsImdldDpiYXlzIiwiZ2V0OmRhdGEiLCJnZXQ6ZHJpbmtzLWRldGFpbCIsInBhdGNoOmJheXMiLCJwYXRjaDpkcmlua3MiLCJwb3N0OmRyaW5rcyJdfQ.d8YJ2STpNNKWkoyJyzOem5sfdF9zlXawZyv-mZHgVIrSgVEOrZJeTTMWoWIDy3JdRYHn6Gn00kRszAPLN_J3HxsYRQ2SwVJCHbBtfsgB5WcNiw6G3ljVpfeHXuiyb1Z5zXrjjTLxuBstkJdCZ5INQKfPhOBGk792F9f68v3L-PIyE_k5H9ZTQw7gtNyzYrOOe-ItoxcALAAc1g6WnCy4RIp5O9gPKU5cPx1yzpxmQhoJ-sIJeVMv6h3jN-0AeOkaT8LrqNHq3-YEs5cmRc1DbfdNIuEiWTSzQFiW9LlMloboJdt9d6rZr5YRfqt9QLUw48dhvpkVjPl64uIzncuwlw",
    "assistant_manager": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjJpZzd3T0p6dEo1MnZDMzFBN2FyNyJ9.eyJpc3MiOiJodHRwczovL2RvdWJsZS1oZWxpeHgudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmMGNmMWM3MmViMzAzMDAxOWM4NzFkZSIsImF1ZCI6ImltYWdlIiwiaWF0IjoxNTk3ODk1OTA1LCJleHAiOjE1OTc5ODIzMDUsImF6cCI6Imw2eW5nNUxGdEtaSUZaNkk1NmZnUHlKcWJmSjN5ZzhVIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YmF5cyIsImdldDpkYXRhIiwiZ2V0OmRyaW5rcy1kZXRhaWwiXX0.oMSt-wCYMggdZkjD8PuguaGS3oY4e1SwgqGiKIbsTmBZ5TYlIW1pGfFwwdy4b1hUqdznzEiPLkaiXqtzVfP-NaaAcWVoom9uAR_eXQL3et3MdkJxnAC2RXusA-8V7-0ZzxttFpTorQEqr2PSGAUfmns0iRwQ-B-aZu1lHH_2Ip7TGfkErWKP6l8zP_--aZP8X8JnMRfe5rVmwZ9b2XJ9KjxhdJWd5GKEkRfnuCTOc0Cjv_o953BNSt1muhlm0CdrBLS8O1Tkc-D1xB9vGpbWaNAf2X1BrZR4x60dOAZX_IBCEPT_vN6NB_aIr_OLdHoMuMOOrHogPPupuuosfMfWOg"
}


# ----------------------------------------------------------------------------#
# *              Constants for Database Configuration
# ----------------------------------------------------------------------------#

database_setup = {
    "database_name": "fyyur",
    "user_name": "postgres",
    "password": "1",
    "port": "localhost:5432"
}


# -------------------------------------------------------------------------------------------------------#
# !                           Used for unit testing
# * Constants for Storing the JSON data used to initialized the database with data.
# -------------------------------------------------------------------------------------------------------#
jsonData = {
    'venue_edit': {
        "id": 1,
        "name": "The Musical Hop",
        "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
        "address": "1015 Folsom Street",
        "city": "San Francisco",
        "state": "CA",
        "phone": "123-123-1234",
        "website": "https://www.themusicalhop.com",
        "facebook_link": "https://www.facebook.com/TheMusicalHop",
        "seeking_talent": True,
        "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
        "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
    },
    'venue_search': {
        "count": 1,
        "data": [{
            "id": 2,
            "name": "The Dueling Pianos Bar",
            "num_upcoming_shows": 0,
        }]},
    'shows_create': [{
        "venue_id": 1,
        "venue_name": "The Musical Hop",
        "artist_id": 4,
        "artist_name": "Guns N Petals",
        "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
        "start_time": "2019-05-21T21:30:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 5,
        "artist_name": "Matt Quevedo",
        "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
        "start_time": "2019-06-15T23:00:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-01T20:00:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-08T20:00:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-15T20:00:00.000Z"
    }]
}

# -------------------------------------------------------------------------------------------------------#
# !                                          Used for unit testing
# * Constants for Storing the JSON data used to create new BAY objects when testing.
# -------------------------------------------------------------------------------------------------------#
new_bay_data = {
    'new_bay':  {
        "bay": "12",
        "data": [{
            "section": "A",
            "name":  "new bay",
            "style": "S5454",
            "row": "4",
            "col": "2",
            "notes":  "Box color is Yellow.",
            "gender":  "M",
            "img":  "https://bit.ly/31sgwi5"
        }]
    },
    'existing_bay': {
        "bay": "1",
        "data": [{
            "section": "A",
            "name":  "new bay",
            "style": "S5454",
            "row": "4",
            "col": "2",
            "notes":  "Box color is Yellow.",
            "gender":  "M",
            "img":  "https://bit.ly/31sgwi5"
        }]
    },
    'edit_bay': {
        "bay": "1",
        "data": [{
            "shoe_id": "5",
            "section": "A",
            "name":  "CHANGED BABY",
            "style": "S5454",
            "row": "4",
            "col": "2",
            "notes":  "SOME NOTES",
            "gender":  "F",
            "img":  "https://images.unsplash.com/photo-1536787175219-c199c3100742?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=634&q=80"
        }]
    },
    'edit_bay_403': {
        "bay": "1",
        "data": [{
            "shoe_id": "10",
            "section": "B",
            "name":  "CHANGED BABY",
            "style": "4554",
            "row": "5",
            "col": "1",
            "notes":  "SOME NOTES",
            "gender":  "M",
            "img":  ""
        }]
    },
    'delete_bay': {
        "bay": "2"
    },
    'edit_bay_404': {
        "bay": "9999",
        "data": [{
            "shoe_id": "10",
            "section": "A",
            "name":  "CHANGED BABY",
            "style": "S5454",
            "row": "4",
            "col": "2",
            "notes":  "SOME NOTES",
            "gender":  "F",
            "img":  "https://images.unsplash.com/photo-1536787175219-c199c3100742?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=634&q=80"
        }]
    }


}
