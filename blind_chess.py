from speech_recognition import SpeechRecognition
from chess import Chess

if __name__ == '__main__':

    print("Creating the speech recognition...")
    walker = SpeechRecognition()
    print("Speech Recognition created...\n")

    print("Creating the board game...")
    game = Chess()
    print("Board Game created...\n")

    turn = 0
    while True:

        print("Play " + ("white" if turn == 0 else "black") + " pieces\n")

        valid_moves = game.get_all_valid_moves(turn)

        chosen_move = walker.listen(valid_moves)

        type_piece = chosen_move[0]
        id_piece = chosen_move[1]
        new_pos = 8 * chosen_move[2] + chosen_move[3]

        game.move_piece(type_piece, id_piece, new_pos)

        print("End..? y / n")
        if input() == "y":
            break

        turn = 1 - turn
