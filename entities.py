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
        self.head_shape_name = None
        self.create_snake()
        self.update_head_shape()
        self.update_head_orientation()

    def create_snake(self):
        for position in self.starting_positions:
            self.add_segment(position)

    def add_segment(self, position):
        segment = turtle.Turtle("square")
        segment.color(self.color)
        segment.penup()
        segment.goto(position)
        self.segments.append(segment)

    def build_head_shape(self):
        shape = turtle.Shape("compound")
        body = ((-10, -10), (10, -10), (10, 10), (-10, 10))
        top_eye = ((2, 2), (8, 2), (8, 8), (2, 8))
        bottom_eye = ((2, -8), (8, -8), (8, -2), (2, -2))
        top_pupil = ((5, 4), (8, 4), (8, 7), (5, 7))
        bottom_pupil = ((5, -7), (8, -7), (8, -4), (5, -4))
        shape.addcomponent(body, self.color)
        shape.addcomponent(top_eye, "#F4EFE2")
        shape.addcomponent(bottom_eye, "#F4EFE2")
        shape.addcomponent(top_pupil, "#111315")
        shape.addcomponent(bottom_pupil, "#111315")
        return shape

    def update_head_shape(self):
        screen = self.segments[0].getscreen()
        self.head_shape_name = f"snake_head_{self.color.replace('#', '')}"
        screen.register_shape(self.head_shape_name, self.build_head_shape())
        self.segments[0].shape(self.head_shape_name)
        for segment in self.segments[1:]:
            segment.color(self.color)

    def update_head_orientation(self):
        headings = {
            "Up": 90,
            "Down": 270,
            "Left": 180,
            "Right": 0,
        }
        self.segments[0].setheading(headings[self.direction])

    def set_color(self, color):
        self.color = color
        self.update_head_shape()

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
        self.update_head_orientation()

    def up(self):
        if self.direction != "Down":
            self.direction = "Up"
            self.update_head_orientation()

    def down(self):
        if self.direction != "Up":
            self.direction = "Down"
            self.update_head_orientation()

    def left(self):
        if self.direction != "Right":
            self.direction = "Left"
            self.update_head_orientation()

    def right(self):
        if self.direction != "Left":
            self.direction = "Right"
            self.update_head_orientation()

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
        self.update_head_shape()
        self.update_head_orientation()

    def hide(self):
        for segment in self.segments:
            segment.hideturtle()

    def show(self):
        for segment in self.segments:
            segment.showturtle()
        self.update_head_orientation()


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
