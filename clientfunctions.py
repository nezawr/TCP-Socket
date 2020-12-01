from sendall import my_sendall
import socket
import struct

def game_seq_progress(connection, message_type, heap_A, heap_B, heap_C): # Returns True if game continues and False if game is over.
    indicator = True
    if (message_type == 0): # INITIAL SERVER MESSAGE
        game_choice_progress(connection, heap_A, heap_B, heap_C)
    elif (message_type == 1): # LEGAL MOVE
        print("Move accepted")
        game_choice_progress(connection, heap_A, heap_B, heap_C)
    elif (message_type == 2): # ILLEGAL MOVE
        print("Illegal move")
        game_choice_progress(connection, heap_A, heap_B, heap_C)
    elif (message_type == 3): # WIN
        print("You win!")
        indicator = False
    elif (message_type == 4): # LOSE
        print("Server win!")
        indicator = False
    elif (message_type == 5): # QUIT
        indicator = False
    else: # INVALID
        print("Invalid Input")
        game_choice_progress(connection, heap_A, heap_B, heap_C)
    return indicator

#Symbols used:
#5: PLAYER QUITS, 6:INVALID INPUT, 0:REGULAR GAME PROGRESSION
def game_choice_progress(connection, heap_A, heap_B, heap_C):
    print(f"Heap A: {heap_A}", f"Heap_B: {heap_B}", f"Heap C: {heap_C}", sep="\n")
    player_choice = input("Your turn: \n")
    if (player_choice == 'Q'):
        data_to_send = struct.pack("i i i",5, 0, 0)
        my_sendall(connection, data_to_send)
    else:
        if is_valid_input(player_choice):
            heap_letter, num = player_choice.split()
            num = int(num)
            heap_num = pick_heap_num(heap_letter)
            data_to_send = struct.pack("i i i", 0, heap_num, num)
            my_sendall(connection, data_to_send)
        else:
            data_to_send = struct.pack("i i i", 6, 0 , 0)
            my_sendall(connection, data_to_send)


def is_valid_input(input_string):
    input_segments = input_string.split()
    if (len(input_segments) != 2):
        return False
    else:
        heap_letter, num = input_segments
        if heap_letter not in ['A', 'B', 'C']:
            return False
        try:
            if float(num) < 0 or int(float(num)) != float(num):
                return False
        except ValueError:
            return False
        return True
        

def pick_heap_num(heap_letter):
    if heap_letter == "A":
        return 0
    elif heap_letter == "B":
        return 1
    elif heap_letter == "C":
        return 2
    else:
        return 3