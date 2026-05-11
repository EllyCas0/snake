import turtle
from pathlib import Path

from entities import Food, Snake
from ui import Border, Button, Scoreboard, StartScreen


SCREEN_WIDTH = 600
SCREEN_HEIGHT = 680
MOVE_DISTANCE = 20
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
PLAYFIELD_BOUNDS = {
    "top": PLAYFIELD_TOP,
    "bottom": PLAYFIELD_BOTTOM,
    "left": PLAYFIELD_LEFT,
    "right": PLAYFIELD_RIGHT,
}


class Game:
    def __init__(self):
        self.selected_difficulty = DEFAULT_DIFFICULTY
        self.game_is_on = False
        self.game_started = False
        self.is_paused = False
        self.current_speed_ms = DIFFICULTY_SPEEDS[self.selected_difficulty]

        self.screen = turtle.Screen()
        self.screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        self.screen.bgcolor(BACKGROUND_COLOR)
        self.screen.title("Snake Game")
        self.screen.tracer(0)

        self.snake = Snake(
            color=SNAKE_COLOR,
            move_distance=MOVE_DISTANCE,
            starting_positions=STARTING_POSITIONS,
            playfield_bounds=PLAYFIELD_BOUNDS,
        )
        self.food = Food(
            playfield_bounds=PLAYFIELD_BOUNDS,
            move_distance=MOVE_DISTANCE,
            food_colors=FOOD_COLORS,
        )
        self.scoreboard = Scoreboard(
            text_color=TEXT_COLOR,
            playfield_top=PLAYFIELD_TOP,
            high_score_file=HIGH_SCORE_FILE,
            difficulty_speeds=DIFFICULTY_SPEEDS,
            selected_difficulty_getter=lambda: self.selected_difficulty,
        )
        self.border = Border(
            border_color=BORDER_COLOR,
            playfield_bounds=PLAYFIELD_BOUNDS,
        )
        self.start_button = Button(
            "Start",
            0,
            -175,
            text_color=TEXT_COLOR,
            border_color=BUTTON_BORDER_COLOR,
            fill_color=START_BUTTON_COLOR,
            hover_color=START_BUTTON_HOVER_COLOR,
        )
        self.play_again_button = Button(
            "Play Again",
            0,
            0,
            text_color=TEXT_COLOR,
            border_color=BUTTON_BORDER_COLOR,
            fill_color=PLAY_AGAIN_BUTTON_COLOR,
            hover_color=PLAY_AGAIN_BUTTON_HOVER_COLOR,
        )
        self.main_menu_button = Button(
            "Main Menu",
            0,
            -60,
            text_color=TEXT_COLOR,
            border_color=BUTTON_BORDER_COLOR,
            width=180,
            height=44,
            fill_color=MENU_BUTTON_COLOR,
            hover_color=MENU_BUTTON_HOVER_COLOR,
        )
        self.easy_button = Button(
            "Easy",
            -120,
            -115,
            text_color=TEXT_COLOR,
            border_color=BUTTON_BORDER_COLOR,
            width=100,
            height=40,
            fill_color=DIFFICULTY_BUTTON_COLOR,
            hover_color=DIFFICULTY_BUTTON_HOVER_COLOR,
            selected_fill_color=DIFFICULTY_BUTTON_SELECTED_COLOR,
        )
        self.normal_button = Button(
            "Normal",
            0,
            -115,
            text_color=TEXT_COLOR,
            border_color=BUTTON_BORDER_COLOR,
            width=100,
            height=40,
            fill_color=DIFFICULTY_BUTTON_COLOR,
            hover_color=DIFFICULTY_BUTTON_HOVER_COLOR,
            selected_fill_color=DIFFICULTY_BUTTON_SELECTED_COLOR,
        )
        self.hard_button = Button(
            "Hard",
            120,
            -115,
            text_color=TEXT_COLOR,
            border_color=BUTTON_BORDER_COLOR,
            width=100,
            height=40,
            fill_color=DIFFICULTY_BUTTON_COLOR,
            hover_color=DIFFICULTY_BUTTON_HOVER_COLOR,
            selected_fill_color=DIFFICULTY_BUTTON_SELECTED_COLOR,
        )
        self.exit_button = Button(
            "Exit",
            0,
            -245,
            text_color=TEXT_COLOR,
            border_color=BUTTON_BORDER_COLOR,
            width=140,
            height=44,
            fill_color=EXIT_BUTTON_COLOR,
            hover_color=EXIT_BUTTON_HOVER_COLOR,
        )
        self.start_screen = StartScreen(
            screen=self.screen,
            start_button=self.start_button,
            title_color=TITLE_COLOR,
            title_shadow_color=TITLE_SHADOW_COLOR,
            text_color=TEXT_COLOR,
            arrow_color=ARROW_COLOR,
            button_glow_colors=BUTTON_GLOW_COLORS,
            animation_ms=START_ANIMATION_MS,
        )

    def all_buttons(self):
        return [
            self.start_button,
            self.play_again_button,
            self.main_menu_button,
            self.easy_button,
            self.normal_button,
            self.hard_button,
            self.exit_button,
        ]

    def difficulty_buttons(self):
        return {
            "Easy": self.easy_button,
            "Normal": self.normal_button,
            "Hard": self.hard_button,
        }

    def set_difficulty(self, name):
        self.selected_difficulty = name
        for difficulty_name, button in self.difficulty_buttons().items():
            button.set_selected(difficulty_name == self.selected_difficulty)

    def bind_controls(self):
        keymap = {
            "Up": self.snake.up,
            "Down": self.snake.down,
            "Left": self.snake.left,
            "Right": self.snake.right,
            "w": self.snake.up,
            "s": self.snake.down,
            "a": self.snake.left,
            "d": self.snake.right,
            "W": self.snake.up,
            "S": self.snake.down,
            "A": self.snake.left,
            "D": self.snake.right,
            "p": self.toggle_pause,
            "P": self.toggle_pause,
            "Escape": self.quit_game,
        }
        self.screen.listen()
        for key, handler in keymap.items():
            self.screen.onkeypress(handler, key)

    def prepare_game(self):
        self.border.show_border()
        self.snake.show()
        self.food.show_food()
        self.scoreboard.reset()
        self.scoreboard.show_score()
        self.scoreboard.clear_pause()
        self.food.refresh(occupied_positions=self.snake.occupied_positions())
        self.play_again_button.hide()
        self.main_menu_button.hide()
        self.start_button.hide()
        self.easy_button.hide()
        self.normal_button.hide()
        self.hard_button.hide()
        self.exit_button.hide()
        self.start_screen.hide()

    def restart_game(self):
        self.snake.reset()
        self.prepare_game()
        self.current_speed_ms = DIFFICULTY_SPEEDS[self.selected_difficulty]
        self.is_paused = False
        self.start_countdown()

    def handle_click(self, x, y):
        for difficulty_name, button in self.difficulty_buttons().items():
            if self.start_screen.is_visible and button.was_clicked(x, y):
                self.set_difficulty(difficulty_name)
                self.screen.update()
                return

        if self.exit_button.was_clicked(x, y):
            self.quit_game()
            return

        if not self.game_started and self.start_button.was_clicked(x, y):
            self.game_started = True
            self.restart_game()
            return

        if not self.game_is_on and self.play_again_button.was_clicked(x, y):
            self.restart_game()
            return

        if not self.game_is_on and self.main_menu_button.was_clicked(x, y):
            self.show_main_menu()

    def handle_mouse_move(self, event):
        x = event.x - (self.screen.window_width() / 2)
        y = (self.screen.window_height() / 2) - event.y

        for button in self.all_buttons():
            button.set_hovered(button.was_clicked(x, y))

        self.screen.update()

    def quit_game(self):
        self.screen.bye()

    def toggle_pause(self):
        if not self.game_started or not self.game_is_on:
            return

        self.is_paused = not self.is_paused

        if self.is_paused:
            self.scoreboard.show_pause()
        else:
            self.scoreboard.clear_pause()
            self.run_game()

        self.screen.update()

    def end_game(self):
        self.game_is_on = False
        self.is_paused = False
        self.scoreboard.clear_pause()
        self.scoreboard.clear_countdown()
        self.scoreboard.game_over()
        self.play_again_button.show()
        self.main_menu_button.show()
        self.exit_button.show()
        self.screen.update()

    def countdown_step(self, index):
        countdown_messages = ["3", "2", "1", "Go!"]

        if index >= len(countdown_messages):
            self.scoreboard.clear_countdown()
            self.game_is_on = True
            self.run_game()
            return

        self.scoreboard.show_countdown(countdown_messages[index])
        self.screen.update()
        self.screen.ontimer(lambda: self.countdown_step(index + 1), 500)

    def start_countdown(self):
        self.game_is_on = False
        self.scoreboard.clear_message()
        self.scoreboard.clear_pause()
        self.countdown_step(0)

    def show_main_menu(self):
        self.game_is_on = False
        self.is_paused = False
        self.game_started = False
        self.border.hide_border()
        self.snake.hide()
        self.food.hide_food()
        self.scoreboard.reset()
        self.scoreboard.hide_score()
        self.scoreboard.clear_pause()
        self.scoreboard.clear_countdown()
        self.play_again_button.hide()
        self.main_menu_button.hide()
        self.start_screen.show()
        self.start_button.show()
        self.easy_button.show()
        self.normal_button.show()
        self.hard_button.show()
        self.set_difficulty(self.selected_difficulty)
        self.exit_button.show()
        self.screen.update()

    def run_game(self):
        if not self.game_is_on or self.is_paused:
            return

        self.snake.move()

        if self.snake.segments[0].distance(self.food) < 15:
            self.snake.extend()
            self.food.refresh(occupied_positions=self.snake.occupied_positions())
            self.scoreboard.increase()
            self.current_speed_ms = max(
                MIN_SPEED_MS,
                self.current_speed_ms - SPEED_STEP_MS,
            )

        if self.snake.hit_wall() or self.snake.hit_tail():
            self.end_game()
            return

        self.screen.update()
        self.screen.ontimer(self.run_game, self.current_speed_ms)

    def start(self):
        self.bind_controls()
        self.border.hide_border()
        self.snake.hide()
        self.food.hide_food()
        self.scoreboard.hide_score()
        self.start_screen.show()
        self.start_button.show()
        self.easy_button.show()
        self.normal_button.show()
        self.hard_button.show()
        self.set_difficulty(self.selected_difficulty)
        self.exit_button.show()
        self.screen.onclick(self.handle_click)
        self.screen.getcanvas().bind("<Motion>", self.handle_mouse_move)
        self.screen.update()
        self.screen.mainloop()
