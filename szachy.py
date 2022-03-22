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
    if request.method == 'POST':
        try:
            # data = request.form
            data = request.form.to_dict()
            pole = data['pole1']+data['pole2'] #request('TAK JAKBY WYSŁANE')
            data = {
                'figura': data['figura'],
                'pole' : pole
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

def wszystkie_figury():
    return chess.UNICODE_PIECE_SYMBOLS

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
        print(board)
        return board.pseudo_legal_moves

    def validate_move(self, na_pole):
        def __init__(self, na_pole):
            self.na_pole = na_pole

        ruch = chess.Move.from_uci(self.uci_valide_move())
        return ruch  # in self.list_available_moves()


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
        }


def slownik_to_json(slownik):
    return json.dumps(slownik.to_json())

krol = King("a3", "a4")
board = chess.Board()
print(krol.list_available_moves(), krol.uci_valide_move())
print(krol.uci_valide_move() in krol.list_available_moves())
print(krol.unicode_symbol())
print(chess.UNICODE_PIECE_SYMBOLS)
print( krol.to_json())
for el in krol.to_json().items():
    print( el )
print( krol.symbol_piece())
print( krol.unicode_symbol())
print(chess.UNICODE_PIECE_SYMBOLS)
print( chess.piece_name(6))
print( type(wszystkie_figury() ))






# print(to_json(krol))
#
#
# class Queen(Figure):
#     def __init__(self, square, na_pole, piece=5):
#         super().__init__(square, na_pole, piece)
#         self.square = square
#         self.piece = piece
#         self.na_pole = na_pole
#
#     def symbol_piece(self):
#         return chess.PieceType(5)  # symbol figury
#
#     def to_json(self):
#         return {
#             "availableMoves": self.list_available_moves(),
#             "error": None,
#             "figure": self.nazwa_figury(),
#             "currentField": self.square,
#         }
#
#
# class Rock(Figure):
#     def __init__(self, square, na_pole, piece=4):
#         super().__init__(square, na_pole, piece)
#         self.square = square
#         self.piece = piece
#         self.na_pole = na_pole
#
#     def symbol_piece(self):
#         return chess.PieceType(4)  # symbol figury
#
#     def to_json(self):
#         return {
#             "availableMoves": self.list_available_moves(),
#             "error": None,
#             "figure": self.nazwa_figury(),
#             "currentField": self.square,
#         }
#
#
# class Bishop(Figure):
#     def __init__(self, square, na_pole, piece=3):
#         super().__init__(square, na_pole, piece)
#         self.square = square
#         self.piece = piece
#         self.na_pole = na_pole
#
#     def symbol_piece(self):
#         return chess.PieceType(3)  # symbol figury
#
#     def to_json(self):
#         return {
#             "availableMoves": self.list_available_moves(),
#             "error": None,
#             "figure": self.nazwa_figury(),
#             "currentField": self.square,
#         }
#
#
# class Knight(Figure):
#     def __init__(self, square, na_pole, piece=2):
#         super().__init__(square, na_pole, piece)
#         self.square = square
#         self.piece = piece
#         self.na_pole = na_pole
#
#     def symbol_piece(self):
#         return chess.PieceType(2)  # symbol figury
#
#     def to_json(self):
#         return {
#             "availableMoves": self.list_available_moves(),
#             "error": None,
#             "figure": self.nazwa_figury(),
#             "currentField": self.square,
#         }
#
#
# class Pawn(Figure):
#     def __init__(self, square, na_pole, piece=1):
#         super().__init__(square, na_pole, piece)
#         self.square = square
#         self.piece = piece
#         self.na_pole = na_pole
#
#     def symbol_piece(self):
#         return chess.PieceType(1)  # symbol figury
#
#     def to_json(self):
#         return {
#             "availableMoves": self.list_available_moves(),
#             "error": None,
#             "figure": self.nazwa_figury(),
#             "currentField": self.square,
#         }


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
