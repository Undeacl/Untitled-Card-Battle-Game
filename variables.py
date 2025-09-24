import pygame, pygame_gui
import random

pygame.init()

WIDTH = 1200

HEIGHT = 800

FPS = 144

clock = pygame.time.Clock()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

#ui manager
manager = pygame_gui.UIManager((WIDTH,HEIGHT))

#attack button
attack_button = pygame_gui.elements.UIButton(pygame.Rect((WIDTH / 2.85, HEIGHT - 70), (100, 50)), manager=manager, text="Attack")

attack_button_rect = attack_button.get_abs_rect()

attack_button.visible = False

#discard button
discard_button = pygame_gui.elements.UIButton(pygame.Rect((WIDTH / 1.78, HEIGHT - 70), (100, 50)), manager=manager, text="Discard")

discard_button_rect = discard_button.get_abs_rect()

discard_button.visible = False

#Citation: Background Image by Nidhoggn https://opengameart.org/content/backgrounds-3
background = pygame.image.load("Images/background.png")

background = pygame.transform.scale(background, (WIDTH, HEIGHT))

#cursor image
cursor = pygame.image.load("Images/Cursor.png")

cursor_rect = cursor.get_rect()

cursor_mask = pygame.mask.from_surface(cursor)

run = True

#the card that is displayed on screen
cards_in_hand = []

#card deck. contain every card and their value except for jokers
deck = {
        
        "Clubs 2": {"value": 2, "suit": "Clubs"},
         
        "Clubs 3": {"value": 3, "suit": "Clubs"},
         
        "Clubs 4": {"value": 4, "suit": "Clubs"},
         
        "Clubs 5": {"value": 5, "suit": "Clubs"},
         
        "Clubs 6": {"value": 6, "suit": "Clubs"},
         
        "Clubs 7": {"value": 7, "suit": "Clubs"},
         
        "Clubs 8": {"value": 8, "suit": "Clubs"},
         
        "Clubs 9": {"value": 9, "suit": "Clubs"},
         
        "Clubs 10": {"value": 10, "suit": "Clubs"},
         
        "Clubs J": {"value": 11, "suit": "Clubs"},
         
        "Clubs Q": {"value": 12, "suit": "Clubs"},
         
        "Clubs K": {"value": 13, "suit": "Clubs"},
        
        "Clubs A": {"value": 14, "suit": "Clubs"},
        
         
        "Diamonds 2": {"value": 2, "suit": "Diamonds"},
         
        "Diamonds 3": {"value": 3, "suit": "Diamonds"},
         
        "Diamonds 4": {"value": 4, "suit": "Diamonds"},
         
        "Diamonds 5": {"value": 5, "suit": "Diamonds"},
         
        "Diamonds 6": {"value": 6, "suit": "Diamonds"},
         
        "Diamonds 7": {"value": 7, "suit": "Diamonds"},
         
        "Diamonds 8": {"value": 8, "suit": "Diamonds"},
         
        "Diamonds 9": {"value": 9, "suit": "Diamonds"},
         
        "Diamonds 10": {"value": 10, "suit": "Diamonds"},
         
        "Diamonds J": {"value": 11, "suit": "Diamonds"},
         
        "Diamonds Q": {"value": 12, "suit": "Diamonds"},
         
        "Diamonds K": {"value": 13, "suit": "Diamonds"},
        
        "Diamonds A": {"value": 14, "suit": "Diamonds"},
        
        
        "Hearts 2": {"value": 2, "suit": "Hearts"},
         
        "Hearts 3": {"value": 3, "suit": "Hearts"},
         
        "Hearts 4": {"value": 4, "suit": "Hearts"},
         
        "Hearts 5": {"value": 5, "suit": "Hearts"},
         
        "Hearts 6": {"value": 6, "suit": "Hearts"},
         
        "Hearts 7": {"value": 7, "suit": "Hearts"},
         
        "Hearts 8": {"value": 8, "suit": "Hearts"},
         
        "Hearts 9": {"value": 9, "suit": "Hearts"},
         
        "Hearts 10": {"value": 10, "suit": "Hearts"},
         
        "Hearts J": {"value": 11, "suit": "Hearts"},
         
        "Hearts Q": {"value": 12, "suit": "Hearts"},
         
        "Hearts K": {"value": 13, "suit": "Hearts"},
        
        "Hearts A": {"value": 14, "suit": "Hearts"},
        
         
        "Spades 2": {"value": 2, "suit": "Spades"},
         
        "Spades 3": {"value": 3, "suit": "Spades"},
         
        "Spades 4": {"value": 4, "suit": "Spades"},
         
        "Spades 5": {"value": 5, "suit": "Spades"},
         
        "Spades 6": {"value": 6, "suit": "Spades"},
         
        "Spades 7": {"value": 7, "suit": "Spades"},
         
        "Spades 8": {"value": 8, "suit": "Spades"},
         
        "Spades 9": {"value": 9, "suit": "Spades"},
         
        "Spades 10": {"value": 10, "suit": "Spades"},
         
        "Spades J": {"value": 11, "suit": "Spades"},
         
        "Spades Q": {"value": 12, "suit": "Spades"},
         
        "Spades K": {"value": 13, "suit": "Spades"},
        
        "Spades A": {"value": 14, "suit": "Spades"}
} 

#card that have already been used either to do damage or discard
used_cards = {}

#card that the player has selected
selected_card = []

#store all value that create a combo
combo = []

#store all unique value selected to check for sequence
sequence_check = []

#damage text sprite group. Use to display damage being dealt
damage_text_group = pygame.sprite.Group()

#combo text sprite group. Display what the combo is
combo_extra_damage_text = pygame.sprite.Group()

#combo damage sprite group. Display the damage of the combo
combo_extra_damage = pygame.sprite.Group()

#Citation: Font designed by Stefie Justprince https://fonts.google.com/specimen/Pixelify+Sans
font = pygame.font.Font("Font/Pixel_Font.ttf", 20)

#calculation event
CARD_EVENT = pygame.USEREVENT + 1

#removing card event
REMOVE_EVENT = pygame.USEREVENT + 2

#attack event
ATTACK_EVENT = pygame.USEREVENT + 3

#text for what the combo is
text = ""

#the combo damage
extra_damage = 0

#start or stop total damage calculation
bonus_dmg_text = False

#total damage = combo damage +  all applicable card value
total_damage = 0

#store the card(s) that's being remove
erased = []

#if there is a combo
combo_detected = False

#to begin removing the card or not
begin_remove = False

#prevent the user from selecting cards
prevent_selection = False

#begin the player attack sequence
begin_attack = False

#stop the attack sequence
finish_attack = False

#are we discarding
is_discard = None

#amount of turn before enemy attack. Some enemy have modifier that can change this amount
amount_turn = 2

#amount of discard the player has. Some enemy have modifier that can change this amount
amount_discard = 3

#a delay before an event happen
action_cooldown = 0

#how much the delay is
action_wait_time = 100

#the enemy
enemy = None

#enemy's health
enemy_hp = None

#info about the enemy, their attribute
enemy_info = None

#enemy stats and attribute
specific_for_enemy = {
        
        "Encounter": {
        
                "Bat": {
                                
                        "Resolution": 64,
                        
                        "Scale": 4,
                        
                        "Y_Offset": 50,
                        
                        "Flip": False,
                        
                        "Animation_Speed_Offset": 15,
                        
                        "HP": random.randrange(200, 300, 30),
                        
                        "Strength": random.randrange(4, 8),

                        "Attribute": "Fast",

                        "Attribute_Info": "-1 Turn",
                        
                        "Turn Modifier": - 1

                },
                
                "Golem": {
                                
                        "Resolution": 90,
                        
                        "Scale": 9,
                        
                        "Y_Offset": 300,
                        
                        "Flip": True,
                        
                        "Animation_Speed_Offset": 0,
                        
                        "HP": random.randrange(400, 600, 30),
                        
                        "Strength": random.randrange(10, 15),

                        "Attribute": "Slow",

                        "Attribute_Info": "+1 Turn",
                        
                        "Turn Modifier": 1
                },
                
                "Mushroom": {
                                
                        "Resolution": 80,
                        
                        "Scale": 3,
                        
                        "Y_Offset": 75,
                        
                        "Flip": False,
                        
                        "Animation_Speed_Offset": 0,
                        
                        "HP": random.randrange(200, 300, 30),
                        
                        "Strength": random.randrange(6, 10),

                        "Attribute": "No Change",

                        "Attribute_Info": "Normal"
                },
                
                
                "Skeleton": {
                                
                        "Resolution": 96,
                        
                        "Scale": 4,
                        
                        "Y_Offset": 150,
                        
                        "Flip": True,
                        
                        "Animation_Speed_Offset": 20,
                        
                        "HP": random.randrange(200, 300, 30),
                        
                        "Strength": 10,

                        "Attribute": "Fixed Dmg",

                        "Attribute_Info": "A fixed 10 Damage"
                },
                
                "Flying": {
                                
                        "Resolution": 64,
                        
                        "Scale": 4,
                        
                        "Y_Offset": 0,
                        
                        "Flip": False,
                        
                        "Animation_Speed_Offset": -125,
                        
                        "HP": random.randrange(200, 300, 30),
                        
                        "Strength": random.randrange(10, 15),

                        "Attribute": "Heavy",

                        "Attribute_Info": "Enemy Deals More Damage, -1 Discard",
                        
                        "Discard Modifier": - 1
                },
        },
        
        "Mini-Boss": {
        
                "Necro": {
                                
                        "Resolution": 160,
                        
                        "Scale": 4,
                        
                        "Y_Offset": 200,
                        
                        "Flip": True,
                        
                        "Animation_Speed_Offset": -20,
                        
                        "HP": random.randrange(300, 400, 20),
                        
                        "Strength": random.randrange(7, 15),

                        "Attribute": "Mini-Boss",

                        "Attribute_Info": "Defeating it gives a modifier (Not Yet Implemented)"
                },
        },
        
        "Boss": {
        
                "NightBorne": {
                
                        "Resolution": 80,
                        
                        "Scale": 6,
                        
                        "Y_Offset": 130,
                        
                        "Flip": True,
                        
                        "Animation_Speed_Offset": -20,
                        
                        "HP": random.randrange(600, 800, 30),
                        
                        "Strength": random.randrange(10, 15),

                        "Attribute": "Boss",

                        "Attribute_Info": "Enemy Deals More Damage, +1 Turn",
                        
                        "Turn Modifier": 1
                },
        }
}

#signify the beginning of card removal
begin_remove_animation = False

#Full deck image
full_deck = pygame.image.load("Images/Fullness/52.png")

full_deck_rect = full_deck.get_rect()

#3/4 full image
three_fourth_deck = pygame.image.load("Images/Fullness/39.png")

#1/2 full image
half_deck = pygame.image.load("Images/Fullness/26.png")

#1/4 full image
fourth_deck = pygame.image.load("Images/Fullness/13.png")

deck_image = None

#Citation:

#Referenced Used: Bonfire (Rest Icon) by Kaleb da Silva Pereira https://www.vecteezy.com/vector-art/9877856-pixel-art-bonfire-june-party-bonfire-vector-icon-for-8bit-game-on-white-background

#Referenced Used: Epic Skeleton Skull (Mini-Boss Icon) by TutsByKai https://www.youtube.com/watch?v=H_ZlJe-pERI
icon_dict = {
    
    "Encounter": {
    
        "image": pygame.image.load("Images/Map_Indicator/Encounter.png"),

        "radius_quotient": 3
    
    },
    
    "Rest": {
    
        "image": pygame.image.load("Images/Map_Indicator/Rest.png"),

        "radius_quotient": 1.8
    
    },
    
    "Mini-Boss": {
    
        "image": pygame.image.load("Images/Map_Indicator/Mini-Boss.png"),

        "radius_quotient": 2.5
    
    },
    
    "Boss": {
    
        "image": pygame.image.load("Images/Map_Indicator/Boss.png"),

        "radius_quotient": 2
    
    },
}

#the player card to house information
player_character_card = pygame.image.load("Images/Player_Info_Card.png")

player_character_card = pygame.transform.scale_by(player_character_card, 3)

player_character_card_rect = player_character_card.get_rect()

player_character_card_rect.center = player_character_card_rect.left - 72, player_character_card_rect.top - 99

#the enemy card to house information
enemy_character_card = pygame.image.load("Images/Enemy_Info_Card.png")

enemy_character_card = pygame.transform.scale_by(enemy_character_card, 3)

enemy_character_card_rect = enemy_character_card.get_rect()

enemy_character_card_rect.center = WIDTH - enemy_character_card_rect.right + 70, enemy_character_card_rect.top - 100

#attribute text
attribute = ""

#attribute text surface
attribute_info = font.render(attribute, True, (0, 0, 0))

attribute_info_rect = attribute_info.get_rect()

#player's attribute
player_info = font.render('Nothing Special', True, (0, 0, 0))

player_info_rect = player_info.get_rect()

#attribute icon image
attribute_icon = pygame.image.load("Images/Info.png")

attribute_icon_rect = attribute_icon.get_rect()

attribute_icon_mask = pygame.mask.from_surface(attribute_icon)

#what the attribute means
attribute_icon_text = ""

#defeat plate image
defeat_plate = pygame.image.load("Images/Defeat.png")

defeat_plate = pygame.transform.scale_by(defeat_plate , 3)

#try again button
try_again_button = pygame_gui.elements.UIButton(pygame.Rect((WIDTH / 2.85, HEIGHT / 2), (100, 50)), manager=manager, text="Try Again")

try_again_button_rect = try_again_button.get_abs_rect()

try_again_button.visible = False #visibility of the button

#quit button
quit_button = pygame_gui.elements.UIButton(pygame.Rect((WIDTH / 1.78, HEIGHT / 2), (100, 50)), manager=manager, text="Quit")

quit_button_rect = quit_button.get_abs_rect()

quit_button.visible = False #visibility of the button

game_state = 0 #0: normal, 1: win = map, -1: lost = defeat screen