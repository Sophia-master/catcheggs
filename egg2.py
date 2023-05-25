import play
import time
from random import randint

frames = 48  # столько раз в секунду проводится основной цикл

# ГЛОБАЛЬНЫЕ ПЕРЕМЕНЫЕ
score = 0 # счет игры
finish = False # флаг конца игры
old_time = 0 #счетчик времени для запуска нового яйца

hello_txt = play.new_text(words='Catch them all!', x=0, y=play.screen.height/2-30)
hello_txt.color = (120, 120, 120) # серый, похож на официальный питоновский
score_txt = play.new_text(words='0', x=play.screen.width/2-80, y=play.screen.height/2-30, color='gold') # очки на экране
help_txt = play.new_text(words="Use 'q', 'a', 'e', 'd' keys", x=0, y=-play.screen.height/2+30)

bunny = play.new_image(image='easter-bunny.png', x=0, y=20) # кролик
bowl = play.new_image(image='bowl.png', x=100,  y=80, size=40) #корзинка

#всего возможно 4 места появления нового яйца
egg_x = [400, -380] 
egg_y = [200, 50]
eggs = [] # список имеющихся яиц

def add_shelf(x, y, a): #создание полок
    shelf = play.new_box(x=x, y=y, width=300, height=10, angle=a)
    shelf.color = (48, 105, 152)
    shelf.start_physics(can_move=False, mass=10, friction=1.0)

def new_egg():
    egg = play.new_circle(color=(255, 212, 59), x=egg_x[randint(0,1)], y=egg_y[randint(0,1)], radius = 15)
    egg.start_physics(mass=1, friction=0.7)
    eggs.append(egg)
    

@play.when_program_starts
def start():
    global old_time
    old_time = time.time()

    add_shelf(300, 150, 20)
    add_shelf(300, 0, 20)
    add_shelf(-300, 150, -20)
    add_shelf(-300, 0, -20)
    new_egg()

@play.repeat_forever
async def game():
    global score, old_time

    if score <= 10:
        z = 3
    elif score > 10 and score <= 25:
        z = 2
    else:
        z = 1

    if play.key_is_pressed('e') or play.key_is_pressed('у'):
        bowl.x = 100
        bowl.y = 80
    if play.key_is_pressed('d') or play.key_is_pressed('в'):
        bowl.x = 100
        bowl.y = -80
    if play.key_is_pressed('q') or play.key_is_pressed('й'):
        bowl.x = -100
        bowl.y = 80
    if play.key_is_pressed('a') or play.key_is_pressed('ф'):
        bowl.x = -100
        bowl.y = -80

    if time.time()-old_time > z:
        new_egg()
        old_time = time.time()

    for egg in eggs:

        if egg.y < -250:
            hello_txt.words = "That's all folks!"
            hello_txt.color = 'red'
            await play.timer(seconds=1)
            quit()

        if egg.is_touching(bowl):
            egg.hide()
            eggs.remove(egg)
            score += 1
            score_txt.words = score

    if score == 50:
        hello_txt.words = "Well done! You've collected all the eggs!"
        hello_txt.color = 'yellow'
        await play.timer(seconds=1)
        quit()

    await play.timer(seconds=1/frames)

play.start_program()