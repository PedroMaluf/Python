import turtle


window = turtle.Screen()
window.title('PONG')
window.bgcolor('black')
window.setup(width=800, height=600)
window.tracer(0)

pen = turtle.Turtle()
pen.speed(0)
pen.color('white')
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write('Blue player: 0  Red player: 0', align = 'center', font = ('Courier', 24, 'normal'))

raquet_a = turtle.Turtle()
raquet_a.speed(0)
raquet_a.shape('square')
raquet_a.color('blue')
raquet_a.shapesize(stretch_wid=5, stretch_len=1)
raquet_a.penup()
raquet_a.goto(-350, 0)

raquet_b = turtle.Turtle()
raquet_b.speed(0)
raquet_b.shape('square')
raquet_b.color('red')
raquet_b.shapesize(stretch_wid=5, stretch_len=1)
raquet_b.penup()
raquet_b.goto(350, 0)

bola = turtle.Turtle()
bola.speed(0)
bola.shape('square')
bola.color('white')
bola.penup()
bola.goto(0, 0)
bola.dx = 0.2
bola.dy = 0.2

def move_a_up():
    y = raquet_a.ycor()
    if y == 240:
        raquet_a.sety(y)
    else:
        raquet_a.sety(y + 20)

def move_a_dw():
    y = raquet_a.ycor()
    if y == -240:
        raquet_a.sety(y)
    else:
        raquet_a.sety(y - 20)

def move_b_up():
    y = raquet_b.ycor()
    if y == 240:
        raquet_b.sety(y)
    else:
        raquet_b.sety(y + 20)

def move_b_dw():
    y = raquet_b.ycor()
    y = raquet_b.ycor()
    if y == -240:
        raquet_b.sety(y)
    else:
        raquet_b.sety(y - 20)

window.listen()
window.onkeypress(move_a_up,'w')
window.onkeypress(move_a_dw,'s')
window.onkeypress(move_b_up,'Up')
window.onkeypress(move_b_dw,'Down')

pontos_a = 0
pontos_b = 0

while True:
    window.update()

    if bola.ycor() >= 280:
        bola.sety(280)
        bola.dy = -bola.dy

    if bola.ycor() <= -280:
        bola.sety(-280)
        bola.dy = -bola.dy

    if bola.xcor() >= 330 and bola.xcor() < 350 and bola.ycor() <= raquet_b.ycor() + 50 and bola.ycor() >= raquet_b.ycor() - 50:
        bola.setx(330)
        bola.dx = -bola.dx

    if bola.xcor() <= -330 and bola.xcor() > -350 and bola.ycor() <= raquet_a.ycor() + 50 and bola.ycor() >= raquet_a.ycor() - 50:
        bola.setx(-330)
        bola.dx = -bola.dx

    if bola.xcor() >= 390:
        bola.goto(0, 0)
        bola.dx = -bola.dx
        pontos_a += 1
        pen.clear()
        pen.write('Blue player: {}  Red player: {}'.format(pontos_a, pontos_b), align = 'center', font = ('Courier', 24, 'normal'))

    if bola.xcor() <= -390:
        bola.goto(0, 0)
        bola.dx = -bola.dx
        pontos_b += 1
        pen.clear()
        pen.write('Blue player: {}  Red player: {}'.format(pontos_a, pontos_b), align = 'center', font = ('Courier', 24, 'normal'))

    bola.setx(bola.xcor() + bola.dx)
    bola.sety(bola.ycor() + bola.dy)
