import random
import turtle


class Snake:
    def __init__(self, color, move_distance, starting_positions, playfield_bounds):
        self.color = color
        self.move_distance = move_distance
        self.starting_positions = list(starting_positions)
        self.playfield_bounds = playfield_bounds
        self.segments = []
        self.direction = "Right"
        self.create_snake()

    def create_snake(self):
        for position in self.starting_positions:
            self.add_segment(position)

    def add_segment(self, position):
        segment = turtle.Turtle("square")
        segment.color(self.color)
        segment.penup()
        segment.goto(position)
        self.segments.append(segment)

    def set_color(self, color):
        self.color = color
        for segment in self.segments:
            segment.color(color)

    def extend(self):
        self.add_segment(self.segments[-1].position())

    def move(self):
        for index in range(len(self.segments) - 1, 0, -1):
            x = self.segments[index - 1].xcor()
            y = self.segments[index - 1].ycor()
            self.segments[index].goto(x, y)

        head = self.segments[0]
        if self.direction == "Up":
            head.sety(head.ycor() + self.move_distance)
        elif self.direction == "Down":
            head.sety(head.ycor() - self.move_distance)
        elif self.direction == "Left":
            head.setx(head.xcor() - self.move_distance)
        elif self.direction == "Right":
            head.setx(head.xcor() + self.move_distance)

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
            head.xcor() > self.playfield_bounds["right"]
            or head.xcor() < self.playfield_bounds["left"]
            or head.ycor() > self.playfield_bounds["top"]
            or head.ycor() < self.playfield_bounds["bottom"]
        )

    def wrap_head(self):
        head = self.segments[0]

        if head.xcor() > self.playfield_bounds["right"]:
            head.setx(self.playfield_bounds["left"])
        elif head.xcor() < self.playfield_bounds["left"]:
            head.setx(self.playfield_bounds["right"])

        if head.ycor() > self.playfield_bounds["top"]:
            head.sety(self.playfield_bounds["bottom"])
        elif head.ycor() < self.playfield_bounds["bottom"]:
            head.sety(self.playfield_bounds["top"])

    def hit_tail(self):
        head = self.segments[0]
        for segment in self.segments[1:]:
            if head.distance(segment) < 10:
                return True
        return False

    def occupied_positions(self):
        return {
            (int(segment.xcor()), int(segment.ycor()))
            for segment in self.segments
        }

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
    def __init__(self, playfield_bounds, move_distance, food_colors):
        super().__init__("circle")
        self.playfield_bounds = playfield_bounds
        self.move_distance = move_distance
        self.food_colors = list(food_colors)
        self.color("red")
        self.penup()
        self.shapesize(0.8, 0.8)
        self.speed("fastest")
        self.refresh()

    def refresh(self, occupied_positions=None):
        occupied_positions = occupied_positions or set()
        min_x = int(self.playfield_bounds["left"] // self.move_distance) + 1
        max_x = int(self.playfield_bounds["right"] // self.move_distance) - 1
        min_y = int(self.playfield_bounds["bottom"] // self.move_distance) + 1
        max_y = int(self.playfield_bounds["top"] // self.move_distance) - 1

        while True:
            x = random.randint(min_x, max_x) * self.move_distance
            y = random.randint(min_y, max_y) * self.move_distance
            if (x, y) not in occupied_positions:
                break

        self.color(random.choice(self.food_colors))
        self.goto(x, y)

    def hide_food(self):
        self.hideturtle()

    def show_food(self):
        self.showturtle()
