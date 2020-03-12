import re
import random
import geocoder
from requests import get
import os


API_KEY_GOOGLE_MAPS = os.environ.get('API_KEY_GOOGLE_MAPS')

FRENCH_STOP_WORDS = ["a","abord","absolument","adresse","afin","ah","ai",
"aie","ailleurs","ainsi","ait","allaient","aller","allez","allo","allons",
"allô","alors","anterieur","anterieure","anterieures","apres","après",
"as","assez","attendu","au","aucun","aucune","aujourd","aujourd'hui",
"aupres","auquel","aura","auraient","aurait","auront","aussi","autre",
"autrefois","autrement","autres","autrui","aux","auxquelles","auxquels",
"avaient","avais","avait","avant","avec","avoir","avons","ayant","b","bah",
"bas","basee","bat","beau","beaucoup","bien","bigre","bot", "boum","bravo",
"brrr","c","car","ce","ceci","cela","celle","celle-ci","celle-là","celles",
"celles-ci","celles-là","celui","celui-ci","celui-là","cent","cependant",
"certain","certaine","certaines","certains","certes","ces","cet","cette",
"ceux","ceux-ci","ceux-là","chacun","chacune","chaque","cher","chers","chez",
"chiche","chut","chemin","chère","chères","ci","cinq","cinquantaine",
"cinquante","cinquantième","cinquième","clac","clic","combien","comme",
"comment","comparable","comparables","compris","concernant","connais",
"connait","connaitre","contre","couic","crac","d","da","dans","de","debout",
"dedans","dehors","deja","delà","depuis","dernier","derniere","derriere",
"derrière","des","desormais","desquelles","desquels","dessous","dessus","deux",
"deuxième","deuxièmement","devant","devers","devra","different","differentes",
"differents","différent","différente","différentes","différents","dire",
"directe","directement","dit","dite","dits","divers","diverse","diverses",
"dix","dix-huit","dix-neuf","dix-sept","dixième","doit","doivent","donc",
"donner","dont","douze","douzième","dring","du","duquel","durant","dès",
"désormais","e","effet","egale","egalement","egales","eh","elle","elle-même",
"elles","elles-mêmes","en","encore","enfin","entre","envers","environ","es",
"est","et","etant","etc","etre","eu","euh","eux","eux-mêmes","exactement",
"excepté","extenso","exterieur","f","fais","faisaient", "faisant","fait",
"façon","feront","fi","flac","floc","font","g","gens","grand papy","grandpapy",
"grandpy","h","ha","hein","hem","hep","hi","ho","holà","hop","hormis","hors",
"hou","houp","hue","hui","huit","huitième","hum","hurrah","hé","hélas","i",
"il","ils","importe","indiquer","j","je","jusqu","jusque","juste","k","l",
"la","laisser","laquelle","las","le","lequel","les","lesquelles","lesquels",
"leur","leurs","longtemps","lors","lorsque","lui","lui-meme","lui-même","là",
"lès","m","ma","maint","maintenant","mais","malgre","malgré","maximale","me",
"meme","memes","merci","mes","mien","mienne","miennes","miens","mille","mince",
"minimale","moi","moi-meme","moi-même","moindres","moins","mon","moyennant",
"multiple","multiples","même","mêmes","n","na","naturel","naturelle",
"naturelles","ne","neanmoins","necessaire","necessairement","neuf","neuvième",
"ni","nombreuses","nombreux","non","nos","notamment","notre","nous",
"nous-mêmes","nouveau","nul","néanmoins","nôtre","nôtres","o","oh","ohé",
"ollé","olé","on","ont","onze","onzième","ore","ou","ouf","ouias","oust",
"ouste","outre","ouvert","ouverte","ouverts","o|","où","p","paf","pan","papy",
"par","parce","parfois","parle","parlent","parler","parmi","parseme","partant",
"particulier","particulière","particulièrement","pas","passé","pendant",
"pense","permet","personne","peu","peut","peuvent","peux","pff","pfft",
"pfut","pif","pire","plein","plouf","plus","plusieurs","plutôt","possessif",
"possessifs","possible","possibles","pouah","pour","pourquoi","pourrais",
"pourrait","pouvait","prealable","precisement","premier","première",
"premièrement","pres","probable","probante","procedant","proche","près",
"psitt","pu","puis","puisque","pur","pure","q","qu","quand","quant",
"quant-à-soi","quanta","quarante","quatorze","quatre","quatre-vingt",
"quatrième","quatrièmement","que","quel","quelconque","quelle",
"quelles","quelqu'un","quelque","quelques","quels","qui","quiconque","quinze",
"quoi","quoique","r","rare","rarement","rares","relative","relativement",
"remarquable","rend","rendre","restant","reste","restent","restrictif",
"retour","revoici","revoilà","rien","s","sa","sacrebleu","sait","salut", 
"sans", "sapristi","sauf","se","sein","seize","selon","semblable","semblaient",
"semble","semblent","sent","sept","septième","sera","seraient","serait",
"seront","ses","seul","seule","seulement","si","sien","sienne","siennes",
"siens","sinon","six","sixième","soi","soi-même","soit","soixante","son",
"sont","sous","souvent","specifique","specifiques","speculatif","stop",
"strictement","subtiles","suffisant","suffisante","suffit","suis","suit",
"suivant","suivante","suivantes","suivants","suivre","superpose","sur",
"surtout","t","ta","tac","tant","tardive","te","tel","telle","tellement",
"telles","tels","tenant","tend","tenir","tente","tes","tic","tien","tienne",
"tiennes","tiens","toc","toi","toi-même","ton","touchant","toujours","tous",
"tout","toute","toutefois","toutes","treize","trente","tres","trois",
"troisième","troisièmement","trop","trouve","trouves","très","tsoin","tsouin",
"tu","té","u","un","une","unes","uniformement","unique","uniques","uns","v",
"va","vais","vas","vers","via","vif","vifs","vingt","vivat","vive","vives",
"vlan","voici","voilà","vont","vos","votre","vous","vous-mêmes","vu","vé",
"vôtre","vôtres","w","x","y","z","zut","à","â","ça","ès","étaient","étais",
"était","étant","été","être","ô"]

RESPONSES = [
            "Quand j'ai connu cet endroit tu n'étais pas encore "
            "né mon cher. Tiens voici l'adresse : ",
            "Tu pourrais demander plus gentillement... La voici : ",
            "Tu es bien tombé ! Je connais cet endroit comme ma poche : ",
            "Bon choix ! Voici l'adresse : "
]

STORIES_INTRODUCTION = [
                        "Tu veux rire ? C'est là bas que j'ai rencontré ma "
                        "femme ! Je vais te raconter un peu l'histoire de ce "
                        "lieu. ",
                        "Tu sais j'adore cet endroit ! Mais pas beaucoup de "
                        "gens le connaisse vraiment. Tu savais que : ",
                        "Mais t'ai-je déjà raconté la petite histoire de ce "
                        "quartier qui m'a presque vu naître ? ",
                        "Je suis sûr que tu ne connais rien de ce lieu ! "
                        "Laisse-moi t'en dire un peu plus. "
]

END_STORIES_QUOTE = [
                    "J'espère que tu as apprécié ma petite histoire. "
                    "N'hésite pas à me poser une autre question !",
                    "Mais qu'est-ce-que tu attends? Pose moi une autre "
                    "question ! J'ai pleins d'histoires à raconter.",
                    "Alors tu l'as trouvé comment mon histoire? Allez, je "
                    "sais que tu en veux une autre ! Il suffit de demander..."
]


class GrandPyBotConversation:
    """Retrieve sentences for Papy Bot answers."""

    responses = RESPONSES
    stories_intro = .STORIES_INTRODUCTION
    end_quotes = .END_STORIES_QUOTE

    @staticmethod
    def random_response():
        """Choose randomly a quote that will introduce papy bot response."""
        random_quote_response = random.choice(GrandPyBotConversation.responses)
        return random_quote_response

    @staticmethod
    def random_story():
        """
        Choose randomly a story that will introduce papy bot story
        about a place.
        """
        random_story_intro = random.choice(
                                        GrandPyBotConversation.stories_intro
        )
        return random_story_intro

    @staticmethod
    def random_end_quote():
        """Choose randomly a quote that will end the current discussion."""
        random_end_story_quote = random.choice(
                                        GrandPyBotConversation.end_quotes
        )
        return random_end_story_quote


class Parser:
    """Clear user input to keep only the key words (address)."""

    @staticmethod
    def arrange_input(sentence):
        """Method that clear input."""
        stop_words = .FRENCH_STOP_WORDS

        # Lowercase each words
        lowercase_sentence = sentence.lower()
        # Remove, replace special characters and split the sentence
        remove = re.sub(r"[-&_,;!?./\']", " ", lowercase_sentence).split()
        # Filter the sentence by removing the words found in stop_words list
        filter_sentence = [word for word in remove if word not in stop_words]
        # Join the remaining words together
        sentence = " ".join(filter_sentence)
        return sentence


class GoogleMapsApi():
    """Retrieve data from Google Maps API."""

    def __init__(self, request):
        self.request = request
        self.latitude = 0
        self.longitude = 0
        self.address = ''

    def get_address_geolocation(self):
        """Method allowing the program to search for a specific place."""
        # Parameters request(user_input), Api key and method places needed
        # to find a specific place.
        request_data = geocoder.google(
                                        self.request,
                                        key=.API_KEY_GOOGLE_MAPS,
                                        method="places"
        )
        # Retrieving data as .json
        address_details = request_data.json
        # Raise an error if the location requested hasn't been found
        try:
            self.longitude, self.latitude, self.address = (
                                                    address_details['lng'],
                                                    address_details['lat'],
                                                    address_details['address']
            )
        except (TypeError, KeyError):
            raise UnknownLocation

        return self.latitude, self.longitude, self.address


class UnknownLocation(Exception):
    """Error if location not found."""


class MediaWikiApi():
    """Retrieve data from Media Wiki API."""

    def __init__(self, maps):
        # Call method to retrieve the place's coordinates
        self.coordinates = maps.get_address_geolocation()

    def request_wiki_page(self):
        """Method searching for a page id and a title of a wiki article."""
        # Searching parameters for wiki_api
        search_params = {
                        'action': 'query',
                        'list': 'geosearch',
                        'gscoord': '{0}|{1}'.format(self.coordinates[0],
                                                    self.coordinates[1]),
                        'gslimit': 1,
                        'gsradius': 10000,
                        'format': 'json'
        }
        request_wiki_data = get(
                                'https://fr.wikipedia.org/w/api.php',
                                params=search_params
        )
        # Transform request data into json
        page_data = request_wiki_data.json()
        # Scan dictionary and only retrieve the two needed data
        page_id = page_data["query"]["geosearch"][0]["pageid"]
        title = page_data["query"]["geosearch"][0]["title"]
        return page_id, title

    @staticmethod
    def request_wiki_summary(page_id=None):
        """Method searching for a summary of the requested place."""
        if not page_id:
            return "Je n'ai aucune histoire pour toi !"
        # Searching parameters for wiki_summary
        search_params = {
                        'action': 'query',
                        'prop': 'extracts',
                        'pageids': page_id,
                        'exlimit': 1,
                        'explaintext': True,
                        'exsentences': 2,
                        'format': 'json'
        }
        request_story_wiki = get(
                                'https://fr.wikipedia.org/w/api.php',
                                params=search_params
        )
        # Transform request data into json
        story_data = request_story_wiki.json()
        # Scan dictionary and only retrieve the needed data
        story_for_location = (
                            story_data["query"]["pages"]
                            [str(page_id)]['extract']
        )
        return story_for_location

maps = GoogleMapsApi('tour eiffel')
story = MediaWikiApi(maps)
page = story.request_wiki_page()
story.request_wiki_summary(page[0])
