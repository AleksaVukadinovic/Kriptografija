import numpy as np
from concrete import fhe

def auction_winner(ana, bojan, marko):
    highest_bid = max(ana, bojan, marko)
    return 0 if ana == highest_bid else 1 if bojan == highest_bid else 2

if __name__ == "__main__":
    compiler = fhe.Compiler(auction_winner, {"ana": "encrypted", "bojan": "encrypted", "marko": "encrypted"})

    bid_values = range(0, 11)

    auction_inputset = [
        (ana, bojan, marko) for ana in bid_values for bojan in bid_values for marko in bid_values
    ]

    auction_circuit = compiler.compile(auction_inputset)

    auction_circuit.keygen()

    ana_bid = 7
    bojan_bid = 9
    marko_bid = 5

    encrypted_input = auction_circuit.encrypt(ana_bid, bojan_bid, marko_bid)
    encrypted_winner_code = auction_circuit.run(encrypted_input)

    winner_code = auction_circuit.decrypt(encrypted_winner_code)

    winner_names = {
        0: "Ana",
        1: "Bojan",
        2: "Marko"
    }

    print("Pobednik:", winner_names[int(winner_code)])
