# 🃏 Untitled Card Battle Game

![](https://github.com/Undeacl/Untitled-Game/blob/main/Images/Untitled%20Game%20Preview.gif)  

A strategic **card-based RPG game** inspired by [Balatro](https://store.steampowered.com/app/2379780/Balatro/) and [The Demon Hand](https://www.leagueoflegends.com/en-us/news/game-updates/the-demons-hand/) built with **Python** and **Pygame**. Players use a deck of cards to attack enemies, build combos, and progress through a dynamic map filled with encounters, rests, mini-bosses, and bosses.

---

## 🚀 Table of Contents
- [Features](#-features)  
- [Gameplay](#-gameplay)  
- [Controls](#-controls)  
- [Mechanics](#-mechanics)
- [What I Learned](#-what-i-learned)
- [Credit](#-credit)  

---

## ✨ Features
- Strategic card combat with **combo detection**.  
- Animated player and enemy characters (Idle, Attack, Hurt, Death).  
- Dynamic map with different node types: **Encounters**, **Rest Points**, **Mini-bosses**, **Bosses**.  
- Deck management with **card replacement** and **discard mechanics**.  
- Visual feedback for **damage**, **combos**, and **card effects**.  
- Rest/Campfire mechanic to **recover health** between battles.  

---

## 🎮 Gameplay
1. Start the game and choose a node on the map.  
2. Select cards from your hand to **perform attacks** or **discard** them strategically.  
3. Build combos to increase total damage:
   - Double, Triple, Quad, Full House, Sequence, Solo, Double Pair  
4. Attack enemies and survive battles to progress through the map.  
5. Manage your deck wisely — only **unused cards** are available for replacement.  
6. Rest at Campfire nodes to **recover health** and prepare for upcoming encounters.  

---

## ⌨ Controls
- **Mouse Click:** Select/deselect cards.  
- **Attack Button:** Execute an attack with selected cards.  
- **Discard Button:** Discard selected cards (limited by remaining discards).  
- **Map Click:** Choose the next node to start a new encounter.  

---

## ⚔ Mechanics
### Combo System
Combos are automatically detected based on selected cards:
- **Double:** Two cards of the same value  
- **Triple:** Three cards of the same value  
- **Quad:** Four cards of the same value  
- **Full House:** Three of a kind + a pair  
- **Sequence:** Consecutive card values (e.g., 2-3-4-5-6)  
- **Solo:** Single card selection  
- **Double Pair:** Two separate pairs  

### Card Management
- **Replacement:** Cards are replaced after use, drawn from the remaining deck.  
- **Discard:** Players can discard cards strategically, but discards are limited.  

### Player & Enemy Turns
- Player selects cards → calculates total damage → attacks.  
- Enemy attacks when the player’s turn ends.  
- Health bars and damage text provide visual feedback.  

### Rest Nodes
- Campfire nodes allow players to **skip combat** and recover health.  

---

## 📝 What I Learned
Through building this game, I furthered my experience in:  
- **Pygame basics:** Handling sprites, animations, and events.  
- **Object-Oriented Programming:** Structuring the game with classes like `Card`, `Character`, and `Map`.  
- **Game Logic:** Implementing card combos, turn-based mechanics, and enemy AI.  
- **UI Design:** Creating interactive buttons and visual feedback for damage and combos.  
- **Project Organization:** Managing multiple Python modules, assets, and global variables efficiently.  
- **Debugging & Optimization:** Fixing animation timing, preventing selection conflicts, and handling sprite updates efficiently.
  
---

## 🎨 Credit
**All sprites used in this project are credited to their respective authors:**
- [Background Image](https://opengameart.org/content/backgrounds-3) by Nidhoggn
- [Font](https://fonts.google.com/specimen/Pixelify+Sans) designed by Stefie Justprince
- Referenced Used: [Bonfire (Rest Icon)](https://www.vecteezy.com/vector-art/9877856-pixel-art-bonfire-june-party-bonfire-vector-icon-for-8bit-game-on-white-background) by Kaleb da Silva Pereira
- Referenced Used: [Epic Skeleton Skull (Mini-Boss Icon)](https://www.youtube.com/watch?v=H_ZlJe-pERI) by TutsByKai
- Referenced Used: [Bonfire (Rest)](https://www.vecteezy.com/vector-art/9877856-pixel-art-bonfire-june-party-bonfire-vector-icon-for-8bit-game-on-white-background) by Kaleb da Silva Pereira
- [Samurai Sprite](https://xzany.itch.io/samurai-2d-pixel-art) by Mattz Art
- [Necromancer Sprite](https://creativekind.itch.io/necromancer-free) by CreativeKind
- [NightBorne Warrior Sprite](https://creativekind.itch.io/nightborne-warrior) by CreativeKind
- [Skeleton Sprite](https://monopixelart.itch.io/skeletons-pack) by MonoPixelArt
- [Bat Sprite](https://monopixelart.itch.io/dark-fantasy-enemies-asset-pack) by MonoPixelArt
- [Golems Sprite](https://monopixelart.itch.io/golems-pack) by MonoPixelArt
- [Mushroom Sprite](https://monopixelart.itch.io/forest-monsters-pixel-art) by MonoPixelArt
- [Flying Monster Sprite](https://monopixelart.itch.io/flying-enemies) by MonoPixelArt
