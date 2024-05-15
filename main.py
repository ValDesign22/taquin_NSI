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
    self.move_count = 0

    self.buttons = [
      {"text": "Mélanger", "x": 100, "y": 450, "width": 100, "height": 50, "color": (255, 255, 255), "hover_color": (200, 200, 200), "clicked": False, "show": True},
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
          self.on_click(event)
      
      self.update()
      self.win.fill((0, 0, 0))
      self.draw()
      self.draw_buttons()
      if self.is_solved() and self.move_count > 0:
        font = pygame.font.SysFont("monospace", 25)
        text = font.render("Gagné !", True, (255, 255, 255))
        self.win.blit(text, (100 + 100 + 10, 450 + 25 - text.get_height() // 2))
        move_text = font.render(f"Nombre de mouvements: {self.move_count}", True, (255, 255, 255))
        self.win.blit(move_text, (100 + 100 + 10, 450 + 25 + 10))
      pygame.display.flip()

      self.clock.tick(60)

  def is_solved(self):
    if self.move_count == 0:
      return False
    numbers = [i for i in range(1, self.size ** 2)]
    numbers.append(0)
    final_state = [[numbers.pop(0) for _ in range(self.size)] for _ in range(self.size)]
    self.buttons[0]["show"] = True
    return self.board == final_state

  def on_click(self, event):
    x, y = event.pos

    # Boutons
    for btn in self.buttons:
      if x > btn["x"] and x < btn["x"] + btn["width"] and y > btn["y"] and y < btn["y"] + btn["height"]:
        btn["clicked"] = True
    
    # Cases
    if x > 100 and x < 100 + self.board_size and y > 0 and y < self.board_size:
      j = (x - 100) // self.tile_size
      i = y // self.tile_size
      if self.board[i][j] == 0:
        return
      if i == self.empty[0] and j == self.empty[1] - 1:
        self.move("RIGHT", -1)
      elif i == self.empty[0] and j == self.empty[1] + 1:
        self.move("LEFT")
      elif i == self.empty[0] - 1 and j == self.empty[1]:
        self.move("DOWN", -1)
      elif i == self.empty[0] + 1 and j == self.empty[1]:
        self.move("UP")

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
    self.move_count = 0

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
        if btn["show"]:
          pygame.draw.rect(self.win, btn["color"], (btn["x"], btn["y"], btn["width"], btn["height"]))
          font = pygame.font.SysFont("monospace", 20)
          text = font.render(btn["text"], True, (0, 0, 0))
          self.win.blit(text, (btn["x"] + btn["width"] // 2 - text.get_width() // 2, btn["y"] + btn["height"] // 2 - text.get_height() // 2))

  def update(self):
    if not self.is_solved():
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
          btn["show"] = False
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
    self.move_count += 1


if __name__ == "__main__":
  game = Taquin()