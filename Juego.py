import pygame
import sys
import random
import time

# Inicializamos PyGame
pygame.init()

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)

# Dimensiones de la pantalla
ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))

# Reloj
reloj = pygame.time.Clock()

# Función para mostrar texto en la pantalla
def mostrar_texto(pantalla, texto, tamaño, color, x, y):
    fuente = pygame.font.Font(None, tamaño)
    superficie_texto = fuente.render(texto, True, color)
    rect_texto = superficie_texto.get_rect()
    rect_texto.center = (x, y)
    pantalla.blit(superficie_texto, rect_texto)

# Menú principal
def menu_principal():
    while True:
        pantalla.fill(NEGRO)
        mostrar_texto(pantalla, "Juego", 74, BLANCO, ANCHO // 2, ALTO // 4)
        mostrar_texto(pantalla, "1. Elegir Modo", 36, BLANCO, ANCHO // 2, ALTO // 2)
        mostrar_texto(pantalla, "2. Salir", 36, BLANCO, ANCHO // 2, ALTO // 1.5)
        mostrar_texto(pantalla, "Presiona Q para salir", 24, BLANCO, ANCHO // 2, ALTO // 1.2)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    elegir_modo()
                if evento.key == pygame.K_2 or evento.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

# Función para elegir el modo
def elegir_modo():
    while True:
        pantalla.fill(NEGRO)
        mostrar_texto(pantalla, "Elige el Modo", 74, BLANCO, ANCHO // 2, ALTO // 4)
        mostrar_texto(pantalla, "1. Sobrevivir", 36, BLANCO, ANCHO // 2, ALTO // 2)
        mostrar_texto(pantalla, "2. Conseguir gema", 36, BLANCO, ANCHO // 2, ALTO // 1.5)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    elegir_dificultad(juego_sobrevivir)
                if evento.key == pygame.K_2:
                    elegir_dificultad(juego_conseguir_gema)

        pygame.display.update()

# Función para elegir la dificultad
def elegir_dificultad(modo):
    global velocidad, tiempo_aparicion_gema
    while True:
        pantalla.fill(NEGRO)
        mostrar_texto(pantalla, "Elige la Dificultad", 74, BLANCO, ANCHO // 2, ALTO // 4)
        mostrar_texto(pantalla, "1. Normal", 36, BLANCO, ANCHO // 2, ALTO // 2)
        mostrar_texto(pantalla, "2. Difícil", 36, BLANCO, ANCHO // 2, ALTO // 1.5)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    velocidad = 5
                    tiempo_aparicion_gema = 10
                    modo()
                if evento.key == pygame.K_2:
                    velocidad = 7
                    tiempo_aparicion_gema = 20
                    modo()

        pygame.display.update()

# Función para el modo sobrevivir
def juego_sobrevivir():
    jugador_pos = [ANCHO // 2, ALTO - 50]
    enemigos_pos = [[random.randint(0, ANCHO-50), random.randint(-ALTO, 0)] for _ in range(5)]
    start_time = time.time()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and jugador_pos[0] > 0:
            jugador_pos[0] -= 5
        if teclas[pygame.K_RIGHT] and jugador_pos[0] < ANCHO - 50:
            jugador_pos[0] += 5
        if teclas[pygame.K_UP] and jugador_pos[1] > 0:
            jugador_pos[1] -= 5
        if teclas[pygame.K_DOWN] and jugador_pos[1] < ALTO - 50:
            jugador_pos[1] += 5

        pantalla.fill(NEGRO)

        pygame.draw.rect(pantalla, AZUL, (jugador_pos[0], jugador_pos[1], 50, 50))

        for pos in enemigos_pos:
            pos[1] += velocidad
            if pos[1] > ALTO:
                pos[0] = random.randint(0, ANCHO-50)
                pos[1] = random.randint(-ALTO, 0)
            pygame.draw.rect(pantalla, ROJO, (pos[0], pos[1], 30, 30))

        for pos in enemigos_pos:
            if jugador_pos[0] < pos[0] + 30 and jugador_pos[0] + 50 > pos[0] and \
               jugador_pos[1] < pos[1] + 30 and jugador_pos[1] + 50 > pos[1]:
                mostrar_texto(pantalla, "¡Perdiste!", 74, BLANCO, ANCHO // 2, ALTO // 2)
                pygame.display.update()
                pygame.time.delay(2000)
                menu_principal()

        tiempo_transcurrido = int(time.time() - start_time)
        mostrar_texto(pantalla, f"Tiempo: {tiempo_transcurrido}", 36, BLANCO, 100, 50)

        if tiempo_transcurrido >= 10:
            mostrar_texto(pantalla, "¡Ganaste!", 74, BLANCO, ANCHO // 2, ALTO // 2)
            pygame.display.update()
            pygame.time.delay(2000)
            menu_principal()

        pygame.display.update()
        reloj.tick(30)

# Función para el modo conseguir gema
def juego_conseguir_gema():
    jugador_pos = [ANCHO // 2, ALTO - 50]
    cuadrados_pos = [[random.randint(0, ANCHO-50), random.randint(-ALTO, 0)] for _ in range(5)]
    start_time = time.time()
    gema_visible = False
    gema_pos = None

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and jugador_pos[0] > 0:
            jugador_pos[0] -= 5
        if teclas[pygame.K_RIGHT] and jugador_pos[0] < ANCHO - 50:
            jugador_pos[0] += 5
        if teclas[pygame.K_UP] and jugador_pos[1] > 0:
            jugador_pos[1] -= 5
        if teclas[pygame.K_DOWN] and jugador_pos[1] < ALTO - 50:
            jugador_pos[1] += 5

        pantalla.fill(NEGRO)

        pygame.draw.rect(pantalla, AZUL, (jugador_pos[0], jugador_pos[1], 50, 50))

        for pos in cuadrados_pos:
            pos[1] += velocidad
            if pos[1] > ALTO:
                pos[0] = random.randint(0, ANCHO-50)
                pos[1] = random.randint(-ALTO, 0)
            pygame.draw.rect(pantalla, ROJO, (pos[0], pos[1], 50, 50))

        for pos in cuadrados_pos:
            if jugador_pos[0] < pos[0] + 50 and jugador_pos[0] + 50 > pos[0] and \
               jugador_pos[1] < pos[1] + 50 and jugador_pos[1] + 50 > pos[1]:
                mostrar_texto(pantalla, "¡Perdiste!", 74, BLANCO, ANCHO // 2, ALTO // 2)
                pygame.display.update()
                pygame.time.delay(2000)
                menu_principal()

        tiempo_transcurrido = int(time.time() - start_time)
        mostrar_texto(pantalla, f"Tiempo: {tiempo_transcurrido}", 36, BLANCO, 100, 50)

        if tiempo_transcurrido >= tiempo_aparicion_gema and not gema_visible:
            gema_visible = True
            gema_pos = [random.randint(0, ANCHO-50), random.randint(0, ALTO-50)]

        if gema_visible:
            pygame.draw.rect(pantalla, VERDE, (gema_pos[0], gema_pos[1], 50, 50))

            if jugador_pos[0] < gema_pos[0] + 50 and jugador_pos[0] + 50 > gema_pos[0] and \
               jugador_pos[1] < gema_pos[1] + 50 and jugador_pos[1] + 50 > gema_pos[1]:
                mostrar_texto(pantalla, "¡Ganaste!", 74, BLANCO, ANCHO // 2, ALTO // 2)
                pygame.display.update()
                pygame.time.delay(2000)
                menu_principal()

        pygame.display.update()
        reloj.tick(30)

menu_principal()
