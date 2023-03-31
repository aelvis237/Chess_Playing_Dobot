import csv

path = 'my_chess/ChessOpeningDatabase.csv'


def find_opening_move(current_fen):
    with open(path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            for field in row:
                if field == current_fen:
                    return row[1]
    return None

def insert_opening_moves(fen,move):
    with open(path, 'a', encoding='UTF8') as f:
        row = fen + ',' + move
        f.write(row)
        f.write("\n")

def insert_opening_name(name):
    with open(path, 'a', encoding='UTF8') as f:
        f.write(name)
        f.write("\n")
