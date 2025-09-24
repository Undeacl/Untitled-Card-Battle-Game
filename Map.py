import pygame
from variables import *

class Node:
        
        def __init__(self, x, y, label, connecting_node, type):
                
                self.type = font.render(type, True, (255, 255, 255)) #node type ex: Encounter
                
                self.type_text = type
                
                self.type_rect = self.type.get_rect()
                
                self.type_rect.x = x
                
                self.type_rect.y = y
                
                image = icon_dict[type] #image icon for the node

                self.label = image["image"]

                self.radius_quotient = image["radius_quotient"] #used to calculate the circle the icon sit on
                                
                self.label_text = label #could be anything (previous used before image icon)
                
                self.label_rect = self.label.get_rect()
                
                self.mask = pygame.mask.from_surface(self.label) #image mask used for collision
                  
                self.label_rect.x = x
                
                self.label_rect.y = y
                
                self.connecting_node = connecting_node #the other nodes that this node is connected to
                
                self.clicked = False #has the node been clicked
                
                self.color = (255, 0, 0) #red to start

                self.radius = self.label_rect.height / self.radius_quotient #radius of the circle
        
        #Reset the node back to its original state
        def reset(self):
                
                self.clicked = False
                
                self.color = (255, 0, 0)
      
        #Hover collision of node  
        def hover(self, cursor, pos):
                
                info = font.render(f"{self.type_text}", True, (0, 0, 0)) #what the node is ex: Encounter
                
                #check to see if mouse collide with the image i.e hover
                if self.mask.overlap(cursor, (pos[0] - self.label_rect.x, pos[1] - self.label_rect.y)) and not self.clicked:
                        
                        #display what type of node it is
                        screen.blit(info, (self.label_rect.centerx - self.type_rect.width / 2, self.label_rect.centery - self.radius - 25))
                        
                        return True
        
        #Node clicking functionality
        def click(self, cursor, pos):
                
                #if we are hovering the node
                if self.hover(cursor, pos):
                                
                        if not self.clicked: #node has not been clicked
                                
                                self.clicked = True #node is now clicked
                                
                                self.color = (0, 255, 0) #green to show that it is clicked
                                
                                return True
                        
                        return False     

        #Drawing of node icon onto screen
        def draw(self, screen):
                
                #Draw a circle under the node icon
                pygame.draw.circle(screen, self.color, (self.label_rect.centerx, self.label_rect.centery), self.radius)
                
                screen.blit(self.label, self.label_rect)
                      
class Map:
        
        def __init__(self, map):
                
                self.map = map #the map, a list
                
                self.starting_point = self.map[0] #the first node is our starting node
                
                self.position = self.starting_point #where the player is
                
                self.visible = False #is the map visible
                
                #the starting node is "clicked"
                self.starting_point.color = (0, 255, 0)
                
                self.starting_point.clicked = True
                
                self.node_click = False #did we click on a node
        
        #Hover check for each node 
        def hover(self, cursor, pos):
                
                for node in self.map:
                        
                        node.hover(cursor, pos)

        #Draw the map
        def draw(self, screen):
                
                here = font.render("You're Here", True, (0, 0, 0)) #indication of where player is
                
                rect = here.get_rect()
                  
                for nodes in self.map:
                        
                        for points in nodes.connecting_node: #the node's index in the map list
                                                                
                                target = self.map[points] #target is the node based on their index
                                
                                #draw a line connected the two nodes
                                pygame.draw.line(screen,
                                                 (255, 255, 255),
                                                 (nodes.label_rect.centerx, nodes.label_rect.centery), 
                                                 (target.label_rect.centerx, target.label_rect.centery), 5)
                                
                for nodes in self.map:
                                                
                        nodes.draw(screen)
                        
                        if nodes == self.position:
                                
                                screen.blit(here, (self.position.label_rect.centerx - rect.width / 2, self.position.label_rect.top - 35))
        
        #Click check for each node and change state of connecting node         
        def click(self, cursor, pos):
                
                for nodes in self.map:
                        
                        for points in nodes.connecting_node: #check to see where we can go
                                
                                if points == self.map.index(self.position): #the node we can go to is connected to our node
                        
                                        if nodes.click(cursor, pos): #if we clicked the node
                                                
                                                self.position = nodes #our position is now that node
                                                
                                                self.visible = False #map is no longer visible i.e we are battling or resting
                                                
                                                self.node_click = True #we clicked on a node
                                                
                                                break
                
                #if node A is connected to node B and C, and we clicked on B, C is now disabled i.e we cannot go there anymore
                
                #iterate again to change the state
                for nodes in self.map:
                                                           
                        if nodes != self.position: #node that is not our current node
                                
                                for point in self.position.connecting_node: #what our node is connected to 
                                   
                                        if point in nodes.connecting_node: #if another node share the same connection point
                                                        
                                                nodes.clicked = True #that node is now "clicked" (disable)
                                                
                                                nodes.color = (100, 100, 100) #change color of that node to gray

        #Reset map back to its original state
        def reset(self):
                
                for nodes in self.map:
                        
                        nodes.reset() #reset each node
                
                self.starting_point = self.map[0]
                
                self.position = self.starting_point
                
                self.visible = False
                
                self.starting_point.color = (0, 255, 0)
                
                self.starting_point.clicked = True
                
                self.node_click = False                  
                        
