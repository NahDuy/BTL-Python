import pygame
import random
import os
import sys


# Lớp định nghĩa cấu hình
class Config():
    def __init__(self):
        # FPS
        self.FPS = 60
        # Kích thước màn hình
        self.SCREENSIZE = (580, 380)
        # Tiêu đề
        self.TITLE = 'Maze Game'
        # Kích thước khối
        self.BLOCKSIZE = 15
        self.MAZESIZE = (20, 35)  # Số hàng * Số cột
        #Căn chỉnh mê cung luôn luôn ở giữa
        self.BORDERSIZE = (
            (self.SCREENSIZE[0] - self.MAZESIZE[1] * self.BLOCKSIZE) // 2,
            (self.SCREENSIZE[1] - self.MAZESIZE[0] * self.BLOCKSIZE) // 2
        )
        # Đường dẫn đến âm nhạc nền
        self.BGM_PATH = os.path.join('Music/bgm.mp3')
        # Đường dẫn đến hình ảnh trong trò chơi
        self.IMAGE_PATHS_DICT = {
            'hero': os.path.join('Image/hero.png'),
        }
        
# Hàm hiển thị văn bản lên màn hình
def showText(screen, font, text, color, position):
    #Tạo 1 văn bản với các thuộc tính
    text_surface = font.render(text, True, color)
    #Vẽ lên màn hình
    screen.blit(text_surface, position)

# Lớp định nghĩa khối trong mê cung
class Block(pygame.sprite.Sprite):
    def __init__(self, coordinate, size, border_size):
        super().__init__()
        #Lưu trữ tọa độ (x,y)
        self.coordinate = coordinate 
        self.size = size
        self.border_size = border_size
        #Đại diện cho các hướng có tường    
        self.has_walls = [True, True, True, True]  # [top, bottom, left, right]
        self.is_visited = False

    def draw(self, screen):
        x, y = self.coordinate
        left = self.border_size[0] + x * self.size #Chiều Ngang
        top = self.border_size[1] + y * self.size #Chiều Dọc
        #TOP
        if self.has_walls[0]:
            pygame.draw.line(screen, (0, 0, 0), (left, top), (left + self.size, top), 1)
        #BOTTOM
        if self.has_walls[1]:
            pygame.draw.line(screen, (0, 0, 0), (left, top + self.size), (left + self.size, top + self.size), 1)
        #LEFT
        if self.has_walls[2]:
            pygame.draw.line(screen, (0, 0, 0), (left, top), (left, top + self.size), 1)
        #RIGHT
        if self.has_walls[3]:
            pygame.draw.line(screen, (0, 0, 0), (left + self.size, top), (left + self.size, top + self.size), 1)

# Lớp định nghĩa mê cung ngẫu nhiên
class RandomMaze():
    def __init__(self, maze_size, block_size, border_size):
        self.block_size = block_size
        self.border_size = border_size #(Ngang,Dọc)
        self.maze_size = maze_size #Lưu kích thước của mê cung (số hàng và số cột)
        self.blocks_list = self.createMaze(maze_size, block_size, border_size) #Khởi tạo danh sách các khối trong mê cung
        self.font = pygame.font.SysFont('Consolas', 15)

    def draw(self, screen):
        for row in range(self.maze_size[0]):
            for col in range(self.maze_size[1]):
                self.blocks_list[row][col].draw(screen)
        # Đánh dấu điểm bắt đầu và điểm đích
        showText(screen, self.font, 'S', (255, 0, 0), (self.border_size[0] - 10, self.border_size[1]))
        showText(screen, self.font, 'D', (255, 0, 0),
                 (self.border_size[0] + (self.maze_size[1] - 1) * self.block_size,
                  self.border_size[1] + self.maze_size[0] * self.block_size + 5))

    @staticmethod
    #Tạo mê cung ngẫu nhiên
    def createMaze(maze_size, block_size, border_size):
        def nextBlock(block_now, blocks_list):
            directions = ['top', 'bottom', 'left', 'right']
            blocks_around = dict(zip(directions, [None] * 4))
            block_next = None
            count = 0
            # Kiểm tra khối phía trên
            if block_now.coordinate[1] - 1 >= 0:
                block_now_top = blocks_list[block_now.coordinate[1] - 1][block_now.coordinate[0]]
                if not block_now_top.is_visited:
                    blocks_around['top'] = block_now_top
                    count += 1
            # Kiểm tra khối phía dưới
            if block_now.coordinate[1] + 1 < maze_size[0]:
                block_now_bottom = blocks_list[block_now.coordinate[1] + 1][block_now.coordinate[0]]
                if not block_now_bottom.is_visited:
                    blocks_around['bottom'] = block_now_bottom
                    count += 1
            # Kiểm tra khối bên trái
            if block_now.coordinate[0] - 1 >= 0:
                block_now_left = blocks_list[block_now.coordinate[1]][block_now.coordinate[0] - 1]
                if not block_now_left.is_visited:
                    blocks_around['left'] = block_now_left
                    count += 1
            # Kiểm tra khối bên phải
            if block_now.coordinate[0] + 1 < maze_size[1]:
                block_now_right = blocks_list[block_now.coordinate[1]][block_now.coordinate[0] + 1]
                if not block_now_right.is_visited:
                    blocks_around['right'] = block_now_right
                    count += 1
            if count > 0:
                while True:
                    direction = random.choice(directions)
                    if blocks_around.get(direction):
                        block_next = blocks_around.get(direction)
                        if direction == 'top':
                            block_next.has_walls[1] = False
                            block_now.has_walls[0] = False
                        elif direction == 'bottom':
                            block_next.has_walls[0] = False
                            block_now.has_walls[1] = False
                        elif direction == 'left':
                            block_next.has_walls[3] = False
                            block_now.has_walls[2] = False
                        elif direction == 'right':
                            block_next.has_walls[2] = False
                            block_now.has_walls[3] = False
                        break
            return block_next

        blocks_list = [[Block([col, row], block_size, border_size) for col in range(maze_size[1])] for row in
                       range(maze_size[0])]
        block_now = blocks_list[0][0]
        records = []
        while True:
            if block_now:
                if not block_now.is_visited:
                    block_now.is_visited = True
                    records.append(block_now)
                block_now = nextBlock(block_now, blocks_list)
            else:
                block_now = records.pop()
                if len(records) == 0:
                    break
        return blocks_list

# Lớp định nghĩa nhân vật hero
class Hero(pygame.sprite.Sprite):
    def __init__(self, imagepath, coordinate, block_size, border_size, **kwargs):
        super().__init__()
        self.image = pygame.image.load("Image/hero.png")
        self.image = pygame.transform.scale(self.image, (block_size, block_size))
        self.rect = self.image.get_rect()
        #Tạo ra tọa độ của hero
        self.rect.left, self.rect.top = coordinate[0] * block_size + border_size[0], coordinate[1] * block_size + border_size[1]
        self.coordinate = coordinate
        self.block_size = block_size
        self.border_size = border_size

    def move(self, direction, maze):
        #Lưu thông tin mê cung từ hàm RandomMaze
        blocks_list = maze.blocks_list
        #Kiểm tra tường có bị chặn không nếu có trả về False
        if direction == 'up':
            if blocks_list[self.coordinate[1]][self.coordinate[0]].has_walls[0]:
                return False
            else:
                self.coordinate[1] = self.coordinate[1] - 1
                return True
        elif direction == 'down':
            if blocks_list[self.coordinate[1]][self.coordinate[0]].has_walls[1]:
                return False
            else:
                self.coordinate[1] = self.coordinate[1] + 1
                return True
        elif direction == 'left':
            if blocks_list[self.coordinate[1]][self.coordinate[0]].has_walls[2]:
                return False
            else:
                self.coordinate[0] = self.coordinate[0] - 1
                return True
        elif direction == 'right':
            if blocks_list[self.coordinate[1]][self.coordinate[0]].has_walls[3]:
                return False
            else:
                self.coordinate[0] = self.coordinate[0] + 1
                return True
        else:
            raise ValueError('Hướng không được hỗ trợ trong Hero.move...')

    def draw(self, screen):
        self.rect.left, self.rect.top = self.coordinate[0] * self.block_size + self.border_size[0], self.coordinate[1] * self.block_size + self.border_size[1]
        screen.blit(self.image, self.rect)

class MenuScreen:
    def __init__(self, screen_width, screen_height):
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.background = pygame.image.load('Image/bgr.png')
        self.background = pygame.transform.scale(self.background, (screen_width, screen_height))
        self.active = True

    def draw(self):
        if self.active:
            self.screen.blit(self.background, (0, 0))
            pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "play"
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.QUIT:  # Xử lý sự kiện đóng cửa sổ
                pygame.quit()
                sys.exit()
        return None

#

class WaitScreen:
    def __init__(self, screen_width, screen_height):
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.background = pygame.image.load('Image/bgrp2.png')
        self.background = pygame.transform.scale(self.background, (screen_width, screen_height))
        self.active = False
        self.font = pygame.font.SysFont('Consolas', 30)
        self.selected_option = 0  # 0 là tiếp tục, 1 là dừng lại

    def draw(self):
        if self.active:
            self.screen.blit(self.background, (0, 0))
            # Hiển thị nút lựa chọn
            continue_text = "Press J to Continue" if self.selected_option == 0 else "Press J to Continue"
            stop_text = "Press K to Menu" if self.selected_option == 1 else "Press K to Menu"
            #showText(self.screen, self.font, continue_text, (255, 0, 0), (100, 200))
            #showText(self.screen, self.font, stop_text, (255, 0, 0), (100, 250))
            pygame.display.flip()

    
    def handle_events(self):
        if self.active:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_j:
                        return "continue"  # Trả về "continue" khi ấn "J"
                    elif event.key == pygame.K_k:
                        return "stop"  # Trả về "stop" khi ấn "K"
        return None





# Lớp chính để chạy trò chơi
class MazeGame():
    def __init__(self):
        pygame.init()
        self.cfg = Config()
        self.screen = pygame.display.set_mode(self.cfg.SCREENSIZE)
        pygame.display.set_caption(self.cfg.TITLE)
        self.resource_loader = self.load_resources()
        self.finished_level = False
        self.wait_screen = WaitScreen(self.cfg.SCREENSIZE[0], self.cfg.SCREENSIZE[1])  # Thêm dòng này
        self.num_steps = 0
    #Đảm bảo các tài nguyên luôn được tải liên tục 
    def load_resources(self):
        resource_loader = ResourceLoader()
        resource_loader.load_image('hero', self.cfg.IMAGE_PATHS_DICT['hero'])
        resource_loader.load_bgm(self.cfg.BGM_PATH)
        return resource_loader

    def run(self):
        clock = pygame.time.Clock()
        font = pygame.font.SysFont('Consolas', 15)
        self.resource_loader.play_bgm()
        num_levels = 0
        best_scores = 'None'
        game_state = "menu"  # Bắt đầu với trạng thái "menu"
        self.num_steps = 0  # Di chuyển biến num_steps ra khỏi vòng lặp

        # Tạo màn hình menu ở ngoài vòng lặp
        menu = MenuScreen(self.cfg.SCREENSIZE[0], self.cfg.SCREENSIZE[1])
        menu.draw()
        pygame.display.flip()

        # Tạo màn hình game một lần duy nhất
        screen = pygame.display.set_mode(self.cfg.SCREENSIZE)

        while num_levels < 3:
            if game_state == "menu":
                menu.draw()
                pygame.display.flip()

                action = menu.handle_events()
                if action == "play":
                    game_state = "playing"  # Chuyển sang trạng thái "playing"
                    num_steps = 0  # Đặt lại số bước đi khi chơi màn mới
                    

            elif game_state == "playing":
                num_levels += 1
                maze_now = RandomMaze(self.cfg.MAZESIZE, self.cfg.BLOCKSIZE, self.cfg.BORDERSIZE)
                hero_now = Hero(self.resource_loader.images['hero'], [0, 0], self.cfg.BLOCKSIZE, self.cfg.BORDERSIZE)

                while True:
                    dt = clock.tick(self.cfg.FPS)
                    screen.fill((255, 255, 255))
                    is_move = False

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            return
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_UP:
                                is_move = hero_now.move('up', maze_now)
                            elif event.key == pygame.K_DOWN:
                                is_move = hero_now.move('down', maze_now)
                            elif event.key == pygame.K_LEFT:
                                is_move = hero_now.move('left', maze_now)
                            elif event.key == pygame.K_RIGHT:
                                is_move = hero_now.move('right', maze_now)

                    num_steps += int(is_move)  # Cập nhật num_steps
                    hero_now.draw(screen)
                    maze_now.draw(screen)

                    showText(screen, font, 'LEVEL DONE: %d' % num_levels, (255, 0, 0), (10, 10))
                    showText(screen, font, 'BEST SCORE: %s' % best_scores, (255, 0, 0), (210, 10))
                    showText(screen, font, 'USED STEPS: %s' % num_steps, (255, 0, 0), (410, 10))
                    

                    
                    if (hero_now.coordinate[0] == self.cfg.MAZESIZE[1] - 1) and (hero_now.coordinate[1] == self.cfg.MAZESIZE[0] - 1):
                        self.wait_screen.active = True  # Kích hoạt màn hình chờ
                        self.waiting_to_continue = True  # Đặt cờ này để chờ

                        while self.waiting_to_continue:
                            self.wait_screen.draw()
                            action = self.wait_screen.handle_events()
                            
                            if action == "continue":
                                self.waiting_to_continue = False  # Tắt cờ
                                
                                game_state = "playing"  # Quay lại trạng thái "playing"
                                break  # Thoát khỏi vòng lặp while bên trong    
                            elif action == "stop":
                                self.waiting_to_continue = False  # Tắt cờ
                                game_state = "menu"  # Quay lại trạng thái "menu"
                                break  # Thoát khỏi vòng lặp while bên trong
                        break

                    self.finished_level = True  # Đánh dấu ván chơi đã kết thúc


                    pygame.display.update()
                if best_scores == 'None':
                    best_scores = num_steps
                else:
                    if best_scores > num_steps:
                        best_scores = num_steps
                num_steps = 0


class ResourceLoader():
    def __init__(self):
        self.images = {}
        self.bgm = None

    def load_image(self, name, path):
        image = pygame.image.load("Image/hero.png")
        self.images[name] = image

    def load_bgm(self, path):
        pygame.mixer.music.load("Music/bgm.mp3")

    def play_bgm(self):
        pygame.mixer.music.play(-1)

if __name__ == '__main__':
    game = MazeGame()
    game.run()