import pygame
from variables import *
from Spritesheet import *
from Text import *

class Character():
        
        def __init__(self, x, y, max_hp, strength, scale, type, name, flip, dimension):
                
                self.type = type #the type of character: Player or Enemy
                
                self.name = name #name of the character
                
                self.name_text = font.render(self.name, True, (0,0,0))
                
                self.name_text_rect = self.name_text.get_rect()
                
                self.flip = flip #if the sprite need to be flipped
                
                self.strength = strength
            
                self.max_hp = max_hp
                
                self.hp = max_hp
                
                self.alive = True
                
                self.load_animations(scale, dimension) #load in animation
                
                self.image = self.master_animation_list[self.current_action][self.frame]
                                                        
                self.width = self.image.get_width()

                self.height = self.image.get_height()
                        
                self.rect = self.image.get_rect()
                        
                self.rect.x = x
                        
                self.rect.y = y
        
        #Reset the player back to normal
        def reset(self, max_hp):
                
                self.max_hp = max_hp
                
                self.hp = max_hp
                
                self.alive = True

        #Load the different type of animation                  
        def load_animations(self, scale, dimension):
                
                #Citation: 
                
                #Samurai Sprite by Mattz Art https://xzany.itch.io/samurai-2d-pixel-art
                
                #Necromancer Sprite by CreativeKind https://creativekind.itch.io/necromancer-free
                
                #NightBorne Warrior Sprite by CreativeKind https://creativekind.itch.io/nightborne-warrior
                
                #Skeleton Sprite by MonoPixelArt https://monopixelart.itch.io/skeletons-pack
                
                #Bat Sprite by MonoPixelArt https://monopixelart.itch.io/dark-fantasy-enemies-asset-pack
                
                #Golems Sprite by MonoPixelArt https://monopixelart.itch.io/golems-pack
                
                #Mushroom Sprite by MonoPixelArt https://monopixelart.itch.io/forest-monsters-pixel-art
                
                #Flying Monster Sprite by MonoPixelArt https://monopixelart.itch.io/flying-enemies
                
                self.dimension = dimension #dimension of each sprite
                
                self.current_action = 0 #what they are currently doing

                self.master_animation_list = []

                self.last_update = pygame.time.get_ticks()

                self.frame = 0 #frame of the animation

                self.animations_types = ["IDLE", "ATTACK", "HURT", "DEATH"] #types of animation
                
                self.animation_complete = False

                for animations in self.animations_types: #see load_animations method in Card class
                
                        empty_list = []

                        type = pygame.image.load(f"Images/Character/{self.type}/{self.name}/{animations}.png").convert_alpha()
                        
                        sprite = SpriteSheet(type, self.dimension)

                        for image in range(int(sprite.total)):

                                empty_list.append(sprite.get_image(image, self.dimension, self.dimension, scale))

                        self.master_animation_list.append(empty_list)
        
        #character attack
        def attack(self, damage, target):
                                
                target.hp -= damage #deal damage to the target
                                
                if target.hp < 1: #the target is dead
                
                        target.hp = 0
                
                        target.alive = False
        
        #Update the current animation of the card (See )              
        def update_animations(self, new_action, COOLDOWN):
                
                #see update_animations in the Card class
                if self.current_action != new_action:
                
                        self.frame = 0
        
                        self.current_action = new_action
        
                        self.last_update = pygame.time.get_ticks()

                        self.animation_complete = False

                if pygame.time.get_ticks() - self.last_update >= COOLDOWN:
                        
                        self.frame += 1

                        self.last_update = pygame.time.get_ticks()

                        if self.frame >= len(self.master_animation_list[self.current_action]):

                            self.frame = 0
                            
                            self.animation_complete = True
                        
                        self.image = self.master_animation_list[self.current_action][self.frame]

                        if self.flip: #flip the image and animation if needed

                               self.image = pygame.transform.flip(self.image, True, False)                    
        
        #draw the player on screen                
        def draw(self, screen):
                
                screen.blit(self.image, self.rect)

class HealthBar():
        
        def __init__(self, max_hp, hp):
                                
                self.max_hp = max_hp
                
                self.hp = hp
        
        #how many hp the character has in text form   
        def info(self, text, font, text_color, x, y):
        
                info = font.render(text, True, text_color) #ex: 100
                                
                screen.blit(info, (x, y)) #text position
                
                return x, y
        
        #draw the hp and healthbar relative to each other 
        def draw(self, screen, hp, info):
                                
                position_x, position_y = info #position of the healthbar
                
                ratio = hp / self.max_hp #ratio between the current hp and max hp
                
                #red bar, how much hp is lost
                pygame.draw.rect(screen, (255, 0, 0), ((position_x - 55, position_y + 22), (170, 20)))
                
                #green bar, representing how much hp is left
                #length of bar is dependent on ratio
                pygame.draw.rect(screen, (0, 255, 0), ((position_x - 55, position_y + 22), (170 * ratio, 20))) #ex: if ratio is 0.5, player is at half hp, green bar is half the full length
                
class CampFire():
        
        def __init__(self, x, y, scale):
                
                pygame.sprite.Sprite.__init__(self)
                
                #Citation:

                #Referenced Used: Bonfire (Rest) by Kaleb da Silva Pereira https://www.vecteezy.com/vector-art/9877856-pixel-art-bonfire-june-party-bonfire-vector-icon-for-8bit-game-on-white-background
                
                self.image = pygame.image.load("Images/Rest.png")

                self.width = self.image.get_width()

                self.height = self.image.get_height()
                               
                self.image = pygame.transform.scale(self.image, (self.width * scale, self.height * scale))
                
                self.rect = self.image.get_rect()
                
                self.rect.x = x
                        
                self.rect.y = y
                
                self.alive = True #the campfire is active ("alive")
                
                self.time = 0 #number of time the campfire has healed
                
                self.animation_complete = False #is campfire finish healing
          
        #reset the campfire      
        def reset(self):
                            
                self.alive = True
                
                self.time = 0
                
                self.animation_complete = False
        
        #draw in the campfire       
        def draw(self, screen):
                
                screen.blit(self.image, self.rect)
        
        #Campfire healing
        def update(self, player): 
                
                global action_cooldown
                        
                if self.time < 10: #if campfire has healed less than 10 times
                        
                        action_cooldown += 1
                        
                        #amount of healing sprite
                        heal = DamageText(random.randrange(self.rect.x, self.rect.x + 200, 50), 250, "+1", (128, 203, 196))
                        
                        if action_cooldown >= 50: #delay between each healing
                        
                                damage_text_group.add(heal)
                                
                                #heal the player by 1 but do not exceed their max hp
                                player.hp = min(player.hp + 1, player.max_hp)
                                
                                action_cooldown = 0
                                
                                self.time += 1 #heal one time
                                
                else: #campfire has healed 10 times
                          
                        self.alive = False #no longer "alive" (active)
                        
                        action_cooldown += 1
                        
                        if action_cooldown >= action_wait_time + 10: #delay before switching back to map
                        
                                self.animation_complete = True #done healing
                                
                                action_cooldown = 0
                