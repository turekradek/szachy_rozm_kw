from flask import Flask, render_template, url_for, request, redirect, jsonify
from abc import ABC, abstractmethod
import chess
import json
# from io import StringIO


app = Flask(__name__)


@app.route("/")
def hello_world():
    figura = chess.square_name(63)
    return render_template("index.html", krol=krol.unicode_symbol(),
                           wszystkie=wszystkie_figury())  # , tekst=jsonify({'tasks': tasks}))

@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():  # reszta do naszego cwiczenia nie potrzebna
    # error = None
    lista = []
    pola = { litera:i+1 for  i,litera  in enumerate('abcdefgh') }
    if request.method == 'POST':
        try:
            # data = request.form
            data = request.form.to_dict()
            pole = data['pole1']+data['pole2'] #request('TAK JAKBY WYSŁANE')
            pole_spr = data['pole3']+data['pole4'] #request('TAK JAKBY WYSŁANE')
            figury_ = {
                'Pawn': Pawn(pole, pole_spr),
                'Knight': Knight(pole, pole_spr),
                'Kishop': Bishop(pole, pole_spr),
                'Rock': Rock(pole, pole_spr),
                'Queen': Queen(pole, pole_spr),
                'King': King(pole, pole_spr),

            }
            lista.append([ data['figura'],pole, chess.piece_name(6)])
            figury = [figury_.keys()]#[King(pole, pole_spr)]
            data = {
                'figura': data['figura'],
                'pole' : pole,
                'pole_spr' : pole_spr,
                'zz': to_json( figury_[data['figura']] ),
                # 'suma': figury_[data['figura']].to_json(),
            }
            figura = wszystkie_figury()[data['figura'][0]]

            return data
        except:
            return 'did not save to database'
    else:
        return 'coś nie halo wez jeszcze raz'

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]
#############
@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})
################
# /api/v1/{chess-figure}/{current-field}
# @app.route('/api/v1/{chess-figure}/{current-field}')
@app.route('/api/v1/krol')
def get_question():
    return krol.to_json()

def wszystkie_figury():
    return chess.UNICODE_PIECE_SYMBOLS

def obiekty_figur():
    numery = [i for i in range( 1,7)]
    nazwy = [ chess.piece_name(i) for i in range( 1,7)]
    klasy = [  King ]
    print( numery )
    print( nazwy )
    print( klasy )

def figura_znak(figura):

    return chess.piece_symbol(figura)

class Figure(ABC):
    def __init__(self, pole, piece, na_pole):
        self.pole = pole
        self.piece = piece
        self.na_pole = na_pole
        self.pola = chess.SQUARE_NAMES

    @abstractmethod
    def symbol_piece(self):
        pass

    @abstractmethod
    def to_json(self):
        pass

    def nazwa_figury(self):
        return chess.piece_name(piece_type=self.piece)

    def unicode_symbol(self):
        return chess.UNICODE_PIECE_SYMBOLS[chess.piece_symbol(self.piece)]

    def uci(self):
        figura = chess.piece_symbol(self.piece)
        return figura + "@" + self.pole

    def uci_valide_move(self):  # , na_pole):

        figura = chess.piece_symbol(self.piece)
        # return figura + "@" + self.na_pole
        move = chess.Move.from_uci(self.pole + self.na_pole)
        return move
        # return self.pole + self.na_pole  ### tutaj zobacz
        # return figura + self.na_pole  ### tutaj zobacz

    def list_available_moves(self):
        kwadraty = [
            "".join([litera, str(i)]) for litera in "abcdefgh" for i in range(1, 9)
        ]
        wszystkie_figury = chess.PIECE_SYMBOLS + [
            el.upper() for el in chess.PIECE_SYMBOLS if el != None
        ]
        board = chess.Board()
        board.clear()
        figura = chess.Move.from_uci(self.uci())
        jaka_figura = self.uci()[0]
        druga_figura = wszystkie_figury[
            abs(wszystkie_figury.index(jaka_figura) - (len(wszystkie_figury) - 1))
        ]

        gdzie_figura2 = kwadraty[
            abs(kwadraty.index(self.uci()[2:]) - (len(kwadraty) - 1))
        ]

        figura2 = chess.Move.from_uci(druga_figura + "@" + gdzie_figura2)

        board.push(figura)
        board.push(figura2)
        # print(board)
        return board.pseudo_legal_moves

    def validate_move(self, na_pole):
        def __init__(self, na_pole):
            self.na_pole = na_pole

        ruch = chess.Move.from_uci(self.uci_valide_move())
        return ruch  # in self.list_available_moves()

def to_json(okiekt):
    return {
        "availableMoves": list(okiekt.list_available_moves()),
        "error": None,
        "figure": okiekt.nazwa_figury(),
        "currentField": okiekt.square,
        f"czy ruch figury {okiekt.nazwa_figury()} z pola {okiekt.pole} na pole {okiekt.na_pole} dozwolony":
        okiekt.uci_valide_move() in okiekt.list_available_moves(),
    }

class King(Figure):
    def __init__(self, square, na_pole, piece=6):
        super().__init__(square, piece, na_pole)
        self.square = square
        self.piece = piece
        self.na_pole = na_pole

    def symbol_piece(self):
        return chess.PieceType(6)  # symbol figury

    def to_json(self):
        return {
            "availableMoves": list(self.list_available_moves()),
            "error": None,
            "figure": self.nazwa_figury(),
            "currentField": self.square,
            f"czy ruch figury {self.nazwa_figury()} z pola {self.pole} na pole {self.na_pole} dozwolony":
                krol.uci_valide_move() in krol.list_available_moves(),
        }

def slownik_to_json(slownik):
    return json.dumps(slownik.to_json())

krol = King("a3", "a4")
board = chess.Board()
# print(1,krol.list_available_moves(),'1-2 ', krol.uci_valide_move())
# print(2,krol.uci_valide_move() in krol.list_available_moves()) # czy ruch dozwolony z pole powyzej

# print(5, krol.to_json()) # obiekt do klasy slownik availableMoves figura gdzie stoi
# for el in krol.to_json().items():
#     print( el )
print(6, krol.symbol_piece()) # symbol numeryczny figury krol
print(7, krol.unicode_symbol()) # symbol unicode figury krol
print(8,chess.UNICODE_PIECE_SYMBOLS) # slownik symboli figur
print(9, chess.piece_name(6)) # nazwa figury o numerze 6 czyli krol
print(10, type(wszystkie_figury() ))
obiekty_figur()
print(11, krol.symbol_piece())
print(12, chess.piece_name(6))
lista = []
lista.append( chess.piece_name(6) )
lista[0] = King('a8','a9')
print( lista )
print( to_json(krol))





class Queen(Figure):
    def __init__(self, square, na_pole, piece=5):
        super().__init__(square, na_pole, piece)
        self.square = square
        self.piece = piece
        self.na_pole = na_pole

    def symbol_piece(self):
        return chess.PieceType(5)  # symbol figury

    def to_json(self):
        return {
            "availableMoves": list(self.list_available_moves()),
            "error": None,
            "figure": self.nazwa_figury(),
            "currentField": self.square,
            # f"czy ruch figury {self.nazwa_figury()} z pola {self.pole} na pole {self.na_pole} dozwolony":
            #     krol.uci_valide_move() in krol.list_available_moves(),
            "Queen": 'krolowa',
        }


class Rock(Figure):
    def __init__(self, square, na_pole, piece=4):
        super().__init__(square, na_pole, piece)
        self.square = square
        self.piece = piece
        self.na_pole = na_pole

    def symbol_piece(self):
        return chess.PieceType(4)  # symbol figury

    def to_json(self):
        return {
            "availableMoves": self.list_available_moves(),
            "error": None,
            "figure": self.nazwa_figury(),
            "currentField": self.square,
        }


class Bishop(Figure):
    def __init__(self, square, na_pole, piece=3):
        super().__init__(square, na_pole, piece)
        self.square = square
        self.piece = piece
        self.na_pole = na_pole

    def symbol_piece(self):
        return chess.PieceType(3)  # symbol figury

    def to_json(self):
        return {
            "availableMoves": self.list_available_moves(),
            "error": None,
            "figure": self.nazwa_figury(),
            "currentField": self.square,
        }


class Knight(Figure):
    def __init__(self, square, na_pole, piece=2):
        super().__init__(square, na_pole, piece)
        self.square = square
        self.piece = piece
        self.na_pole = na_pole

    def symbol_piece(self):
        return chess.PieceType(2)  # symbol figury

    def to_json(self):
        return {
            "availableMoves": self.list_available_moves(),
            "error": None,
            "figure": self.nazwa_figury(),
            "currentField": self.square,
        }


class Pawn(Figure):
    def __init__(self, square, na_pole, piece=1):
        super().__init__(square, na_pole, piece)
        self.square = square
        self.piece = piece
        self.na_pole = na_pole

    def symbol_piece(self):
        return chess.PieceType(1)  # symbol figury

    def to_json(self):
        return {
            "availableMoves": list(self.list_available_moves()),
            "error": None,
            "figure": self.nazwa_figury(),
            "currentField": self.square,
            # f"czy ruch figury {self.nazwa_figury()} z pola {self.pole} na pole {self.na_pole} dozwolony":
            #     krol.uci_valide_move() in krol.list_available_moves(),
        }


# print(krolowa.list_available_moves())
# print(krolowa.validate_move("a3"))
"""
print(board)
print(board.legal_moves)
print(board)
# board.clear()
print(board, "\n")
# krol.set_piece_at()
print(board.legal_moves)
a = chess.Move.from_uci("g1h3")
b = chess.Move.from_uci("P@a3")
kr2 = chess.Move.from_uci("k@b2")
board.push(kr2)
kr = chess.Move.from_uci("K@d4")
board.push(kr)

print(board)
print(board.legal_moves.count(), board.legal_moves)
print(board.pseudo_legal_moves.count(), board.pseudo_legal_moves)
"""


"""
# krolowa = Queen(1)
# print(
#     krol.pokaz_pole(),
#     krol.nazwa_figury(),
#     krol.pozycja_figury(),
#     krol._set_piece_at(),
#     krol.set_piece_at(),
#     krol.list_available_moves(),
# )
# print(krolowa.pokaz_pole(), krolowa.nazwa_figury(), krol._set_piece_at())
# print(krol.symbol_piece(), " symbol_piece")
# print(krol.pokaz_pole(), " pokaz_pole")
# # print(krol.nazwa_pola())
# print(krol.list_available_moves("a2"), " available_moves")
# print(krol.piece_at(1))


# print(krol.nazwa_pola())
# print(chess.piece_name(6))
# print(krol.nazwa_pola())
# board = chess.Board()
# board
# print(chess.piece_symbol(6))
# print(chess.KING)
# print(chess.parse_square("a2"))
# # Gets the square index for the given square name (e.g., a1 returns 0).
# # squares = chess.SquareSet([chess.A8, chess.A1])
# # print(squares)
# # board.legal_moves.count()
# print(Figure.list_available_moves("a1"))
# krol = King(0)
# print(krol.pokaz_pole())
# print(krol.nazwa_pola())
# print(chess.SQUARE_NAMES)
"""
