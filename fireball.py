import pygame


class Fireball(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        # Загружаем изображение снаряда и масштабируем его
        self.image = pygame.image.load('bullet.png')
        self.image = pygame.transform.scale(self.image, (50, 20))
        self.image.set_colorkey((255, 255, 255))  # Делаем белый цвет прозрачным, если нужно
        # Позиция снаряда, смещённая вниз на 50 пикселей
        adjusted_position = (position[0], position[1] + 60)
        self.rect = self.image.get_rect(center=adjusted_position)
        self.velocity = -0.6  # Снаряд летит влево

    def update(self):
        self.rect.x += self.velocity
        # Удаляем снаряд, если он выходит за пределы экрана
        if self.rect.right < 0:
            self.kill()
