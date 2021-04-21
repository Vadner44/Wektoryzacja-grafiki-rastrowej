import numpy as np
from PIL import Image
import cv2
from matplotlib import pyplot as plt
import os


def algorytm_canny(img, zmienna1, zmienna2):
    # zamiana oryginalnego obrazka w skalę szarości
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Redukcja szumu
    img = cv2.GaussianBlur(img, (5, 5), zmienna1)

    # Wyznaczenie pochodnej kierunkowej
    gx = cv2.Sobel(np.float32(img), cv2.CV_64F, 1, 0, 3)
    gy = cv2.Sobel(np.float32(img), cv2.CV_64F, 0, 1, 3)

    # Zamiana współrzędnych kartezjańskich na biegunowe
    grad, kat = cv2.cartToPolar(gx, gy, angleInDegrees=True)

    # Ustalanie minimalnych i maksymalnych progów
    grad_max = np.max(grad)
    dolny = None
    gorny = None
    if not dolny:
        dolny = grad_max * zmienna2
    if not gorny:
        gorny = grad_max * 1

    # Pobranie wymiarów obrazu wejściowego
    height, width = img.shape

    # Tłumienie niemaksymalnych pikseli
    sasiad_1_x = None
    sasiad_1_y = None
    sasiad_2_x = None
    sasiad_2_y = None

    for i_x in range(width):
        for i_y in range(height):

            grad_kat = kat[i_y, i_x]
            grad_kat = abs(grad_kat - 180) if abs(grad_kat) > 180 else abs(grad_kat)

            # Wybranie sąsiednich pikseli względem docelowego
            # zgodnie z kierunkiem gradientu w kierunku osi x
            if grad_kat <= 22.5:
                sasiad_1_x, sasiad_1_y = i_x - 1, i_y
                sasiad_2_x, sasiad_2_y = i_x + 1, i_y

            # kierunek prawy górny
            elif 22.5 < grad_kat <= (22.5 + 45):
                sasiad_1_x, sasiad_1_y = i_x - 1, i_y - 1
                sasiad_2_x, sasiad_2_y = i_x + 1, i_y + 1

            # W kierunku osi y
            elif (22.5 + 45) < grad_kat <= (22.5 + 90):
                sasiad_1_x, sasiad_1_y = i_x, i_y - 1
                sasiad_2_x, sasiad_2_y = i_x, i_y + 1

            # kierunek lewy górny
            elif (22.5 + 90) < grad_kat <= (22.5 + 135):
                sasiad_1_x, sasiad_1_y = i_x - 1, i_y + 1
                sasiad_2_x, sasiad_2_y = i_x + 1, i_y - 1

            # Ponowne uruchomienie cyklu
            elif (22.5 + 135) < grad_kat <= (22.5 + 180):
                sasiad_1_x, sasiad_1_y = i_x - 1, i_y
                sasiad_2_x, sasiad_2_y = i_x + 1, i_y

            # Krok tłumienia
            if width > sasiad_1_x >= 0 and height > sasiad_1_y >= 0:
                if grad[i_y, i_x] < grad[sasiad_1_y, sasiad_1_x]:
                    grad[i_y, i_x] = 0
                    continue

            if width > sasiad_2_x >= 0 and height > sasiad_2_y >= 0:
                if grad[i_y, i_x] < grad[sasiad_2_y, sasiad_2_x]:
                    grad[i_y, i_x] = 0

    ids = np.zeros_like(img)

    # Podwójny stopień progowania
    for i_x in range(width):
        for i_y in range(height):

            badany = grad[i_y, i_x]

            if badany < dolny:
                grad[i_y, i_x] = 0
            elif gorny > badany >= dolny:
                ids[i_y, i_x] = 1
            else:
                ids[i_y, i_x] = 2

    # Zwracanie gradientów krawędzi
    return grad


def wektoryzacja(img, folder, nazwa):
    plt.clf()
    img2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    (w, h) = img2.shape
    kontury, _ = cv2.findContours(img2, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    plt.figure(figsize=(h/77.5, w/77))
    for k in kontury:
        plt.plot(k[:, 0, 0], h - k[:, 0, 1], 'k', linewidth=1.2)
    plt.autoscale(tight=True)
    plt.axis('off')
    if not os.path.exists(folder + '/wektoryzacja'):
        os.makedirs(folder + '/wektoryzacja')

    plt.savefig(folder + '/wektoryzacja/' + nazwa + '.svg', format="svg", bbox_inches='tight', transparent=True, pad_inches=0)
    plt.savefig(folder + '/wektoryzacja/' + nazwa + '.png', format="png", bbox_inches='tight', transparent=True, pad_inches=0)


def run(obrazek, zmienna1, zmienna2, folder, nazwa):
    canny = algorytm_canny(obrazek, zmienna1, zmienna2)
    im = Image.fromarray(canny).convert('L')
    im.save(folder + '/' + 'canny.png')
    obrazek2 = cv2.imread(folder + '/' + 'canny.png')
    wektoryzacja(obrazek2, folder, nazwa)
    os.remove(folder + '/' + 'canny.png')
