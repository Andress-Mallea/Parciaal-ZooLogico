import pygame
import time
def music(ruta):
# Inicializar pygame
    pygame.mixer.init()

# Cargar la música
    pygame.mixer.music.load(ruta)

# Reproducir la música
    pygame.mixer.music.play(-1)  # -1 hace que la música se repita indefinidamente

# Mantener el programa en ejecución mientras la música suena
def detenermusica():
    pygame.mixer.music.stop()

#    server = "LAPTOP-QKJ8CHC7"
#    driver = "ODBC Driver 17 for SQL Server"
#    "Database=Proyecto Zoologico;"