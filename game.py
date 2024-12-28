import pygame
from random import choice
import math

window_width = 640
window_height = 480

#Classes
class Character:
  def __init__(self, image: str):
    self.image = pygame.image.load(f"{image}")
    self.height = self.image.get_height()
    self.width = self.image.get_width() 

##Robot 
class Robot(Character):
    def __init__(self, image):
        super().__init__(image)
        self.x = (window_width-self.width)/2
        self.y = window_height - self.height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.speed = 3
        
    def move_right(self):
        self.x += self.speed
        self.rect.topleft=self.x, self.y
    def move_left(self):
        self.x -= self.speed
        self.rect.topleft=self.x, self.y
    def move_up(self):
        self.y -= self.speed
        self.rect.topleft=self.x, self.y
    def move_down(self):
        self.y += self.speed
        self.rect.topleft=self.x, self.y
        
##Monster 
class Monster(Character):
    def __init__(self, image):
        super().__init__(image)
        self.x = (window_width-self.width)/2
        self.y = 0
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.speed = 0.5
        
    def monster_movement(self, robot: Robot):
        if robot.y > self.y:
            self.y += self.speed
        elif robot.y < self.y:
            self.y -= self.speed
        
        if robot.x > self.x:
            self.x += self.speed
        elif robot.x < self.x:
            self.x -= self.speed
        
        self.rect.topleft = (self.x, self.y)
        
            
##Door
class Door(Character):
    def __init__(self, image):
        super().__init__(image)
        self.x = (window_width-self.width)/2
        self.y = (window_height-self.height)/2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
       
##Coin
class Coin(Character):
    def __init__(self, image):
        super().__init__(image)
        self.x = (window_width-self.width)/4
        self.y = (window_height-self.height)/2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.is_visible = True
        
    def new_position(self, robot: Robot):
        x_range = list(range(0, math.floor(robot.x))) + list(range(math.floor(robot.x)+robot.width, window_width-self.width))
        y_range = list(range(0, robot.y)) + list(range(robot.y+robot.height, window_height-self.height))
        new_x = choice(x_range)
        new_y = choice(y_range)
        self.x = new_x
        self.y = new_y
        self.rect.topleft = (self.x, self.y)
        
    def hide_coin(self):
        self.x = window_width*2
        self.y = window_height*2
        self.rect.topleft = (self.x, self.y)

##Game
class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Get and bank 5 coins via touching the door - Touching the Monster is game over!")
        self.window_width = window_width
        self.window_height = window_height
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        self.clock = pygame.time.Clock()
        
        #fonts
        self.game_font = pygame.font.SysFont("microsoftsansserif", 20)
        self.game_over_font = pygame.font.SysFont("microsoftsansserif", 40)
        
        self.reset_game()
            
    def game_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    exit()
                if event.key == pygame.K_F2:
                    self.reset_game()
                if self.is_game_won or self.is_game_won:
                    return
                if event.key == pygame.K_LEFT:
                    self.to_left = True
                if event.key == pygame.K_RIGHT:
                    self.to_right = True
                if event.key == pygame.K_UP:
                    self.to_up = True
                if event.key == pygame.K_DOWN:
                    self.to_down = True

        
            if event.type == pygame.KEYUP:
                if self.is_game_won or self.is_game_won:
                    return
                if event.key == pygame.K_LEFT:
                    self.to_left = False
                if event.key == pygame.K_RIGHT:
                    self.to_right = False
                if event.key == pygame.K_UP:
                    self.to_up = False
                if event.key == pygame.K_DOWN:
                    self.to_down = False

            if event.type == pygame.QUIT:
                exit()
            
    def update_game(self):
        if not self.is_game_over:
            if self.to_right and self.robot.x + self.robot.width < self.window_width:
                self.robot.move_right()
            if self.to_left and self.robot.x > 0:
                self.robot.move_left()
            if self.to_up and self.robot.y > 0:
                self.robot.move_up()
            if self.to_down and self.robot.y + self.robot.height < self.window_height:
                self.robot.move_down()


        if self.robot.rect.colliderect(self.monster.rect) and not self.is_game_over and not self.is_game_won:
            self.is_game_over = True

        if self.robot.rect.colliderect(self.coin.rect):
            self.coin.new_position(self.robot)
            self.coin.is_visible = False
            self.coin.hide_coin()

        if self.robot.rect.colliderect(self.door.rect) and not self.coin.is_visible:
            self.coin.is_visible = True
            self.coin.new_position(self.robot)
            self.coins_remaining -= 1
            self.monster.speed += 0.25
        
        if not self.is_game_won:
            self.monster.monster_movement(self.robot)
        
        if self.coins_remaining == 0:
            self.is_game_won = True
            
    def draw_window(self):
        self.window.fill((211,211,211))
        
        #Text
        quit_text = self.game_font.render(f"Q = Quit", True, (255, 0, 0))
        self.window.blit(quit_text, (5, 5))
        coins_left_text = self.game_font.render(f"Coins remaining: {self.coins_remaining}", True, (255, 0, 0))
        self.window.blit(coins_left_text, (5, 452))
        new_game_text = self.game_font.render(f"F2 = New Game", True, (255, 0, 0))
        self.window.blit(new_game_text, (480, 5))

        #PNG drawing
        self.window.blit(self.door.image, (self.door.x, self.door.y))
        if self.coin.is_visible:
            self.window.blit(self.coin.image, (self.coin.x, self.coin.y))
        self.window.blit(self.robot.image, (self.robot.x, self.robot.y))
        self.window.blit(self.monster.image, (self.monster.x, self.monster.y))

        #If game is lost
        if self.is_game_over:
            self.game_over()
        
        #If game is won
        if self.is_game_won:
            self.game_won()

        pygame.display.flip()
    
    def game_over(self):
        game_over_text = self.game_over_font.render("Game Over!", True, (255, 0, 0))
        game_over_text2 = self.game_over_font.render(f"You needed {self.coins_remaining} more {"coins" if self.coins_remaining > 1 else "coin"} to win!", True, (255, 0, 0))
        self.window.blit(game_over_text, ((self.window_width - game_over_text.get_width()) / 2, 275))
        self.window.blit(game_over_text2, ((self.window_width - game_over_text2.get_width()) / 2, 320)) 
    
    def game_won(self):
        game_won_text = self.game_over_font.render("Congratulations!", True, (255, 0, 0))
        game_won_text2 = self.game_over_font.render(f"A winner is you!", True, (255, 0, 0))
        self.window.blit(game_won_text, ((self.window_width - game_won_text.get_width()) / 2, 275))
        self.window.blit(game_won_text2, ((self.window_width - game_won_text2.get_width()) / 2, 320)) 
    
    def run(self):
        while True:
            self.game_events()
            self.update_game()
            self.draw_window()
            self.clock.tick(60)
            
    def reset_game(self):
        self.robot = Robot("robot.png")
        self.monster = Monster("monster.png")
        self.door = Door("door.png")
        self.coin = Coin("coin.png")

        self.to_right = False
        self.to_left = False
        self.to_up = False
        self.to_down = False
        self.is_game_over = False
        self.is_game_won = False
        self.coins_remaining = 5

if __name__ == "__main__":
    game = Game()
    game.run()
    