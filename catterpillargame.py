import turtle as t
import random as rd

t.bgcolor('black')

caterpillar = t.Turtle()
caterpillar.shape('classic')
caterpillar.color('brown')
caterpillar.fillcolor('green')
caterpillar.speed(100)
#caterpillar.pendown() -> pendown() is the default state of turtle. It will ensure the turtle draws when it’s moving with your commands such as forward() or setpos().

caterpillar.penup()  #will lift the turtle off the “digital canvas” and if you move the turtle in penup state it won’t draw.

caterpillar.hideturtle()   #It's a good idea to do this while you're in the middle of a complicated drawing, because hiding the turtle speeds up the drawing observably.

leaf = t.Turtle()
leaf_shape = ((0,0),(20,6),(24,10),(26,24),(12,22),(8,12))
t.register_shape('leaf',leaf_shape)
leaf.shape('leaf')
leaf.color('green')
leaf.penup()
leaf.hideturtle()   #to hide leaf before starting the game
leaf.speed()

ob1 = t.Turtle()
ob1.shape("square")
ob1.speed(0)
ob1.color("red")
ob1.penup()
ob1.hideturtle()
ob1.goto(0, 100)
ob1.shapesize(stretch_wid=1, stretch_len=1)

ob2 = t.Turtle()
ob2.shape("square")
ob2.speed(0)
ob2.color("red")
ob2.penup()
ob2.hideturtle()
ob2.goto(0, 1000)
ob2.shapesize(stretch_wid=1, stretch_len=1)

ob3 = t.Turtle()
ob3.shape("square")
ob3.speed(0)
ob3.color("red")
ob3.penup()
ob3.hideturtle()
ob3.goto(0, 1500)
ob3.shapesize(stretch_wid=1, stretch_len=1)

ob4 = t.Turtle()
ob4.shape("square")
ob4.speed(0)
ob4.color("red")
ob4.penup()
ob4.hideturtle()
ob4.goto(0, 1100)
ob4.shapesize(stretch_wid=1, stretch_len=1)

ob5 = t.Turtle()
ob5.shape("square")
ob5.speed(0)
ob5.color("red")
ob5.penup()
ob5.hideturtle()
ob5.goto(0, 400)
ob5.shapesize(stretch_wid=1, stretch_len=1)



game_started = False
text_turtle = t.Turtle()
text_turtle.color('white')
text_turtle.write('Press SPACE to start',align='center',font=('Arial',16,'bold'))
text_turtle.hideturtle()

score_turtle = t.Turtle()
score_turtle.color('white')
score_turtle.hideturtle()
score_turtle.speed(0)

def outside_window():
    left_wall = -t.window_width()/2  #means restricted area for turtle
    right_wall = t.window_width()/2
    top_wall = t.window_height()/2
    bottom_wall = -t.window_height()/2
    (x,y) = caterpillar.pos()   #Return the turtle's current location (x,y), as a Vec2D-vector.
    outside = x < left_wall or  x > right_wall or  y < bottom_wall or y > top_wall
    return outside

def game_over():
    caterpillar.color('purple')
    # leaf.color('yellow')
    t.penup()
    t.hideturtle()
    t.write('GAME OVER!',align='center' , font=('Aerial',30,'normal'))

def display_score(current_score):
    score_turtle.clear()
    score_turtle.penup()
    x = (t.window_width() / 2)-50
    y = (t.window_height() / 2)-50
    score_turtle.setpos(x,y)
    score_turtle.write(str(current_score) , align = 'center',font=('Arial',30,'bold'))

def place_leaf():
    leaf.hideturtle()
    leaf.setx(rd.randint(-200,200))
    leaf.sety(rd.randint(-200,200))
    leaf.showturtle()

def place_obstacle():
    ob1.hideturtle()
    ob1.setx(rd.randint(-200,200))
    ob1.sety(rd.randint(-200,200))
    ob1.showturtle()

    ob2.hideturtle()
    ob2.setx(rd.randint(-200,200))
    ob2.sety(rd.randint(-200,200))
    ob2.showturtle()

    ob3.hideturtle()
    ob3.setx(rd.randint(-200,200))
    ob3.sety(rd.randint(-200,200))
    ob3.showturtle()

    ob4.hideturtle()
    ob4.setx(rd.randint(-200,400))
    ob4.sety(rd.randint(-200,200))
    ob4.showturtle()

    ob5.hideturtle()
    ob5.setx(rd.randint(-200,200))
    ob5.sety(rd.randint(-200,200))
    ob5.showturtle()

def start_game():    # start frrom here
    global game_started
    if game_started:
        return
    game_started = True

    score = 0
    text_turtle.clear()

    caterpillar_speed = 2
    caterpillar_length = 3
    caterpillar.shapesize(1,caterpillar_length,5) # Stretch length  , Stretch width  ,Outline width
    caterpillar.showturtle()
    display_score(score)
    place_leaf()
    place_obstacle()

    while True:
        caterpillar.forward(caterpillar_speed)  #(caterpillar moving with  speed  2 )
        if caterpillar.distance(leaf)<20:
            place_leaf()
            caterpillar_length = caterpillar_length + 1
            caterpillar.shapesize(1,caterpillar_length,1)
            caterpillar_speed = caterpillar_speed + 1
            score = score + 10
            display_score(score)
        if caterpillar.distance(ob1) < 20 :
            game_over()
            break
        if caterpillar.distance(ob2) < 20 :
            game_over()
            break
        if caterpillar.distance(ob3) < 20 :
            game_over()
            break
        if caterpillar.distance(ob4) < 20 :
            game_over()
            break
        if caterpillar.distance(ob5) < 20 :
            game_over()
            break
        if outside_window():
            game_over()
            break

def move_up():
    if caterpillar.heading() == 0 or caterpillar.heading() == 180:
        caterpillar.setheading(90)

def move_down():
    if caterpillar.heading() == 0 or caterpillar.heading() == 180:
        caterpillar.setheading(270)

def move_left():
    if caterpillar.heading() == 90 or caterpillar.heading() == 270:
        caterpillar.setheading(180)

def move_right():
    if caterpillar.heading() == 90 or caterpillar.heading() == 270:
        caterpillar.setheading(0)

t.onkey(start_game,'space')   #This function is used to bind fun to the key-release event of the key. In order to be able to register key-events, TurtleScreen must have focus.
t.onkey(move_up,'Up')
t.onkey(move_right,'Right')
t.onkey(move_down,'Down')
t.onkey(move_left,'Left')
t.listen()  #listen() listens for overall the entire turtle module's inputs, whilst screen. listen() listens for screen / window inputs
t.mainloop()   #•	t.mainloop() tells the window to wait for the user to do something