import pygame
import random
import json
import os
from abc import ABC, abstractmethod

pygame.init()

WIDTH = 600
HEIGHT = 407
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
VERDE = (80, 200, 120)
VERDEOSCURO = (0, 100, 0)
LIMAVERDE = (50, 205, 50)
AZULOSCURO = (0, 0, 139)

pantalla = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de Tortuga")

tortuga_imagen = pygame.image.load('img/tortuga2.png')
hoja_imagen = pygame.image.load('img/p2.png')
camarones_imagen = pygame.image.load('img/p3.png')
algas_imagen = pygame.image.load('img/p4.png')
roca_imagen = pygame.image.load('img/p5.png')
medusa_imagen = pygame.image.load('img/p6.png')
fondo_imagen = pygame.image.load('img/12.jpg')
principal_imagen = pygame.image.load('img/pra.jpg')

# Redimensionar imágenes
tortuga_imagen = pygame.transform.scale(tortuga_imagen, (100, 100))
hoja_imagen = pygame.transform.scale(hoja_imagen, (80, 80))
camarones_imagen = pygame.transform.scale(camarones_imagen, (80, 80))
algas_imagen = pygame.transform.scale(algas_imagen, (80, 80))
roca_imagen = pygame.transform.scale(roca_imagen, (80, 80))
medusa_imagen = pygame.transform.scale(medusa_imagen, (80, 80))
fondo_imagen = pygame.transform.scale(fondo_imagen, (WIDTH, HEIGHT))

fuente_menu = pygame.font.Font('font/AkayaKanadaka-Regular.ttf', 22)
fuente_puntuacion = pygame.font.Font('font/AkayaKanadaka-Regular.ttf', 18)

class Alimento(ABC):
    def __init__(self, velocidad):
        self.tamano = random.randint(30, 50)
        self.x = random.randint(0, WIDTH - self.tamano)
        self.y = random.randint(-90, -self.tamano)
        self.velocidad = velocidad

    @abstractmethod
    def dibujar(self, superficie):
        pass

    def caer(self):
        self.y += self.velocidad

class Hoja(Alimento):
    def dibujar(self, superficie):
        superficie.blit(hoja_imagen, (self.x, self.y))

class Camarones(Alimento):
    def dibujar(self, superficie):
        superficie.blit(camarones_imagen, (self.x, self.y))

class Algas(Alimento):
    def dibujar(self, superficie):
        superficie.blit(algas_imagen, (self.x, self.y))

class Peligro(ABC):
    def __init__(self, velocidad):
        self.tamano = random.randint(30, 50)
        self.x = random.randint(0, WIDTH - self.tamano)
        self.y = random.randint(-90, -self.tamano)
        self.velocidad = velocidad

    @abstractmethod
    def dibujar(self, superficie):
        pass

    def caer(self):
        self.y += self.velocidad

class Roca(Peligro):
    def dibujar(self, superficie):
        superficie.blit(roca_imagen, (self.x, self.y))

class Medusa(Peligro):
    def dibujar(self, superficie):
        superficie.blit(medusa_imagen, (self.x, self.y))

class Jugador:
    def __init__(self):
        self.imagen = tortuga_imagen
        self.rect = self.imagen.get_rect(center=(WIDTH // 2, HEIGHT - 50))

    def mover(self, dx):
        self.rect.x += dx
        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))

    def dibujar(self, superficie):
        superficie.blit(self.imagen, self.rect)

class Colision:
    @staticmethod
    def verificar_colisiones(jugador, alimentos, peligros):
        colision_alimentos = []
        colision_peligros = False

        for alimento in alimentos:
            if jugador.rect.colliderect(pygame.Rect(alimento.x, alimento.y, alimento.tamano, alimento.tamano)):
                colision_alimentos.append(alimento)

        for alimento in colision_alimentos:
            alimentos.remove(alimento)

        for peligro in peligros:
            if jugador.rect.colliderect(pygame.Rect(peligro.x, peligro.y, peligro.tamano, peligro.tamano)):
                colision_peligros = True

        return colision_alimentos, colision_peligros

def cargar_puntuacion():
    if os.path.exists('puntuacion.json'):
        with open('puntuacion.json', 'r') as f:
            return json.load(f).get('mejorpuntuacion', 0)
    return 0

def guardar_puntuacion(puntuacion):
    with open('puntuacion.json', 'w') as f:
        json.dump({'mejorpuntuacion': puntuacion}, f)

def menu_principal():
    while True:
        pantalla.blit(fondo_imagen, (0, 0))
        dibujar_texto("Menú Principal", fuente_menu, (LIMAVERDE), pantalla, 50, 50)  
        dibujar_texto("1. Jugar", fuente_menu, (VERDE), pantalla, 50, 80)  
        dibujar_texto("2. Opciones", fuente_menu, (VERDE), pantalla, 50, 100) 
        dibujar_texto("3. Salir", fuente_menu, (VERDE), pantalla, 50, 120)  

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    return seleccion_dificultad()
                if evento.key == pygame.K_2:
                    opciones()
                if evento.key == pygame.K_3:
                    pygame.quit()
                    return

        pygame.display.flip()

def seleccion_dificultad():
    while True:
        pantalla.blit(fondo_imagen, (0, 0))
        dibujar_texto("Selecciona Dificultad", fuente_menu, (LIMAVERDE), pantalla, 50, 50)
        dibujar_texto("1. Fácil", fuente_menu, (VERDE), pantalla, 50, 80)
        dibujar_texto("2. Medio", fuente_menu, (VERDE), pantalla, 50, 100)
        dibujar_texto("3. Difícil", fuente_menu, (VERDE), pantalla, 50, 120)
        dibujar_texto("Esc para volver", fuente_menu, (VERDE), pantalla, 50, 140)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    return 1
                if evento.key == pygame.K_2:
                    return 2
                if evento.key == pygame.K_3:
                    return 3
                if evento.key == pygame.K_ESCAPE:
                    return

        pygame.display.flip()

def opciones():
    while True:
        pantalla.blit(fondo_imagen, (0, 0))
        dibujar_texto("Opciones", fuente_menu, (LIMAVERDE), pantalla, 50, 50)
        dibujar_texto("No hay opciones de volumen disponibles", fuente_menu, (VERDE), pantalla, 50, 100)
        dibujar_texto("Esc para volver", fuente_menu, (VERDE), pantalla, 50, 120)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return

        pygame.display.flip()

def dibujar_texto(texto, fuente, color, superficie, x, y):
    texto_renderizado = fuente.render(texto, True, color)
    superficie.blit(texto_renderizado, (x, y))

def game_over(puntuacion, mejor_puntuacion):
    while True:
        pantalla.blit(fondo_imagen, (0, 0))
        dibujar_texto("Juego Terminado", fuente_menu, (LIMAVERDE), pantalla, 50, 50)
        dibujar_texto(f"Puntuación: {puntuacion}", fuente_menu, (VERDE), pantalla, 50, 80)
        dibujar_texto(f"Mejor Puntuación: {mejor_puntuacion}", fuente_menu, (VERDE), pantalla, 50, 100)
        dibujar_texto("Presiona 'R' para volver al menú", fuente_menu, (VERDE), pantalla, 50, 120)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    return 

        pygame.display.flip()

def main():
    while True: 
        dificultad = menu_principal()
        if dificultad is None:
            return

        velocidad_caida = {1: 4, 2: 5, 3: 8}
        velocidad = velocidad_caida[dificultad]

        reloj = pygame.time.Clock()
        
        jugador = Jugador()
        alimentos = []
        peligros = []
        corriendo = True
        tiempo_generacion = 0
        tiempo_peligros = 0
        puntuacion = 0

        mejor_puntuacion = cargar_puntuacion()

        while corriendo:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    corriendo = False

            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_LEFT]:
                jugador.mover(-5)
            if teclas[pygame.K_RIGHT]:
                jugador.mover(5)

            if tiempo_generacion >= 40:
                alimentos.append(random.choice([Hoja(velocidad), Camarones(velocidad), Algas(velocidad)]))
                tiempo_generacion = 0

            if tiempo_peligros >= 60:
                peligros.append(random.choice([Roca(velocidad), Medusa(velocidad)]))
                tiempo_peligros = 0

            for alimento in alimentos + peligros:
                alimento.caer()

            colision_alimentos, colision_peligros = Colision.verificar_colisiones(jugador, alimentos, peligros)
            
            puntuacion += len(colision_alimentos)

            if colision_peligros:
                corriendo = False 

            for alimento in alimentos[:]:
                if alimento.y > HEIGHT:
                    alimentos.remove(alimento)
                    puntuacion = max(0, puntuacion - 1)

            mejor_puntuacion = max(mejor_puntuacion, puntuacion)
            guardar_puntuacion(mejor_puntuacion)

            pantalla.blit(principal_imagen, (0, 0))
            texto_puntuacion = fuente_puntuacion.render(f'Puntuación: {puntuacion}', True, (NEGRO))  
            texto_mejor_puntuacion = fuente_puntuacion.render(f'Mejor Puntuación: {mejor_puntuacion}', True, (NEGRO)) 

            pantalla.blit(texto_puntuacion, (20, 20))
            pantalla.blit(texto_mejor_puntuacion, (10, 40))
            jugador.dibujar(pantalla)
            for alimento in alimentos:
                alimento.dibujar(pantalla)
            for peligro in peligros:
                peligro.dibujar(pantalla)

            pygame.display.flip()
            reloj.tick(30)
            tiempo_generacion += 1
            tiempo_peligros += 1

        game_over(puntuacion, mejor_puntuacion)  
    pygame.quit()

if __name__ == "__main__":
    main()