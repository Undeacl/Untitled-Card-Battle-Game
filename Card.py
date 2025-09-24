import pygame
from variables import *
from Spritesheet import *

class Card():
        
        def __init__(self, value, suit, path, scale, dimension):

                self.value = value
            
                self.suit = suit
                
                self.scale = scale
                
                self.path = path #image path

                image = pygame.image.load(self.path).convert_alpha()

                self.image = pygame.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))
                
                self.original_image = self.image #create a copy of the original image
                
                self.load_animations(scale, dimension) #load in all animation
                
                self.current_animation = None

                self.width = self.image.get_width()

                self.height = self.image.get_height()
                
                #turn all white pixel within the image to gray     
                for x in range(self.width):
                
                        for y in range(self.height):
                                                
                                r, g, b, a = self.image.get_at((x, y))
                        
                                if r > 240 and g > 240 and b > 240:
                        
                                        self.image.set_at((x, y), (230, 230, 230, a))
                
                self.rect = self.image.get_rect()
                
                self.mask = pygame.mask.from_surface(self.image) #image mask used for collision detection
                
                self.click = False #has the card when clicked
        
        #The cards position                 
        def position(self, x, y):
                
                self.rect.x = x
                
                self.rect.y = y
                
                self.original_y = y
                
                self.original_x = x

        #Load the different type of animation
        def load_animations(self, scale, dimension):
              
                self.dimension = dimension #dimension of the card image
                
                self.current_action = 0

                self.master_animation_list = []

                self.last_update = pygame.time.get_ticks()

                self.frame = 0 #frame of animation we are on

                self.animations_types = ["SHINE", "RIP"]
                
                self.animation_complete = False

                for animations in self.animations_types: #different animation
                
                        empty_list = [] #create a temporary list

                        #load in the sprite sheet for each animation
                        type = pygame.image.load(f"Images/Deck/Animation/{animations}.png").convert_alpha()

                        sprite = SpriteSheet(type, self.dimension)

                        for image in range(int(sprite.total)): #get the total number of sprite within the sheet

                                #add each sprite to the temporary list
                                empty_list.append(sprite.get_image(image, self.dimension, self.dimension, scale))

                        self.master_animation_list.append(empty_list) #add the temporary list to the master list
        
        #Collision detection
        def hover(self, cursor, pos):
                
                #check collision between the mouse cursor and card
                if self.mask.overlap(cursor, (pos[0] - self.rect.x, pos[1] - self.rect.y)) and self.current_action != 1:

                        self.update_animations(self.animations_types.index("SHINE"), 125, cursor, pos) #shine animation
                                                
                        return True
                else:
                        self.image = self.original_image #return the image back to normal

        #Update the current animation of the card
        def update_animations(self, new_action, COOLDOWN, cursor, pos):

                if self.current_action != new_action: #if it is a new animation
                
                        self.frame = 0 #reset the frame, prevent error where one animation have more frame than another
        
                        self.current_action = new_action #set the new action
        
                        self.last_update = pygame.time.get_ticks()

                        self.animation_complete = False #animation is not done b/c new animation

                #rate at which each frame is being shown
                if pygame.time.get_ticks() - self.last_update >= COOLDOWN:
                        
                        self.frame += 1

                        self.last_update = pygame.time.get_ticks()

                        #frame is now bigger than the length of the animation
                        if self.frame >= len(self.master_animation_list[self.current_action]):

                            self.frame = 0 #reset frame back
                            
                            self.animation_complete = True #animation is now done
                        
                        if self.hover(cursor, pos): #if the card is being hover
                        
                                self.image = self.original_image.copy() #make a copy of the original image

                                shine_frame = self.master_animation_list[self.current_action][self.frame] #load the shine animation
                                
                                #draw the shine animation into the card
                                self.image.blit(shine_frame, (0, 0), special_flags=pygame.BLEND_ADD)
                        
                        else: #specifically for rip animation
                                
                                self.image = self.master_animation_list[self.current_action][self.frame]

        #Check to see whether the card is clicked or not
        def clicked(self):
                
                #the card has not been clicked and the player had selected less than 5 cards
                if not self.click and len(selected_card) < 5:
                                                
                        self.rect.y = self.original_y - 10 #make the card go up to show selection
                        
                        self.click = True #the card is now clicked
                        
                        return True

                #the card is clicked
                elif self.click and len(selected_card) <= 5:
                                                
                        self.rect.y = self.original_y #set the card back
                        
                        self.click = False #card is now not clicked
        
        #draw the card on screen    
        def draw(self, screen):
                
                screen.blit(self.image, self.rect)
                