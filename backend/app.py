from flask import Flask, request, session, redirect
from flask_cors import CORS
import sqlite3
from datetime import datetime
import os
import re


app = Flask(__name__)
CORS(app)

# Set FLASK_SECRET_KEY in your hosting provider environment variables.
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or os.urandom(32)

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database.db")




def init_db():

    conn = sqlite3.connect(DB_PATH)

    # -------------------------
    # MESSAGES TABLE
    # -------------------------

    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            subject TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT
        )
    """)

    # -------------------------
    # CREATED_AT COLUMN CHECK
    # -------------------------

    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(messages)")
    columns = [column[1] for column in cursor.fetchall()]

    if "created_at" not in columns:
        conn.execute(
            "ALTER TABLE messages ADD COLUMN created_at TEXT"
        )

    # -------------------------
    # OLD MESSAGES DATE UPDATE
    # -------------------------

    conn.execute("""
        UPDATE messages
        SET created_at = ?
        WHERE created_at IS NULL
    """, (
        datetime.now().strftime("%d-%m-%Y %I:%M %p"),
    ))

    # -------------------------
    # SONGS TABLE
    # -------------------------

    conn.execute("""
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            artist TEXT NOT NULL,
            year TEXT,
            duration TEXT,
            video_id TEXT
        )
    """)

    # Migrate older databases to include the column used by song queries.
    cursor.execute("PRAGMA table_info(songs)")
    song_columns = [column[1] for column in cursor.fetchall()]
    if "release_date" not in song_columns:
        conn.execute("ALTER TABLE songs ADD COLUMN release_date TEXT")

    # -------------------------
    # SONG DATA
    # -------------------------

    songs = [
        (
            "Katchi Sera",
            "Sai Abhyankkar",
            "2024",
            "3:42",
            "VU23OPQ1Pmc"
        ),
        (
            "Aasa Kooda",
            "Sai Abhyankkar",
            "2024",
            "",
            "a3Ue-LN5B9U"
        ),
        (
            "Pavazha Malli",
            "Sai Abhyankkar",
            "2026",
            "",
            "b68HETiNO98"
        ),
        (
            "Sithira Puthira",
            "Sai Abhyankkar",
            "2025",
            "",
            "PqVvrF7pwDQ"
        ),
        (
            "Vizhi Veekura",
            "Sai Abhyankkar",
            "2025",
            "",
            "_e45NEdNMXE"
        ),
        (
            "Radhimaa",
            "Sai Abhyankkar",
            "2026",
            "",
            "jR3rWCBeO6M"
        )
    ]

    # -------------------------
    # REMOVE DUPLICATE SONGS
    # -------------------------

    conn.execute("""
        DELETE FROM songs
        WHERE id NOT IN (
            SELECT MIN(id)
            FROM songs
            GROUP BY title
        )
    """)

    # -------------------------
    # INSERT SONGS
    # -------------------------

    for song in songs:

        existing = conn.execute("""
            SELECT id
            FROM songs
            WHERE title = ?
        """, (song[0],)).fetchone()

        if not existing:
            conn.execute("""
                INSERT INTO songs
                (title, artist, year, duration, video_id)
                VALUES (?, ?, ?, ?, ?)
            """, song)






#         VIDEO_CATEGORIES = {
#          "interview": [
#         {
#             "title": "GRT Jewellers Interview",
#             "video_id": "PF2vF0N807A"
#         },
#         {
#             "title": "Katchi Sera Exclusive Interview",
#             "video_id": "abaca87H3MM"
#         },
#         {
#             "title": "Katchi Sera - RJ Jawi",
#             "video_id": "E0UWmucvDFw"
#         },
#         {
#             "title": "Aasa Kooda Interview",
#             "video_id": "2GL8qvlAnoQ"
#         },
#         {
#             "title": "Provoke Podcast",
#             "video_id": "9Q2qOJO8v-w"
#         },
#         {
#             "title": "Billboard India Interview",
#             "video_id": "Av3pw4fScuI"
#         }
#     ],

#     "audio_launch": [
#         {
#             "title": "Baththa Audio Launch",
#             "video_id": "y_xkEFg8D5s"
#         },
#         {
#             "title": "Pavazha Malli Release Event",
#             "video_id": "8ClfSLzwCdw"
#         },
#         {
#             "title": "Diwali Music Concert",
#             "video_id": "AwEAsvb8U4k"
#         },
#         {
#             "title": "Kochi Lulu Mall Event",
#             "video_id": "0YzT8XtvoKw"
#         }
#     ],

#     "awards": [
#         {
#             "title": "Nambikkai Awards 2024",
#             "video_id": "zvusJj0MOes"
#         },
#         {
#             "title": "Ananda Vikatan Cinema Awards",
#             "video_id": "1XH1Oz-_NZs"
#         }
#     ]
# }


# VIDEO_CATEGORIES = {
#     "interview": [
#         {
#             "title": "GRT Jewellers Interview",
#             "video_id": "PF2vF0N807A"
#         },
#         {
#             "title": "Katchi Sera Exclusive Interview",
#             "video_id": "abaca87H3MM"
#         },
#         {
#             "title": "RJ Jawi Interview",
#             "video_id": "E0UWmucvDFw"
#         },
#         {
#             "title": "Aasa Kooda Interview",
#             "video_id": "2GL8qvlAnoQ"
#         },
#         {
#             "title": "Provoke Podcast",
#             "video_id": "9Q2qOJO8v-w"
#         },
#         {
#             "title": "Billboard India Interview",
#             "video_id": "Av3pw4fScuI"
#         }
#     ],

#     "audio_launch": [
#         {
#             "title": "Baththa Audio Launch",
#             "video_id": "y_xkEFg8D5s"
#         },
#         {
#             "title": "Pavazha Malli Release Event",
#             "video_id": "8ClfSLzwCdw"
#         },
#         {
#             "title": "Diwali Music Concert",
#             "video_id": "AwEAsvb8U4k"
#         },
#         {
#             "title": "Kochi Lulu Mall Event",
#             "video_id": "0YzT8XtvoKw"
#         }
#     ],

#     "awards": [
#         {
#             "title": "Nambikkai Awards 2024",
#             "video_id": "zvusJj0MOes"
#         },
#         {
#             "title": "Ananda Vikatan Cinema Awards",
#             "video_id": "1XH1Oz-_NZs"
#         }
#     ]
# }

VIDEO_CATEGORIES = {
    # Videos are grouped by their actual title/content. A video can appear in
    # more than one category when it fits both (for example, a live launch event).
    "interview": [
        {"title": "GRT Jewellers Interview", "video_id": "PF2vF0N807A"},
        {"title": "Katchi Sera Exclusive Interview", "video_id": "abaca87H3MM"},
        {"title": "Katchi Sera - RJ Jawi Interview", "video_id": "E0UWmucvDFw"},
        {"title": "Aasa Kooda Release - Sai Abhyankkar", "video_id": "2GL8qvlAnoQ"},
        {"title": "Sai Abhyankkar Interview (Tamil)", "video_id": "ehKi8JYKr9o"},
        {"title": "Sai Abhyankkar Special Interview", "video_id": "fW3v4zitY-8"},
        {"title": "Billboard India Interview", "video_id": "Av3pw4fScuI"},
        {"title": "Music Interview - Simbu's Call and Anirudh Comparisons", "video_id": "zD1dN1wAJqU"},
        {"title": "InFocus - THR India", "video_id": "Q4sX3dT2ufo"},
        {"title": "Baththa Team Interview - Atlee and Sai Abhyankkar", "video_id": "Za94vzROmT4"},
        {"title": "Sai Abhyankkar Cute Comments - I Am Single", "video_id": "rO0UOhxggwQ"},
    ],
    "audio_launch": [
        {"title": "Baththa Audio Launch - Comedy Speech", "video_id": "y_xkEFg8D5s"},
        {"title": "Karuppu Suriya New Song Launch Speech", "video_id": "dAO6EDgYubQ"},
        {"title": "Pavazha Malli Song Release Event - Live Performance", "video_id": "8ClfSLzwCdw"},
        {"title": "Balti Trailer Launch - Kochi", "video_id": "0YzT8XtvoKw"},
    ],
    "awards": [
        {"title": "Nambikkai Awards 2024", "video_id": "zvusJj0MOes"},
        {"title": "Ananda Vikatan Cinema Awards", "video_id": "1XH1Oz-_NZs"},
        {"title": "Vikatan Cinema Awards - Red Carpet", "video_id": "YX1DV02DSx4"},
        {"title": "STR 49 Love Song - Award Related Video", "video_id": "29rlJQGGj4s"},
    ],
    "live_performances": [
        {"title": "Aasa Kooda - Live", "video_id": "gP6g9DUpHwg"},
        {"title": "Pavazha Malli - Live", "video_id": "dqvb6f882Uw"},
        {"title": "Sai Abhyankkar Dance of the Decade - Pavazha Malli", "video_id": "AQgwiM1CFiY"},
        {"title": "Sai Abhyankkar Sings for Mamitha Baiju - Live", "video_id": "cuV7y6DU4zw"},
        {"title": "Kadavule Thalapathy - Live Performance", "video_id": "LcNCEdLzQo0"},
        {"title": "Mesmerizing Performance - Aasa Kooda", "video_id": "DkWS6nifcD0"},
        {"title": "Diwali Music Concert - Live", "video_id": "AwEAsvb8U4k"},
        {"title": "Raathu Raasan - Live Performance", "video_id": "K8UJiAzDJ4o"},
        {"title": "Naanga Naalu Peru - Live Performance", "video_id": "GFGBPTz8Yqg"},
        {"title": "God Mode - Live Performance", "video_id": "J7R-UKGQQ_g"},
        {"title": "Ooroda Oththa Don - Live Performance", "video_id": "q8sgLhmoB4o"},
        {"title": "Pavazha Malli Song Release Event - Live Performance", "video_id": "8ClfSLzwCdw"},
    ],
    "podcast": [
        {"title": "Sai Abhyankkar - Provoke Podcast", "video_id": "9Q2qOJO8v-w"},
        {"title": "Fries With Potate x Sai Abhyankkar", "video_id": "g_zIBrA9Gg4"},
    ],
    "music_videos": [
        {"title": "Refugee - Official Music Video (Jordan Sandhu)", "video_id": "xLj0OR5j1UI"},
    ],
    "promotional": [
        {"title": "One Corner Vs Full-home", "video_id": "k29G-awiwks"},
        {"title": "Built to be Unreasonable - Only Possible with Ultraviolette", "video_id": "dqvb6f882Uw"},
        {"title": "It's The Time To Moto - Moto G37 Power", "video_id": "jj9zCQq3U1s"},
        {"title": "BlackRock Hong Kong Snapshot", "video_id": "aBBHKtdD_3U"},
        {"title": "Moto Edge 70 Fusion - Big Billion Moto Deals", "video_id": "RvgtyI2CB6M"},
        {"title": "Worth Aana Workout Mix ft. RJ Balaji and Sai Abhyankkar", "video_id": "B3YP1JIBPIk"},
        {"title": "Truth & Spice Season 1 Episode 1 - Kullu x Larissa", "video_id": "JHClPSWr_9o"},
    ],
    "all_videos": [
        {"title": "Aasa Kooda - Live", "video_id": "gP6g9DUpHwg"},
        {"title": "Pavazha Malli - Live", "video_id": "dqvb6f882Uw"},
        {"title": "Sai Abhyankkar Dance of the Decade - Pavazha Malli", "video_id": "AQgwiM1CFiY"},
        {"title": "Nambikkai Awards 2024", "video_id": "zvusJj0MOes"},
        {"title": "Sai Abhyankkar Sings for Mamitha Baiju - Live", "video_id": "cuV7y6DU4zw"},
        {"title": "Kadavule Thalapathy - Live Performance", "video_id": "LcNCEdLzQo0"},
        {"title": "One Corner Vs Full-home", "video_id": "k29G-awiwks"},
        {"title": "Ananda Vikatan Cinema Awards", "video_id": "1XH1Oz-_NZs"},
        {"title": "Pavazha Malli Song Release Event - Live Performance", "video_id": "8ClfSLzwCdw"},
        {"title": "Built to be Unreasonable - Only Possible with Ultraviolette", "video_id": "dqvb6f882Uw"},
        {"title": "Balti Trailer Launch - Kochi", "video_id": "0YzT8XtvoKw"},
        {"title": "Refugee - Official Music Video (Jordan Sandhu)", "video_id": "xLj0OR5j1UI"},
        {"title": "Diwali Music Concert - Live", "video_id": "AwEAsvb8U4k"},
        {"title": "Raathu Raasan - Live Performance", "video_id": "K8UJiAzDJ4o"},
        {"title": "Naanga Naalu Peru - Live Performance", "video_id": "GFGBPTz8Yqg"},
        {"title": "God Mode - Live Performance", "video_id": "J7R-UKGQQ_g"},
        {"title": "Baththa Audio Launch - Comedy Speech", "video_id": "y_xkEFg8D5s"},
        {"title": "Ooroda Oththa Don - Live Performance", "video_id": "q8sgLhmoB4o"},
        {"title": "GRT Jewellers Interview", "video_id": "PF2vF0N807A"},
        {"title": "Katchi Sera Exclusive Interview", "video_id": "abaca87H3MM"},
        {"title": "Katchi Sera - RJ Jawi Interview", "video_id": "E0UWmucvDFw"},
        {"title": "Aasa Kooda Release - Sai Abhyankkar", "video_id": "2GL8qvlAnoQ"},
        {"title": "Mesmerizing Performance - Aasa Kooda", "video_id": "DkWS6nifcD0"},
        {"title": "Sai Abhyankkar - Provoke Podcast", "video_id": "9Q2qOJO8v-w"},
        {"title": "Sai Abhyankkar Interview (Tamil)", "video_id": "ehKi8JYKr9o"},
        {"title": "Sai Abhyankkar Special Interview", "video_id": "fW3v4zitY-8"},
        {"title": "Billboard India Interview", "video_id": "Av3pw4fScuI"},
        {"title": "Truth & Spice Season 1 Episode 1 - Kullu x Larissa", "video_id": "JHClPSWr_9o"},
        {"title": "It's The Time To Moto - Moto G37 Power", "video_id": "jj9zCQq3U1s"},
        {"title": "Karuppu Suriya New Song Launch Speech", "video_id": "dAO6EDgYubQ"},
        {"title": "Sai Abhyankkar Cute Comments - I Am Single", "video_id": "rO0UOhxggwQ"},
        {"title": "Fries With Potate x Sai Abhyankkar", "video_id": "g_zIBrA9Gg4"},
        {"title": "Music Interview - Simbu's Call and Anirudh Comparisons", "video_id": "zD1dN1wAJqU"},
        {"title": "BlackRock Hong Kong Snapshot", "video_id": "aBBHKtdD_3U"},
        {"title": "Moto Edge 70 Fusion - Big Billion Moto Deals", "video_id": "RvgtyI2CB6M"},
        {"title": "InFocus - THR India", "video_id": "Q4sX3dT2ufo"},
        {"title": "Worth Aana Workout Mix ft. RJ Balaji and Sai Abhyankkar", "video_id": "B3YP1JIBPIk"},
        {"title": "Baththa Team Interview - Atlee and Sai Abhyankkar", "video_id": "Za94vzROmT4"},
    ],
}

@app.route("/ai-chat", methods=["POST"])
def ai_chat():
    try:
        data = request.get_json(silent=True) or {}
        message = data.get("message", "").strip()

        if not message:
            return {"reply": "Please enter a message."}, 400

        text = message.lower().strip()

        video_id = None
        videos = []
        reply = ""

        # ---------------------------------
        # VIDEO CATEGORY SEARCH
        # Keep these checks before song search so category requests return lists.
        # ---------------------------------
        category_requests = [
            (("interview", "interviews"), "interview", "Here are Sai Abhyankkar's interview videos! 🎤💗"),
            (("audio launch", "audio launches", "song launch", "release event", "launch videos"), "audio_launch", "Here are the audio launch and release-event videos! 🎬🎵"),
            (("award", "awards", "red carpet"), "awards", "Here are the award-related videos! 🏆🎬"),
            (("podcast", "podcasts"), "podcast", "Here are the podcast and talk-show videos! 🎙️💗"),
            (("live performance", "live performances", "live concert", "live concerts", "concert", "concerts", "performances"), "live_performances", "Here are the live performances and concert videos! 🎤🎶"),
            (("music video", "music videos", "official video", "official music video"), "music_videos", "Here are the music-video links! 🎵🎬"),
            (("promo", "promotional", "advertisement", "ads", "brand video"), "promotional", "Here are the promotional and brand videos! ✨🎬"),
        ]

        asks_for_list = any(word in text for word in ["show", "list", "all", "give", "display", "videos", "video", "watch", "see"])
        if asks_for_list:
            for keywords, category_key, category_reply in category_requests:
                if any(keyword in text for keyword in keywords):
                    return {
                        "reply": category_reply + " Choose any video below.",
                        "video_id": None,
                        "videos": VIDEO_CATEGORIES[category_key]
                    }

            if any(word in text for word in ["all videos", "all the videos", "every video", "videos on this website", "all categories"]):
                return {
                    "reply": "Here are the videos currently listed on this website! 🎬💗 Choose any video below.",
                    "video_id": None,
                    "videos": VIDEO_CATEGORIES["all_videos"]
                }

        # Single specific event videos still play directly when requested by name.
        if "baththa" in text and ("audio launch" in text or "launch video" in text):
            return {"reply": "Here is the Baththa Audio Launch video! 🎬🎤", "video_id": "y_xkEFg8D5s", "videos": []}
        if "karuppu suriya" in text and ("launch" in text or "video" in text or "watch" in text):
            return {"reply": "Here is the Karuppu Suriya Song Launch video! 🎬🎤", "video_id": "dAO6EDgYubQ", "videos": []}
        if "pavazha malli" in text and ("release event" in text or "launch" in text):
            return {"reply": "Here is the Pavazha Malli Release Event! 🎬🎤", "video_id": "8ClfSLzwCdw", "videos": []}
        if "red carpet" in text and "award" in text:
            return {"reply": "Here is the Vikatan Cinema Awards Red Carpet video! 🏆", "video_id": "YX1DV02DSx4", "videos": []}
        if "str 49" in text and ("award" in text or "love song" in text):
            return {"reply": "Here is the STR 49 Love Song video! 🏆🎬", "video_id": "29rlJQGGj4s", "videos": []}

        # ---------------------------------
        # DATABASE SONG SEARCH
        # ---------------------------------
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row

        try:
            songs = conn.execute("""
                SELECT id, title, artist, year, duration,
                       video_id, release_date
                FROM songs
            """).fetchall()
        finally:
            conn.close()

        song = None

        for item in songs:
            if item["title"] and item["title"].lower() in text:
                song = dict(item)
                break

        # ---------------------------------
        # PLAY SONG FROM DATABASE
        # ---------------------------------
        if song and any(word in text for word in [
            "play", "watch", "video", "live"
        ]):
            return {
                "reply": f"Playing {song['title']} 🎵🎬",
                "video_id": song["video_id"],
                "videos": []
            }

        # ---------------------------------
        # SONG ARTIST / SINGER
        # ---------------------------------
        if song and any(phrase in text for phrase in [
            "who sang",
            "who is the artist",
            "who is the singer",
            "singer of",
            "artist of"
        ]):
            return {
                "reply": (
                    f"{song['title']} was sung by "
                    f"{song['artist']}. 🎤🎵"
                ),
                "video_id": None,
                "videos": []
            }

        # ---------------------------------
        # SONG RELEASE DATE
        # ---------------------------------
        if song and any(phrase in text for phrase in [
            "when was", "release date", "released"
        ]):
            return {
                "reply": (
                    f"{song['title']} was released on "
                    f"{song['release_date']}. 📅🎵"
                ),
                "video_id": None,
                "videos": []
            }

        # ---------------------------------
        # SONG SEARCH BY YEAR
        # ---------------------------------
        year_match = re.search(r"\b(20\d{2})\b", text)

        if year_match and any(word in text for word in [
            "songs", "song", "released"
        ]):
            search_year = year_match.group(1)

            conn = sqlite3.connect(DB_PATH)
            conn.row_factory = sqlite3.Row

            try:
                songs_list = conn.execute("""
                    SELECT title, artist, year, release_date
                    FROM songs
                    WHERE year = ?
                    ORDER BY id
                """, (search_year,)).fetchall()
            finally:
                conn.close()

            if songs_list:
                song_text = "\n".join(
                    f"🎵 {item['title']} - {item['artist']} "
                    f"({item['year']}) - Released: {item['release_date']}"
                    for item in songs_list
                )

                return {
                    "reply": (
                        f"Here are the songs from {search_year}:\n\n"
                        f"{song_text}"
                    ),
                    "video_id": None,
                    "videos": []
                }

            return {
                "reply": f"No songs found from {search_year}. 🎵",
                "video_id": None,
                "videos": []
            }

        # ---------------------------------
        # SONG SEARCH BY ARTIST
        # ---------------------------------
        if "songs by" in text or "songs from artist" in text:
            artist_name = text.replace("show songs by", "").strip()
            artist_name = artist_name.replace("songs by", "").strip()
            artist_name = artist_name.replace("songs from artist", "").strip()

            display_artist = (
                "Sai Abhyankkar"
                if artist_name.lower() == "sai abhyankkar"
                else artist_name
            )

            conn = sqlite3.connect(DB_PATH)
            conn.row_factory = sqlite3.Row

            try:
                songs_list = conn.execute("""
                    SELECT title, artist, year, release_date
                    FROM songs
                    WHERE LOWER(artist) = LOWER(?)
                    ORDER BY id
                """, (artist_name,)).fetchall()
            finally:
                conn.close()

            if songs_list:
                song_text = "\n".join(
                    f"🎵 {item['title']} - {item['artist']} "
                    f"({item['year']}) - Released: {item['release_date']}"
                    for item in songs_list
                )

                return {
                    "reply": (
                        f"Here are the songs by {display_artist}:\n\n"
                        f"{song_text}"
                    ),
                    "video_id": None,
                    "videos": []
                }

            return {
                "reply": f"No songs found for {artist_name}. 🎵",
                "video_id": None,
                "videos": []
            }

        # ---------------------------------
        # RELATED SONGS
        # ---------------------------------
        if "like radhimaa" in text:
            return {
                "reply": (
                    "If you like Radhimaa, you can also explore "
                    "Pavazha Malli and Aasa Kooda. 🎵💖"
                ),
                "video_id": None,
                "videos": []
            }

        # ---------------------------------
        # SONG RECOMMENDATION
        # ---------------------------------
        if any(phrase in text for phrase in [
            "recommend me a song",
            "recommend a song",
            "suggest a song",
            "suggest me a song"
        ]):
            return {
                "reply": "🎵 I recommend Radhimaa! Give it a listen. 💖🎶",
                "video_id": "jR3rWCBeO6M",
                "videos": []
            }

        # ---------------------------------
        # MOOD-BASED RECOMMENDATIONS
        # ---------------------------------
        if "romantic" in text or "love song" in text:
            return {
                "reply": "💖 I recommend Radhimaa for a romantic mood! 🎶",
                "video_id": None,
                "videos": []
            }

        if "melody" in text or "calm" in text:
            return {
                "reply": "🎶 I recommend Pavazha Malli for a calm mood! 💕",
                "video_id": "b68HETiNO98",
                "videos": []
            }

        if "energetic" in text or "energy" in text:
            return {
                "reply": "🔥 I recommend Katchi Sera for an energetic mood! 🎵",
                "video_id": "VU23OPQ1Pmc",
                "videos": []
            }

        if "dance" in text or "dancing" in text:
            return {
                "reply": "💃 I recommend Katchi Sera! 🎵🔥",
                "video_id": "VU23OPQ1Pmc",
                "videos": []
            }

        if "party" in text:
            return {
                "reply": "🎉 I recommend Katchi Sera for a party mood! 🔥🎶",
                "video_id": "VU23OPQ1Pmc",
                "videos": []
            }

        if "relax" in text or "relaxing" in text:
            return {
                "reply": "😌 I recommend Pavazha Malli for a relaxing mood! 🎶💖",
                "video_id": "b68HETiNO98",
                "videos": []
            }

        if "night" in text:
            return {
                "reply": "🌙 I recommend Radhimaa for a night mood! 🎶✨",
                "video_id": "jR3rWCBeO6M",
                "videos": []
            }

        # ---------------------------------
        # SONG INFORMATION
        # ---------------------------------
        if song:
            return {
                "reply": (
                    f"{song['title']} is a song by {song['artist']}. "
                    f"Year: {song['year']}. "
                    f"Release date: {song['release_date']}. "
                    f"Duration: {song['duration']}. 🎵"
                ),
                "video_id": None,
                "videos": []
            }

        # ---------------------------------
        # SONG LIST
        # ---------------------------------
        if any(phrase in text for phrase in [
            "what songs", "list songs", "show songs",
            "available songs", "all songs"
        ]):
            conn = sqlite3.connect(DB_PATH)
            conn.row_factory = sqlite3.Row

            try:
                songs_list = conn.execute("""
                    SELECT title, artist, year, release_date
                    FROM songs
                    ORDER BY id
                """).fetchall()
            finally:
                conn.close()

            song_text = "\n".join(
                f"🎵 {item['title']} - {item['artist']} "
                f"({item['year']}) - Released: {item['release_date']}"
                for item in songs_list
            )

            return {
                "reply": (
                    "Here are the songs available on this website:\n\n"
                    + (song_text or "No songs found.")
                ),
                "video_id": None,
                "videos": []
            }

        # ---------------------------------
        # GREETINGS
        # ---------------------------------
        if text in ["hi", "hello", "hey", "hai", "hii", "hlo"]:
            reply = "Hi! 👋 I'm Sai AI. How can I help you?"

        # ---------------------------------
        # ABOUT SAI
        # ---------------------------------
        elif any(phrase in text for phrase in [
            "who is sai",
            "who is sai abhyankkar",
            "tell me about sai",
            "about sai"
        ]):
            reply = (
                "Sai Abhyankkar is a singer, songwriter and performer. "
                "🎵 You can explore his music and performances here."
            )

        # ---------------------------------
        # SONG-SPECIFIC REQUESTS
        # ---------------------------------
        elif "katchi sera" in text:
            if any(word in text for word in ["watch", "video", "live", "play"]):
                reply = "Playing Katchi Sera 🎵🎬"
                video_id = "VU23OPQ1Pmc"
            else:
                reply = "Katchi Sera is one of Sai Abhyankkar's popular songs. 🎶"

        elif "aasa kooda" in text:
            if any(word in text for word in ["watch", "video", "live", "play"]):
                reply = "Playing Aasa Kooda 🎵🎬"
                video_id = "a3Ue-LN5B9U"
            else:
                reply = "Aasa Kooda is one of Sai Abhyankkar's songs. 🎵"

        elif "pavazha malli" in text:
            if any(word in text for word in ["watch", "video", "live", "play"]):
                reply = "Playing Pavazha Malli 🎵🎬"
                video_id = "b68HETiNO98"
            else:
                reply = "Pavazha Malli is one of Sai Abhyankkar's songs. 🎵"

        elif "sithira puthira" in text or "sithra pudhiri" in text:
            if any(word in text for word in ["watch", "video", "live", "play"]):
                reply = "Playing Sithira Puthira 🎵🎬"
                video_id = "PqVvrF7pwDQ"
            else:
                reply = "Sithira Puthira is one of Sai Abhyankkar's songs. 🎵"

        elif "vizhi veekura" in text:
            if any(word in text for word in ["watch", "video", "live", "play"]):
                reply = "Playing Vizhi Veekura 🎵🎬"
                video_id = "_e45NEdNMXE"
            else:
                reply = "Vizhi Veekura is one of Sai Abhyankkar's songs. 🎵"

        elif "radhimaa" in text:
            if any(word in text for word in ["watch", "video", "live", "play"]):
                reply = "Playing Radhimaa 🎵🎬"
                video_id = "jR3rWCBeO6M"
            else:
                reply = "Radhimaa is one of Sai Abhyankkar's songs. 🎵"

        # ---------------------------------
        # LIVE PERFORMANCES
        # ---------------------------------
        elif "live performance" in text or "live performances" in text:
            reply = (
                "You can watch Sai Abhyankkar's live performances "
                "in the Videos section. 🎤🎶"
            )

        elif "live concert" in text or "concert" in text:
            reply = (
                "You can explore Sai Abhyankkar's live concerts "
                "in the Videos section. 🎤🎶"
            )

        # ---------------------------------
        # WEBSITE QUESTIONS
        # ---------------------------------
        elif "where can i listen" in text:
            reply = "You can listen to Sai Abhyankkar's songs in the Music section. 🎧"

        elif "where can i watch" in text:
            reply = "You can watch Sai Abhyankkar's performances in the Videos section. 🎬"

        # ---------------------------------
        # AI INTRODUCTION
        # ---------------------------------
        elif any(phrase in text for phrase in [
            "what is your name", "who are you", "your name"
        ]):
            reply = (
                "I'm Sai AI 🤖, the AI assistant for this website. "
                "I can help you explore Sai Abhyankkar's songs, videos "
                "and performances."
            )

        # ---------------------------------
        # GENERAL SONG / MUSIC REQUEST
        # ---------------------------------
        elif (
            "what songs" in text
            or "songs does sai have" in text
            or "what songs does sai have" in text
            or "songs" in text
            or "music" in text
        ):
            reply = "You can explore Sai Abhyankkar's songs in the Music section. 🎧🎶"

        # ---------------------------------
        # GENERAL VIDEO REQUEST
        # ---------------------------------
        elif "video" in text or "videos" in text:
            reply = "Here are the videos currently listed on this website! 🎬💗 Choose any video below."
            videos = VIDEO_CATEGORIES["all_videos"]

        # ---------------------------------
        # GENERAL RESPONSE
        # ---------------------------------
        else:
            reply = (
                "I'm Sai AI 🤖. I can help you explore Sai Abhyankkar's "
                "music, songs, videos and performances. Try asking me "
                "about a song, video or Sai!"
            )

        return {
            "reply": reply,
            "video_id": video_id,
            "videos": videos
        }

    except Exception as error:
        import traceback
        print("AI CHAT ERROR:", repr(error))
        traceback.print_exc()

        return {
            "reply": "Sorry, something went wrong. Please try again."
        }, 500




# ================= HOME =================

@app.route("/")
def home():

    return "Backend is working!"


@app.route("/songs", methods=["GET"])
def get_songs():

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    songs = conn.execute("""
        SELECT id, title, artist, year, duration, video_id, release_date
        FROM songs
        ORDER BY id
    """).fetchall()

    conn.close()

    return {
        "songs": [dict(song) for song in songs]
    }


def find_song(song_name):

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    song = conn.execute("""
        SELECT id, title, artist, year, duration, video_id, release_date
        FROM songs
        WHERE LOWER(title) = LOWER(?)
    """, (song_name,)).fetchone()

    conn.close()

    return dict(song) if song else None
# ================= CONTACT FORM =================

@app.route("/contact", methods=["POST"])
def contact():
    conn = None

    try:
        name = request.form.get("name", "")
        email = request.form.get("email", "")
        subject = request.form.get("subject", "")
        message = request.form.get("message", "")

        created_at = datetime.now().strftime("%d-%m-%Y %I:%M %p")

        conn = sqlite3.connect(DB_PATH)

        conn.execute("""
            INSERT INTO messages
            (name, email, subject, message, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            name,
            email,
            subject,
            message,
            created_at
        ))

        conn.commit()
        return "Message saved successfully!", 200

    except Exception as error:
        print("CONTACT FORM ERROR:", repr(error))

        if conn:
            conn.rollback()

        return "Unable to save message.", 500

    finally:
        if conn:
            conn.close()

# ================= ADMIN LOGIN =================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if (username == os.environ.get("ADMIN_USERNAME", "admin")
                and os.environ.get("ADMIN_PASSWORD")
                and password == os.environ.get("ADMIN_PASSWORD")):

            session["admin"] = True

            return redirect("/dashboard")

        return """
        <div style="
            text-align:center;
            font-family:Arial;
            margin-top:100px;
        ">

            <h3 style="color:red;">
                Invalid username or password
            </h3>

            <a href="/login">
                Try Again
            </a>

        </div>
        """

    return """
    <!DOCTYPE html>

    <html>

    <head>

        <title>Admin Login</title>

        <style>

            * {
                box-sizing: border-box;
            }

            body {
                margin: 0;
                font-family: Arial, sans-serif;
                background: #0b0b0f;
                color: white;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
            }

            .login-box {
                width: 380px;
                background: #17171d;
                padding: 40px;
                border-radius: 20px;
                box-shadow: 0 0 30px rgba(255, 79, 216, 0.15);
            }

            .logo {
                text-align: center;
                font-size: 35px;
            }

            h2 {
                text-align: center;
                color: #ff4fd8;
                margin-bottom: 30px;
            }

            input {
                width: 100%;
                padding: 14px;
                margin-bottom: 15px;
                border: 1px solid #333;
                border-radius: 10px;
                background: #222229;
                color: white;
                outline: none;
            }

            input:focus {
                border-color: #ff4fd8;
            }

            button {
                width: 100%;
                padding: 14px;
                border: none;
                border-radius: 10px;
                background: #ff4fd8;
                color: white;
                font-size: 16px;
                font-weight: bold;
                cursor: pointer;
            }

            button:hover {
                background: #ff2fcf;
            }

        </style>

    </head>

    <body>

        <div class="login-box">

            <div class="logo">🎵</div>

            <h2>Admin Login</h2>

            <form method="POST">

                <input
                    type="text"
                    name="username"
                    placeholder="Username"
                    required
                >

                <input
                    type="password"
                    name="password"
                    placeholder="Password"
                    required
                >

                <button type="submit">
                    Login
                </button>

            </form>

        </div>

    </body>

    </html>
    """


# ================= DASHBOARD =================

@app.route("/dashboard")
def dashboard():

    if not session.get("admin"):
        return redirect("/login")

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM messages")
    total_messages = cursor.fetchone()[0]

    cursor.execute("""
        SELECT *
        FROM messages
        ORDER BY id DESC
        LIMIT 5
    """)

    latest_messages = cursor.fetchall()

    conn.close()

    html = f"""
    <!DOCTYPE html>

    <html>

    <head>

        <title>Admin Dashboard</title>

        <style>

            * {{
                box-sizing: border-box;
            }}

            body {{
                margin: 0;
                font-family: Arial, sans-serif;
                background: #0b0b0f;
                color: white;
            }}

            .navbar {{
                background: #17171d;
                padding: 20px 40px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-bottom: 1px solid #292932;
            }}

            .brand {{
                font-size: 22px;
                font-weight: bold;
                color: #ff4fd8;
            }}

            .logout {{
                text-decoration: none;
                color: white;
                background: #ff4fd8;
                padding: 10px 18px;
                border-radius: 8px;
            }}

            .container {{
                padding: 40px;
            }}

            .welcome {{
                margin-bottom: 30px;
            }}

            .welcome h1 {{
                margin-bottom: 8px;
            }}

            .welcome p {{
                color: #888;
            }}

            .cards {{
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 20px;
                margin-bottom: 35px;
            }}

            .card {{
                background: #17171d;
                border: 1px solid #292932;
                border-radius: 16px;
                padding: 25px;
            }}

            .card-icon {{
                font-size: 30px;
            }}

            .card-title {{
                color: #888;
                margin-top: 10px;
            }}

            .card-number {{
                font-size: 35px;
                font-weight: bold;
                color: #ff4fd8;
                margin-top: 8px;
            }}

            .messages-box {{
                background: #17171d;
                border: 1px solid #292932;
                border-radius: 16px;
                padding: 25px;
            }}

            .messages-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
            }}

            .messages-header h2 {{
                margin: 0;
            }}

            .view-btn {{
                text-decoration: none;
                color: #ff4fd8;
                font-weight: bold;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
            }}

            th,
            td {{
                padding: 14px;
                border-bottom: 1px solid #292932;
                text-align: left;
            }}

            th {{
                color: #ff4fd8;
            }}

            td {{
                color: #ddd;
            }}

            @media (max-width: 800px) {{

                .cards {{
                    grid-template-columns: 1fr;
                }}

                .container {{
                    padding: 20px;
                }}

            }}

        </style>

    </head>

    <body>

        <div class="navbar">

            <div class="brand">
                🎵 Sai Admin
            </div>

            <a
                class="logout"
                href="/logout"
            >
                Logout
            </a>

        </div>

        <div class="container">

            <div class="welcome">

                <h1>
                    Welcome, Admin 👋
                </h1>

                <p>
                    Manage your website messages from here.
                </p>

            </div>

            <div class="cards">

                <div class="card">

                    <div class="card-icon">
                        📩
                    </div>

                    <div class="card-title">
                        Total Messages
                    </div>

                    <div class="card-number">
                        {total_messages}
                    </div>

                </div>

                <div class="card">

                    <div class="card-icon">
                        🎵
                    </div>

                    <div class="card-title">
                        Music
                    </div>

                    <div class="card-number">
                        6
                    </div>

                </div>

                <div class="card">

                    <div class="card-icon">
                        🎬
                    </div>

                    <div class="card-title">
                        Videos
                    </div>

                    <div class="card-number">
                        3
                    </div>

                </div>

            </div>

            <div class="messages-box">

                <div class="messages-header">

                    <h2>
                        Recent Messages
                    </h2>

                    <a
                        class="view-btn"
                        href="/messages"
                    >
                        View All →
                    </a>

                </div>

                <table>

                    <tr>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Subject</th>
                        <th>Date & Time</th>
                    </tr>
    """

    for row in latest_messages:

        html += f"""
                    <tr>

                        <td>{row[1]}</td>

                        <td>{row[2]}</td>

                        <td>{row[3]}</td>

                        <td>{row[5]}</td>

                    </tr>
        """

    html += """
                </table>

            </div>

        </div>

    </body>

    </html>
    """

    return html


# ================= VIEW ALL + SEARCH =================

@app.route("/messages")
def messages():

    if not session.get("admin"):
        return redirect("/login")

    search = request.args.get("search", "").strip()

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    if search:

        cursor.execute("""
            SELECT *
            FROM messages
            WHERE name LIKE ?
               OR email LIKE ?
               OR subject LIKE ?
               OR message LIKE ?
            ORDER BY id DESC
        """, (
            f"%{search}%",
            f"%{search}%",
            f"%{search}%",
            f"%{search}%"
        ))

    else:

        cursor.execute("""
            SELECT *
            FROM messages
            ORDER BY id DESC
        """)

    data = cursor.fetchall()

    conn.close()

    html = f"""
    <!DOCTYPE html>

    <html>

    <head>

        <title>Contact Messages</title>

        <style>

            * {{
                box-sizing: border-box;
            }}

            body {{
                margin: 0;
                font-family: Arial, sans-serif;
                background: #0b0b0f;
                color: white;
                padding: 30px;
            }}

            .top-bar {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 25px;
            }}

            h1 {{
                color: #ff4fd8;
            }}

            .buttons a {{
                text-decoration: none;
                color: white;
                padding: 10px 16px;
                border-radius: 8px;
                margin-left: 8px;
            }}

            .dashboard-btn {{
                background: #333;
            }}

            .logout-btn {{
                background: #ff4fd8;
            }}

            .search-box {{
                margin-bottom: 25px;
                display: flex;
                gap: 10px;
            }}

            .search-box input {{
                flex: 1;
                padding: 13px;
                border: 1px solid #333;
                border-radius: 8px;
                background: #17171d;
                color: white;
                outline: none;
            }}

            .search-box button {{
                padding: 13px 22px;
                border: none;
                border-radius: 8px;
                background: #ff4fd8;
                color: white;
                cursor: pointer;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                background: #17171d;
            }}

            th,
            td {{
                padding: 14px;
                border-bottom: 1px solid #333;
                text-align: left;
            }}

            th {{
                background: #222229;
                color: #ff4fd8;
            }}

            td {{
                color: #ddd;
            }}

            .reply-btn {{
                color: #4fd8ff;
                text-decoration: none;
                font-weight: bold;
                margin-right: 12px;
            }}

            .reply-btn:hover {{
                color: #00bfff;
            }}

            .delete-btn {{
                color: #ff4fd8;
                text-decoration: none;
                font-weight: bold;
            }}

            .delete-btn:hover {{
                color: red;
            }}

            .no-results {{
                text-align: center;
                color: #888;
                padding: 30px;
            }}

            @media (max-width: 800px) {{

                body {{
                    padding: 15px;
                }}

                .top-bar {{
                    flex-direction: column;
                    align-items: flex-start;
                    gap: 15px;
                }}

                .search-box {{
                    flex-direction: column;
                }}

                table {{
                    font-size: 12px;
                }}

                th,
                td {{
                    padding: 8px;
                }}

            }}

        </style>

    </head>

    <body>

        <div class="top-bar">

            <h1>
                Contact Messages
            </h1>

            <div class="buttons">

                <a
                    class="dashboard-btn"
                    href="/dashboard"
                >
                    Dashboard
                </a>

                <a
                    class="logout-btn"
                    href="/logout"
                >
                    Logout
                </a>

            </div>

        </div>

        <form
            class="search-box"
            method="GET"
            action="/messages"
        >

            <input
                type="text"
                name="search"
                value="{search}"
                placeholder="Search name, email, subject or message..."
            >

            <button type="submit">
                🔎 Search
            </button>

        </form>

        <table>

            <tr>

                <th>ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Subject</th>
                <th>Message</th>
                <th>Date & Time</th>
                <th>Reply</th>
                <th>Action</th>

            </tr>
    """

    if data:

        for row in data:

            html += f"""
            <tr>

                <td>{row[0]}</td>

                <td>{row[1]}</td>

                <td>{row[2]}</td>

                <td>{row[3]}</td>

                <td>{row[4]}</td>

                <td>{row[5]}</td>

                <td>

                    <a
                        class="reply-btn"
                        href="/reply/{row[0]}"
                    >
                        Reply
                    </a>

                </td>

                <td>

                    <a
                        class="delete-btn"
                        href="/delete/{row[0]}"
                    >
                        Delete
                    </a>

                </td>

            </tr>
            """

    else:

        html += """
            <tr>

                <td
                    class="no-results"
                    colspan="8"
                >
                    No messages found.
                </td>

            </tr>
        """

    html += """
        </table>

    </body>

    </html>
    """

    return html



    # ================= REPLY PAGE =================

@app.route("/reply/<int:id>", methods=["GET", "POST"])
def reply(id):

    if not session.get("admin"):
        return redirect("/login")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM messages WHERE id = ?",
        (id,)
    )

    message_data = cursor.fetchone()

    conn.close()

    if not message_data:
        return "Message not found!"

    email = message_data[2]
    subject = message_data[3]

    if request.method == "POST":

        reply_message = request.form.get("reply_message")

        # இப்போதைக்கு reply message-ஐ test மட்டும் செய்கிறோம்
        return f"""
        <div style="
            font-family: Arial;
            background: #0b0b0f;
            color: white;
            min-height: 100vh;
            padding: 50px;
            text-align: center;
        ">

            <h2 style="color:#ff4fd8;">
                Reply Ready 💌
            </h2>

            <p>
                Reply prepared for: <b>{email}</b>
            </p>

            <p>
                Your reply:
            </p>

            <div style="
                background:#17171d;
                padding:20px;
                border-radius:12px;
                max-width:600px;
                margin:20px auto;
            ">
                {reply_message}
            </div>

            <a
                href="/messages"
                style="
                    display:inline-block;
                    margin-top:20px;
                    padding:12px 20px;
                    background:#ff4fd8;
                    color:white;
                    text-decoration:none;
                    border-radius:8px;
                "
            >
                ← Back to Messages
            </a>

        </div>
        """

    return f"""
    <!DOCTYPE html>

    <html>

    <head>

        <title>Reply Message</title>

        <style>

            * {{
                box-sizing: border-box;
            }}

            body {{
                margin: 0;
                font-family: Arial, sans-serif;
                background: #0b0b0f;
                color: white;
                padding: 40px;
            }}

            .reply-box {{
                max-width: 700px;
                margin: auto;
                background: #17171d;
                padding: 30px;
                border-radius: 18px;
                border: 1px solid #292932;
            }}

            h1 {{
                color: #ff4fd8;
                text-align: center;
                margin-bottom: 30px;
            }}

            label {{
                display: block;
                margin-bottom: 8px;
                color: #aaa;
            }}

            input,
            textarea {{
                width: 100%;
                padding: 13px;
                margin-bottom: 20px;
                border: 1px solid #333;
                border-radius: 8px;
                background: #222229;
                color: white;
                outline: none;
            }}

            textarea {{
                height: 180px;
                resize: vertical;
            }}

            input:focus,
            textarea:focus {{
                border-color: #ff4fd8;
            }}

            .send-btn {{
                width: 100%;
                padding: 14px;
                border: none;
                border-radius: 8px;
                background: #ff4fd8;
                color: white;
                font-size: 16px;
                font-weight: bold;
                cursor: pointer;
            }}

            .back-btn {{
                display: block;
                text-align: center;
                margin-top: 15px;
                color: #aaa;
                text-decoration: none;
            }}

        </style>

    </head>

    <body>

        <div class="reply-box">

            <h1>
                📩 Reply Message
            </h1>

            <form method="POST">

                <label>
                    To
                </label>

                <input
                    type="email"
                    value="{email}"
                    readonly
                >

                <label>
                    Subject
                </label>

                <input
                    type="text"
                    value="Re: {subject}"
                    readonly
                >

                <label>
                    Your Reply
                </label>

                <textarea
                    name="reply_message"
                    placeholder="Type your reply here..."
                    required
                ></textarea>

                <button
                    class="send-btn"
                    type="submit"
                >
                    📤 Send Reply
                </button>

            </form>

            <a
                class="back-btn"
                href="/messages"
            >
                ← Back to Messages
            </a>

        </div>

    </body>

    </html>
    """


# ================= DELETE MESSAGE =================

@app.route("/delete/<int:id>")
def delete_message(id):

    if not session.get("admin"):
        return redirect("/login")

    conn = sqlite3.connect(DB_PATH)

    conn.execute(
        "DELETE FROM messages WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/messages")


# ================= LOGOUT =================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


# ================= RUN SERVER ================

init_db()

if __name__ == "__main__":

    app.run(debug=os.environ.get("FLASK_DEBUG", "false").lower() == "true")