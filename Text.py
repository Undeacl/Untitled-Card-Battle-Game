import pygame
from variables import *

class DamageText(pygame.sprite.Sprite): #the damage that is shown when the enemy attacks the player
        
        def __init__(self, x, y, damage, color):
        
                pygame.sprite.Sprite.__init__(self)

                self.damage = int(damage)
                
                self.image = font.render(damage, True, color) #damage number as a pygame Surface
                
                self.rect = self.image.get_rect()
                
                self.rect.center = (x, y)
                
                self.timer = 0 #how long the sprite last
                
                self.color = color
        
        def update(self):
                
                self.rect.y -= 1 #make the sprite go up
                
                self.timer += 1
                
                if self.timer > 40:
                        
                        self.kill() #remove the sprite from existence

class ComboText(pygame.sprite.Sprite): #what the combo is ex: Double, Full House, ect. . .
        
        def __init__(self, x, y, type_combo, color):
                
                pygame.sprite.Sprite.__init__(self)
                
                self.color = color

                self.image = font.render(type_combo, True, self.color) #the text showing the combo

                self.rect = self.image.get_rect()

                self.rect.centerx = x
                
                self.rect.centery = y
                        
class ComboDamage(pygame.sprite.Sprite): #the damage number under the combo
        
        def __init__(self, damage, color, combo_text):
                
                pygame.sprite.Sprite.__init__(self)

                self.damage = int(damage) #initial damage

                self.color = color

                self.image = font.render(damage, True, self.color) #the number that adds to the total damage

                self.rect = self.image.get_rect()

                self.combo_text = combo_text
                
                self.rect.centerx = self.combo_text.rect.centerx

                self.rect.centery = self.combo_text.rect.centery + 20

def game_info(text, font, text_color, x, y): #used to draw turn and discard remaining
        
        info = font.render(text, True, text_color)
        
        screen.blit(info, (x, y))
        
        return x, y, info.width, info.height + 5
