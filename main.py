import pygame


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

    numbers = [i for i in range(1, self.size ** 2)]
    numbers.append(0)
    self.board = [[numbers.pop(0) for _ in range(self.size)] for _ in range(self.size)]
    self.empty = self.find_empty()

    while self.running:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.running = False
      
      self.update()
      self.draw()

      self.clock.tick(60)

  def find_empty(self):
    for i in range(self.size):
      for j in range(self.size):
        if self.board[i][j] == 0:
          return (i, j)

  def draw(self):
    self.win.fill((0, 0, 0))
    for i in range(self.size):
      for j in range(self.size):
        if self.board[i][j] != 0:
          pygame.draw.rect(self.win, (255, 255, 255), (j * self.tile_size, i * self.tile_size, self.tile_size, self.tile_size))
          font = pygame.font.SysFont("monospace", 50)
          text = font.render(str(self.board[i][j]), True, (0, 0, 0))
          self.win.blit(text, (j * self.tile_size + self.tile_size // 2 - text.get_width() // 2, i * self.tile_size + self.tile_size // 2 - text.get_height() // 2))
    pygame.display.flip()

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