from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint


class PongPaddle(Widget):
    score = NumericProperty(0)
    orientation = ObjectProperty([0, 0])
    can_move = ObjectProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            if self.orientation[0] == 25:                
                offset = (ball.center_y - self.center_y) / (self.height / 2)
                bounced = Vector(-1 * vx, vy)
                vel = bounced * 1.1
                ball.velocity = vel.x, vel.y + offset
            else:
                offset = (ball.center_x - self.center_x) / (self.width / 2)
                bounced = Vector(vx, -1 * vy)
                vel = bounced * 1.1
                ball.velocity = vel.x + offset, vel.y


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    player3 = ObjectProperty(None)
    player4 = ObjectProperty(None)

    def initialize(self):
        SCORE = 1
        self.player1.orientation = [25, 200]
        self.player2.orientation = [25, 200]
        self.player3.orientation = [200, 25]
        self.player4.orientation = [200, 25]
        self.player1.score = SCORE
        self.player2.score = SCORE
        self.player3.score = SCORE
        self.player4.score = SCORE
        self.player1.can_move = 1
        self.player2.can_move = 1
        self.player3.can_move = 1
        self.player4.can_move = 1
        self.serve_ball()

    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        self.ball.move()

        #bounce of paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)
        self.player3.bounce_ball(self.ball)
        self.player4.bounce_ball(self.ball)

        #bounce ball off bottom or top
        if ((self.ball.y < self.y) and not self.player3.can_move) \
           or ((self.ball.top > self.top) and not self.player4.can_move):
            self.ball.velocity_y *= -1
        if ((self.ball.x < self.x) and not self.player1.can_move) \
           or ((self.ball.right > self.width) and not self.player2.can_move):
            self.ball.velocity_x *= -1

        #went off to a side to score point?
        if self.ball.x < self.x and self.player1.can_move == 1:
            self.player1.score -= 1
            self.serve_ball(vel=(4, randint(1, 4)))
            if self.player1.score <= 0:
                self.player1.can_move = 0
        elif self.ball.x > self.width and self.player2.can_move == 1:
            self.player2.score -= 1
            self.serve_ball(vel=(-4, randint(1, 4)))
            if self.player2.score <= 0:
                self.player2.can_move = 0
        elif self.ball.y > self.height and self.player4.can_move == 1:
            self.player4.score -= 1
            self.serve_ball(vel = (randint(1, 4), -4))
            if self.player4.score <= 0:
                self.player4.can_move = 0
        elif self.ball.y < self.y and self.player3.can_move == 1:
            self.player3.score -= 1
            self.serve_ball(vel = (randint(1, 4), 4))
            if self.player3.score <= 0:
                self.player3.can_move = 0

        if self.player1.can_move + self.player2.can_move + \
           self.player3.can_move + self.player4.can_move == 1:
            self.ball.velocity = (0, 0)
            Clock.unschedule(self.update)

            self.win_label = Label(size_hint=(None, None),
                              text='[ref=winner]Winner![/ref]',
                              markup=True, font_size=70, color=[1,0,0,1])
            #win_label.texture_update()
            #self.win_label.pos = (self.width / 2, self.height / 2 - 70)
            self.win_label.center = self.center
##            win_label.size =  win_label.texture_size[0] + 20, \
##                             win_label.texture_size[1] + 20
            self.win_label.bind(on_ref_press=self.click_win_label)
            self.win_label.texture_update()
            self.add_widget(self.win_label)


    def click_win_label(self, instance, value):
        self.remove_widget(self.win_label)
        #self.remove_widget(instance) # this should also work:
        self.initialize()
        Clock.schedule_interval(self.update, 1.0 / 60.0)



    def on_touch_move(self, touch):
        if touch.x < self.width / 3 and touch.y > self.height / 6 \
            and touch.y < 5 * self.height / 6 and self.player1.can_move:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3 and touch.y > self.height / 6 \
            and touch.y < 5 * self.height / 6 and self.player2.can_move:
            self.player2.center_y = touch.y
        if touch.y < self.height / 3 and touch.x > self.width / 6 \
            and touch.x < 5 * self.width / 6 and self.player3.can_move:
            self.player3.center_x = touch.x
        if touch.y > 2* self.height / 3 and touch.x > self.width / 6 \
            and touch.x < 5 * self.width / 6 and self.player4.can_move:
            self.player4.center_x = touch.x


class PongApp(App):
    def build(self):
        game = PongGame()
        game.initialize()
        #game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game

if __name__ == '__main__':
    PongApp().run()