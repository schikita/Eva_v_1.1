import pygame


class Car(pygame.sprite.Sprite):
    def __init__(self, image_path, position, velocity):
        super().__init__()
        # Загружаем изображение машины и настраиваем прозрачность
        self.image = pygame.image.load(image_path).convert_alpha()
        # Можно добавить масштабирование, если изображение слишком большое
        # self.image = pygame.transform.scale(self.image, (50, 30))
        self.rect = self.image.get_rect(center=position)
        self.velocity = velocity  # Скорость машины

    def update(self):
        self.rect.x += self.velocity
        # Удаляем машину, если она вышла за пределы экрана
        if self.rect.right < 0:
            self.kill()


