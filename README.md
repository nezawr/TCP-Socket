# TCP-Socket

TCP socket programming code, implements Nim game: https://en.wikipedia.org/wiki/Nim#:~:text=Nim%20is%20a%20mathematical%20game,the%20same%20heap%20or%20pile.

PROTOCOL DESCRIPTION
The client sends 3 integers:
    First: indicates which type of procedure should the server follow. Zero is for normal game progression, five for when the player                chooses to quit and six is when the input is invalid.
    Second: indicates which heap was chosen, for quit and invalid choices default 0 is sent instead.
    Third: indicates how many elements the player chose to take from the heap, for quit and invalid inputs default 0 is used.
The server sends 4 integers:
    First: Message type, 0: starting msg, 1: Legal Move, 2: Illegal Move, 3: Win, 4: Lose, 5: Quit,
           6: Invalid Input
    Second, Third and fourth integers indicate accordingly the number of elements in the heaps A, B, C.
In addition to the server.py, client.py scripts there are additional 3 files:
    sendall.py: Implementation of the sendall function.
    clientfunction.py: Implementations of functions used in client.py.
    serverfunction.py: Implementation of functions used in server.py.
