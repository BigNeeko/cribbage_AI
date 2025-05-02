#imports

import tkinter as tk
from tkinter import PhotoImage
from functools import partial
from PIL import Image, ImageTk
import random
import cards
from itertools import combinations
from collections import Counter


#constants
global MAXSCORE, MAXCOUNT
MAXSCORE = 121
MAXCOUNT = 31


#int variables
global count, player_column, opponent_column, o_points, p_points

count = 0
player_column = 0
opponent_column = 0
o_points = 0
p_points = 0


#lists
global crib, player_played_cards, opponent_played_cards, all_played_cards
crib = []
player_played_cards = []
opponent_played_cards = []
all_played_cards = []



window = tk.Tk()
window.title("Cribbage")
window.geometry("1400x800")
window.configure(bg="green")

#------------functions------------------

def cont():
    winner_frame.forget()
    menu_frame.pack(fill="both", expand=True)


def card_selection():
    for widget in start_frame.winfo_children():
        widget.destroy()

    select_deck = cards.Deck()
    select_deck.shuffle()
    full_deck = select_deck.cards.copy()

    selections = {
        "player_card": None,
        "opponent_card": None,
        "selected_buttons": {},
        "available_cards": full_deck.copy()
    }

    value_order = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
        '8': 8, '9': 9, '10': 10,
        'jack': 11, 'queen': 12, 'king': 13, 'ace': 1
    }

    result_label = tk.Label(start_frame, text="", font=("Helvetica", 25), bg="green", fg="white")
    result_label.config(text="Select a card, lowest gets first crib")
    result_label.grid(row=5, column=0, columnspan=13, pady=10)

    def reveal_card(btn, card_name):
        global dealer

        card_img = resize_cards(f'Card Images/{card_name}.png')
        btn.config(image=card_img, state="disabled")
        btn.image = card_img
        selections["player_card"] = card_name
        for other_btn in selections["selected_buttons"].values():
            other_btn.config(state="disabled")
        selections["available_cards"].remove(card_name)

        opponent_card = random.choice(selections["available_cards"])
        selections["opponent_card"] = opponent_card
        selections["available_cards"].remove(opponent_card)

        #Flip opponent card
        opp_btn = selections["selected_buttons"][opponent_card]
        opp_img = resize_cards(f'Card Images/{opponent_card}.png')
        opp_btn.config(image=opp_img, state="disabled")
        opp_btn.image = opp_img

        #Determine who goes first
        player_val = value_order[select_deck.get_value(card_name)]
        opponent_val = value_order[select_deck.get_value(opponent_card)]

        if player_val < opponent_val:
            winner = "Your crib first!"
            dealer = 'player'
        elif player_val > opponent_val:
            winner = "Opponent's crib first!"
            dealer = 'opponent'
        else:
            winner = "Tie, Pick again."

        result_label.config(text=winner)

        # Start if no tie
        if "tie" in winner.lower():
            start_frame.after(3000, lambda: (
                card_selection()
            ))

        else:
            start_frame.after(3000, lambda: (
                start_frame.forget(),
                game_frame.pack(fill="both", expand=True)
            ))
            new_round()
    #display deck

    for i in range(4):
        for j in range(13):
            index = i * 13 + j
            card_name = full_deck[index]
            btn = tk.Button(start_frame, image=card_back)
            btn.grid(row=i, column=j, padx=2, pady=2)
            btn.config(command=partial(reveal_card, btn, card_name))
            selections["selected_buttons"][card_name] = btn


def new_game():
    global o_points, p_points, dealer
    o_points = 0
    p_points = 0
    opponent_points.config(text="Opponent Points = " + str(o_points))
    player_points.config(text="Player Points = " + str(p_points))
    dealer = ''

    menu_frame.forget()
    start_frame.pack(fill="both", expand=True, padx=20, pady=40)

    card_selection()



def new_round():
    global all_played_cards, count, player_column, opponent_column
    player_column = 0
    opponent_column = 0
    count = 0

    crib_frame.grid_remove()
    cut_frame.grid_remove()

    all_played_cards.clear()
    crib.clear()
    crib_frame.config(text="Crib " + str(len(crib)) + ' cards')
    play_frame.config(text='Count = ' + str(count))

    global stage
    stage = 'crib'

    global deck
    deck = cards.Deck()
    deck.shuffle()

    global dealer

    global playerHand, opponentHand, player_images, opponent_images
    opponentHand = []
    playerHand = []
    player_images = []
    opponent_images = []

    playerHand.clear()
    opponentHand.clear()

    for widget in player_frame.winfo_children():
        widget.destroy()
    for widget in opponent_frame.winfo_children():
        widget.destroy()
    for widget in crib_frame.winfo_children():
        widget.destroy()
    for widget in cut_frame.winfo_children():
        widget.destroy()
    for widget in play_frame.winfo_children():
        widget.destroy()



    def give_player_cards():
        card = deck.deal()
        playerHand.append(card)
        card_img = resize_cards(f'Card Images/{card}.png')
        player_images.append(card_img)
        btn = tk.Button(player_frame, image=card_img)
        btn.config(command=partial(select_card, card, btn))
        btn.pack(side="left", padx=5)

        print("player has " + card)

    def give_opponent_cards():
        card = deck.deal()
        opponentHand.append(card)
        opponent_images.append(card_back)
        label = tk.Label(opponent_frame, image=card_back)
        label.pack(side="left", padx=5)

        print("opponent has " + card)

    if dealer == 'opponent':
        for i in range(6):
            give_player_cards()

            give_opponent_cards()

        info_label.config(text="Choose two cards to go \n"
                               "into the opponent's crib")


    elif dealer == 'player':
        for i in range(6):
            give_opponent_cards()

            give_player_cards()

        info_label.config(text="Choose two cards to \n"
                               "go into your crib")

    else:
        print('Invalid')


def exit_game():
    game_frame.forget()
    menu_frame.pack(fill="both", expand=True)


def select_card(card_name, button):

    global crib

    if stage == 'crib':

        if any(card_name == selected[0] for selected in crib):
            return

        if len(crib) < 2:
            crib.append(card_name)
            button.config(relief=tk.SUNKEN, bg="yellow")

        if len(crib) == 2:
            card1_name = crib[0].replace('_', ' ')
            card2_name = crib[1].replace('_', ' ')

            info_label.config(text=f"You are sending these \n"
                                   f" cards to the crib?\n "
                                   f"{card1_name}\n {card2_name}",
                              font=("Arial", 25))

            confirm_button.grid(row=1, column=0, pady=10)
            cancel_button.grid(row=1, column=1, pady=10)

    elif stage == 'play':
        play_card(card_name, button)

    else:
        print("invalid")


def minimax_play(opponent_hand, played_cards, current_count, depth, is_opponent_turn, alpha=float('-inf'),
                 beta=float('inf')):

    if depth == 0:
        return evaluate_position(played_cards, current_count), None

    if is_opponent_turn:
        best_score = float('-inf') #maximise points
        best_card = None

        for card in opponent_hand:
            card_value = card_point_value(card)

            if current_count + card_value > MAXCOUNT:
                continue

            new_count = current_count + card_value
            new_played = played_cards + [card]
            new_hand = opponent_hand.copy()
            new_hand.remove(card)

            immediate_points = calculate_immediate_points(new_played, new_count)

            score, _ = minimax_play(new_hand, new_played, new_count, depth - 1, False, alpha, beta)
            total_score = immediate_points + score

            if total_score > best_score:
                best_score = total_score
                best_card = card

            alpha = max(alpha, best_score)
            if beta <= alpha:
                break

        if not best_card:
            score, _ = minimax_play(opponent_hand, played_cards, current_count, depth - 1, False, alpha, beta)
            return score, None

        return best_score, best_card

    else:
        best_score = float('inf') #mimimise points
        possible_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

        for value in possible_values:
            if current_count + value > MAXCOUNT:
                continue

            new_count = current_count + value

            score, _ = minimax_play(opponent_hand, played_cards, new_count, depth - 1, True, alpha, beta)
            best_score = min(best_score, score)

            beta = min(beta, best_score)
            if beta <= alpha:
                break

        if best_score == float('inf'):
            score, _ = minimax_play(opponent_hand, played_cards, current_count, depth - 1, True, alpha, beta)
            return score, None

        return best_score, None

def evaluate_position(played_cards, current_count):
    score = 0

    if current_count == 15:
        score += 2
    elif current_count == MAXCOUNT:
        score += 2

    if len(played_cards) >= 2:
        last_card = played_cards[-1]
        last_rank = deck.get_value(last_card)

        pair_count = 1
        for i in range(len(played_cards) - 2, max(-1, len(played_cards) - 4), -1):
            if deck.get_value(played_cards[i]) == last_rank:
                pair_count += 1

        # pairs
        if pair_count == 2:
            score += 2
        elif pair_count == 3:
            score += 6
        elif pair_count == 4:
            score += 12

    #runs
    run_points = check_for_run(played_cards)
    score += run_points

    return score


def calculate_immediate_points(played_cards, current_count):
    points = 0

    #Check for fifteen or thirty-one
    if current_count == 15:
        points += 2
    elif current_count == MAXCOUNT:
        points += 2

    if len(played_cards) >= 2:
        points += check_for_pairs(played_cards)

    run_points = check_for_run(played_cards)
    points += run_points

    return points


def get_best_opponent_play(opponent_hand, played_cards, current_count):

    DEPTH = 5

    legal_cards = [card for card in opponent_hand
                   if current_count + card_point_value(card) <= MAXCOUNT]

    if not legal_cards:
        return None

    _, best_card = minimax_play(legal_cards, played_cards.copy(),
                                current_count, DEPTH, True)
    return best_card



def monte_carlo_discard(hand, simulations=300):
    best_discard = None
    best_score = float('-inf')

    d = cards.Deck()
    d.shuffle()
    sim_deck = deck.cards.copy()

    for discard_pair in combinations(hand, 2):
        keep = [card for card in hand if card not in discard_pair]
        score_total = 0

        for _ in range(simulations):
            available_cards = [c for c in sim_deck if c not in hand]
            starter = random.choice(available_cards)

            sim_crib = list(discard_pair) + random.sample(available_cards, 2)

            hand_score = monte_carlo_score_hand(keep + [starter])
            crib_score = monte_carlo_score_hand(sim_crib + [starter])

            if dealer == 'opponent':
                total = hand_score + crib_score

            else:
                total = hand_score - crib_score

            score_total += total

        avg_score = score_total / simulations

        if avg_score > best_score:
            best_score = avg_score
            best_discard = discard_pair

    return best_discard


def move_to_crib():
    global crib, playerHand

    for card_name in crib:
        if card_name in playerHand:
            playerHand.remove(card_name)


    back_label = tk.Label(crib_frame, image=card_back)
    back_label.pack(side="left", padx=5)

    discard = monte_carlo_discard(opponentHand)
    for card in discard:
        opponentHand.remove(card)
        crib.append(card)


        print(f"{card} has gone to the crib")

        display_sorted_hands()

    confirm_button.grid_remove()
    cancel_button.grid_remove()
    info_label.config(text="Cards sent to crib!")
    crib_frame.grid(row=1, column=1, pady=20)
    crib_frame.config(text="Crib " + str(len(crib)) + ' cards')

    cut_for_starter_card()



def cancel_crib_selection():
    crib.clear()
    confirm_button.grid_remove()
    cancel_button.grid_remove()
    info_label.config(text="Canceled. Pick again.")


def display_sorted_hands():
    for widget in player_frame.winfo_children():
        widget.destroy()
    for widget in opponent_frame.winfo_children():
        widget.destroy()




    for card in playerHand:
        card_img = resize_cards(f'Card Images/{card}.png')
        player_images.append(card_img)
        btn = tk.Button(player_frame, image=card_img)
        btn.config(command=partial(select_card, card, btn))
        btn.pack(side="left", padx=5)

    for card in opponentHand:
        card_img = resize_cards(f'Card Images/card_back.png')
        opponent_images.append(card_img)
        label = tk.Label(opponent_frame, image=card_img)
        label.pack(side="left", padx=5)





def sort_by_rank():
    value_order = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
        '8': 8, '9': 9, '10': 10,
        'jack': 11, 'queen': 12, 'king': 13, 'ace': 1
    }


    playerHand.sort(key=lambda card: value_order[deck.get_value(card)])
    display_sorted_hands()





def sort_by_suit():
    suit_order = {'hearts': 0, 'clubs': 1, 'diamonds': 2, 'spades': 3}
    value_order = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
        '8': 8, '9': 9, '10': 10,
        'jack': 11, 'queen': 12, 'king': 13, 'ace': 1
    }

    playerHand.sort(key=lambda card: (suit_order[deck.get_suit(card)], value_order[deck.get_value(card)]))

    display_sorted_hands()





def resize_cards(card):
    our_card_img = Image.open(card)

    our_card_resize_image = our_card_img.resize((90, 130))

    global our_card_image
    our_card_image = ImageTk.PhotoImage(our_card_resize_image)

    return our_card_image

card_back = resize_cards('Card Images/card_back.png')



def resize_cut_cards(card):
    our_card_img = Image.open(card)

    our_card_resize_image = our_card_img.resize((45, 65))

    global our_card_image
    our_card_image = ImageTk.PhotoImage(our_card_resize_image)

    return our_card_image

cut_card_back = resize_cut_cards('Card Images/card_back.png')



def check_winner(points, winner):
    if points >= MAXSCORE:
        game_frame.after(2000, lambda: (
            game_frame.forget(),
            winner_frame.pack(fill="both", expand=True),
            winner_label.config(text=winner + " reached 121 points!! \n"
                                              "Winner!!"),

        ))



def cut_for_starter_card():

    global stage, opponent_passed, player_passed
    stage = "play"
    opponent_passed = False
    player_passed = False

    global starter_card

    confirm_button.grid_remove()
    cancel_button.grid_remove()


    cut_frame.grid(row=1, column=2, rowspan=4, columnspan=2, pady=20, padx=20)

    if dealer == 'opponent':
        info_label.config(text="Pick the starter card")

        selections = {}

        def reveal_cut_card(btn, card_name):
            global starter_card
            starter_card = card_name
            card_img = resize_cards(f'Card Images/{card_name}.png')
            btn.config(image=card_img, state="disabled")
            btn.image = card_img

            for other_card_name, other_btn in selections.items():
                if other_btn != btn:
                    other_btn.destroy()

            info_label.config(text=f"You picked: \n"
                                   f"{starter_card.replace('_', ' ').title()}")

            check_for_jack()

            game_frame.after(2000, lambda: (
                cut_frame.grid(),
                go_button.grid(row=0, column=2, pady=10),
                info_label.config(text="Select a card \n"
                                       "in your hand")

            ))

        for index, card_name in enumerate(deck.cards):
            btn = tk.Button(cut_frame, image=cut_card_back)
            btn.grid(row=index // 8, column=index % 8, padx=2, pady=2)
            btn.config(command=partial(reveal_cut_card, btn, card_name))
            selections[card_name] = btn

    elif dealer == 'player':

        starter_card = random.choice(deck.cards)

        card_img = resize_cards(f'Card Images/{starter_card}.png')
        label = tk.Label(cut_frame, image=card_img)
        label.image = card_img
        label.grid(row=0, column=0, padx=2, pady=2)

        info_label.config(text=f"Opponent picked: \n"
                               f"{starter_card.replace('_', ' ').title()}")

        check_for_jack()

        game_frame.after(2000, lambda: (
            go_button.grid(row=0, column=2, pady=10),
            opponent_play()
        ))
    else:
        print("Invalid dealer.")


def check_for_jack():
    global p_points, o_points

    if deck.get_value(starter_card) == 'jack':
        if dealer == 'player':
            p_points += 2
            info_label.config(text="His Heels! You (Dealer) get 2 points!")
        else:
            o_points += 2
            info_label.config(text="His Heels! Opponent (Dealer) gets 2 points!")

        opponent_points.config(text="Opponent Points = " + str(o_points))
        player_points.config(text="Player Points = " + str(p_points))





def play_card(card_name=None, button=None):
    global count, p_points, player_turn, player_passed, opponent_passed,    player_column, player_played_cards, all_played_cards

    #No cards in hand
    if not playerHand:
        player_passed = True
        info_label.config(text="You have no cards left. You pass.")
        if no_cards():
            return
        if player_passed:
            handle_both_passed()
        player_turn = False
        game_frame.after(1000, opponent_play)
        return

    card_value = card_point_value(card_name)
    if count + card_value > MAXCOUNT:
        info_label.config(text="Card exceeds 31. Choose another.")
        return

    #Valid card play
    playerHand.remove(card_name)
    player_played_cards.append(card_name)
    all_played_cards.append(card_name)
    button.destroy()
    count += card_value

    points_scored, messages = score_play(all_played_cards)
    if points_scored > 0:
        p_points += points_scored
        check_winner(p_points, 'Player')
        info_label.config(text=" and ".join(messages) + "!")
        player_points.config(text="Player Points = " + str(p_points))

    play_frame.config(text='Count = ' + str(count))

    card_img = resize_cards(f'Card Images/{card_name}.png')
    label = tk.Label(play_frame, image=card_img)
    label.image = card_img
    label.grid(row=1, column=player_column, padx=5)
    player_column += 1

    if check_for_go('player'):
        handle_both_passed()

    player_passed = False
    player_turn = False
    if not no_cards():
        game_frame.after(1000, opponent_play)


def opponent_play():
    global count, o_points, player_turn, player_passed, opponent_passed, opponent_column, opponent_played_cards

    if not opponentHand:
        opponent_passed = True
        info_label.config(text="Opponent has no cards left. Opponent passes.")
        if no_cards():
            return
        if player_passed:
            handle_both_passed()
        player_turn = True
        return

    #Check if any card can be legally played
    can_play = False
    for card in opponentHand:
        if count + card_point_value(card) <= MAXCOUNT:
            can_play = True
            break

    if not can_play:
        opponent_passed = True
        info_label.config(text="Opponent cannot play. Opponent passes.")
        if player_passed:
            handle_both_passed()
            return
        player_turn = True
        return

    #Get best card using minimax
    best_card = get_best_opponent_play(opponentHand, all_played_cards, count)

    if best_card is None:
        #Opponent must pass
        opponent_passed = True
        info_label.config(text="Opponent cannot play. Opponent passes.")
        if player_passed:
            handle_both_passed()
        player_turn = True
        return

    #Play the best card
    card_value = card_point_value(best_card)
    if count + card_value > MAXCOUNT:
        opponent_passed = True
        info_label.config(text="Opponent cannot play. Opponent passes.")
        if player_passed:
            handle_both_passed()
        player_turn = True
        return

    #Valid play
    opponentHand.remove(best_card)
    opponent_played_cards.append(best_card)
    all_played_cards.append(best_card)
    display_sorted_hands()

    count += card_value

    points_scored, messages = score_play(all_played_cards)
    if points_scored > 0:
        o_points += points_scored
        check_winner(o_points, 'Opponent')
        info_label.config(text="Opponent scores " + " and ".join(messages) + "!")
        opponent_points.config(text="Opponent Points = " + str(o_points))

    play_frame.config(text='Count = ' + str(count))

    card_img = resize_cards(f'Card Images/{best_card}.png')
    label = tk.Label(play_frame, image=card_img)
    label.image = card_img
    label.grid(row=0, column=opponent_column, padx=5)
    opponent_column += 1


    if check_for_go('opponent'):
        handle_both_passed()

    if no_cards():
        return
    player_turn = True


def check_for_go(last_player):


    for card in playerHand:
        if count + card_point_value(card) <= MAXCOUNT:
            return False
    for card in opponentHand:
        if count + card_point_value(card) <= MAXCOUNT:
            return False


    if count < MAXCOUNT:
        if last_player == 'player':
            global p_points
            p_points += 1
            info_label.config(text="You get 1 point for last card!")
            player_points.config(text="Player Points = " + str(p_points))
            check_winner(p_points, 'Player')
        else:
            global o_points
            o_points += 1
            info_label.config(text="Opponent gets 1 point for last card!")
            opponent_points.config(text="Opponent Points = " + str(o_points))
            check_winner(o_points, 'Opponent')

    return True


def check_for_run(played_cards):
    if len(played_cards) < 3:  # minimum run of 3
        return 0

    rank_order = {'ace': 1, '2': 2, '3': 3, '4': 4, '5': 5,
                  '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
                  'jack': 11, 'queen': 12, 'king': 13}

    max_length = min(7, len(played_cards))  # Maximum 7 cards in a run during play

    # Try different lengths starting from the most recent cards
    for length in range(max_length, 2, -1):
        # Take the last 'length' cards in their played order
        recent_cards = played_cards[-length:]

        # Get ranks in the order they were played
        ranks = []
        for card in recent_cards:
            rank = deck.get_value(card)
            ranks.append(rank_order[rank])

        # Make a sorted copy to check if these numbers could form a run
        sorted_ranks = sorted(ranks)
        if sorted_ranks == list(range(min(sorted_ranks), max(sorted_ranks) + 1)):
            return length  # Found a run

    return 0

def check_for_pairs(played_cards):

    if len(played_cards) < 2:
        return 0

    #Get last card played and second to last card
    last_card = played_cards[-1]
    previous_card = played_cards[-2]

    #Get ranks of both cards
    last_rank = deck.get_value(last_card)
    previous_rank = deck.get_value(previous_card)


    #no match
    if last_rank != previous_rank:
        return 0

    #pair found
    matching_count = 2

    #Check if 3 or 4
    if len(played_cards) >= 3:
        third_last = deck.get_value(played_cards[-3])
        if third_last == last_rank:
            matching_count = 3
            if len(played_cards) >= 4:
                fourth_last = deck.get_value(played_cards[-4])
                if fourth_last == last_rank:
                    matching_count = 4

    if matching_count == 2:
        return 2  #One pair
    elif matching_count == 3:
        return 6  #Three of a kind
    elif matching_count == 4:
        return 12  #Four of a kind

    return 0


def score_play(played_cards):
    if not played_cards:
        return 0, []

    points = 0
    messages = []

    #Check for 15
    if count == 15:
        points += 2
        messages.append("Fifteen for 2")

    #Only check the last 4 cards for pairs/runs
    check_cards = played_cards[-4:] if len(played_cards) >= 4 else played_cards

    last_card = check_cards[-1]
    last_rank = deck.get_value(last_card)

    consecutive_matches = 1
    for i in range(len(check_cards) - 2, -1, -1):
        prev_rank = deck.get_value(check_cards[i])
        if prev_rank == last_rank:
            consecutive_matches += 1
        else:
            break  #Stop at first non-match

    #score based on consecutive matches
    if consecutive_matches == 2:
        points += 2
        messages.append("Pair for 2")
    elif consecutive_matches == 3:
        points += 6
        messages.append("Three of a kind for 6")
    elif consecutive_matches == 4:
        points += 12
        messages.append("Four of a kind for 12")

    #Check for 31
    if count == MAXCOUNT:
        points += 2
        messages.append("Thirty-one for 2")
        return points, messages


    return points, messages



def player_pass():
    global player_passed, opponent_passed, count, player_turn, player_played_cards, opponent_played_cards

    player_passed = True
    info_label.config(text="You passed.")

    if opponent_passed:
        info_label.config(text="Both passed. Count resets to 0.")
        count = 0
        play_frame.config(text='Count = ' + str(count))
        player_passed = False
        opponent_passed = False

        for widget in play_frame.winfo_children():
            widget.destroy()

    player_turn = False
    if not no_cards():
        game_frame.after(1000, opponent_play)



def card_point_value(card_name):
    rank = deck.get_value(card_name)
    if rank in ['jack', 'queen', 'king']:
        return 10
    elif rank == 'ace':
        return 1
    else:
        return int(rank)


def handle_both_passed():
    global count, all_played_cards
    count = 0
    all_played_cards = []
    for widget in play_frame.winfo_children():
        widget.destroy()
    play_frame.config(text='Count = 0')





def check_for_31(card_value):
    global count
    if count + card_value > MAXCOUNT:
        return False
    elif count + card_value == MAXCOUNT:
        for widget in play_frame.winfo_children():
            widget.destroy()
        return "score"
    else:
        # Check if this would be the last playable card
        if count + card_value < MAXCOUNT:
            temp_count = count + card_value
            # Check if any other cards could be played after this
            for card in playerHand + opponentHand:
                if card_point_value(card) + temp_count <= MAXCOUNT:
                    return True
        return True


def no_cards():
    if not playerHand and not opponentHand:
        info_label.config(text="All cards played.")
        game_frame.after(2000, show)
        return True
    return False


def show():
    global player_played_cards, opponent_played_cards, p_points, o_points, playerHand, opponentHand, dealer

    go_button.grid_remove()

    playerHand = player_played_cards.copy()
    opponentHand = opponent_played_cards.copy()


    player_played_cards.clear()
    opponent_played_cards.clear()



    info_label.config(text="Scoring hands now...")

    print(playerHand)
    print(opponentHand)

    print(score_hand(playerHand))
    print(score_hand(opponentHand))

    if dealer == 'player':

        new_p_points = score_hand(playerHand)
        game_frame.after(2000, lambda : (update_p_points(new_p_points)))

        new_o_points = score_hand(opponentHand)
        game_frame.after(2000, lambda: (update_o_points(new_o_points)))

        info_label.config(text="Opponent scored = " + str(new_o_points) + "\n"
                                   " you scored = " + str(new_p_points))

    else:
        new_o_points = score_hand(opponentHand)
        game_frame.after(2000, lambda : (update_o_points(new_o_points)))

        new_p_points = score_hand(playerHand)
        game_frame.after(2000, lambda: (update_p_points(new_p_points)))

        info_label.config(text="Opponent scored = " + str(new_o_points) +  "\n"
                                   " you scored = " + str(new_p_points))


    game_frame.after(3000, score_crib)






def update_p_points(points):
    global p_points
    p_points += points
    check_winner(p_points, 'Player')
    player_points.config(text="Player Points = " + str(p_points))



def update_o_points(points):
    global o_points
    o_points += points
    check_winner(o_points, 'Opponent')
    opponent_points.config(text="Opponent Points = " + str(o_points))


def score_crib():
    global o_points, p_points, dealer

    print(score_hand(crib))

    if dealer == 'opponent':
        new_o_points = score_hand(crib)
        update_o_points(new_o_points)
        opponent_points.config(text="Opponent Points = " + str(o_points))
        info_label.config(text="In their crib, opponent scored " + str(new_o_points))

        dealer = 'player'

    elif dealer == 'player':
        new_p_points = score_hand(crib)
        update_p_points(new_p_points)
        player_points.config(text="Player Points = " + str(p_points))
        info_label.config(text="In your crib, you scored, " + str(new_p_points))
        dealer = 'opponent'

    game_frame.after(2000, lambda : new_round())


def monte_carlo_score_hand(hand):
    global starter_card


    rank_order = {'ace': 1, '2': 2, '3': 3, '4': 4, '5': 5,
                  '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
                  'jack': 11, 'queen': 12, 'king': 13}

    scoring_values = []
    run_ranks = []

    for card in hand:
        rank = deck.get_value(card)
        run_ranks.append(rank_order[rank])
        scoring_values.append(card_point_value(card))

    scoring_values.sort()
    run_ranks.sort()

    fifteen_points = 0
    pair_points = 0
    flush_points = 0

    # Fifteens
    for r in range(2, len(scoring_values) + 1):
        for comb in combinations(scoring_values, r):
            if sum(comb) == 15:
                fifteen_points += 2

    #Runs
    def calculate_run_points(ranks):
        points = 0
        used_combos = set()

        for r in range(len(ranks), 2, -1):
            combos = combinations(enumerate(ranks), r)
            for combo in combos:
                indices, values = zip(*combo)
                sorted_vals = sorted(values)
                if sorted_vals == list(range(min(sorted_vals), max(sorted_vals) + 1)):
                    if indices not in used_combos:
                        used_combos.add(indices)
                        points += r
            if points:  #Stop at first (longest) runs found
                break

        return points

    run_points = calculate_run_points(run_ranks)

    # Pairs
    frequency = Counter(run_ranks)
    for cnt in frequency.values():
        if cnt == 2:
            pair_points += 2
        elif cnt == 3:
            pair_points += 6
        elif cnt == 4:
            pair_points += 12

    # Flushes
    suits = [deck.get_suit(c) for c in hand]
    if len(set(suits)) == 1:
        flush_points = 4

    total_points = fifteen_points + run_points + pair_points + flush_points
    return total_points



def score_hand(hand):

    fifteen_points = 0
    pair_points = 0
    flush_points = 0
    nobs_points = 0

    global starter_card

    starter_suit = deck.get_suit(starter_card)

    for card in hand:
        if deck.get_value(card) == 'jack' and deck.get_suit(card) == starter_suit:
            nobs_points = 1
            break

    hand.append(starter_card)

    print(hand)

    rank_order = {'ace': 1, '2': 2, '3': 3, '4': 4, '5': 5,
                  '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
                  'jack': 11, 'queen': 12, 'king': 13}

    scoring_values = []
    run_ranks = []

    for card in hand:
        rank = deck.get_value(card)
        run_ranks.append(rank_order[rank])
        scoring_values.append(card_point_value(card))


    scoring_values.sort()
    run_ranks.sort()





    # Fifteens
    for r in range(2, len(scoring_values) + 1):
        for comb in combinations(scoring_values, r):
            if sum(comb) == 15:
                fifteen_points += 2

    # Runs
    def calculate_run_points(ranks):
        points = 0
        used_combos = set()

        for r in range(len(ranks), 2, -1):
            combos = combinations(enumerate(ranks), r)
            for combo in combos:
                indices, values = zip(*combo)
                sorted_vals = sorted(values)
                if sorted_vals == list(range(min(sorted_vals), max(sorted_vals) + 1)):
                    if indices not in used_combos:
                        used_combos.add(indices)
                        points += r
            if points:  # Stop at first (longest) runs found
                break

        return points

    run_points = calculate_run_points(run_ranks)

    #Pairs
    frequency = Counter(run_ranks)
    for cnt in frequency.values():
        if cnt == 2:
            pair_points += 2
        elif cnt == 3:
            pair_points += 6
        elif cnt == 4:
            pair_points += 12

    # Flushes
    suits = [deck.get_suit(c) for c in hand]
    if len(set(suits)) == 1:
        flush_points = 4

    total_points = fifteen_points + run_points + pair_points + flush_points + nobs_points

    hand.pop()

    return total_points




#------------------------frames------------------#

#menu frame

menu_frame = tk.Frame(window,
                      bg='light blue',
                      width=1200,
                      height=800)
menu_frame.pack(fill="both", expand=True)

menu_label = tk.Label(menu_frame,
                      text="Cribbage Game",
                      font=('Arial', 50),
                      bg='light blue',
                      fg='black')
menu_label.pack(pady=20, padx=20)

start_button = tk.Button(menu_frame,
                         text="Start",
                         bd=2,
                         command=new_game,
                         width=6,
                         height=2,
                         font=('Arial', 30))
start_button.place(relx=0.5, rely=0.38, anchor='center')

exit_button = tk.Button(menu_frame,
                        text="Exit",
                        bd=2,
                        command=quit,
                        width=6,
                        height=2,
                        font=('Arial', 30))
exit_button.place(relx=0.5, rely=0.5, anchor='center')

#---------------------------------------------------#


#-----------------start frame-----------------#
start_frame = tk.Frame(window,
                       bg='green',
                       width=1200,
                       height=800)



#-----------------game frame-----------------#
game_frame = tk.Frame(window,
                      bg="#8c401f",
                      width=1200,
                      height=800)


#-----------------crib frame-----------------#

crib_frame = tk.LabelFrame(game_frame,
                           text="",
                           bg="darkgreen",
                           fg="white")
crib_frame.config(text="Crib " + str(len(crib)) + ' cards')


#---------- points frame-----------------#

points_frame = tk.LabelFrame(game_frame,
                             text="Points | Target = 121",
                             bg="blue",
                             fg="white")
points_frame.grid(row=0, column=2, columnspan=5, pady=20, padx=20)


opponent_points = tk.Label(points_frame,
                           text="Opponent Points = " +str(o_points),
                           fg="white",
                           bg="blue",
                           font=("Arial", 15))
opponent_points.pack(pady=10, padx=10)


player_points = tk.Label(points_frame,
                         text="Player Points = " + str(p_points),
                         fg="white",
                         bg="blue",
                         font=("Arial", 15))
player_points.pack(pady=10, padx=10)


#----------------cut frame-----------------#
cut_frame = tk.Frame(game_frame, bg="green")

info_label = tk.Label(game_frame,
                      bg="#8c401f",
                      text='',
                      font=('Arial', 25))
info_label.grid(row=3, column=1, pady=10, padx=10)



#-----------------player frame-----------------#


player_frame = tk.LabelFrame(game_frame,
                             text="Your hand",
                             bg="#8c401f",
                             bd=2)
player_frame.grid(row=3, column=0, ipadx=20, padx=20)


#-----------------opponent frame-----------------#

opponent_frame = tk.LabelFrame(game_frame,
                               text="Opponent's hand",
                               bg="#8c401f",
                               bd=2)
opponent_frame.grid(row=0, column=0, ipadx=20, padx=20, pady=20)

player_label = tk.Label(player_frame,
                        text='')
player_label.pack(pady=20)

opponent_label = tk.Label(opponent_frame,
                          text='',
                          background="white",
                          foreground="white")
opponent_label.pack(pady=20)


#-----------------play frame -----------------#


play_frame = tk.LabelFrame(game_frame,
                           text='Count = ' + str(count),
                           bd=2,
                           bg="green",
                           height=50,
                           width=50,
                           font=('Arial', 15))
play_frame.grid(row=1, rowspan=2, column=0, pady=20, padx=20)


#-----------button frame--------------–#


button_frame = tk.LabelFrame(game_frame, bg="#8c401f",)
button_frame.grid(row=4, column=0, pady=20, padx=20)

sort_rank_button = tk.Button(button_frame,
                             text="Sort by Rank",
                             command=sort_by_rank)
sort_rank_button.grid(row=0, column=0, pady=10)

sort_suit_button = tk.Button(button_frame,
                             text="Sort by Suit",
                             command=sort_by_suit)
sort_suit_button.grid(row=0, column=1, pady=10)

confirm_button = tk.Button(button_frame,
                           text="Confirm",
                           command=move_to_crib,
                           bg="darkred",
                           fg="black",
                           font=("Arial", 14))
confirm_button.grid_remove()

cancel_button = tk.Button(button_frame,
                          text="Cancel",
                          command=cancel_crib_selection,
                          bg="darkred",
                          fg="black",
                          font=("Arial", 14))
cancel_button.grid_remove()

exit_game_button = tk.Button(game_frame,
                             text="Exit",
                             command=exit_game)
exit_game_button.grid(row=5, column=0, pady=10)

go_button = tk.Button(button_frame,
                        text="Go",
                        command=player_pass,
                        bg="darkgrey",
                        fg="black",
                        font=("Arial", 14))
go_button.grid_remove()


#-----------------winner frame -----------------#

winner_frame = tk.Frame(window,
                        width=1200,
                        height=800,
                        bg='#FFD700')


winner_label = tk.Label(winner_frame,
                        text="Winner",
                        font=('Arial', 50),
                        fg='black',
                        bg='#FFD700')
winner_label.pack(pady=20, padx=20)



continue_button = tk.Button(winner_frame,
                            text="Continue",
                            command=cont)
continue_button.pack(pady=20, padx=20)


window.mainloop()
