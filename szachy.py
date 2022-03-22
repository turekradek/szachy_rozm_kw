from flask import Flask, render_template, url_for, request, redirect, jsonify
from abc import ABC, abstractmethod
import chess
import json

app = Flask(__name__)

@app.route("/")
def hello_world():
    figury = chess.UNICODE_PIECE_SYMBOLS
    a = {'a':'A',
         'b':'B'}
    return render_template("index.html", wszystkie=figury)#wszystkie_figury() ) # , tekst=jsonify({'tasks': tasks})) krol=krol.unicode_symbol(),


@app.route("/liczby/<int:figura>/<int:pole>")
def answer(figura, pole):
    pola = wszystkie_pola()
    square = pola[pole]
    return f'{chess.piece_name(figura) }  {chess.square_name(pole)}'



@app.route("/<figura>/<pole>")
def answer_text(figura,pole):
    pola = wszystkie_pola()
    pola_ = {item: item for key, item in pola.items()}
    square = pola_[pole]
    slownik_figur_ = { 'None':None , 'pawn':Pawn(square, pole), 'knight':Knight(square, pole), 'bishop':Bishop(square, pole),
                      'rock':Rock(square, pole),'queen': Queen(square, pole), 'king':King(square, pole) }
    return f" {to_json_(slownik_figur_[figura])} " # OK

@app.route("/czy_ruch_dozwolony/<figura>/<pole>/<na_pole>")
def czy_ruch_z_pola_mozliwy(figura,pole, na_pole):
    na_pole = na_pole.lower()
    pola = wszystkie_pola()
    pola_ = {item: item for key, item in pola.items()}
    square = pola_[pole]
    slownik_figur_ = { 'None':None , 'pawn':Pawn(pole, na_pole), 'knight':Knight(pole, na_pole), 'bishop':Bishop(pole, na_pole),
                      'rock':Rock(pole, na_pole),'queen': Queen(pole, na_pole), 'king':King(pole, na_pole) }
    prawda = {'True':'Ruch prawidłowy',
              'False':'Ruch nieprawidłowy'}
    return f"""Czy ruch figury {figura} z pola {pole} na pole {na_pole} jest mozliwy ? 
           {prawda[str(slownik_figur_[figura].uci_valide_move() in slownik_figur_[figura].list_available_moves())]}"""


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():  # reszta do naszego cwiczenia nie potrzebna
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            pole = data['pole1']+data['pole2'] #request('TAK JAKBY WYSŁANE')
            data = {
                'figura': data['figura'],
                'pole' : pole
            }

            return f"""Jeśli chcesz sprawdzić czy wszysto ok wpisz w terminalu dalsza część:<br> 
            curl -i http://127.0.0.1:5000/{data['figura']}/{data['pole']} <br>
otrzymasz wynik zapytania w którym są możliwe ruchy dla wybranej figury z wybranego pola.<br>
jeśli chchesz sprawdzić  czy ruch na konkretne pole jest możliwy ,<br>
 skopiuj  curl -i http://127.0.0.1:5000/czy_ruch_dozwolony/{data['figura']}/{data['pole']}/   <br> a na końcu dopisz wybrane pole z szachownicy,
 pole powinno być w formacie a1, h8 itp"""
        except:
            return 'did not save to database'
    else:
        return 'coś nie halo wez jeszcze raz'

def wszystkie_figury():
    symbole =  chess.PIECE_SYMBOLS
    lista = chess.PIECE_NAMES
    slownik = { symbole[i]: figura for i , figura in enumerate(lista) }
    return slownik


def wszystkie_pola():
    squares = chess.SQUARE_NAMES
    squares = { i:square for  i, square in enumerate(squares) }
    return  squares


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
        move = chess.Move.from_uci(self.pole + self.na_pole)
        return move


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
            "availableMoves": self.list_available_moves() ,
            "error": None,
            "figure": self.nazwa_figury(),
            "currentField": self.square,
        }

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
            "availableMoves": self.list_available_moves(),
            "error": None,
            "figure": self.nazwa_figury(),
            "currentField": self.square,
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
            "availableMoves": self.list_available_moves(),
            "error": None,
            "figure": self.nazwa_figury(),
            "currentField": self.square,
        }

def slownik_to_json(slownik):
    return json.dumps(slownik.to_json())
def to_json_( obiekt ):
    return obiekt.to_json()

krol = King('b2','d2')
print(2,krol.uci_valide_move() in krol.list_available_moves())


