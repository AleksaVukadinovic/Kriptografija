# TODO
import torch
import torch.nn as nn
import pandas as pd
import numpy as np

from concrete.ml.sklearn import NeuralNetRegressor

np.random.seed(42)
torch.manual_seed(42)

X_train_nn = X_train_scaled.astype(np.float32)
X_test_nn = X_test_scaled.astype(np.float32)

# NeuralNetRegressor očekuje y kao matricu oblika (broj_instanci, broj_izlaza)
y_train_nn = y_train.reshape(-1, 1).astype(np.float32)

fhe_nn_model = NeuralNetRegressor(
    # Broj slojeva neuronske mreže
    module__n_layers=2,

    # Aktivaciona funkcija između slojeva
    module__activation_function=nn.ReLU,

    # broj neurona u skriven sloju
    module__n_hidden_neurons_multiplier=10,

    # Broj bitova za kvantizaciju težina modela
    # Manji broj bitova znači brže FHE izvršavanje, ali potencijalno slabiju preciznost
    module__n_w_bits=3,

    # Broj bitova za kvantizaciju aktivacija
    # I ovde je kompromis između brzine FHE-a i tačnosti modela
    module__n_a_bits=3,

    # Broj bitova za akumulirane vrednosti tokom računanja
    # Ako je premalo, model može izgubiti preciznost; ako je previše, FHE je sporiji
    module__n_accum_bits=8, max_epochs=15, batch_size=64, lr=0.01, train_split=None,verbose=0)

# Treniranje FHE-kompatibilne neuronske mreže
fhe_nn_model.fit(X_train_nn, y_train_nn)

# Kompajliranje neuronske mreže u FHE kolo
fhe_nn_model.compile(X_train_nn[:200])

# Clear predikcija neuronske mreže
nn_clear_pred = fhe_nn_model.predict(X_test_nn[:20])

# FHE simulacija neuronske mreže
nn_sim_pred = fhe_nn_model.predict(X_test_nn[:20], fhe="simulate")

# Pravo FHE izvršavanje neuronske mreže
nn_execute_pred = fhe_nn_model.predict(X_test_nn[:20], fhe="execute")

pd.DataFrame({
    "actual_value": np.ravel(y_test[:10]),
    "clear_prediction": np.ravel(nn_clear_pred[:10]),
    "fhe_simulate_prediction": np.ravel(nn_sim_pred[:10]),
    "fhe_execute_prediction": np.ravel(nn_execute_pred[:10])
})
