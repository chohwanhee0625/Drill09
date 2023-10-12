# 이것은 각 상태들을 객체로 구현한 것임.
import math

from pico2d import load_image


class Idle:

    @staticmethod
    def enter(boy):
        boy.frame = 0  # 시작할 때 frame을 0으로 만들어줌
        print('Idle Enter')

    @staticmethod
    def exit():
        print('Idle Exit')

    @staticmethod
    def do(boy):  # boy의 애니메이션을 만들어줌
        boy.frame = (boy.frame + 1) % 8
        print('Idle Do')

    @staticmethod
    def draw(boy):  # boy를 그려줌
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)
        pass


class Sleep:

    @staticmethod
    def enter(boy):
        boy.frame = 0  # 시작할 때 frame을 0으로 만들어줌
        print('head down')

    @staticmethod
    def exit():
        print('head up')

    @staticmethod
    def do(boy):  # boy의 애니메이션을 만들어줌
        boy.frame = (boy.frame + 1) % 8
        print('zzzz')

    @staticmethod
    def draw(boy):  # boy를 그려줌
        boy.image.clip_composite_draw(boy.frame * 100, boy.action * 100, 100, 100,
                                      math.pi / 2, '', boy.x - 25, boy.y - 25, 100, 100)
        pass


class StateMachine:
    def __init__(self, boy):
        self.cur_state = Sleep
        self.boy = boy

    def start(self):
        self.cur_state.enter(self.boy)

    def update(self):
        self.cur_state.do(self.boy)

    def draw(self):
        self.cur_state.draw(self.boy)


class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.action = 3
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        pass

    def draw(self):
        self.state_machine.draw()
