import pygame

class SpriteSheet():
        
        def __init__(self, image, dimension):
		
                self.dimension = dimension
  
                self.sheet = image #full spritesheet

                self.width = self.sheet.get_width()             
                
                self.total = self.width / self.dimension #total amount of sprite within the sheet

        def get_image(self, frame, width, height, scale):
		
                #create a transparent surface the size of one individual sprite
                image = pygame.Surface((width, height), pygame.SRCALPHA, 32)
		
                #split spritesheet up into individual sprite and drawing each sprite onto the surface
                image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
		
                #scale the image up
                image = pygame.transform.scale(image, (width * scale, height * scale))
                
                return image
