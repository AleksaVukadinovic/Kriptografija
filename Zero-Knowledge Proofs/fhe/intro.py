from time import time

from concrete import fhe
from concrete.fhe.compilation.utils import inputset

# funkcija koju server izvrsava nad siforvanim podacima
def private_score(x, y):
    return 5*x + 4*y + 2

if __name__ == "__main__":
    start_time = time()
    # server kompajlira funkciju u FHE kolo, inputset je skup ulaznih vrednosti koji treba kompajleru
    compiler = fhe.Compiler(private_score, {"x": "encrypted", "y": "encrypted"})
    inputset = [(x,y) for x in range(8) for y in range(8)]

    circuit = compiler.compile(inputset)

    # korisnik generise kljuceve
    circuit.keygen()
    x_private = 4
    y_private = 6

    # korisnik sifruje podatke
    encrypted_input = circuit.encrypt(x_private, y_private)

    # server izvrsava funkciju nad sifrovanim podacima
    encrypted_result = circuit.run(encrypted_input)

    # korisnik desifruje sta je dobio od servera
    result = circuit.decrypt(encrypted_result)

    end_time = time()
    print(end_time - start_time)
    print("Actual result:", 3 * x_private + 2 * y_private + 1)
