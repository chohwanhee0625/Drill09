# 이것은 각 상태들을 객체로 구현한 것임.
import math

from pico2d import load_image, get_time
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDL_KEYUP, SDLK_RIGHT, SDLK_LEFT


def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


def time_out(e):
    return e[0] == 'TIME_OUT'


def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


class Idle:

    @staticmethod
    def enter(boy, e):
        boy.frame = 0  # 시작할 때 frame을 0으로 만들어줌
        boy.wait_time = get_time()
        if boy.action == 0:
            boy.action = 2
        elif boy.action == 1:
            boy.action = 3
        print('Idle Enter')

    @staticmethod
    def exit(boy, e):
        print('Idle Exit')

    @staticmethod
    def do(boy):  # boy의 애니메이션을 만들어줌
        boy.frame = (boy.frame + 1) % 8
        if get_time() - boy.wait_time > 3.0:
            boy.state_machine.handle_event('TIME_OUT', 0)
        print('Idle Do')

    @staticmethod
    def draw(boy):  # boy를 그려줌
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)
        pass


class Sleep:

    @staticmethod
    def enter(boy, e):
        boy.frame = 0  # 시작할 때 frame을 0으로 만들어줌
        print('head down')

    @staticmethod
    def exit(boy, e):
        print('head up')
        pass

    @staticmethod
    def do(boy):  # boy의 애니메이션을 만들어줌
        boy.frame = (boy.frame + 1) % 8
        print('zzzz')

    @staticmethod
    def draw(boy):  # boy를 그려줌
        if boy.action == 2:
            boy.image.clip_composite_draw(boy.frame * 100, boy.action * 100, 100, 100,
                                          -math.pi / 2, '', boy.x - 25, boy.y - 25, 100, 100)
        else:
            boy.image.clip_composite_draw(boy.frame * 100, boy.action * 100, 100, 100,
                                          math.pi / 2, '', boy.x - 25, boy.y - 25, 100, 100)


class Run:

    @staticmethod
    def enter(boy, e):
        boy.frame = 0  # 시작할 때 frame을 0으로 만들어줌
        if right_down(e) or left_up(e):
            boy.action, boy.dir = 1, 1
        elif left_down(e) or right_up(e):
            boy.action, boy.dir = 0, -1
        print('Run enter')

    @staticmethod
    def exit(boy, e):
        print('Run exit')

    @staticmethod
    def do(boy):  # boy의 애니메이션을 만들어줌
        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.dir*5
        print('Run do')

    @staticmethod
    def draw(boy):  # boy를 그려줌
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)
        pass


class StateMachine:
    def __init__(self, boy):
        self.cur_state = Idle
        self.boy = boy
        self.table = {  # dictionary 이용
            Sleep: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, space_down: Idle},
            Idle: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, time_out: Sleep},
            Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle}
        }

    def start(self):
        self.cur_state.enter(self.boy, ('START', 0))

    def update(self):
        self.cur_state.do(self.boy)

    def draw(self):
        self.cur_state.draw(self.boy)

    def handle_event(self, e):  # state event
        for check_event, next_state, in self.table[self.cur_state].items():
            # table[Sleep].items() -> space_down(), IDLE
            if check_event(e):
                self.cur_state.exit(self.boy, e)  # 상태 변환 전 exit action
                self.cur_state = next_state
                self.cur_state.enter(self.boy, e)  # 상태 변환 후 enter action
                return True  # 성공적으로 event 변환

        return False  # 이벤트 처리를 소모하지 못함


class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.action = 3
        self.dir = 0
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):  # 튜플을 이용해 pico2d 용 event를 state_machine용 event로 변환
        self.state_machine.handle_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()
