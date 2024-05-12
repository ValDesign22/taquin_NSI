import pygame
from random import choice


class Taquin:
  def __init__(self):
    pygame.init()
    pygame.font.init()
    self.width = 600
    self.height = 600
    self.board_size = 400
    self.size = 4
    self.win = pygame.display.set_mode((self.width, self.height))
    pygame.display.set_caption("Taquin")
    self.clock = pygame.time.Clock()
    self.tile_size = self.board_size // self.size
    self.running = True
    self.moving = False

    self.buttons = [
      {"text": "Mélanger", "x": 100, "y": 450, "width": 100, "height": 50, "color": (255, 255, 255), "hover_color": (200, 200, 200), "clicked": False},
      {"text": "Résoudre", "x": 400, "y": 450, "width": 100, "height": 50, "color": (255, 255, 255), "hover_color": (200, 200, 200), "clicked": False}
    ]

    numbers = [i for i in range(1, self.size ** 2)]
    numbers.append(0)
    self.board = [[numbers.pop(0) for _ in range(self.size)] for _ in range(self.size)]
    self.empty = self.find_empty()

    while self.running:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
          for btn in self.buttons:
            if btn["x"] <= event.pos[0] <= btn["x"] + btn["width"] and btn["y"] <= event.pos[1] <= btn["y"] + btn["height"]:
              btn["clicked"] = True
      
      self.update()
      self.win.fill((0, 0, 0))
      self.draw()
      self.draw_buttons()
      pygame.display.flip()

      self.clock.tick(60)

  def shuffle(self, moves=1000):
    for _ in range(moves):
      move = choice(["UP", "DOWN", "LEFT", "RIGHT"])
      match move:
        case "UP":
          self.move("UP")
        case "DOWN":
          self.move("DOWN", -1)
        case "LEFT":
          self.move("LEFT")
        case "RIGHT":
          self.move("RIGHT", -1)

  def find_empty(self):
    for i in range(self.size):
      for j in range(self.size):
        if self.board[i][j] == 0:
          return (i, j)

  def draw(self):
    for i in range(self.size):
      for j in range(self.size):
        if self.board[i][j] != 0:
          pygame.draw.rect(self.win, (255, 255, 255), (100 + j * self.tile_size, i * self.tile_size, self.tile_size, self.tile_size))
          font = pygame.font.SysFont("monospace", 50)
          text = font.render(str(self.board[i][j]), True, (0, 0, 0))
          self.win.blit(text, (100 + j * self.tile_size + self.tile_size // 2 - text.get_width() // 2, i * self.tile_size + self.tile_size // 2 - text.get_height() // 2))

  def draw_buttons(self):
    for btn in self.buttons:
      pygame.draw.rect(self.win, btn["color"], (btn["x"], btn["y"], btn["width"], btn["height"]))
      font = pygame.font.SysFont("monospace", 20)
      text = font.render(btn["text"], True, (0, 0, 0))
      self.win.blit(text, (btn["x"] + btn["width"] // 2 - text.get_width() // 2, btn["y"] + btn["height"] // 2 - text.get_height() // 2))

  def update(self):
    keys = pygame.key.get_pressed()
    if not self.moving:
      if keys[pygame.K_UP]:
        self.move("UP")
      if keys[pygame.K_DOWN]:
        self.move("DOWN", -1)
      if keys[pygame.K_LEFT]:
        self.move("LEFT")
        self.moving = True
      if keys[pygame.K_RIGHT]:
        self.move("RIGHT", -1)

    if not keys[pygame.K_UP] and not keys[pygame.K_DOWN] and not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
      self.moving = False

    for btn in self.buttons:
      if btn["clicked"]:
        if btn["text"] == "Mélanger":
          self.shuffle()
        btn["clicked"] = False

  def move(self, direction, orientation=1):
    if direction in ["UP", "DOWN"]:
      distance = self.size - 1 - self.empty[0] if direction == "UP" else self.empty[0]
      if distance > 0:
        self.board[self.empty[0]][self.empty[1]] = self.board[self.empty[0] + orientation][self.empty[1]]
        self.board[self.empty[0] + orientation][self.empty[1]] = 0
        self.empty = (self.empty[0] + orientation, self.empty[1])
    elif direction in ["LEFT", "RIGHT"]:
      distance = self.size - 1 - self.empty[1] if direction == "LEFT" else self.empty[1]
      if distance > 0:
        self.board[self.empty[0]][self.empty[1]] = self.board[self.empty[0]][self.empty[1] + orientation]
        self.board[self.empty[0]][self.empty[1] + orientation] = 0
        self.empty = (self.empty[0], self.empty[1] + orientation)
    self.moving = True


if __name__ == "__main__":
  game = Taquin()