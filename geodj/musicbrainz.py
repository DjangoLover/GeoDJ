import musicbrainzngs
from geodj.genre_parser import GenreParser

class MusicBrainz:
    def __init__(self):
        musicbrainzngs.set_useragent("GeoDJ", "0.0.1", "https://github.com/6/djangodash2013")

    def get_artist(self, musicbrainz_id, includes=[]):
        if musicbrainz_id is None or musicbrainz_id.strip() == "":
            return None
        try:
            result = musicbrainzngs.get_artist_by_id(musicbrainz_id, includes=includes)
        except musicbrainzngs.WebServiceError as exc:
            print "Something went wrong with the request: %s" % exc
            return None
        except musicbrainzngs.MusicBrainzError as exc:
            print "Something went wrong with MusicBrainz: %s" % exc
            return None
        else:
            return result

    def is_artist_from_country(self, musicbrainz_id, country_code):
        result = self.get_artist(musicbrainz_id)
        if result is None:
            return False

        if 'artist' in result and 'country' in result['artist']:
            return result['artist']['country'] == country_code
        return False

    def get_artist_genres(self, musicbrainz_id):
        genres = []
        result = self.get_artist(musicbrainz_id, includes=['tags'])
        if result is not None and 'tag-list' in result['artist']:
            for tag in result['artist']['tag-list']:
                genre = GenreParser.parse(tag['name'])
                if genre is not None:
                    genres.append(genre)
        return set(genres)
