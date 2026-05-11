import turtle


class Scoreboard(turtle.Turtle):
    def __init__(
        self,
        text_color,
        playfield_top,
        high_score_file,
        difficulty_speeds,
        selected_difficulty_getter,
    ):
        super().__init__()
        self.score = 0
        self.text_color = text_color
        self.playfield_top = playfield_top
        self.high_score_file = high_score_file
        self.difficulty_speeds = difficulty_speeds
        self.selected_difficulty_getter = selected_difficulty_getter
        self.high_scores = self.load_high_scores()
        self.color(self.text_color)
        self.penup()
        self.hideturtle()
        self.goto(0, self.playfield_top + 24)
        self.message_turtle = turtle.Turtle()
        self.message_turtle.hideturtle()
        self.message_turtle.color(self.text_color)
        self.message_turtle.penup()
        self.pause_turtle = turtle.Turtle()
        self.pause_turtle.hideturtle()
        self.pause_turtle.color(self.text_color)
        self.pause_turtle.penup()
        self.countdown_turtle = turtle.Turtle()
        self.countdown_turtle.hideturtle()
        self.countdown_turtle.color(self.text_color)
        self.countdown_turtle.penup()
        self.write_score()

    def load_high_scores(self):
        try:
            contents = self.high_score_file.read_text(encoding="utf-8").strip()
        except FileNotFoundError:
            return {difficulty: 0 for difficulty in self.difficulty_speeds}

        default_scores = {difficulty: 0 for difficulty in self.difficulty_speeds}

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
            for difficulty in self.difficulty_speeds
        ]
        self.high_score_file.write_text("\n".join(lines), encoding="utf-8")

    def current_difficulty(self):
        return self.selected_difficulty_getter()

    def current_high_score(self):
        return self.high_scores[self.current_difficulty()]

    def write_score(self):
        self.clear()
        self.write(
            f"Score: {self.score}   {self.current_difficulty()} Best: {self.current_high_score()}",
            align="center",
            font=("Arial", 18, "bold"),
        )

    def increase(self):
        self.score += 1
        if self.score > self.current_high_score():
            self.high_scores[self.current_difficulty()] = self.score
            self.save_high_scores()
        self.write_score()

    def reset(self):
        self.score = 0
        self.goto(0, self.playfield_top + 24)
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

    def hide_score(self):
        self.clear()

    def show_score(self):
        self.write_score()


class Border(turtle.Turtle):
    def __init__(self, border_color, playfield_bounds):
        super().__init__()
        self.playfield_bounds = playfield_bounds
        self.hideturtle()
        self.color(border_color)
        self.pensize(3)
        self.penup()
        self.is_visible = False

    def show_border(self):
        self.clear()
        self.is_visible = True
        self.penup()
        self.goto(self.playfield_bounds["left"], self.playfield_bounds["top"])
        self.pendown()
        for _ in range(2):
            self.forward(
                self.playfield_bounds["right"] - self.playfield_bounds["left"]
            )
            self.right(90)
            self.forward(
                self.playfield_bounds["top"] - self.playfield_bounds["bottom"]
            )
            self.right(90)
        self.penup()

    def hide_border(self):
        self.is_visible = False
        self.clear()


class Button:
    def __init__(
        self,
        text,
        center_x,
        center_y,
        text_color,
        border_color,
        width=180,
        height=50,
        fill_color="#000000",
        hover_color=None,
        selected_fill_color=None,
    ):
        self.text = text
        self.center_x = center_x
        self.center_y = center_y
        self.text_color = text_color
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
        self.box.color(border_color)
        self.box.fillcolor(self.fill_color)
        self.box.pensize(3)
        self.box.hideturtle()

        self.label = turtle.Turtle()
        self.label.penup()
        self.label.hideturtle()
        self.label.color(self.text_color)

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
    def __init__(
        self,
        screen,
        start_button,
        title_color,
        title_shadow_color,
        text_color,
        arrow_color,
        button_glow_colors,
        animation_ms,
    ):
        self.screen = screen
        self.start_button = start_button
        self.title_color = title_color
        self.title_shadow_color = title_shadow_color
        self.text_color = text_color
        self.button_glow_colors = list(button_glow_colors)
        self.animation_ms = animation_ms
        self.is_visible = False
        self.arrow_offset = 0
        self.arrow_direction = 1
        self.button_glow_step = 0

        self.shadow = turtle.Turtle()
        self.shadow.hideturtle()
        self.shadow.color(self.title_shadow_color)
        self.shadow.penup()

        self.title = turtle.Turtle()
        self.title.hideturtle()
        self.title.color(self.title_color)
        self.title.penup()

        self.subtitle = turtle.Turtle()
        self.subtitle.hideturtle()
        self.subtitle.color(self.text_color)
        self.subtitle.penup()

        self.instructions = turtle.Turtle()
        self.instructions.hideturtle()
        self.instructions.color(self.text_color)
        self.instructions.penup()

        self.difficulty_label = turtle.Turtle()
        self.difficulty_label.hideturtle()
        self.difficulty_label.color(self.text_color)
        self.difficulty_label.penup()

        self.arrows = turtle.Turtle()
        self.arrows.hideturtle()
        self.arrows.color(arrow_color)
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
        center_y = 82

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

        self.button_glow_step = (self.button_glow_step + 1) % len(
            self.button_glow_colors
        )
        self.draw_arrow_icons()
        self.start_button.show(
            fill_color=self.button_glow_colors[self.button_glow_step],
        )
        self.screen.update()
        self.screen.ontimer(self.animate, self.animation_ms)

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
        self.shadow.goto(3, 146)
        self.shadow.write(
            "Snake Game",
            align="center",
            font=("Arial", 30, "bold"),
        )
        self.title.goto(0, 150)
        self.title.write(
            "Snake Game",
            align="center",
            font=("Arial", 30, "bold"),
        )
        self.subtitle.goto(0, 100)
        self.subtitle.write(
            "Move with arrow keys or W A S D",
            align="center",
            font=("Arial", 16, "normal"),
        )
        self.instructions.goto(0, 65)
        self.instructions.write(
            "Press P to pause or continue",
            align="center",
            font=("Arial", 16, "normal"),
        )
        self.draw_arrow_icons()
        self.difficulty_label.clear()
        self.difficulty_label.goto(0, 5)
        self.difficulty_label.write(
            "Choose difficulty",
            align="center",
            font=("Arial", 16, "normal"),
        )
        self.screen.ontimer(self.animate, self.animation_ms)

    def hide(self):
        self.is_visible = False
        self.shadow.clear()
        self.title.clear()
        self.subtitle.clear()
        self.instructions.clear()
        self.difficulty_label.clear()
        self.arrows.clear()


class SettingsScreen:
    def __init__(self, title_color, title_shadow_color, text_color):
        self.is_visible = False

        self.shadow = turtle.Turtle()
        self.shadow.hideturtle()
        self.shadow.color(title_shadow_color)
        self.shadow.penup()

        self.title = turtle.Turtle()
        self.title.hideturtle()
        self.title.color(title_color)
        self.title.penup()

        self.subtitle = turtle.Turtle()
        self.subtitle.hideturtle()
        self.subtitle.color(text_color)
        self.subtitle.penup()

        self.section_label = turtle.Turtle()
        self.section_label.hideturtle()
        self.section_label.color(text_color)
        self.section_label.penup()

        self.border_label = turtle.Turtle()
        self.border_label.hideturtle()
        self.border_label.color(text_color)
        self.border_label.penup()

        self.border_hint = turtle.Turtle()
        self.border_hint.hideturtle()
        self.border_hint.color(text_color)
        self.border_hint.penup()

        self.coming_soon = turtle.Turtle()
        self.coming_soon.hideturtle()
        self.coming_soon.color(text_color)
        self.coming_soon.penup()

    def show(self):
        self.is_visible = True
        self.shadow.clear()
        self.title.clear()
        self.subtitle.clear()
        self.section_label.clear()
        self.border_label.clear()
        self.border_hint.clear()
        self.coming_soon.clear()

        self.shadow.goto(3, 116)
        self.shadow.write(
            "Settings",
            align="center",
            font=("Arial", 28, "bold"),
        )
        self.title.goto(0, 120)
        self.title.write(
            "Settings",
            align="center",
            font=("Arial", 28, "bold"),
        )
        self.subtitle.goto(0, 78)
        self.subtitle.write(
            "Customize your snake",
            align="center",
            font=("Arial", 15, "normal"),
        )
        self.section_label.goto(0, 38)
        self.section_label.write(
            "Choose snake color",
            align="center",
            font=("Arial", 18, "bold"),
        )
        self.border_label.goto(0, -112)
        self.border_label.write(
            "Walls",
            align="center",
            font=("Arial", 18, "bold"),
        )
        self.border_hint.goto(0, -140)
        self.border_hint.write(
            "Off lets you wrap around the screen",
            align="center",
            font=("Arial", 13, "normal"),
        )
        

    def hide(self):
        self.is_visible = False
        self.shadow.clear()
        self.title.clear()
        self.subtitle.clear()
        self.section_label.clear()
        self.border_label.clear()
        self.border_hint.clear()
        self.coming_soon.clear()
