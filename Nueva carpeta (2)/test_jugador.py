import unittest
import pygame
from juego import Jugador, WIDTH  

class TestJugador(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.jugador = Jugador()

    def tearDown(self):
        pygame.quit()
    def test_mover(self):
        initial_position = self.jugador.rect.x
        self.jugador.mover(10)
        self.assertEqual(self.jugador.rect.x, initial_position + 10)

    def test_mover_limites(self):
        self.jugador.rect.x = 0
        self.jugador.mover(-10)
        self.assertEqual(self.jugador.rect.x, 0)  

        self.jugador.rect.x = WIDTH - self.jugador.rect.width
        self.jugador.mover(10)
        self.assertEqual(self.jugador.rect.x, WIDTH - self.jugador.rect.width)  

if __name__ == "__main__":
    unittest.main()