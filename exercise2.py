import time

import pygame,random
import numpy as np
from gauge import Gauge
trend =[]
reflection =[]

game = 4 # 1-trening słuchowo-wzrokowy, 2 - tylko słuch, 3 - tylko wzrok

exercise_window = pygame.display.set_mode((1200, 675))

# Ustawienia
def task(chann,czas_trwania = 200, pauza = 20):
    if chann == 0:
        task = [880, 440, 440]  # Częstotliwości w Hz
        pygame.mixer.Channel(0).set_volume(1.0)
        pygame.mixer.Channel(1).set_volume(0.0)
    elif chann == 1:
        task = [440, 440, 880]
        pygame.mixer.Channel(0).set_volume(0.0)
        pygame.mixer.Channel(1).set_volume(1.0)
    else:
        task =[440,880,440]
        pygame.mixer.Channel(0).set_volume(0.1)
        pygame.mixer.Channel(1).set_volume(0.1)

    # Generowanie dźwięków
    for czestotliwosc in task:
        # Tworzenie tablicy z próbkami dźwięku
        sample_array = np.int16(32767.0 * np.sin(2 * np.pi * czestotliwosc * np.arange(0, czas_trwania/1000, 1/44100.0)))

        # Odtwarzanie dźwięku

        pygame.mixer.Sound(sample_array).play()

        # Pauza
        print(czas_trwania , pauza, czas_trwania + pauza)
        pygame.time.delay(czas_trwania + pauza)

def exercise():
    pygame.init()
    pygame.mixer.init(channels=2)

    pygame.joystick.init()
    joystick_count = pygame.joystick.get_count()
    while joystick_count == 0:

        screen = pygame.image.load('images/error01.jpg')
        screen = pygame.transform.scale(screen, (1200, 675))
        exercise_window.blit(screen, (0, 0))
        pygame.display.update()
        pygame.joystick.init()
        time.sleep(5)
        exit()

    gamepad = pygame.joystick.Joystick(0)
    gamepad.init()



    #DisplayInfo('info/exercise1/')



    FONT = pygame.font.SysFont('Franklin Gothic Heavy', 60)


    my_gauge = Gauge(
            screen=exercise_window,
            FONT=FONT,
            x_cord=exercise_window.get_width() / 2,
            y_cord=exercise_window.get_height() / 2 + 100,
            thickness=20,
            radius=100,
            circle_colour=(240,20,20),
            glow=False)

    percentage = 0

    screen = pygame.image.load('images/gamepad_screen.jpg')

    no = pygame.image.load('images/no.png')
    ok = pygame.image.load('images/ok.png')
    arrow_l = pygame.image.load("images/line-clipart-L.png")
    arrow_r = pygame.image.load("images/line-clipart-R.png")
    result_position = (exercise_window.get_width()/2.0 - 100, 30)


    counter_y = 0
    counter_n = 0
    setpoint = 0
    offset = 0.5


    my_gauge.draw(percent=offset*100)
    pygame.display.update()
    time.sleep(3)

    #time.sleep(5)

    #main loop:

    while True:
        t = random.randint(0,1)
        task(t,int(offset*1000),int(offset*100))
        answer = -1

        start_time = pygame.time.get_ticks()
        while answer == -1:
            timer = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.JOYBUTTONDOWN:

                    elapsed_time = pygame.time.get_ticks() - start_time
                    reflection.append(elapsed_time)
                    start_time = elapsed_time
                    answer = event.button - 9
                    if answer == 0:
                        exercise_window.blit(arrow_l,(50,200))

                    elif answer == 1:
                        exercise_window.blit(arrow_r, (850, 200))


                    if answer == t:
                        exercise_window.blit(screen, (0, 0))
                        exercise_window.blit(ok, result_position)
                        pygame.display.update()
                        counter_y += 1
                        offset=offset -0.03
                    else:

                        exercise_window.blit(screen,(0,0))
                        exercise_window.blit(no, result_position)
                        pygame.display.update()
                        offset = offset + 0.02
                        counter_n += 1
                    break
            time.sleep(2)
            exercise_window.blit(screen, (0, 0))
            pygame.display.update()

        trend.append(offset)
        if offset<0.2:
            setpoint +=1
            offset = 0.01
        if setpoint > 2:
            exit()
        time.sleep(2)

    return([reflection,trend,counter_y,counter_n])
# Wyłączenie Pygame

print (exercise())
pygame.quit()
