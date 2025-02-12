import pygame
import sys
import math
import random
from pygame.locals import *
from PIL import Image

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 5)
        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed
        self.color = color
        self.radius = random.randint(2, 4)
        self.life = self.initial_life = random.randint(20, 40)
        self.surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        alpha = 128
        pygame.draw.circle(self.surface, self.color + (alpha,), (self.radius, self.radius), self.radius)
    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.dy += 0.1
        self.life -= 1

    def draw(self, surface):
        if self.life > 0:
            surface.blit(self.surface, (int(self.x - self.radius), int(self.y - self.radius)))
class GrowingCircle:
    def __init__(self, x, y, initial_radius, color):
        self.x = x
        self.y = y
        self.radius = initial_radius
        self.color = color
        self.alpha = 255  # Opacité initiale maximale
        self.growth_rate = 2  # Vitesse de croissance du cercle
        self.fade_rate = 5    # Vitesse de disparition du cercle
        self.max_radius = 500  # Rayon maximal

    def update(self):
        self.radius += self.growth_rate
        self.alpha -= self.fade_rate
        if self.alpha < 0:
            self.alpha = 0

    def draw(self, surface):
        if self.alpha > 0:
            temp_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(temp_surface, self.color + (int(self.alpha),), (int(self.radius), int(self.radius)), int(self.radius), 5)
            surface.blit(temp_surface, (int(self.x - self.radius), int(self.y - self.radius)))

class AnimatedGIF:
    def __init__(self, filepath):
        self.frames = []
        self.frame_durations = []
        self.load_gif(filepath)
        self.current_frame_index = 0
        self.accumulator = 0

    def load_gif(self, filepath):
        pil_image = Image.open(filepath)
        frame_count = 0
        try:
            while True:
                pil_frame = pil_image.convert('RGBA')
                frame_duration = pil_image.info.get('duration', 100)
                self.frame_durations.append(frame_duration)
                data = pil_frame.tobytes()
                size = pil_frame.size
                mode = pil_frame.mode
                image = pygame.image.frombuffer(data, size, mode)
                self.frames.append(image)
                frame_count += 1
                pil_image.seek(pil_image.tell() + 1)
        except EOFError:
            pass
        print(f"Chargement de {frame_count} frames du GIF.")

    def update(self, dt):
        if len(self.frames) > 1:
            self.accumulator += dt * 1000
            frame_duration = self.frame_durations[self.current_frame_index]
            while self.accumulator >= frame_duration:
                self.accumulator -= frame_duration
                self.current_frame_index = (self.current_frame_index + 1) % len(self.frames)

    def reset(self):
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

    sound = pygame.mixer.Sound("./assets/alicante.wav") ## PUT YOUR MUSIC HERE

    sound_channel = pygame.mixer.Channel(0)

    gif_path = "./assets/cat-dancing.gif" ## PUT YOUR GIF HERE
    animated_gif = AnimatedGIF(gif_path)

    gif_width, gif_height = animated_gif.frames[0].get_size()

    len_screen, height_screen = screen.get_size()
    x = (len_screen - gif_width) // 2
    y = (height_screen - gif_height) // 2 - 100

    center_x = x + gif_width // 2
    center_y = y + gif_height // 2

    padding = 200
    rayon_standard = max(gif_width, gif_height) // 2 + padding
    rayon_courant = rayon_standard


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
    previous_color = color

    ball = {
        'x': len_screen // 2 - 100,
        'y': height_screen // 2 - 250,
        'dx': 4,
        'dy': 0,
        'radius': 10,
        'color': color,
    }


    color_circle = color

    gravity = 0.1
    restitution = 1
    radius_plus = 2.5

    circle_pulse_timer = 0

    particles = []
    growing_circles = []

    gif_playing = False

    collision_time = None

    simulation_started = False

    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 0))  # Fond noir

    loop = True
    clock = pygame.time.Clock()
    while loop:
        dt = clock.tick(60) / 1000

        current_time = pygame.time.get_ticks()

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
                elif event.key == pygame.K_SPACE:
                    simulation_started = True

        screen.blit(background, (0, 0))

        if simulation_started:
            ball['dy'] += gravity

            ball['x'] += ball['dx']
            ball['y'] += ball['dy']

            dx = ball['x'] - center_x
            dy = ball['y'] - center_y
            distance = math.hypot(dx, dy)

            collision_occurred = False
            if distance + ball['radius'] >= rayon_standard:
                collision_occurred = True

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

                ball['x'] = center_x + nx * (rayon_standard - ball['radius'])
                ball['y'] = center_y + ny * (rayon_standard - ball['radius'])

                circle_pulse_timer = 5

                previous_color = color

                for _ in range(20):
                    particle = Particle(ball['x'], ball['y'], previous_color)
                    particles.append(particle)

                growing_circle = GrowingCircle(center_x, center_y, rayon_courant, color_circle)
                growing_circles.append(growing_circle)

                while True:
                    new_color = random.choice(predefined_colors)
                    if new_color != previous_color:
                        color = new_color
                        break

                ball['color'] = color
                color_circle = color

                collision_time = current_time

                if not sound_channel.get_busy():
                    sound_channel.play(sound)
                    animated_gif.reset()
                    gif_playing = True
                else:
                    pass

            if collision_time is not None:
                elapsed_time = current_time - collision_time
                if elapsed_time >= 1000:
                    if gif_playing:
                        gif_playing = False
                        sound_channel.stop()
                    collision_time = None


            rayon_courant = rayon_standard

            if circle_pulse_timer > 0:
                rayon_courant = rayon_standard + 15
                circle_pulse_timer -= 1

            for gc in growing_circles[:]:
                gc.update()
                gc.draw(screen)
                if gc.alpha == 0 or gc.radius >= gc.max_radius:
                    growing_circles.remove(gc)

            sizeof_circ = 5
            pygame.draw.circle(screen, color_circle, (center_x, center_y), rayon_courant, sizeof_circ)


            pygame.draw.circle(screen, ball['color'], (int(ball['x']), int(ball['y'])), int(ball['radius']))
            

            if gif_playing:
                animated_gif.update(dt)
                animated_gif.draw(screen, (x, y))
            else:
                screen.blit(animated_gif.frames[0], (x, y))

            for particle in particles[:]:
                particle.update()
                particle.draw(screen)
                if particle.life <= 0:
                    particles.remove(particle)

            time_text = font.render(f"time : {current_time/1000:.2f}", True, (255, 255, 255))
            screen.blit(time_text, (10, 10))

        else:
            pause_text = font.render("Appuyez sur Espace pour démarrer la simulation", True, (255, 255, 255))
            text_rect = pause_text.get_rect(center=(len_screen // 2, height_screen // 2))
            screen.blit(pause_text, text_rect)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
