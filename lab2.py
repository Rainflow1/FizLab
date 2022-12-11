import numpy as np
from matplotlib import pyplot

#pyplot.rcParams['text.usetex'] = True

# Dane
Dane = {
    "Sprężyny": [
        {
            "długość": 6.8,     # w cm
            "masa": 20,         # w g
            "r": 0.0375,        # w cm
            "R": 0.905,         # w cm
            "N": 84,
            "liczbaCiężarków": 4,
            "statyczna": [12, 17, 22.3, 27.5],  # Długość spręrzyny w cm przy odpowiednio 50, 100, 150, 200g
            "dynamiczna": [                     # Pomiary okresu sprężyny w 5 próbach dla 4 różnych obciążeń
                [0.46, 0.50, 0.46, 0.48, 0.50], # 50g
                [0.56, 0.65, 0.64, 0.66, 0.65], # 100g
                [0.75, 0.7, 0.76, 0.74, 0.74],  # 150g
                [0.95, 0.86, 0.88, 0.88, 0.84]  # 200g
            ], 
            "równolegle": False,
            "szeregowo": False
        },
        {
            "długość": 7.3,     # w cm
            "masa": 28,         # w g
            "r": 0.055,         # w cm
            "R": 0.9825,        # w cm
            "N": 69,
            "liczbaCiężarków": 4,
            "statyczna": [9.3, 11.4, 13.5, 15.6],  # Długość spręrzyny w cm przy odpowiednio 50, 100, 150, 200g
            "dynamiczna": [                     # Pomiary okresu sprężyny w 5 próbach dla 4 różnych obciążeń
                [0.31, 0.29, 0.3, 0.36, 0.34], # 50g
                [0.38, 0.45, 0.41, 0.42, 0.42], # 100g
                [0.51, 0.49, 0.49, 0.52, 0.5],  # 150g
                [0.53, 0.58, 0.6, 0.57, 0.52]  # 200g
            ], 
            "równolegle": False,
            "szeregowo": False
        },
        {
            "długość": 10,     # w cm
            "masa": None,         
            "r": None,       
            "R": None,         
            "N": None,
            "liczbaCiężarków": 4,
            "statyczna": [11.5, 13.5, 15, 16.5],  # Długość spręrzyny w cm przy odpowiednio 50, 100, 150, 200g
            "dynamiczna": [                     # Pomiary okresu sprężyny w 5 próbach dla 4 różnych obciążeń
                [0.34, 0.3, 0.31, 0.32, 0.3], # 50g
                [0.41, 0.38, 0.39, 0.4, 0.42], # 100g
                [0.49, 0.46, 0.46, 0.44, 0.47],  # 150g
                [0.6, 0.53, 0.55, 0.5, 0.54]  # 200g
            ], 
            "równolegle": True,
            "szeregowo": False
        },
        {
            "długość": 22,     # w cm
            "masa": None,         
            "r": None,       
            "R": None,         
            "N": None,
            "liczbaCiężarków": 3,
            "statyczna": [29.3, 36.6, 44.1],  # Długość spręrzyny w cm przy odpowiednio 50, 100, 150, 200g
            "dynamiczna": [                     # Pomiary okresu sprężyny w 5 próbach dla 4 różnych obciążeń
                [0.66, 0.56, 0.59, 0.62, 0.58], # 50g
                [0.81, 0.76, 0.77, 0.84, 0.84], # 100g
                [1.04, 1.02, 1, 1.02, 0.97],  # 150g
            ], 
            "równolegle": False,
            "szeregowo": True
        }
    ],

    "Ciężarki": 50 # masa w g
}

def kwadraty(x: list, y: list, n: int):

    suma_x = sum(x)
    suma_x2 = sum([pow(i, 2) for i in x])
    suma_y = sum(y)
    suma_xy = sum([i*j for i, j in zip(x, y)])
    srednia_x = suma_x/n
    srednia_y = suma_y/n

    a = (suma_xy - (n * srednia_x * srednia_y))/(suma_x2 - (n * pow(srednia_x, 2)))
    b = srednia_y - a * srednia_x

    return (a, b)

def rysujWykresyStatyczne(dane: dict):

    for n, s in enumerate(dane["Sprężyny"]):
        print("Zestaw sprężyn nr " + str(n+1) + ":")

        ciężarki = [dane["Ciężarki"] * i for i in range(1, s["liczbaCiężarków"]+1)]
        x = [i - s["długość"] for i in s["statyczna"]]

        k = kwadraty(x, ciężarki, s["liczbaCiężarków"])

        f = lambda x: k[0] * x + k[1]

        print("a = " + str(k[0]) + " b = " + str(k[1]))

        fig, ax = pyplot.subplots()

        if(s["równolegle"]):
            ax.set_title("Wykres masy ciężarków od wychylenia \ndla układu sprężyn 1 i 2 połączonych równolegle")
        elif(s["szeregowo"]):
            ax.set_title("Wykres masy ciężarków od wychylenia \ndla układu sprężyn 1 i 2 połączonych szeregowo")
        else:
            ax.set_title("Wykres masy ciężarków od wychylenia dla sprężyny nr. " + str(n+1))

        ax.set_ylabel("m [g]")
        ax.set_xlabel("x [cm]")
        ax.scatter(x, ciężarki, color="blue")
        ax.plot(x, [f(i) for i in x], color="black")
        fig.savefig("WykresStatyczny" + str(n+1), dpi=300)

def rysujWykresyDynamiczne(dane: dict):

    for n, s in enumerate(dane["Sprężyny"]):
        print("Zestaw sprężyn nr " + str(n+1) + ":")

        ciężarki = [l for l in [dane["Ciężarki"] * i for i in range(1, s["liczbaCiężarków"]+1)] for j in range(5)]
        okresy = [pow(i, 2) for i in np.concatenate(s["dynamiczna"]).flat]

        k = kwadraty(okresy, ciężarki, s["liczbaCiężarków"] * 5)

        f = lambda x: k[0] * x + k[1]

        print("a = " + str(k[0]) + " b = " + str(k[1]))

        fig, ax = pyplot.subplots()

        if(s["równolegle"]):
            ax.set_title("Wykres masy ciężarków od kwadratu okresu \ndla układu sprężyn 1 i 2 połączonych równolegle")
        elif(s["szeregowo"]):
            ax.set_title("Wykres masy ciężarków od kwadratu okresu \ndla układu sprężyn 1 i 2 połączonych szeregowo")
        else:
            ax.set_title("Wykres masy ciężarków od kwadratu okresu dla sprężyny nr. " + str(n+1))

        ax.set_ylabel("m [g]")
        ax.set_xlabel("T [s^2]")
        ax.scatter(okresy, ciężarki, color="blue")
        ax.plot(okresy, [f(i) for i in okresy], color="black")
        fig.savefig("WykresDynamiczny" + str(n+1), dpi=300)


rysujWykresyStatyczne(Dane)
rysujWykresyDynamiczne(Dane)