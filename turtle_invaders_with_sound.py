import random
import time
import turtle
import winsound  # For Windows OS. For other OS, use alternative audio libraries.

# Constants
FRAME_RATE = 30
TIME_FOR_1_FRAME = 1 / FRAME_RATE

# Game Parameters
CANNON_STEP = 10
LASER_LENGTH = 20
LASER_SPEED = 20
ALIEN_SPAWN_INTERVAL = 1.2
ALIEN_SPEED = 3.5
GUTTER = 0.025 * turtle.window_width()

# Setup window
window = turtle.Screen()
window.title("The Real Python Space Invaders")
window.bgcolor("black")
window.setup(800, 600)
window.tracer(0)

# Background image
window.bgpic("background.gif")

# Register sound files
winsound.PlaySound("background.wav", winsound.SND_LOOP + winsound.SND_ASYNC)  # Background music

# Sound files
LASER_SOUND = "laser.wav"
HIT_SOUND = "hit.wav"
BONUS_SOUND = "bonus.wav"

# Create laser cannon
cannon = turtle.Turtle()
cannon.penup()
cannon.color("white")
cannon.shape("square")
cannon.setposition(0, -250)
cannon.cannon_movement = 0

# Create turtle for writing text
text = turtle.Turtle()
text.penup()
text.hideturtle()
text.setposition(-380, 280)
text.color("white")

lasers = []
aliens = []

# Functions
def draw_cannon():
    cannon.clear()
    cannon.turtlesize(1, 4)
    cannon.stamp()
    cannon.sety(-240)
    cannon.turtlesize(1, 1.5)
    cannon.stamp()
    cannon.sety(-230)
    cannon.turtlesize(0.8, 0.3)
    cannon.stamp()
    cannon.sety(-250)

def move_left():
    cannon.cannon_movement = -1

def move_right():
    cannon.cannon_movement = 1

def stop_cannon_movement():
    cannon.cannon_movement = 0

def create_laser():
    laser = turtle.Turtle()
    laser.penup()
    laser.color("red")
    laser.hideturtle()
    laser.setposition(cannon.xcor(), cannon.ycor())
    laser.setheading(90)
    laser.pendown()
    laser.pensize(3)
    laser.showturtle()

    lasers.append(laser)
    play_sound(LASER_SOUND)

def move_laser(laser):
    laser.clear()
    laser.forward(LASER_SPEED)
    laser.forward(LASER_LENGTH)
    laser.forward(-LASER_LENGTH)

def create_alien():
    alien = turtle.Turtle()
    alien.penup()
    alien.turtlesize(1.5)
    alien.setposition(
        random.randint(
            int(-380 + GUTTER),
            int(380 - GUTTER),
        ),
        250,
    )
    alien.shape("turtle")
    alien.setheading(-90)
    alien.color(random.random(), random.random(), random.random())

    aliens.append(alien)

def remove_sprite(sprite, sprite_list):
    sprite.clear()
    sprite.hideturtle()
    sprite_list.remove(sprite)


def play_sound(sound_file):
    winsound.PlaySound(sound_file, winsound.SND_ASYNC)

# Key bindings
window.listen()
window.onkeypress(move_left, "Left")
window.onkeypress(move_right, "Right")
window.onkeyrelease(stop_cannon_movement, "Left")
window.onkeyrelease(stop_cannon_movement, "Right")
window.onkeypress(create_laser, "space")
window.onkeypress(turtle.bye, "q")

draw_cannon()

# Game loop
alien_timer = 0
game_timer = time.time()
score = 0
game_running = True
bonus_given = False  # Flag to track if bonus has been given
while game_running:
    timer_this_frame = time.time()

    time_elapsed = time.time() - game_timer
    text.clear()
    text.write(
        f"Time: {time_elapsed:5.1f}s\nScore: {score:5}",
        font=("Courier", 20, "bold"),
    )

    new_x = cannon.xcor() + CANNON_STEP * cannon.cannon_movement
    if -380 + GUTTER <= new_x <= 380 - GUTTER:
        cannon.setx(new_x)
        draw_cannon()

    for laser in lasers.copy():
        move_laser(laser)
        if laser.ycor() > 250:
            remove_sprite(laser, lasers)
            break
        for alien in aliens.copy():
            if laser.distance(alien) < 20:
                remove_sprite(laser, lasers)
                remove_sprite(alien, aliens)
                score += 20
                play_sound(HIT_SOUND)
                break

    if time.time() - alien_timer > ALIEN_SPAWN_INTERVAL:
        create_alien()
        alien_timer = time.time()

    for alien in aliens:
        alien.forward(ALIEN_SPEED)
        if alien.ycor() < -250:
            game_running = False
            break

    # Check for bonus
    if score % 1000 == 0 and score != 0 and not bonus_given:
        text.clear()
        text.write(
            f"Time: {time_elapsed:5.1f}s\nScore: {score:5}\nBONUS: 500",
            font=("Courier", 20, "bold"),
        )
        score += 500
        play_sound(BONUS_SOUND)
        bonus_given = True

    # Reset bonus_given flag if score is no longer a multiple of 1000
    if score % 1000 != 0:
        bonus_given = False

    time_for_this_frame = time.time() - timer_this_frame
    if time_for_this_frame < TIME_FOR_1_FRAME:
        time.sleep(TIME_FOR_1_FRAME - time_for_this_frame)
    window.update()

winsound.PlaySound(None, winsound.SND_PURGE)  # Stop background music
splash_text = turtle.Turtle()
splash_text.hideturtle()
splash_text.color("white")
splash_text.write("GAME OVER", font=("Courier", 40, "bold"), align="center")
turtle.done()
