import pygame
import sys
import random

# ---------- Init ----------
pygame.init()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ClashCycle: Hero vs Monster (Pygame)")
clock = pygame.time.Clock()

# Fonts
FONT = pygame.font.SysFont(None, 24)
BIG = pygame.font.SysFont(None, 36)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HP_GREEN = (60, 180, 75)
MANA_BLUE = (50, 130, 200)
MON_RED = (200, 60, 60)
GRAY = (40, 40, 40)

# ---------- Helpers ----------
def draw_text(surf, text, x, y, font=FONT, color=WHITE):
    img = font.render(text, True, color)
    surf.blit(img, (x, y))

def draw_centered_text(surf, text, y, font=BIG, color=WHITE):
    img = font.render(text, True, color)
    rect = img.get_rect(center=(WIDTH // 2, y))
    surf.blit(img, rect)

def draw_bar(surf, x, y, w, h, pct, fg_color, bg_color=(80,80,80)):
    # pct is 0..100
    pygame.draw.rect(surf, bg_color, (x, y, w, h))
    fill_w = int(w * max(0, min(100, pct)) / 100)
    if fill_w > 0:
        pygame.draw.rect(surf, fg_color, (x, y, fill_w, h))
    # Thicker, more visible border
    pygame.draw.rect(surf, WHITE, (x, y, w, h), 3)

def draw_main_menu(selected_difficulty=None):
    #screen.fill(GRAY)
    screen.fill((50, 50, 50))
    #screen.blit(pygame.transform.scale(pygame.image.load('solo.jpg'), (WIDTH, HEIGHT)), (0, 0))
    draw_centered_text(screen, "ClashCycle: Hero vs Monster", 80)
    draw_centered_text(screen, "Select Difficulty: ", HEIGHT // 2 - 80, font=FONT)
    draw_centered_text(screen, " 1) Easy", HEIGHT // 2 - 50, font=FONT)
    draw_centered_text(screen, " 2) Normal", HEIGHT // 2 - 20, font=FONT)
    draw_centered_text(screen, " 3) Hard", HEIGHT // 2 + 10, font=FONT)
    if selected_difficulty is not None:
        draw_centered_text(screen, f"Selected: {selected_difficulty}", HEIGHT // 2 + 20, font=BIG)
        draw_centered_text(screen, "Press Enter to Play", HEIGHT // 2 + 70, font=BIG)
    else:
        draw_centered_text(screen, "Choose difficulty (1-3), then press Enter to start", HEIGHT // 2 + 80, font=BIG)
    draw_text(screen, "Press ESC to quit", WIDTH - 160, 10)
def draw_game_over(hero_hp,monster_hp):
    screen.fill(GRAY)
    #screen.blit(pygame.transform.scale(pygame.image.load('solo.jpg'), (WIDTH, HEIGHT)), (0, 0))
    if monster_hp <= 0 and hero_hp > 0:
        result_text = "You Win 🎉 You Defeated the Monster"
    else:
        result_text = "You Lose 💀 It Defeated the Hero"

    draw_centered_text(screen, result_text, HEIGHT // 2 - 60, font=BIG, color=WHITE)
    draw_centered_text(screen, "GAME OVER", HEIGHT // 2 - 20, font=BIG)
    draw_centered_text(screen, "Press R to Restart or ESC to Quit", HEIGHT // 2 + 20, font=FONT)

# ---------- Game logic functions (converted from your original code) ----------
def use_potion(hero_hp, potion):
    heal = random.randint(30, 35)
    hero_hp = min(100, hero_hp + heal)
    potion -= 1
    msg = f"Used Potion: +{heal} HP!"
    return hero_hp, potion, msg

def use_superbean(hero_power, superbean):
    boost = random.randint(20, 27)
    hero_power = min(100, hero_power + boost)
    superbean -= 1
    msg = f"Used Superbean: +{boost} Mana!"
    return hero_power, superbean, msg

def hero_action(choice, hero_hp, hero_power, monster_hp, potion, superbean, infinity_active):

    msg = ""
    if choice == "1":  # Normal Attack
        damage = random.randint(8, 13)
        monster_hp = max(0, monster_hp - damage)
        # small chance to find item
        if random.random() < 0.35:
            potion += 1
            msg = f"Normal attack dealt {damage}. You found a Potion!"
        else:
            superbean += 1
            msg = f"Normal attack dealt {damage}. You found a Superbean!"
    elif choice == "2":  # Thunder Fang
        if hero_power >= 15:
            damage = random.randint(15, 19)
            hero_power = max(0, hero_power - 15)
            monster_hp = max(0, monster_hp - damage)
            if random.random() < 0.35:
                potion += 1
                msg = f"Thunder Fang {damage} dmg. Found a Potion!"
            else:
                superbean += 1
                msg = f"Thunder Fang {damage} dmg. Found a Superbean!"
        else:
            msg = "Not enough Mana for Thunder Fang."
    elif choice == "3":  # Inferno Edge
        if hero_power >= 20:
            damage = random.randint(19, 25)
            hero_power = max(0, hero_power - 20)
            monster_hp = max(0, monster_hp - damage)
            if random.random() < 0.35:
                potion += 1
                msg = f"Inferno Edge {damage} dmg. Found a Potion!"
            else:
                superbean += 1
                msg = f"Inferno Edge {damage} dmg. Found a Superbean!"
        else:
            msg = "Not enough Mana for Inferno Edge."
    elif choice == "4":  # Activate Infinity
        if infinity_active == 0:
            if hero_power >= 30:
                infinity_active = 2
                hero_power = max(0, hero_power - 30)
                msg = "Infinity activated! (Blocks next 2 attacks)"
            else:
                msg = "Not enough Mana to activate Infinity."
        else:
            msg = "Infinity already active."
    elif choice == "5":  # Excalibur
        if hero_power >= 50:
            damage = random.randint(39, 50)
            hero_power = max(0, hero_power - 50)
            monster_hp = max(0, monster_hp - damage)
            if random.random() < 0.35:
                potion += 1
                msg = f"EXCALIBUR {damage} dmg. Found a Potion!"
            else:
                superbean += 1
                msg = f"EXCALIBUR {damage} dmg. Found a Superbean!"
        else:
            msg = "Not enough Mana for Excalibur."
    elif choice == "6":  # Use Potion
        if potion > 0:
            hero_hp, potion, potion_msg = use_potion(hero_hp, potion)
            msg = potion_msg
        else:
            msg = "No Potion left."
    elif choice == "7":  # Use Superbean
        if superbean > 0:
            hero_power, superbean, sb_msg = use_superbean(hero_power, superbean)
            msg = sb_msg
        else:
            msg = "No Superbean left."
    else:
        # Bad input - small penalty
        damage = random.randint(8, 12)
        hero_hp = max(0, hero_hp - damage)
        msg = f"Invalid move! You fumbled and took {damage} damage."

    # keep stats in range
    hero_hp = max(0, min(100, hero_hp))
    hero_power = max(0, min(100, hero_power))
    monster_hp = max(0, min(100, monster_hp))
    return hero_hp, hero_power, monster_hp, potion, superbean, infinity_active, msg

def monster_action(hero_hp, monster_hp, infinity_active,monster_damage_mult=1.0):

    # 20% chance to heal itself
    if random.random() < 0.2:
        heal = random.randint(10, 25)
        monster_hp = min(100, monster_hp + heal)
        return hero_hp, monster_hp, infinity_active, f"Monster regenerates +{heal} HP!"

    # Infinity blocks
    if infinity_active > 0:
        infinity_active -= 1
        return hero_hp, monster_hp, infinity_active, f"Infinity blocked the attack! (blocks left: {infinity_active})"

    attack = random.choice(["Fiery Breath", "Tail Whip", "Claw Frenzy", "Shadow Roar", "Meteor Slam"])
    if attack == "Fiery Breath":
        damage = random.randint(11, 16)
    elif attack == "Tail Whip":
        damage = random.randint(10, 17)
    elif attack == "Claw Frenzy":
        damage = random.randint(12, 18)
    elif attack == "Shadow Roar":
        damage = random.randint(10, 15)
    else:  # Meteor Slam
        damage = random.randint(20, 30)
    hero_hp = max(0, hero_hp - int(damage * monster_damage_mult))
    #hero_hp = max(0, hero_hp - damage)
    return hero_hp, monster_hp, infinity_active, f"{attack} hit you for {damage} damage!"

# ---------- Main loop + state machine ----------
def run_game():
    # initial stats
    hero_hp = 100
    hero_power = 100
    monster_hp = 100
    potion = 0
    superbean = 0
    infinity_active = 0
    difficulty = None

    # state management
    state = "menu"   # menu, player_turn, waiting, game_over
    last_message = "Press Enter to Start"
    message_end = 0
    first_msg = 0
    post_action = None  # 'monster' or 'after_mon'

    running = True
    while running:
        now = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                # Universal keys
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break

                if state == "menu":
                    draw_main_menu(difficulty)
                    # select difficulty with 1/2/3
                    if event.key == pygame.K_1:
                        difficulty = "Easy"
                        monster_hp_base = 100
                        monster_damage_mult = 0.8
                        drop_rate = 0.5
                        hero_bonus_hp = 10
                        last_message = "Selected Easy. Press Enter to start."
                    elif event.key == pygame.K_2:
                        difficulty = "Normal"
                        monster_hp_base = 100
                        monster_damage_mult = 1.0
                        drop_rate = 0.35
                        hero_bonus_hp = 0
                        last_message = "Selected Normal. Press Enter to start."
                    elif event.key == pygame.K_3:
                        difficulty = "Hard"
                        monster_hp_base = 150
                        monster_damage_mult = 1.2
                        drop_rate = 0.25
                        hero_bonus_hp = -5
                        last_message = "Selected Hard. Press Enter to start."
                    elif event.key == pygame.K_RETURN:
                        if difficulty is None:
                            last_message = "Pick a difficulty first (press 1, 2, or 3)."
                        else: # start game with selected difficulty
                             hero_hp = max(0, min(100, 100 + hero_bonus_hp))
                             hero_power = 100
                             monster_hp = monster_hp_base
                             potion, superbean, infinity_active = 0, 0, 0
                             state = "player_turn"
                             last_message = f"Game start ({difficulty})! Choose a move (1-7)."
                             message_end = now + 1000

                elif state == "player_turn":
                    # map 1-7 keys to choices
                    keymap = {
                        pygame.K_1: "1", pygame.K_2: "2", pygame.K_3: "3",
                        pygame.K_4: "4", pygame.K_5: "5", pygame.K_6: "6",
                        pygame.K_7: "7"
                    }
                    if event.key in keymap:
                        choice = keymap[event.key]
                        (hero_hp, hero_power, monster_hp,
                         potion, superbean, infinity_active, msg) = hero_action(
                            choice, hero_hp, hero_power, monster_hp, potion, superbean, infinity_active
                        )
                        last_message = msg
                        message_end = now + 1100
                        post_action = 'monster'   # after waiting, run monster
                        state = "waiting"
                elif state == "game_over":
                    if event.key == pygame.K_r:
                        # restart
                        hero_hp, hero_power, monster_hp = 100, 100, 100
                        potion, superbean, infinity_active = 0, 0, 0
                        state = "player_turn"
                        last_message = "Restarted! Choose a move (1-7)."
                        message_end = now + 1000

        # Handle waiting timeouts and turn switching
        if state == "waiting" and now >= message_end:
            if post_action == 'monster':
                # check victory first
                if monster_hp <= 0:
                    last_message = "🎉 You defeated the monster!"
                    state = "game_over"
                    message_end = now + 1500
                else:
                    # monster acts
                    hero_hp, monster_hp, infinity_active, mon_msg = monster_action(hero_hp, monster_hp, infinity_active,monster_damage_mult)

                    last_message = mon_msg
                    message_end = now + 1300
                    post_action = 'after_mon'
                    state = "waiting"  # stay in waiting until monster message shows
            elif post_action == 'after_mon':
                # after monster message, go to player's turn (if alive)
                if hero_hp <= 0:
                    last_message = "💀 You were defeated..."
                    state = "game_over"
                    message_end = now + 1500
                else:
                    state = "player_turn"
                    last_message = "Your turn. Press 1-7."
                    # do not set message_end; show until player acts

        # ---------- Draw UI ----------
        screen.fill((12, 12, 20))
        # Title and instructions
        #screen.blit(pygame.transform.scale(pygame.image.load('solo.jpg'), (WIDTH, HEIGHT)), (0, 0))
        # Hero HP
        # Hero HP - bigger and more prominent
        draw_text(screen, "HERO HP:", 30, 70)
        draw_bar(screen, 120, 70, 300, 25, hero_hp, HP_GREEN)
        hp_text = f"{hero_hp}/100"
        hp_img = FONT.render(hp_text, True, WHITE)
        hp_rect = hp_img.get_rect(center=(120 + 300 // 2, 70 + 25 // 2))  # Center of bar
        screen.blit(hp_img, hp_rect)

        # Monster HP - bigger and more prominent
        draw_text(screen, "MONSTER HP:", WIDTH - 400, 70)  # Right side
        draw_bar(screen, WIDTH - 280, 65, 250, 25, monster_hp, MON_RED)
        monster_text = f"{monster_hp}/100"
        monster_img = FONT.render(monster_text, True, WHITE)
        monster_rect = monster_img.get_rect(center=(WIDTH - 280 + 250 // 2, 65 + 25 // 2))  # Use 250 instead of 300
        screen.blit(monster_img, monster_rect)

        # Mana - keep it smaller since it's less important
        draw_text(screen, "MANA:", 30, 95)
        draw_bar(screen, 120, 95, 200, 15, hero_power, MANA_BLUE)
        # Text INSIDE the bar
        mana_text = f"{hero_power}/100"
        mana_img = FONT.render(mana_text, True, WHITE)
        mana_rect = mana_img.get_rect(center=(120 + 200 // 2, 95 + 15 // 2))  # Center of mana bar
        screen.blit(mana_img, mana_rect)

        # Inventory
        draw_text(screen, f"Potions: {potion}", 30, 180)
        draw_text(screen, f"Superbeans: {superbean}", 160, 180)
        draw_text(screen, f"Infinity Blocks: {infinity_active}", 330, 180)

        # Show choices when in player turn
        draw_text(screen, "Enter Your Choice( 1 - 7 ): ", 30, 220)
        draw_text(screen, "1) Normal         2) Thunder Fang (15)  3) Inferno Edge (20)", 30, 250)
        draw_text(screen, "4) Infinity (30)  5) Excalibur    (50)  6) Potion            7) Superbean", 30, 280)
        # Show last message
        draw_text(screen, f"> {last_message}", 30, 320)

        # Show menu or game over screen hints
        if state == "menu":
            draw_main_menu()
        if state == "game_over":
            draw_game_over(hero_hp, monster_hp)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    run_game()