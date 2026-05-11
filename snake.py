import random
import turtle
from pathlib import Path


SCREEN_WIDTH = 600
SCREEN_HEIGHT = 680
MOVE_DISTANCE = 20
START_SPEED_MS = 70
MIN_SPEED_MS = 35
SPEED_STEP_MS = 2
STARTING_POSITIONS = [(0, 0), (-20, 0), (-40, 0)]
START_ANIMATION_MS = 260
HUD_HEIGHT = 80
PLAYFIELD_TOP = (SCREEN_HEIGHT // 2) - HUD_HEIGHT
PLAYFIELD_BOTTOM = -(SCREEN_HEIGHT // 2) + 10
PLAYFIELD_LEFT = -(SCREEN_WIDTH // 2) + 10
PLAYFIELD_RIGHT = (SCREEN_WIDTH // 2) - 10
BACKGROUND_COLOR = "#111315"
SNAKE_COLOR = "#8FA06E"
BORDER_COLOR = "#D7D0C3"
TITLE_COLOR = "#C8B38A"
TITLE_SHADOW_COLOR = "#4D4436"
TEXT_COLOR = "#EEE8DE"
ARROW_COLOR = "#72848B"
BUTTON_BORDER_COLOR = "#D8D0C2"
START_BUTTON_COLOR = "#7A8C67"
PLAY_AGAIN_BUTTON_COLOR = "#6F7D62"
EXIT_BUTTON_COLOR = "#8D5F5F"
MENU_BUTTON_COLOR = "#7B6C58"
START_BUTTON_HOVER_COLOR = "#95A77B"
PLAY_AGAIN_BUTTON_HOVER_COLOR = "#849272"
EXIT_BUTTON_HOVER_COLOR = "#A36F6F"
MENU_BUTTON_HOVER_COLOR = "#94826B"
DIFFICULTY_BUTTON_COLOR = "#4D5A63"
DIFFICULTY_BUTTON_HOVER_COLOR = "#61707A"
DIFFICULTY_BUTTON_SELECTED_COLOR = "#8B9E74"
BUTTON_GLOW_COLORS = ["#7A8C67", "#83966F", "#8BA074", "#83966F", "#7A8C67", "#80926C"]
FOOD_COLORS = ["#B56F62", "#C0926D", "#C4A56F", "#9E7C8D", "#6E8C95", "#8B829E"]
HIGH_SCORE_FILE = Path(__file__).with_name("high_score.txt")
DIFFICULTY_SPEEDS = {
    "Easy": 90,
    "Normal": 70,
    "Hard": 50,
}
DEFAULT_DIFFICULTY = "Normal"
selected_difficulty = DEFAULT_DIFFICULTY


class Snake:
    def __init__(self):
        self.segments = []
        self.direction = "Right"
        self.create_snake()

    def create_snake(self):
        for position in STARTING_POSITIONS:
            self.add_segment(position)

    def add_segment(self, position):
        segment = turtle.Turtle("square")
        segment.color(SNAKE_COLOR)
        segment.penup()
        segment.goto(position)
        self.segments.append(segment)

    def extend(self):
        self.add_segment(self.segments[-1].position())

    def move(self):
        for index in range(len(self.segments) - 1, 0, -1):
            x = self.segments[index - 1].xcor()
            y = self.segments[index - 1].ycor()
            self.segments[index].goto(x, y)

        head = self.segments[0]
        if self.direction == "Up":
            head.sety(head.ycor() + MOVE_DISTANCE)
        elif self.direction == "Down":
            head.sety(head.ycor() - MOVE_DISTANCE)
        elif self.direction == "Left":
            head.setx(head.xcor() - MOVE_DISTANCE)
        elif self.direction == "Right":
            head.setx(head.xcor() + MOVE_DISTANCE)

    def up(self):
        if self.direction != "Down":
            self.direction = "Up"

    def down(self):
        if self.direction != "Up":
            self.direction = "Down"

    def left(self):
        if self.direction != "Right":
            self.direction = "Left"

    def right(self):
        if self.direction != "Left":
            self.direction = "Right"

    def hit_wall(self):
        head = self.segments[0]
        return (
            head.xcor() > PLAYFIELD_RIGHT
            or head.xcor() < PLAYFIELD_LEFT
            or head.ycor() > PLAYFIELD_TOP
            or head.ycor() < PLAYFIELD_BOTTOM
        )

    def hit_tail(self):
        head = self.segments[0]
        for segment in self.segments[1:]:
            if head.distance(segment) < 10:
                return True
        return False

    def reset(self):
        for segment in self.segments:
            segment.hideturtle()
            segment.goto(1000, 1000)

        self.segments.clear()
        self.direction = "Right"
        self.create_snake()

    def hide(self):
        for segment in self.segments:
            segment.hideturtle()

    def show(self):
        for segment in self.segments:
            segment.showturtle()


class Food(turtle.Turtle):
    def __init__(self):
        super().__init__("circle")
        self.color("red")
        self.penup()
        self.shapesize(0.8, 0.8)
        self.speed("fastest")
        self.refresh()

    def refresh(self):
        min_x = int(PLAYFIELD_LEFT // MOVE_DISTANCE) + 1
        max_x = int(PLAYFIELD_RIGHT // MOVE_DISTANCE) - 1
        min_y = int(PLAYFIELD_BOTTOM // MOVE_DISTANCE) + 1
        max_y = int(PLAYFIELD_TOP // MOVE_DISTANCE) - 1
        x = random.randint(min_x, max_x) * MOVE_DISTANCE
        y = random.randint(min_y, max_y) * MOVE_DISTANCE
        self.color(random.choice(FOOD_COLORS))
        self.goto(x, y)

    def hide_food(self):
        self.hideturtle()

    def show_food(self):
        self.showturtle()


class Scoreboard(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.high_scores = self.load_high_scores()
        self.color(TEXT_COLOR)
        self.penup()
        self.hideturtle()
        self.goto(0, PLAYFIELD_TOP + 24)
        self.message_turtle = turtle.Turtle()
        self.message_turtle.hideturtle()
        self.message_turtle.color(TEXT_COLOR)
        self.message_turtle.penup()
        self.pause_turtle = turtle.Turtle()
        self.pause_turtle.hideturtle()
        self.pause_turtle.color(TEXT_COLOR)
        self.pause_turtle.penup()
        self.countdown_turtle = turtle.Turtle()
        self.countdown_turtle.hideturtle()
        self.countdown_turtle.color(TEXT_COLOR)
        self.countdown_turtle.penup()
        self.write_score()

    def load_high_scores(self):
        try:
            contents = HIGH_SCORE_FILE.read_text(encoding="utf-8").strip()
        except FileNotFoundError:
            return {difficulty: 0 for difficulty in DIFFICULTY_SPEEDS}

        default_scores = {difficulty: 0 for difficulty in DIFFICULTY_SPEEDS}

        if not contents:
            return default_scores

        if "=" not in contents:
            try:
                legacy_score = int(contents)
            except ValueError:
                return default_scores
            default_scores["Normal"] = legacy_score
            return default_scores

        for line in contents.splitlines():
            if "=" not in line:
                continue
            difficulty, value = line.split("=", 1)
            difficulty = difficulty.strip()
            if difficulty not in default_scores:
                continue
            try:
                default_scores[difficulty] = int(value.strip())
            except ValueError:
                continue

        return default_scores

    def save_high_scores(self):
        lines = [
            f"{difficulty}={self.high_scores[difficulty]}"
            for difficulty in DIFFICULTY_SPEEDS
        ]
        HIGH_SCORE_FILE.write_text("\n".join(lines), encoding="utf-8")

    def current_high_score(self):
        return self.high_scores[selected_difficulty]

    def write_score(self):
        self.clear()
        self.write(
            f"Score: {self.score}   {selected_difficulty} Best: {self.current_high_score()}",
            align="center",
            font=("Arial", 18, "bold"),
        )

    def increase(self):
        self.score += 1
        if self.score > self.current_high_score():
            self.high_scores[selected_difficulty] = self.score
            self.save_high_scores()
        self.write_score()

    def reset(self):
        self.score = 0
        self.goto(0, PLAYFIELD_TOP + 24)
        self.write_score()
        self.clear_message()

    def game_over(self):
        self.message_turtle.goto(0, 40)
        self.message_turtle.write(
            "Game Over",
            align="center",
            font=("Arial", 24, "bold"),
        )

    def clear_message(self):
        self.message_turtle.clear()

    def show_pause(self):
        self.pause_turtle.clear()
        self.pause_turtle.goto(0, 5)
        self.pause_turtle.write(
            "Paused\nPress P to continue",
            align="center",
            font=("Arial", 20, "bold"),
        )

    def clear_pause(self):
        self.pause_turtle.clear()

    def show_countdown(self, text):
        self.countdown_turtle.clear()
        self.countdown_turtle.goto(0, 10)
        self.countdown_turtle.write(
            text,
            align="center",
            font=("Arial", 28, "bold"),
        )

    def clear_countdown(self):
        self.countdown_turtle.clear()


class Border(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.color(BORDER_COLOR)
        self.pensize(3)
        self.penup()
        self.goto(PLAYFIELD_LEFT, PLAYFIELD_TOP)
        self.pendown()
        for _ in range(2):
            self.forward(PLAYFIELD_RIGHT - PLAYFIELD_LEFT)
            self.right(90)
            self.forward(PLAYFIELD_TOP - PLAYFIELD_BOTTOM)
            self.right(90)
        self.penup()


class Button:
    def __init__(
        self,
        text,
        center_x,
        center_y,
        width=180,
        height=50,
        fill_color=START_BUTTON_COLOR,
        hover_color=None,
        selected_fill_color=None,
    ):
        self.text = text
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.fill_color = fill_color
        self.hover_color = hover_color or fill_color
        self.selected_fill_color = selected_fill_color or self.hover_color
        self.current_fill_color = fill_color
        self.is_visible = False
        self.is_hovered = False
        self.is_selected = False

        self.box = turtle.Turtle()
        self.box.penup()
        self.box.hideturtle()
        self.box.color(BUTTON_BORDER_COLOR)
        self.box.fillcolor(self.fill_color)
        self.box.pensize(3)
        self.box.hideturtle()

        self.label = turtle.Turtle()
        self.label.penup()
        self.label.hideturtle()
        self.label.color(TEXT_COLOR)

    def show(self, fill_color=None, width=None, height=None):
        if fill_color is None:
            fill_color = self.fill_color
        if width is None:
            width = self.width
        if height is None:
            height = self.height

        self.is_visible = True
        self.current_fill_color = fill_color

        left = self.center_x - (width / 2)
        top = self.center_y + (height / 2)

        self.box.clear()
        self.box.fillcolor(fill_color)
        self.box.goto(left, top)
        self.box.setheading(0)
        self.box.pendown()
        self.box.begin_fill()
        for _ in range(2):
            self.box.forward(width)
            self.box.right(90)
            self.box.forward(height)
            self.box.right(90)
        self.box.end_fill()
        self.box.penup()

        self.label.clear()
        self.label.goto(self.center_x, self.center_y - 14)
        self.label.write(
            self.text,
            align="center",
            font=("Arial", 18, "bold"),
        )

    def hide(self):
        self.is_visible = False
        self.is_hovered = False
        self.is_selected = False
        self.box.clear()
        self.label.clear()

    def was_clicked(self, x, y):
        half_width = self.width / 2
        half_height = self.height / 2
        return (
            self.center_x - half_width <= x <= self.center_x + half_width
            and self.center_y - half_height <= y <= self.center_y + half_height
        )

    def set_hovered(self, hovered):
        if not self.is_visible or self.is_hovered == hovered:
            return

        self.is_hovered = hovered
        self.redraw()

    def set_selected(self, selected):
        if self.is_selected == selected:
            return

        self.is_selected = selected
        if self.is_visible:
            self.redraw()

    def redraw(self):
        if not self.is_visible:
            return

        if self.is_selected:
            fill_color = self.selected_fill_color
        elif self.is_hovered:
            fill_color = self.hover_color
        else:
            fill_color = self.fill_color
        self.show(fill_color=fill_color)


class StartScreen:
    def __init__(self):
        self.is_visible = False
        self.arrow_offset = 0
        self.arrow_direction = 1
        self.button_glow_step = 0

        self.shadow = turtle.Turtle()
        self.shadow.hideturtle()
        self.shadow.color(TITLE_SHADOW_COLOR)
        self.shadow.penup()

        self.title = turtle.Turtle()
        self.title.hideturtle()
        self.title.color(TITLE_COLOR)
        self.title.penup()

        self.subtitle = turtle.Turtle()
        self.subtitle.hideturtle()
        self.subtitle.color(TEXT_COLOR)
        self.subtitle.penup()

        self.instructions = turtle.Turtle()
        self.instructions.hideturtle()
        self.instructions.color(TEXT_COLOR)
        self.instructions.penup()

        self.difficulty_label = turtle.Turtle()
        self.difficulty_label.hideturtle()
        self.difficulty_label.color(TEXT_COLOR)
        self.difficulty_label.penup()

        self.arrows = turtle.Turtle()
        self.arrows.hideturtle()
        self.arrows.color(ARROW_COLOR)
        self.arrows.pensize(3)
        self.arrows.penup()

    def draw_arrow(self, x, y, heading):
        self.arrows.goto(x, y)
        self.arrows.setheading(heading)
        self.arrows.pendown()
        self.arrows.forward(16)
        self.arrows.backward(16)
        self.arrows.left(25)
        self.arrows.forward(7)
        self.arrows.backward(7)
        self.arrows.right(50)
        self.arrows.forward(7)
        self.arrows.backward(7)
        self.arrows.left(25)
        self.arrows.penup()

    def draw_arrow_icons(self):
        self.arrows.clear()
        left_center_x = -230 - self.arrow_offset
        right_center_x = 230 + self.arrow_offset
        center_y = 12

        self.draw_arrow(left_center_x - 14, center_y, 180)
        self.draw_arrow(left_center_x + 14, center_y, 0)
        self.draw_arrow(left_center_x, center_y + 14, 90)
        self.draw_arrow(left_center_x, center_y - 14, 270)

        self.draw_arrow(right_center_x - 14, center_y, 180)
        self.draw_arrow(right_center_x + 14, center_y, 0)
        self.draw_arrow(right_center_x, center_y + 14, 90)
        self.draw_arrow(right_center_x, center_y - 14, 270)

    def animate(self):
        if not self.is_visible:
            return

        self.arrow_offset += self.arrow_direction * 4
        if self.arrow_offset >= 8:
            self.arrow_offset = 8
            self.arrow_direction = -1
        elif self.arrow_offset <= 0:
            self.arrow_offset = 0
            self.arrow_direction = 1

        self.button_glow_step = (self.button_glow_step + 1) % 6
        self.draw_arrow_icons()
        start_button.show(
            fill_color=BUTTON_GLOW_COLORS[self.button_glow_step],
        )
        screen.update()
        screen.ontimer(self.animate, START_ANIMATION_MS)

    def show(self):
        self.is_visible = True
        self.arrow_offset = 0
        self.arrow_direction = 1
        self.button_glow_step = 0
        self.shadow.clear()
        self.title.clear()
        self.subtitle.clear()
        self.instructions.clear()
        self.arrows.clear()
        self.shadow.goto(3, 76)
        self.shadow.write(
            "Snake Game",
            align="center",
            font=("Arial", 30, "bold"),
        )
        self.title.goto(0, 80)
        self.title.write(
            "Snake Game",
            align="center",
            font=("Arial", 30, "bold"),
        )
        self.subtitle.goto(0, 30)
        self.subtitle.write(
            "Move with arrow keys or W A S D",
            align="center",
            font=("Arial", 16, "normal"),
        )
        self.instructions.goto(0, -5)
        self.instructions.write(
            "Press P to pause or continue",
            align="center",
            font=("Arial", 16, "normal"),
        )
        self.draw_arrow_icons()
        self.difficulty_label.clear()
        self.difficulty_label.goto(0, -60)
        self.difficulty_label.write(
            "Choose difficulty",
            align="center",
            font=("Arial", 16, "normal"),
        )
        screen.ontimer(self.animate, START_ANIMATION_MS)

    def hide(self):
        self.is_visible = False
        self.shadow.clear()
        self.title.clear()
        self.subtitle.clear()
        self.instructions.clear()
        self.difficulty_label.clear()
        self.arrows.clear()


screen = turtle.Screen()
screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
screen.bgcolor(BACKGROUND_COLOR)
screen.title("Snake Game")
screen.tracer(0)

snake = Snake()
food = Food()
scoreboard = Scoreboard()
border = Border()
start_screen = StartScreen()
start_button = Button(
    "Start",
    0,
    -175,
    fill_color=START_BUTTON_COLOR,
    hover_color=START_BUTTON_HOVER_COLOR,
)
play_again_button = Button(
    "Play Again",
    0,
    0,
    fill_color=PLAY_AGAIN_BUTTON_COLOR,
    hover_color=PLAY_AGAIN_BUTTON_HOVER_COLOR,
)
main_menu_button = Button(
    "Main Menu",
    0,
    -60,
    width=180,
    height=44,
    fill_color=MENU_BUTTON_COLOR,
    hover_color=MENU_BUTTON_HOVER_COLOR,
)
easy_button = Button(
    "Easy",
    -120,
    -115,
    width=100,
    height=40,
    fill_color=DIFFICULTY_BUTTON_COLOR,
    hover_color=DIFFICULTY_BUTTON_HOVER_COLOR,
    selected_fill_color=DIFFICULTY_BUTTON_SELECTED_COLOR,
)
normal_button = Button(
    "Normal",
    0,
    -115,
    width=100,
    height=40,
    fill_color=DIFFICULTY_BUTTON_COLOR,
    hover_color=DIFFICULTY_BUTTON_HOVER_COLOR,
    selected_fill_color=DIFFICULTY_BUTTON_SELECTED_COLOR,
)
hard_button = Button(
    "Hard",
    120,
    -115,
    width=100,
    height=40,
    fill_color=DIFFICULTY_BUTTON_COLOR,
    hover_color=DIFFICULTY_BUTTON_HOVER_COLOR,
    selected_fill_color=DIFFICULTY_BUTTON_SELECTED_COLOR,
)
exit_button = Button(
    "Exit",
    0,
    -245,
    width=140,
    height=44,
    fill_color=EXIT_BUTTON_COLOR,
    hover_color=EXIT_BUTTON_HOVER_COLOR,
)
game_is_on = False
game_started = False
is_paused = False
current_speed_ms = DIFFICULTY_SPEEDS[selected_difficulty]


def all_buttons():
    return [
        start_button,
        play_again_button,
        main_menu_button,
        easy_button,
        normal_button,
        hard_button,
        exit_button,
    ]


def difficulty_buttons():
    return {
        "Easy": easy_button,
        "Normal": normal_button,
        "Hard": hard_button,
    }


def set_difficulty(name):
    global selected_difficulty

    selected_difficulty = name
    for difficulty_name, button in difficulty_buttons().items():
        button.set_selected(difficulty_name == selected_difficulty)


def bind_controls():
    screen.listen()
    screen.onkeypress(snake.up, "Up")
    screen.onkeypress(snake.down, "Down")
    screen.onkeypress(snake.left, "Left")
    screen.onkeypress(snake.right, "Right")
    screen.onkeypress(snake.up, "w")
    screen.onkeypress(snake.down, "s")
    screen.onkeypress(snake.left, "a")
    screen.onkeypress(snake.right, "d")
    screen.onkeypress(snake.up, "W")
    screen.onkeypress(snake.down, "S")
    screen.onkeypress(snake.left, "A")
    screen.onkeypress(snake.right, "D")
    screen.onkeypress(toggle_pause, "p")
    screen.onkeypress(toggle_pause, "P")
    screen.onkeypress(quit_game, "Escape")


def prepare_game():
    snake.show()
    food.show_food()
    scoreboard.reset()
    scoreboard.clear_pause()
    food.refresh()
    play_again_button.hide()
    main_menu_button.hide()
    start_button.hide()
    easy_button.hide()
    normal_button.hide()
    hard_button.hide()
    exit_button.hide()
    start_screen.hide()


def restart_game():
    global current_speed_ms, game_is_on, is_paused

    snake.reset()
    prepare_game()
    current_speed_ms = DIFFICULTY_SPEEDS[selected_difficulty]
    is_paused = False
    start_countdown()


def handle_click(x, y):
    global game_started

    for difficulty_name, button in difficulty_buttons().items():
        if start_screen.is_visible and button.was_clicked(x, y):
            set_difficulty(difficulty_name)
            screen.update()
            return

    if exit_button.was_clicked(x, y):
        quit_game()
        return

    if not game_started and start_button.was_clicked(x, y):
        game_started = True
        restart_game()
        return

    if not game_is_on and play_again_button.was_clicked(x, y):
        restart_game()
        return

    if not game_is_on and main_menu_button.was_clicked(x, y):
        show_main_menu()


def handle_mouse_move(event):
    x = event.x - (screen.window_width() / 2)
    y = (screen.window_height() / 2) - event.y

    for button in all_buttons():
        button.set_hovered(button.was_clicked(x, y))

    screen.update()


def quit_game():
    screen.bye()


def toggle_pause():
    global is_paused

    if not game_started or not game_is_on:
        return

    is_paused = not is_paused

    if is_paused:
        scoreboard.show_pause()
    else:
        scoreboard.clear_pause()
        run_game()

    screen.update()


def end_game():
    global game_is_on, is_paused

    game_is_on = False
    is_paused = False
    scoreboard.clear_pause()
    scoreboard.clear_countdown()
    scoreboard.game_over()
    play_again_button.show()
    main_menu_button.show()
    exit_button.show()
    screen.update()


def countdown_step(index):
    global game_is_on

    countdown_messages = ["3", "2", "1", "Go!"]

    if index >= len(countdown_messages):
        scoreboard.clear_countdown()
        game_is_on = True
        run_game()
        return

    scoreboard.show_countdown(countdown_messages[index])
    screen.update()
    screen.ontimer(lambda: countdown_step(index + 1), 500)


def start_countdown():
    global game_is_on

    game_is_on = False
    scoreboard.clear_message()
    scoreboard.clear_pause()
    countdown_step(0)


def show_main_menu():
    global game_is_on, is_paused, game_started

    game_is_on = False
    is_paused = False
    game_started = False
    snake.hide()
    food.hide_food()
    scoreboard.reset()
    scoreboard.clear_pause()
    scoreboard.clear_countdown()
    play_again_button.hide()
    main_menu_button.hide()
    start_screen.show()
    start_button.show()
    easy_button.show()
    normal_button.show()
    hard_button.show()
    set_difficulty(selected_difficulty)
    exit_button.show()
    screen.update()


def run_game():
    if not game_is_on or is_paused:
        return

    global current_speed_ms

    snake.move()

    if snake.segments[0].distance(food) < 15:
        food.refresh()
        snake.extend()
        scoreboard.increase()
        current_speed_ms = max(MIN_SPEED_MS, current_speed_ms - SPEED_STEP_MS)

    if snake.hit_wall() or snake.hit_tail():
        end_game()
        return

    screen.update()
    screen.ontimer(run_game, current_speed_ms)


bind_controls()
snake.hide()
food.hide_food()
start_screen.show()
start_button.show()
easy_button.show()
normal_button.show()
hard_button.show()
set_difficulty(selected_difficulty)
exit_button.show()
screen.onclick(handle_click)
screen.getcanvas().bind("<Motion>", handle_mouse_move)
screen.update()
screen.mainloop()
