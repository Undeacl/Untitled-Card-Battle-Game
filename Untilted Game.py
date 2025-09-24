import pygame, pygame_gui, random, os
from Card import *
from Text import *
from variables import *
from Character import *
from collections import Counter
from Map import *

pygame.init()

#--------------------Game Functions--------------------#

#Reset/clear lists, variables, and sprite groups
def reset_everything():
        
        global text, extra_damage
        
        selected_card.clear()

        combo.clear()

        sequence_check.clear()

        combo_extra_damage_text.empty()

        combo_extra_damage.empty()
        
        text = ""

        extra_damage = 0

#Calculate the total damage output  
def total_damage_calculation():
                
        global total_damage, begin_remove, action_cooldown, begin_remove_animation
                
        if event.type == CARD_EVENT and selected_card:
                      
                card = selected_card.pop(0)

                erased.append(card) #add the card to the erased list to be remove later on
                
                #number that shows up op top of card
                additional_damage = DamageText(card.rect.centerx, card.rect.centery - 70, f"+{str(card.value)}", (10, 25, 47))
                
                damage_text_group.add(additional_damage)
                
                total_damage += int(additional_damage.damage)
                                
                combo_extra_damage_text.empty() #clear the sprite group to update to current total damage
                
                dmg_text = ComboDamage(f"{total_damage}", (128, 203, 196), text)
                                
                combo_extra_damage_text.add(text, dmg_text)

                if not selected_card:

                        begin_remove_animation = True
                        
        if begin_remove_animation: 
                
                action_cooldown += 1

                if action_cooldown >= 2: #add a tiny delay

                        begin_remove = True #begin removing the card from screen

                        pygame.time.set_timer(CARD_EVENT, 0)
                                                                        
                        pygame.time.set_timer(REMOVE_EVENT, 88) #prepare for card removing
                        
                        pygame.time.set_timer(ATTACK_EVENT, 85) #prepare for attacking

                        begin_remove_animation = False

                        action_cooldown = 0

#Player attacking              
def attack():
        
        global finish_attack, amount_turn, begin_attack, total_damage
        
        if event.type == ATTACK_EVENT and player.animation_complete: #only run when the attack animation has finished
                
                player.attack(total_damage, enemy)

                finish_attack = True

                amount_turn -= 1
                        
        if finish_attack:
                
                begin_attack = False
                
                pygame.time.set_timer(ATTACK_EVENT, 0) #stop attack event
                
                total_damage = 0
                
                finish_attack = False

#Remove card from hand                               
def remove_card(current_card):
        
        global erased, bonus_dmg_text, begin_attack
        
        amount_card = len(erased) #the number of card being replaced
        
        #update the used_cards dictionary
        used_cards.update({
        
        f"{os.path.basename(current_card.path).split(".")[0]}": 

                {"value": f"{current_card.value}", "suit": f"{current_card.suit}"}
        
        })
        
        if event.type == REMOVE_EVENT and current_card.animation_complete: #occur when the rip animation finishes
                                   
                for card in erased[:]: #prevent the loop from alternating by creating a shallow version
                                                              
                        cards_in_hand.remove(card) #remove the card from player's hand
                                
                        erased.remove(card) #remove the card from erased list
                        
                if not erased: #once erased list is empty
                        
                        if not is_discard and enemy.alive: #are we discarding or attacking
                                
                                begin_attack = True #attack
                                
                                bonus_dmg_text = False #stop total calculation output
                        
                        pygame.time.set_timer(REMOVE_EVENT, 0) #stop the removal (there's nothing left to remove)
                        
                        add_new_card(amount_card) #add in new card

#Add/replace cards    
def add_new_card(amount):
        
        global begin_remove, prevent_selection
        
        reset_everything() 
        
        #get the card currently in hand in dictionary form
        card_in_hand = {
                
                f"{os.path.basename(card.path).split(".")[0]}"
                
                for card in cards_in_hand
        }

        #available card for replacement
        available_card = {
                       
                name: info 
                
                for name, info in deck.items() 
                
                if name not in card_in_hand and name not in used_cards
        
        }
                
        #amount being replaced: amount specified by parameter or available card
        amount = min(len(available_card), amount) #whichever is less
                
        replacement = random.sample(list(available_card.items()), amount) #get the replacement card
        
        for card in replacement:
                        
                name = card[0] #ex: Diamonds A
                
                info = card[1] #contains the card value and suit
                
                value = info["value"] #value: 14
                
                suit = info["suit"] #suit: Diamonds
                
                image_path = f"Images/Deck/{suit}/{name}.png" #directory to the image ex: Images/Deck/Diamonds/Diamonds A.png
                
                cards_in_hand.append(Card(value, suit, image_path, 1, 128)) #add the new to hand
        
        cards_in_hand.sort(key = lambda card: card.value) #sort least to greatest card value

        for index, card in enumerate(cards_in_hand):

                card.position(WIDTH / 6.5 + index * 100, HEIGHT - 200) #draw the card in their respective position
                                
        begin_remove = False #stop the removal process
        
        prevent_selection = False #cards are now clickable

#Detect any combination of card
def combo_detection():
        
        global text, extra_damage, combo_detected, sequence_check
        
        combo_check = []
        
        for card in selected_card:
                
                combo_check.append(card.value)  #stored all cards value that have been selected

        combo_check.sort() #sort the value

        combo_check = Counter(combo_check) #count occurrence of each value
        
        #combo text corresponding with the count of value 
        combo_texts = {
                                     
                2: "Double",
                
                3: "Triple",
                
                4: "Quad"
        }
        
        double_pair = [] #stored double pair, ex: two 10 and two Ace
        
        combo_detected = False
        
        for value, count in combo_check.items(): #iterate through combo_check: value = card value, count = # occurrence
                                                                     
                if count in combo_texts: #we have a combo!
                                                                                
                        combo.append(value) #append the value into combo list
                        
                        text = ComboText((attack_button_rect.right + discard_button_rect.left) / 2, attack_button_rect.centery - 10, f"{combo_texts[count]}", (128, 203, 196)) #text ex: Double
                                                
                        extra_damage = ComboDamage(f"{combo_check[value] * 10}", (128, 203, 196), text) #damage of combo ex: 20
                                                
                        combo_extra_damage.add(text, extra_damage) #add to sprite group
                        
                        combo_detected = True
                
                if 3 in combo_check.values() and 2 in combo_check.values(): #Full House: # occurrence is 3 and 2
                                                
                        combo_extra_damage.empty() #prevent overlap b/c another combo was found before
                
                        text = ComboText((attack_button_rect.right + discard_button_rect.left) / 2, attack_button_rect.centery - 10, "Full House", (128, 203, 196))

                        extra_damage = ComboDamage("70", (128, 203, 196), text)

                        combo_extra_damage.add(text, extra_damage)

                if count == 2:
                        
                        double_pair.append(value)
                       
        if not combo_detected: #we have no combo :(
                                
                text = ComboText((attack_button_rect.right + discard_button_rect.left) / 2, attack_button_rect.centery - 10, f"Solo", (128, 203, 196))
                
                extra_damage = ComboDamage("10", (128, 203, 196), text)
                                        
                combo_extra_damage.add(text, extra_damage)
        
        if not combo_check: #player deselect all card
                
                combo_extra_damage.empty()
                
                combo_extra_damage_text.empty()
        
        if len(double_pair) == 2: #two value have 2 occurrence each
                
                combo_extra_damage.empty()
                
                text = ComboText((attack_button_rect.right + discard_button_rect.left) / 2, attack_button_rect.centery - 10, "Double Pair", (128, 203, 196))
                
                extra_damage = ComboDamage("40", (128, 203, 196), text)
                        
                combo_extra_damage.add(text, extra_damage)
        
        sequence_check = list(combo_check.keys()) #a list of all card value
                
        if len(sequence_check) == 5:
                                
                for i in range(1, len(sequence_check)):
                        
                        #ex sequence: (2, 3, 4, 5, 6), 3 - 2 = 1 and so on
                        #ex not: (2, 3, 4, 5, 9), 9 - 5 != 1
                        if sequence_check[i] - sequence_check[i-1] != 1:
                                
                                return False
                
                combo_detected = True #this is a combo
                           
                combo_extra_damage.empty()
                
                text = ComboText((attack_button_rect.right + discard_button_rect.left) / 2, attack_button_rect.centery - 10, "Sequence", (128, 203, 196))
                
                extra_damage = ComboDamage("100", (128, 203, 196), text)
                
                combo_extra_damage.add(text, extra_damage)

#Identify and remove card who's value is not going to be counted towards the total damage                         
def eliminate_card():

        #update the used_cards dict
        used_cards.update({
        
        f"{os.path.basename(card.path).split(".")[0]}": 

                {"value": f"{card.value}", "suit": f"{card.suit}"}

        for card in selected_card
        
        })
        
        #if we have a combo ex: Triple                
        if combo:

                for card in selected_card[:]: #create shallow list to avoid changing iteration
                                                        
                        if card.value not in combo: #ex: (5, 5, 5, 10, 14) 10 and 14 is not part of combo
                                
                                selected_card.remove(card) #remove those card: 10 and Ace
                                
                                erased.append(card) #add all card into erased list
        
        #if we do not have a combo: Solo
        if not combo_detected:
                
                #get the highest value card
                highest = max(card.value for card in selected_card)
                        
                for card in selected_card[:]:
                                
                        if card.value < highest: #any card who's value is less than the highest
                                
                                selected_card.remove(card) #remove the card
                                
                                erased.append(card)

#Begin the next encounter, or rest
def new_run(node_type):
        
        global enemy_hp, action_cooldown, amount_turn, enemy, amount_discard, enemy_info, attribute, attribute_icon_text, game_state, prevent_selection
        
        game_state = 0
        
        if node_type != "Rest": #if we are not resting
                
                #get the info of a random enemy based on the node we are on
                enemy_info = random.choice(list(specific_for_enemy[node_type].items()))
                
                #create the enemy
                enemy = Character(0, 0, enemy_info[1]["HP"], enemy_info[1]["Strength"], enemy_info[1]["Scale"], "Enemy", enemy_info[0], enemy_info[1]["Flip"], enemy_info[1]["Resolution"])

                attribute = enemy_info[1]["Attribute"] #enemy attribute
                
                attribute_icon_text = enemy_info[1]["Attribute_Info"] #what the attribute means
                
                enemy_hp = HealthBar(enemy.max_hp, enemy.hp) #enemy hp and healthbar
 
                #enemy position
                enemy.rect.x = (WIDTH / 2) - (enemy.width / 2) + 310
        
                enemy.rect.y = HEIGHT / 2 - enemy.height + enemy_info[1]["Y_Offset"]

                action_cooldown = 0

                amount_turn = 2 + (enemy_info[1]["Turn Modifier"] if "Turn Modifier" in enemy_info[1] else 0)

                amount_discard = 3 + (enemy_info[1]["Discard Modifier"] if "Discard Modifier" in enemy_info[1] else 0)

        else: #if we are not battling, then we are resting
                
                enemy = CampFire(0, 0, 3) #"enemy" is a campfire
                
                #campfire position
                enemy.rect.x = WIDTH / 2
        
                enemy.rect.y = HEIGHT / 2 - enemy.height - 75
                                
                prevent_selection = True
                
                amount_turn = 2 #reset amount of turn back to normal (don't really need this here, but added just for the ui to look nice)
        
        map.node_click = False
        
        used_cards.clear() #reset used_cards dict
        
        add_new_card(8 - len(cards_in_hand)) #add in new card

        attack_button.visible = True #make the attack button visible
        
        discard_button.visible = True #make the discard button visible

#Player action and animation
def player_action():

        global action_cooldown, game_state
    
        if begin_attack: #if we are attacking

                attack()

                player.update_animations(player.animations_types.index("ATTACK"), 80) #attack animation
                
        elif amount_turn == 0 and player.alive and enemy.alive: #turn is now over i.e enemy is attacking
                
                action_cooldown += 1
                
                #continue idle animation until a specific point in the enemy attack animation
                if action_cooldown <= action_wait_time - enemy_info[1]["Animation_Speed_Offset"]:
                        
                        player.update_animations(player.animations_types.index("IDLE"), 80)
                
                else: #try to time the hurt animation when enemy attack
                        player.update_animations(player.animations_types.index("HURT"), 80)
        
        elif not player.alive: #player is dead
                                
                player.update_animations(player.animations_types.index("DEATH"), 80) #Death animation
                
                game_state = -1
                                        
        else: #Nothing is happening
                
                player.update_animations(player.animations_types.index("IDLE"), 80) #Idle animation

#Enemy action and animation
def enemy_action():
        
        global prevent_selection, amount_turn
        
        if map.position.type_text != "Rest": #for actually enemy, not campfire
        
                if amount_turn == 0 and enemy.alive: #turn is now over, enemy is attacking
                                
                        enemy.update_animations(enemy.animations_types.index("ATTACK"), 80) #Attack animation
                                
                        if enemy.animation_complete:
                                        
                                        #sprite showing damage enemy is doing
                                        damage_text = DamageText(player.rect.x + player.width / 2, 250, f"-{enemy.strength}", (128, 203, 196))
                                        
                                        damage_text_group.add(damage_text)
                                        
                                        enemy.attack(enemy.strength, player) #do damage to player based on enemy strength
                                        
                                        #reset the amount of turn back to normal
                                        amount_turn = 2 + (enemy_info[1]["Turn Modifier"] if "Turn Modifier" in enemy_info[1] else 0)
                                        
                                        #allow player to select card
                                        prevent_selection = False
                
                elif begin_attack: #player is attacking
                        
                        enemy.update_animations(enemy.animations_types.index("HURT"), 160) #Hurt animation
                        
                elif not enemy.alive: #enemy is dead
                                
                        enemy.update_animations(enemy.animations_types.index("DEATH"), 80) #Death animation
                        
                else: #Nothing is happening
                        
                        enemy.update_animations(enemy.animations_types.index("IDLE"), 80) #Idle animation
        
        else: #For CampFire only
                enemy.update(player)

#Card action and animation
def card_action(cursor, pos, screen):

        for card in cards_in_hand: #iterate through hand 
        
                if begin_remove and card in erased: #identify which card is being removed
                        
                        card.update_animations(card.animations_types.index("RIP"), 88, cursor, pos) #Rip animation
                                
                        remove_card(card) #remove the card
        
                else:
                                  
                        card.hover(cursor, pos) #Continue Shine animation for every other card
                
                card.draw(screen) #draw all cards in hand

#Draw the player and enemy card, attribute, hp, and healthbar
def draw_ui_info():
        
        global attribute_info, attribute_info_rect
        
        #enemy attribute text ex: Slow
        attribute_info = font.render(attribute, True, (0, 0, 0))

        attribute_info_rect = attribute_info.get_rect()
        
        #attribute position relative to the enemy card's position
        attribute_info_rect.x = enemy_character_card_rect.centerx + 188 - attribute_info_rect.width / 2
                
        attribute_info_rect.y = enemy_character_card_rect.bottom - attribute_info_rect.height / 2
        
        #attribute icon's position      
        attribute_icon_rect.x = attribute_info_rect.right + 5
                
        attribute_icon_rect.y = enemy_character_card_rect.bottom - attribute_icon.height / 2
        
        #draw the player card
        screen.blit(player_character_card, (player_character_card_rect.center))
        
        #draw the player's hp and healthbar             
        player_hp.draw(screen, player.hp, player_hp.info(f"HP: {player.hp}", font, (255, 0, 0), player_character_card_rect.centerx + 160, player_character_card_rect.centery + 223))
        
        #draw the player's name
        screen.blit(player.name_text, (player.name_text_rect.width, player.rect.y + 5))
        
        #draw the player's info
        screen.blit(player_info, (player_character_card_rect.centerx + 191 - player_info_rect.width / 2, player_character_card_rect.bottom - 15))
        
        #draw the enemy card, name, hp and healthbar, and info
        if map.position.type_text != "Rest": #only when player is battling
                
                screen.blit(enemy_character_card, (enemy_character_card_rect.center))
                        
                enemy_hp.draw(screen, enemy.hp, enemy_hp.info(f"HP: {enemy.hp}", font, (255, 0, 0), enemy_character_card_rect.centerx * 1.18, enemy_character_card_rect.bottom + 30))
                        
                screen.blit(enemy.name_text, (enemy_character_card_rect.centerx + 188 - enemy.name_text_rect.width / 2, 25))
                        
                screen.blit(attribute_info, (attribute_info_rect))
                        
                screen.blit(attribute_icon, (attribute_icon_rect))

#Overlay the screen with either the map or defeat screen
def draw_map_defeat_screen(cursor, pos):
        
        global game_state, prevent_selection

        if not enemy.alive and enemy.animation_complete: #player won the battle, moving onto the next
                
                game_state = 1
                
                screen.fill((120, 170, 200)) #light blue color
                
                map.draw(screen) #draw the map on screen
                
                map.visible = True #map is now visible i.e that user can see it
                
                map.hover(cursor, pos)
                
        elif not player.alive and player.animation_complete: #player lost the battle
                
                screen.fill((0, 0, 0)) #black
                
                #draw in the defeat plate
                screen.blit(defeat_plate, ((WIDTH - defeat_plate.width) / 2, HEIGHT / 2 - defeat_plate.height + 75))
                
                try_again_button.visible = True #try again button is now visible
                        
                quit_button.visible = True #quit button is now visible
        
        if game_state != 0: #if we are in the defeat or map screen
           
                attack_button.visible = False #attack button is not visible
                
                discard_button.visible = False #discard button is not visible
                
                prevent_selection = True #cards are not clickable

#Change the fullness of the deck depending on how many cards are left
def draw_deck_fullness():
        
        global deck_image
        
        if remaining_card <= 13:
        
                deck_image = fourth_deck
                
        elif remaining_card <= 26:
                
                deck_image = half_deck

        elif remaining_card <= 39:
                
                deck_image = three_fourth_deck
                
        else:
                deck_image = full_deck
                
        screen.blit(deck_image, (WIDTH - 190, HEIGHT - 125))     

#Enable/Disable the attack and discard button
def button_availability():
        
        #the player has not select any card or the player cannot select any card  
        if not selected_card or prevent_selection:
                        
                attack_button.disable() #disable the button
        
                discard_button.disable() #disable the button
                           
        else:
                attack_button.enable() #enable the button

                discard_button.enable() #enable the button
                
        if amount_discard == 0: #player ran out of discard
                
                discard_button.disable()

#Display what the attribute means when the player hover over the icon
def attribute_info_hover(cursor, pos):
        
        #check if player is hovering over the icon 
        if attribute_icon_mask.overlap(cursor, (pos[0] - attribute_icon_rect.x, pos[1] - attribute_icon_rect.y)):
                
                attribute_text = font.render(attribute_icon_text, True, (0, 0, 0)) #text for what the icon means
                
                attribute_text_width = attribute_text.width #get the text width
                
                attribute_text_height = attribute_text.height #get the text height
                
                box_width = attribute_text_width + 40 #create a box with a width relative to the text width
                
                box_height = attribute_text_height + 5 #same thing but for height
                
                #the rectangular box and its attribute
                box_rect =  pygame.Rect(attribute_icon_rect.x - box_width - 2, enemy_character_card_rect.bottom - attribute_info_rect.height / 2, box_width, box_height)
                
                #draw the box in
                pygame.draw.rect(screen, (255, 255, 255), box_rect, border_radius=8)
                
                screen.blit(attribute_text, (box_rect.x + 20, box_rect.y)) #draw the text in the box

#--------------------Defined Game Variable--------------------#

#the map that the player will see
map = Map([
        
        Node(WIDTH / 15, HEIGHT - 100, "A", [], "Encounter"),
        
        Node(WIDTH / 4, HEIGHT - 100, "B", [0], "Encounter"),
             
        Node(WIDTH / 2, HEIGHT - 150, "C", [1], "Rest"),
        
        Node(WIDTH / 1.5, HEIGHT - 200, "D", [2], "Encounter"),       
        
        Node(WIDTH - 250, HEIGHT - 100, "E", [2], "Mini-Boss"),

        Node(WIDTH - 200, HEIGHT - 250, "F", [3, 4], "Encounter"),
        
        Node(WIDTH - 75, HEIGHT - 300, "G", [5], "Rest"),
        
        Node(WIDTH - 300, HEIGHT - 600, "H", [6], "Encounter"),
        
        Node(WIDTH / 1.5, HEIGHT - 350, "I", [7], "Rest"),

        Node(WIDTH / 2, HEIGHT - 300, "J", [8], "Encounter"),
        
        Node(WIDTH / 2, HEIGHT - 550, "K", [8], "Mini-Boss"),
        
        Node(WIDTH / 4, HEIGHT - 350, "L", [9, 10], "Encounter"),

        Node(WIDTH / 13, HEIGHT - 500, "M", [11], "Encounter"),

        Node(WIDTH / 3, HEIGHT - 600, "N", [12], "Rest"),

        Node(WIDTH / 10, HEIGHT - 730, "O", [12], "Mini-Boss"),

        Node(WIDTH / 2, HEIGHT - 750, "P", [13, 14], "Rest"),

        Node(WIDTH - 200, HEIGHT - 775, "Q", [15], "Boss"),

        ]
)

player = Character(0, 0, 100, 0, 5, "Player", "Samurai", False, 96) #the player character

player_hp = HealthBar(player.max_hp, player.hp)

#player's position
player.rect.x = WIDTH / 2 - player.width * 1.3

player.rect.y = HEIGHT / 2 - player.height + 100

#--------------------Game Loop--------------------#

new_run(map.position.type_text) #start the game

#game loop
if __name__ == "__main__":
        while run:
                                
                clock.tick(FPS) 
                                
                screen.blit(background, (0,0))
                
                damage_text_group.update() 

                #draw in sprite group to screen
                damage_text_group.draw(screen)
                                
                combo_extra_damage.draw(screen)
                
                combo_extra_damage_text.draw(screen)
                
                #remaining card and drawing it in
                remaining_card = len(deck) - len(used_cards) - len(cards_in_hand)
                
                deck_amount = font.render(f"{remaining_card} / 52", True, (0, 0, 0), (255, 255, 255))
                
                screen.blit(deck_amount, (WIDTH - 240, (HEIGHT - 125) + full_deck_rect.centery - 15))
                
                draw_deck_fullness()
                
                draw_ui_info()
                
                pos = pygame.mouse.get_pos()
                
                attribute_info_hover(cursor_mask, pos)
                
                pygame.mouse.set_visible(False)
                        
                card_action(cursor_mask, pos, screen)

                player_action()        
                
                enemy_action()
                                
                button_availability()
                
                #display the amount of turn left                
                amount_turn_box =  pygame.Rect(game_info(f"Turn Left: {amount_turn}", font, (0, 0, 0), WIDTH / 2 - 50, HEIGHT - 760))
                
                pygame.draw.rect(screen, (255, 255, 255), amount_turn_box, border_radius=8)
                
                game_info(f"Turn Left: {amount_turn}", font, (0, 0, 0), amount_turn_box.x, amount_turn_box.y)
                
                for event in pygame.event.get():
                        
                        manager.process_events(event)
                        
                        if event.type == pygame.QUIT:
                                
                                run = False
                                
                        if bonus_dmg_text: #execute total damage calculation
                                
                                total_damage_calculation()
                                
                                is_discard = False           
                        
                        if event.type == pygame_gui.UI_BUTTON_PRESSED: #if one of the button is pressed
                                
                                if hasattr(event, 'ui_element'):
                                
                                        if event.ui_element == attack_button: #attack is clicked
                                                
                                                #original damage before the cards are counted
                                                total_damage = extra_damage.damage #ex: Double = 20
                                                                                        
                                                combo_extra_damage_text.empty()
                        
                                                combo_extra_damage.empty()
                                                                                        
                                                eliminate_card()
                                                
                                                combo_extra_damage_text.add(text, extra_damage)
                                                
                                                bonus_dmg_text = True
                                                
                                                prevent_selection = True

                                                pygame.time.set_timer(CARD_EVENT, 1000) #start calculating total damage
                                                
                                        elif event.ui_element == discard_button: #discard button is clicked
                                                                        
                                                is_discard = True #we are discarding
                                                
                                                amount_discard -= 1
                                                
                                                for card in selected_card: #add all selected card into erased list
                                                        
                                                        erased.append(card)

                                                #begins removing
                                                pygame.time.set_timer(REMOVE_EVENT, 88)
                                                
                                                prevent_selection = True
                                                
                                                begin_remove = True
                                        
                                        elif event.ui_element == try_again_button: #try again button
                                                
                                                quit_button.visible = False
                                                
                                                try_again_button.visible = False
                                                                                        
                                                player.reset(100) #reset the player
                                                
                                                map.reset() #reset the map
                                                
                                                new_run(map.position.type_text) #new game
                                        
                                        elif event.ui_element == quit_button: #quit button
                                                
                                                run = False #close the program
                                                        
                        if event.type == pygame.MOUSEBUTTONDOWN: #if the player is clicking their mouse
                                
                                for card in cards_in_hand:
                                        
                                        #if the card is being hovered, we can select the card, and we are resting
                                        if card.hover(cursor_mask, pos) and not prevent_selection and map.position.type_text != "Rest":

                                                #card has not been clicked, add the card
                                                if card.clicked() and card not in selected_card:

                                                        selected_card.append(card)
                                                
                                                #card is clicked, remove the card (see comment Card class)
                                                if not card.click and card in selected_card:

                                                        selected_card.remove(card)

                                                #every time a card is click, check for combo
                                                combo_extra_damage.empty()
                                                
                                                combo.clear()
                                                
                                                combo_detection()
                                                
                                if map.visible: #user can see the map
                                        
                                        map.click(cursor_mask, pos)
                                
                                        if map.node_click: #if one of the node is clicked
                                                
                                                new_run(map.position.type_text) #new battle
                                                                                        
                player.draw(screen)
                
                enemy.draw(screen)
                
                #draw in the amount of discard left    
                pygame.draw.circle(screen, (80, 163, 246), (discard_button_rect.x + 105, discard_button_rect.y + 25), 15)
                                                
                game_info(f"{amount_discard}", font, (255, 0, 0), discard_button_rect.x + 100, discard_button_rect.y + 12)
                
                draw_map_defeat_screen(cursor_mask, pos)
                
                manager.update(FPS)
                
                manager.draw_ui(screen) #draw in all ui element (buttons)
                
                screen.blit(cursor, pos) #draw the cursor sprite at mouse position
                
                pygame.display.update() 
        
pygame.quit()