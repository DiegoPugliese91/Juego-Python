import pygame
import sys
import random
import time

pygame.init()

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)

# Constantes
TIEMPO_APARICION_GEMA_DIFIC_NORMAL = 10
TIEMPO_APARICION_GEMA_DIFIC_DIFICIL = 20
VELOCIDAD_MINIMA = 10
VELOCIDAD_MAXIMA = 15

# Dimensiones de la pantalla
ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))

# Reloj
reloj = pygame.time.Clock()

class Jugador:
    def __init__(self, x, y, tamaño, color):
        self.pos = [x, y]
        self.tamaño = tamaño
        self.color = color

    def dibujar(self):
        pygame.draw.rect(pantalla, self.color, (self.pos[0], self.pos[1], self.tamaño, self.tamaño))

    def mover(self, teclas):
        if teclas[pygame.K_LEFT] and self.pos[0] > 0:
            self.pos[0] -= 5
        if teclas[pygame.K_RIGHT] and self.pos[0] < ANCHO - self.tamaño:
            self.pos[0] += 5
        if teclas[pygame.K_UP] and self.pos[1] > 0:
            self.pos[1] -= 5
        if teclas[pygame.K_DOWN] and self.pos[1] < ALTO - self.tamaño:
            self.pos[1] += 5

class Enemigo:
    def __init__(self, x, y, tamaño, color, velocidad):
        self.pos = [x, y]
        self.tamaño = tamaño
        self.color = color
        self.velocidad = velocidad

    def mover(self):
        self.pos[1] += self.velocidad
        if self.pos[1] > ALTO:
            self.pos[0] = random.randint(0, ANCHO - self.tamaño)
            self.pos[1] = random.randint(-ALTO, 0)

    def dibujar(self):
        pygame.draw.rect(pantalla, self.color, (self.pos[0], self.pos[1], self.tamaño, self.tamaño))

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
        mostrar_texto(pantalla, "Evadiendo", 74, BLANCO, ANCHO // 2, ALTO // 4)
        mostrar_texto(pantalla, "1. Elegir Modo", 36, BLANCO, ANCHO // 2, ALTO // 2)
        mostrar_texto(pantalla, "2. Salir", 36, BLANCO, ANCHO // 2, ALTO // 1.5)

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
                    velocidad = VELOCIDAD_MINIMA
                    tiempo_aparicion_gema = TIEMPO_APARICION_GEMA_DIFIC_NORMAL
                    modo()
                if evento.key == pygame.K_2:
                    velocidad = VELOCIDAD_MAXIMA
                    tiempo_aparicion_gema = TIEMPO_APARICION_GEMA_DIFIC_DIFICIL
                    modo()

        pygame.display.update()

# Función para el modo sobrevivir
def juego_sobrevivir():
    jugador = Jugador(ANCHO // 2, ALTO - 50, 50, AZUL) #centrar el jugador
    enemigos = [Enemigo(random.randint(0, ANCHO - 50), random.randint(-ALTO, 0), 30, ROJO, velocidad) for _ in range(5)]
    start_time = time.time()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        teclas = pygame.key.get_pressed()
        jugador.mover(teclas)

        pantalla.fill(NEGRO)

        jugador.dibujar()

        for enemigo in enemigos:
            enemigo.mover()
            enemigo.dibujar()

        for enemigo in enemigos:
            if jugador.pos[0] < enemigo.pos[0] + enemigo.tamaño and \
               jugador.pos[0] + jugador.tamaño > enemigo.pos[0] and \
               jugador.pos[1] < enemigo.pos[1] + enemigo.tamaño and \
               jugador.pos[1] + jugador.tamaño > enemigo.pos[1]:
                mostrar_texto(pantalla, "¡Perdiste!", 74, BLANCO, ANCHO // 2, ALTO // 2)
                pygame.display.update()
                pygame.time.delay(2000)
                menu_principal()

        tiempo_transcurrido = int(time.time() - start_time)
        mostrar_texto(pantalla, f"Tiempo: {tiempo_transcurrido}", 36, BLANCO, 100, 50)

        if tiempo_transcurrido >= TIEMPO_APARICION_GEMA_DIFIC_NORMAL:
            mostrar_texto(pantalla, "¡Ganaste!", 74, BLANCO, ANCHO // 2, ALTO // 2)
            pygame.display.update()
            pygame.time.delay(2000)
            menu_principal()

        pygame.display.update()
        reloj.tick(30)

# Función para el modo conseguir gema
def juego_conseguir_gema():
    jugador = Jugador(ANCHO // 2, ALTO - 50, 50, AZUL)
    enemigos = [Enemigo(random.randint(0, ANCHO - 50), random.randint(-ALTO, 0), 30, ROJO, velocidad) for _ in range(5)]
    start_time = time.time()
    gema_visible = False
    gema_pos = None

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        teclas = pygame.key.get_pressed()
        jugador.mover(teclas)

        pantalla.fill(NEGRO)

        jugador.dibujar()

        for enemigo in enemigos:
            enemigo.mover()
            enemigo.dibujar()

        for enemigo in enemigos:
            if jugador.pos[0] < enemigo.pos[0] + enemigo.tamaño and \
               jugador.pos[0] + jugador.tamaño > enemigo.pos[0] and \
               jugador.pos[1] < enemigo.pos[1] + enemigo.tamaño and \
               jugador.pos[1] + jugador.tamaño > enemigo.pos[1]:
                mostrar_texto(pantalla, "¡Perdiste!", 74, BLANCO, ANCHO // 2, ALTO // 2)
                pygame.display.update()
                pygame.time.delay(2000)
                menu_principal()

        if not gema_visible and time.time() - start_time >= tiempo_aparicion_gema:
            gema_pos = [random.randint(0, ANCHO - 50), random.randint(0, ALTO - 50)]
            gema_visible = True

        if gema_visible:
            pygame.draw.rect(pantalla, VERDE, (gema_pos[0], gema_pos[1], 30, 30))
            if jugador.pos[0] < gema_pos[0] + 30 and \
               jugador.pos[0] + jugador.tamaño > gema_pos[0] and \
               jugador.pos[1] < gema_pos[1] + 30 and \
               jugador.pos[1] + jugador.tamaño > gema_pos[1]:
                mostrar_texto(pantalla, "¡Ganaste!", 74, BLANCO, ANCHO // 2, ALTO // 2)
                pygame.display.update()
                pygame.time.delay(2000)
                menu_principal()

        pygame.display.update()
        reloj.tick(30)

menu_principal()
