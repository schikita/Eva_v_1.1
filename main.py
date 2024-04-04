import pygame                              # Подключение модулей и директорий к проекту игры
import sys                                 # Подключение модулей и директорий к проекту игры
from video import Video                    # Подключение модулей и директорий к проекту игры
from player import Player                  # Подключение модулей и директорий к проекту игры
from spear import Spear                    # Подключение модулей и директорий к проекту игры
from boss import Boss                      # Подключение модулей и директорий к проекту игры
from boss_2 import BossTwo                 # Подключение модулей и директорий к проекту игры
from boss_3 import BossThree               # Подключение модулей и директорий к проекту игры
from fireball import Fireball              # Подключение модулей и директорий к проекту игры
import random                              # Подключение модулей и директорий к проекту игры
from meteo import Meteo                    # Подключение модулей и директорий к проекту игры
from Car import Car                        # Подключение модулей и директорий к проекту игры

# Инициализация Pygame
pygame.init()

# Основные настройки экрана
screen_width, screen_height = 1000, 800 # высота экрана
screen = pygame.display.set_mode((screen_width, screen_height)) # установка ширины, высоты экрана
pygame.display.set_caption("Evangelion") # вывод заголовка

# Инициализация групп спрайтов
all_sprites = pygame.sprite.Group()
spears = pygame.sprite.Group() # включение копъя в группу спрайтов

# Загрузка изображения листа спрайтов и создание игрока
player_image_sheet = pygame.image.load('Sprite-player-1.png')
player = Player(player_image_sheet, (100, 100), all_sprites, spears, screen_height)

# Загрузка видео для интро
intro_video_path = 'video-1.mp4'  # Укажите здесь правильный путь к вашему видеофайлу
intro_video = Video(intro_video_path)
intro_video.set_size((1000, 800))


def intro():
    pygame.mixer.music.stop()  # Останавливаем музыку перед началом интро
    intro_video.set_volume(1)  # добавляем громкость  для видео
    intro_video.restart()  # Перезапуск видео с начала
    intro_video.resume()  # Возобновляем воспроизведение видео, на случай если оно было остановлено

    while intro_video.active:  # Пока видео активно
        intro_video.draw(screen, (0, 0))  # Отрисовка кадра видео
        pygame.display.update()  # Обновление экрана для отображения кадра
        for event in pygame.event.get(): #обработка событий 
            if event.type == pygame.QUIT: # при нажатии QUIT,
                pygame.quit() # пользователь выходит из игры
                sys.exit() # программа закрывается
            elif event.type == pygame.KEYDOWN: # формирование события нажатия клавиши
                if event.key == pygame.K_ESCAPE: #модуль работы с клавиатурой: когда пользователь нажимает ESCAPE
                    intro_video.close()  # Закрываем видео
                    return  # Выход из функции, возвращение в главное меню
        pygame.time.wait(int(intro_video.frame_delay * 1000))  # Задержка для синхронизации с частотой кадров

    # pygame.mixer.music.play(-1)  # Воспроизведение музыки снова после окончания видео


all_sprites.add(player) #добавление спрайта

fireballs = pygame.sprite.Group() # инициализация группы спрайтов

meteo_image = pygame.image.load('meteo.png').convert_alpha() # добавление рисунка
meteos = pygame.sprite.Group() # инициализация группы спрайтов

cars = pygame.sprite.Group() # инициализация группы спрайтов

# Загрузка спрайтового листа босса
boss_image_sheet = pygame.image.load('Boss-1.png').convert_alpha()
boss_position = (screen_width - 300, screen_height - 260)  # Учитывая, что размер спрайта босса - 250x250

# Создание экземпляра босса
boss = Boss(screen, boss_image_sheet, boss_position, all_sprites, fireballs)
boss_two = BossTwo(screen, boss_image_sheet, boss_position, all_sprites, fireballs)
boss_three = BossTwo(screen, boss_image_sheet, boss_position, all_sprites, fireballs)

# Добавление босса в группу всех спрайтов
all_sprites.add(boss)

# Иконка игры
programIcon = pygame.image.load('Icon-1.png') # загрузка изображения иконки игры
pygame.display.set_icon(programIcon) # установка иконки 

# Фон и музыка для первоначального меню
menu_background_image = pygame.image.load('Start-game-1.png') # загрузка изображения 
pygame.mixer.music.load('04-Cruel-Angel_s-Thesis.ogg') # загрузка музыки
pygame.mixer.music.play(-1) # уровень воспроизведения

start_image = pygame.image.load('first_image.png') # начало загрузки картинки
image_rect = start_image.get_rect(center=(screen_width // 2, screen_height // 2))
fade_duration = 5000  # Продолжительность затемнения в миллисекундах
alpha_level = 255  # Начальный уровень альфа-канала

screen.blit(start_image, image_rect) # вывод на экран 
pygame.display.flip() #обновляет содержимое основного окна игры

# Время начала показа
start_time = pygame.time.get_ticks()

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Шрифты
pygame.font.init()  # Необходимо для работы с шрифтами в pygame
font = pygame.font.Font(None, 36) # установка шрифта

# Переменные состояния игры
current_screen = "menu" # меню
selected_option = 0 # выбор пункта меню
pause_selected_option = 0 
in_game = False
pause_options = ["Continue", "Mute", "Exit"] # опции паузы -  "продолжить", "отключить звук", "Выход"
menu_options = ["Level 1", "Level 2", "Level 3", "Intro", "Mute", "Exit"] # опции меню - "Уровень 1", "Уровень 2", "Уровень 3", "Введение", "Выключить звук", "Выход"
music_muted = False

# Фоновые изображения и музыка для каждого уровня
backgrounds = {
    "Level 1": "BG-Level-1.png",
    "Level 2": "BG_levels_2.png",
    "Level 3": "BG-level-3.png",
}
music_files = {                         # файлы музыки
    "Level 1": "08-Angel-Attack.ogg",
    "Level 2": "12-EVA-00.ogg",
    "Level 3": "23-The-Beast.ogg",
}
current_background = None   #  текущее состояние 
current_music = None        #  текущая музыка

level_1_completed = False
level_2_completed = False
level_3_completed = False


screen.blit(start_image, image_rect) # вывод на экран
pygame.display.flip() #обновляет содержимое основного окна игры
pygame.time.wait(5000) #  время ожидания 

def toggle_music(): # переключение музыки
    global music_muted # логика включения паузы
    music_muted = not music_muted
    if music_muted: # выполнение условия: если музыка отключена
        pygame.mixer.music.pause() # музыка на паузе
    else:
        pygame.mixer.music.unpause() # иначе снять с паузы музыку


def load_level(level): # загрузка уровня игры
    global current_background, current_music, in_game, boss, boss_two, boss_three
    current_background = pygame.image.load(backgrounds[level])
    current_music = music_files[level] # 
    pygame.mixer.music.load(current_music) # загрузка музыки
    pygame.mixer.music.play(-1) # проигрывание музыки
    in_game = True

    # Сброс предыдущего состояния уровня
    if boss: #  если босс 
        boss.kill() # убит
        boss = None # нет босса
    if boss_two:  # Добавлено условие для второго босса
        boss_two.kill() # босс два убит
        boss_two = None # нет второго босса
    if boss_three: # если босс три ( условие)
        boss_three.kill() # третий босс убит
        boss_three = None # нет третьего босса 

    if level == "Level 1": # условие для первого уровня
        boss = Boss(screen, boss_image_sheet, boss_position, all_sprites, fireballs)
        all_sprites.add(boss) # добавление босса 
    elif level == "Level 2": # условие для второго уровня
        boss_two_image_sheet = pygame.image.load('Boss-2.png').convert_alpha()  # Убедитесь, что у вас есть 'Boss-2.png' # добавление изображения босса 
        boss_two_position = (screen_width - 300, screen_height - 260) # указываем размеры для позиции второго босса 
        boss_two = BossTwo(screen, boss_two_image_sheet, boss_two_position, all_sprites, fireballs)
        all_sprites.add(boss_two) #инициализация второго босса
    elif level == "Level 3":
        boss_three_image_sheet = pygame.image.load(
            'Boss-3.png').convert_alpha()  # Убедитесь, что у вас есть 'Boss-2.png'
        boss_three_position = (screen_width - 300, screen_height - 260)
        boss_three = BossThree(screen, boss_three_image_sheet, boss_three_position, all_sprites, fireballs)

        all_sprites.add(boss_three) #инициализация третьего босса

    else:
        # Удаляем босса из всех групп спрайтов, если это не первый уровень
        if boss:
            boss.kill()
            boss = None  # Сброс boss в None после удаления
            boss_two = None


def draw_level():
    screen.blit(current_background, (0, 0)) # вывод на экран


def process_menu_selection(option): # выбор меню
    global current_screen, in_game, running 
    if option in ["Level 1", "Level 2", "Level 3"]: # логика загрузки уровней игры
        load_level(option) #загрузка уровня
        current_screen = option # вывод на экран
        in_game = True # начало игры
    elif option == "Intro": 
        intro_video.restart()
        intro_video.set_volume(1)
        intro()
    elif option == "Mute":
        toggle_music()
    elif option == "Exit":
        running = False
        pygame.quit()
        sys.exit()


def process_pause_selection(option):  # выбор пунка паузы
    global current_screen, in_game, running
    if option == "Continue":  #  если выбрали пунк "Продолжить"
        current_screen = "game"  # включается окно игры
        in_game = True  # игра продолжается
    elif option == "Mute":  # если выбрали опцию "выключить звук"
        toggle_music()
    elif option == "Exit":  # если выбрали опцию "выход"
        current_screen = "menu"  # выход в меню
        in_game = False
        pygame.mixer.music.stop()  # музыка останавливается
        pygame.mixer.music.load('04-Cruel-Angel_s-Thesis.ogg')  # загрузка аудиофайла
        pygame.mixer.music.play(-1)  # игрвет музыка


def draw_menu(options, selected):  # выбор меню
    screen.blit(menu_background_image, (0, 0)) 
    menu_x = screen_width * 3 / 4
    for i, option in enumerate(options):
        if i == 0 and level_1_completed:  # Если это первый уровень и он завершен
            color = (100, 100, 100)  # Серый цвет для неактивного пункта
        else:
            color = WHITE if i == selected else (100, 100, 100)
        text = font.render(option, True, color)
        screen.blit(text, (menu_x - text.get_width() / 2, 150 + 50 * i))


def main(font):
    global current_screen, selected_option, pause_selected_option, in_game, music_muted, boss

    running = True
    level_complete = False  # Флаг завершения уровня

    while running:  # процесс игры
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and in_game:
                    current_screen = "pause"
                    continue

                if current_screen == "menu":
                    if event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % len(menu_options)
                    elif event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % len(menu_options)
                    elif event.key == pygame.K_RETURN:
                        process_menu_selection(menu_options[selected_option])

                elif current_screen == "pause":
                    if event.key == pygame.K_DOWN:
                        pause_selected_option = (pause_selected_option + 1) % len(pause_options)
                    elif event.key == pygame.K_UP:
                        pause_selected_option = (pause_selected_option - 1) % len(pause_options)
                    elif event.key == pygame.K_RETURN:
                        process_pause_selection(pause_options[pause_selected_option])

                elif current_screen == "level 2" and boss_two and boss_two.alive():
                    boss_two_health_text = font.render(f"Boss 2 Health: {boss_two.health}", True, WHITE)
                    screen.blit(boss_two_health_text, (10, 50))
                elif current_screen == "level 3" and boss_three and boss_three.alive():
                    boss_three_health_text = font.render(f"Boss 3 Health: {boss_three.health}", True, WHITE)
                    screen.blit(boss_three_health_text, (10, 50))

        keys = pygame.key.get_pressed()
        screen.fill(BLACK)

        if current_screen == "menu":
            draw_menu(menu_options, selected_option)
        elif current_screen == "pause":
            draw_menu(pause_options, pause_selected_option)
        elif current_screen == "intro":
            intro()
        elif in_game:
            draw_level()
            player.update(keys)  # Обновление игрока с передачей клавиш

            player_health_text = font.render(f"Player Health: {player.health}", True, (255, 255, 255))
            screen.blit(player_health_text, (10, 10))  # Размещение в левом верхнем углу

            # Отрисовка индикации жизней босса, если босс существует и жив
            if boss and boss.alive():
                boss_health_text = font.render(f"Boss Health: {boss.health}", True, (255, 0, 0))
                screen.blit(boss_health_text,
                            (screen_width - boss_health_text.get_width() - 10, 10))  # Размещение в правом верхнем углу

            if boss_three and boss_three.alive():
                hits = pygame.sprite.spritecollide(boss_three, spears,
                                                   True)  # True означает, что копья будут уничтожены при столкновении
                for hit in hits:
                    boss_three.hit()  # Вызываем метод hit() для третьего босса
                    # Отрисовка индикатора здоровья босса, если он жив
                    boss_three_health_text = font.render(f"Boss 3 Health: {boss_three.health}", True, WHITE)
                    screen.blit(boss_three_health_text, (10, 70))  # Позиция индикатора здоровья босса

            if current_screen == 'Level 2' and boss_two and boss_two.alive():
                hits = pygame.sprite.spritecollide(boss_two, spears, True)

                cars.update()  # Обновляем машины

                if random.randint(1, 1500) == 1:
                    car_y_position = screen_height - 100
                    new_car = Car('car.png', (screen_width, car_y_position), -0.6)
                    cars.add(new_car)
                    all_sprites.add(new_car)

                for hit in hits:
                    boss_two.hit()
                    if boss_two.health <= 0:
                        level_complete = True
                        display_time = pygame.time.get_ticks()
                        boss_two.kill()

                boss_two_health_text = font.render(f"Boss 2 Health: {boss_two.health}", True, (255, 255, 255))
                screen.blit(boss_two_health_text, (10, 60))

            if current_screen == 'Level 3' and boss_three and boss_three.alive():
                meteos.update()  # Обновляем метеориты
                if random.randint(1, 800) == 1:  # С некоторым шансом добавляем метеорит
                    new_meteo = Meteo(meteo_image, screen_width, screen_height)
                    meteos.add(new_meteo)
                    all_sprites.add(new_meteo)

                hits = pygame.sprite.spritecollide(boss_three, spears, True)
                for hit in hits:
                    boss_three.hit()
                    if boss_two.health <= 0:
                        level_complete = True
                        display_time = pygame.time.get_ticks()
                        boss_three.kill()

                boss_three_health_text = font.render(f"Boss 3 Health: {boss_three.health}", True, (255, 255, 255))
                screen.blit(boss_three_health_text, (10, 60))

            fireballs.update()

            # Обновляем спрайты, исключая игрока, если в группе all_sprites есть и другие спрайты
            for sprite in all_sprites:
                if sprite != player:
                    sprite.update()

            spears.update()

            all_sprites.draw(screen)
            spears.draw(screen)
            fireballs.draw(screen)

            # Проверка столкновений между игроком и шариками
            hits = pygame.sprite.spritecollide(player, fireballs, True)
            for hit in hits:
                player.take_damage()
                if player.health <= 0:
                    # Если жизни игрока закончились, показываем сообщение "You lose"
                    screen.fill((0, 0, 0))  # Очищаем экран
                    font = pygame.font.Font(None, 74)
                    lose_text = font.render('You Lost', True, (255, 0, 0))
                    text_rect = lose_text.get_rect(center=(screen_width / 2, screen_height / 2))
                    screen.blit(lose_text, text_rect)
                    pygame.display.flip()
                    pygame.time.wait(2000)  # Даем время увидеть сообщение
                    current_screen = "menu"
                    in_game = False
                    break  # Выход из цикла, чтобы не обрабатывать другие столкновения после смерти

            # Проверяем столкновения метеоритов с игроком
            hits = pygame.sprite.spritecollide(player, meteos, True)
            for hit in hits:
                player.take_damage()
                # Проверяем, остались ли у игрока жизни после попадания
                if player.health <= 0:
                    # Если жизни игрока закончились, показываем сообщение "You lose"
                    screen.fill((0, 0, 0))  # Очищаем экран
                    font = pygame.font.Font(None, 74)
                    lose_text = font.render('You Lost', True, (255, 0, 0))
                    text_rect = lose_text.get_rect(center=(screen_width / 2, screen_height / 2))
                    screen.blit(lose_text, text_rect)
                    pygame.display.flip()
                    pygame.time.wait(2000)  # Даем время увидеть сообщение
                    current_screen = "menu"
                    in_game = False
                    break  # Выход из цикла, чтобы не обрабатывать другие столкновения после смерти

            # Позже, в игровом цикле, проверка столкновений могла бы выглядеть так:
            hits = pygame.sprite.spritecollide(player, cars, True)
            for hit in hits:
                player.take_damage()
                if player.health <= 0:
                    # Если жизни игрока закончились, показываем сообщение "You lose"
                    screen.fill((0, 0, 0))  # Очищаем экран
                    font = pygame.font.Font(None, 74)
                    lose_text = font.render('You Lost', True, (255, 0, 0))
                    text_rect = lose_text.get_rect(center=(screen_width / 2, screen_height / 2))
                    screen.blit(lose_text, text_rect)
                    pygame.display.flip()
                    pygame.time.wait(2000)  # Даем время увидеть сообщение
                    current_screen = "menu"
                    in_game = False
                    break  # Выход из цикла, чтобы не обрабатывать другие столкновения после смерти

            # Проверка столкновений
            if boss is not None and boss.alive():  # Добавлена проверка на существование объекта boss
                hits = pygame.sprite.spritecollide(boss, spears, True)
                for hit in hits:
                    boss.hit()
                    if boss.health <= 0:  # Проверяем здоровье босса после попадания
                        level_complete = True
                        display_time = pygame.time.get_ticks()
                        boss.kill()  # Удаляем босса из всех групп спрайтов
                        level_1_completed = True  # Указываем, что первый уровень завершен

            # Показываем сообщение "Level Complete", если уровень завершен
            if level_complete:
                if pygame.time.get_ticks() - display_time < 3000:  # Отображаем сообщение в течение 5 секунд
                    font = pygame.font.Font(None, 74)
                    text = font.render('Level Complete', True, WHITE)
                    text_rect = text.get_rect(center=(screen_width / 2, screen_height / 2))
                    screen.blit(text, text_rect)
                else:
                    # Возвращение в главное меню после 5 секунд
                    current_screen = "menu"
                    in_game = False
                    level_complete = False  # Сброс флага завершения уровня для возможного повторного прохождения

        pygame.display.flip()

    pygame.quit() # выход из игры
    sys.exit() # выход из приложения


if __name__ == "__main__":
    pygame.font.init()
    font = pygame.font.Font(None, 36)
    main(font)
