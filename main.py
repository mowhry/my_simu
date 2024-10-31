import pygame
import sys
import math
import random
from pygame.locals import *
from PIL import Image

# Définition de la classe Particle
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 5)
        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed
        self.color = color  # Utiliser la couleur passée en paramètre
        self.radius = random.randint(2, 4)
        self.life = self.initial_life = random.randint(20, 40)

        # Créer une surface pour la particule avec per-pixel alpha
        self.surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        # Dessiner le cercle sur la surface avec transparence
        alpha = 128  # Ajustez cette valeur pour changer l'opacité (0-255)
        pygame.draw.circle(self.surface, self.color + (alpha,), (self.radius, self.radius), self.radius)
    
    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.dy += 0.1  # Gravité
        self.life -= 1

    def draw(self, surface):
        if self.life > 0:
            # Blitter la surface de la particule sur l'écran
            surface.blit(self.surface, (int(self.x - self.radius), int(self.y - self.radius)))

# Définition de la classe GrowingCircle
class GrowingCircle:
    def __init__(self, x, y, initial_radius, color):
        self.x = x
        self.y = y
        self.radius = initial_radius
        self.color = color
        self.alpha = 255  # Opacité initiale maximale
        self.growth_rate = 2  # Vitesse à laquelle le cercle grandit
        self.fade_rate = 5    # Vitesse à laquelle le cercle devient transparent
        self.max_radius = 500  # Rayon maximal que le cercle peut atteindre

    def update(self):
        # Augmenter le rayon
        self.radius += self.growth_rate
        # Diminuer l'opacité
        self.alpha -= self.fade_rate
        if self.alpha < 0:
            self.alpha = 0

    def draw(self, surface):
        if self.alpha > 0:
            # Créer une surface temporaire avec per-pixel alpha
            temp_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
            # Dessiner le cercle vide sur la surface temporaire
            pygame.draw.circle(temp_surface, self.color + (int(self.alpha),), (int(self.radius), int(self.radius)), int(self.radius), 5)
            # Blitter la surface temporaire sur l'écran
            surface.blit(temp_surface, (int(self.x - self.radius), int(self.y - self.radius)))

# Définition de la classe AnimatedGIF
class AnimatedGIF:
    def __init__(self, filepath):
        self.frames = []
        self.frame_durations = []  # Durées de chaque frame en millisecondes
        self.load_gif(filepath)
        self.current_frame_index = 0
        self.accumulator = 0  # Accumulateur de temps pour changer de frame

    def load_gif(self, filepath):
        # Ouvrir le GIF avec PIL
        pil_image = Image.open(filepath)
        # Parcourir toutes les frames
        frame_count = 0
        try:
            while True:
                # Convertir la frame actuelle en mode RGBA
                pil_frame = pil_image.convert('RGBA')
                frame_duration = pil_image.info.get('duration', 100)  # Durée par défaut de 100 ms
                self.frame_durations.append(frame_duration)
                # Convertir la frame en surface Pygame
                data = pil_frame.tobytes()
                size = pil_frame.size
                mode = pil_frame.mode
                image = pygame.image.frombuffer(data, size, mode)
                self.frames.append(image)
                frame_count += 1
                pil_image.seek(pil_image.tell() + 1)
        except EOFError:
            pass  # Fin des frames
        print(f"Chargement de {frame_count} frames du GIF.")

    def update(self, dt):
        # Mettre à jour l'index de la frame en fonction du temps écoulé
        if len(self.frames) > 1:
            self.accumulator += dt * 1000  # Convertir dt en millisecondes
            frame_duration = self.frame_durations[self.current_frame_index]
            while self.accumulator >= frame_duration:
                self.accumulator -= frame_duration
                self.current_frame_index = (self.current_frame_index + 1) % len(self.frames)

    def reset(self):
        # Réinitialiser l'animation
        self.current_frame_index = 0
        self.accumulator = 0

    def draw(self, surface, position):
        image = self.frames[self.current_frame_index]
        surface.blit(image, position)

def main():
    pygame.init()
    screen = pygame.display.set_mode((720, 1280))
    pygame.display.set_caption("Animation GIF avec Pygame")
    font = pygame.font.SysFont('Arial', 24)

    # Charger le son
    sound = pygame.mixer.Sound("./assets/alicante.wav")

    # Charger le GIF animé
    gif_path = "./assets/cat-dancing.gif"
    animated_gif = AnimatedGIF(gif_path)

    # Obtenir les dimensions du GIF
    gif_width, gif_height = animated_gif.frames[0].get_size()

    # Positionnement du GIF au centre
    len_screen, height_screen = screen.get_size()
    x = (len_screen - gif_width) // 2
    y = (height_screen - gif_height) // 2 - 100

    center_x = x + gif_width // 2
    center_y = y + gif_height // 2

    padding = 200
    rayon_standard = max(gif_width, gif_height) // 2 + padding  # Rayon standard du cercle
    rayon_courant = rayon_standard  # Rayon utilisé pour le dessin du cercle

    # Liste des couleurs prédéfinies
    predefined_colors = [
        (255, 0, 0),    # Rouge
        (0, 255, 0),    # Vert
        (0, 0, 255),    # Bleu
        (255, 255, 0),  # Jaune
        (255, 165, 0),  # Orange
        (128, 0, 128),  # Violet
        (0, 255, 255),  # Cyan
        (255, 192, 203) # Rose
    ]

    # Couleur initiale (violet)
    color = (128, 0, 128)
    previous_color = color  # Initialiser la couleur précédente

    # Initialisation de la boule
    ball = {
        'x': len_screen // 2 - 100,
        'y': height_screen // 2 - 250,
        'dx': 4,
        'dy': 0,
        'radius': 10,
        'color': color,
    }

    # Couleur du cercle
    color_circle = color

    # Gravité
    gravity = 0.1
    # Coefficient de restitution
    restitution = 1
    # Incrémentation du rayon de la boule par collision
    radius_plus = 2.5

    # Timer pour l'agrandissement du cercle
    circle_pulse_timer = 0  # Nombre de frames restantes pour le cercle agrandi

    # Liste des particules
    particles = []
    # Liste des cercles qui grandissent
    growing_circles = []

    # Indicateur pour savoir si le GIF est en cours de lecture
    gif_playing = False

    # Temps depuis la dernière collision
    time_since_last_collision = 2  # Initialiser à plus de 1 seconde

    # Création du background
    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 0))  # Fond noir ou autre couleur de votre choix

    # Boucle d'événements
    loop = True
    clock = pygame.time.Clock()
    while loop:
        dt = clock.tick(60) / 1000  # Temps écoulé depuis la dernière frame en secondes

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == QUIT:
                loop = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    loop = False
                elif event.key == pygame.K_UP:
                    gravity += 0.05
                elif event.key == pygame.K_DOWN:
                    gravity = max(0, gravity - 0.05)
            # Vous pouvez ajouter d'autres événements si nécessaire

        # Mise à jour de la vitesse verticale avec la gravité
        ball['dy'] += gravity

        # Mise à jour de la position de la boule
        ball['x'] += ball['dx']
        ball['y'] += ball['dy']

        # Calcul de la distance entre la boule et le centre du cercle
        dx = ball['x'] - center_x
        dy = ball['y'] - center_y
        distance = math.hypot(dx, dy)

        # Mise à jour du temps depuis la dernière collision
        time_since_last_collision += dt

        # Détection de collision avec les bords intérieurs du cercle
        collision_occurred = False
        if distance + ball['radius'] >= rayon_standard:
            collision_occurred = True
            time_since_last_collision = 0  # Réinitialiser le timer

            if distance != 0:
                nx = dx / distance
                ny = dy / distance
                if ball['radius'] <= 330:
                    ball['radius'] += radius_plus
            else:
                nx, ny = 0, 0

            dot = ball['dx'] * nx + ball['dy'] * ny

            ball['dx'] -= 2 * dot * nx
            ball['dy'] -= 2 * dot * ny

            ball['dx'] *= restitution
            ball['dy'] *= restitution

            # Repositionner la boule juste à l'intérieur du cercle
            ball['x'] = center_x + nx * (rayon_standard - ball['radius'])
            ball['y'] = center_y + ny * (rayon_standard - ball['radius'])

            # Démarrer le timer pour l'agrandissement du cercle
            circle_pulse_timer = 5  # Le cercle restera agrandi pendant 5 frames

            # **Conserver la couleur précédente**
            previous_color = color

            # **Générer des particules avec la couleur précédente**
            for _ in range(20):  # Nombre de particules à générer
                particle = Particle(ball['x'], ball['y'], previous_color)
                particles.append(particle)

            # **Ajouter un nouveau cercle qui grandit avec la couleur précédente**
            growing_circle = GrowingCircle(center_x, center_y, rayon_courant, color_circle)
            growing_circles.append(growing_circle)

            # **Choisir une nouvelle couleur différente de la précédente**
            while True:
                new_color = random.choice(predefined_colors)
                if new_color != previous_color:
                    color = new_color
                    break

            # **Appliquer la nouvelle couleur à la boule et au cercle**
            ball['color'] = color
            color_circle = color

        # Contrôle du GIF et du son en fonction des collisions
        if collision_occurred:
            if not gif_playing:
                gif_playing = True
                time_since_last_collision = 0  # Réinitialiser le timer
                sound.play()
                animated_gif.reset()  # Réinitialiser le GIF
        elif time_since_last_collision >= 1:
            if gif_playing:
                gif_playing = False
                sound.stop()

        # Gestion de l'agrandissement temporaire du cercle
        # Réinitialiser le rayon courant du cercle
        rayon_courant = rayon_standard

        # Si le timer est actif, agrandir le cercle
        if circle_pulse_timer > 0:
            rayon_courant = rayon_standard + 15
            circle_pulse_timer -= 1

        # Blitting du background
        screen.blit(background, (0, 0))


        # Mettre à jour et dessiner les cercles qui grandissent
        for gc in growing_circles[:]:
            gc.update()
            gc.draw(screen)
            # Supprimer le cercle s'il est complètement transparent ou a atteint le rayon maximal
            if gc.alpha == 0 or gc.radius >= gc.max_radius:
                growing_circles.remove(gc)

        # Dessin du cercle principal vide autour du GIF
        sizeof_circ = 5  # Épaisseur du contour
        pygame.draw.circle(screen, color_circle, (center_x, center_y), rayon_courant, sizeof_circ)

        # Dessin de la boule
        pygame.draw.circle(screen, ball['color'], (int(ball['x']), int(ball['y'])), ball['radius'])
        
		# Mise à jour et affichage du GIF animé
        if gif_playing:
            animated_gif.update(dt)
            animated_gif.draw(screen, (x, y))
        else:
            # Afficher la première frame si le GIF n'est pas en lecture
            screen.blit(animated_gif.frames[0], (x, y))

        # Mettre à jour et dessiner les particules
        for particle in particles[:]:
            particle.update()
            particle.draw(screen)
            if particle.life <= 0:
                particles.remove(particle)

        # Afficher le temps à l'écran (optionnel)
        current_time = pygame.time.get_ticks()
        time_text = font.render(f"time : {current_time/1000:.2f}", True, (255, 255, 255))
        screen.blit(time_text, (10, 10))

        # Mise à jour de l'affichage
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
