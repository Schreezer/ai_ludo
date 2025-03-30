#DataFlair - Importing Modules.
from tkinter import *
from tkinter import messagebox
from PIL import Image,ImageTk
import time
from random import randint, choice

'''Ludo= Ludo_Game
canvas = board
Green_coin = Green_coin
Red_label = Red_label
Total_player = Total_player
Predict_BlockValue = Predict_BlockValue
block_number_side = Dice_side
 six_side_block,five_side_block,four_side_block,three_side_block,two_side_block,one_side_block =Dice_side_one, Dice_side_two, Dice_side_three, Dice_side_four, Dice_side_five, Dice_side_six
Red_coord = Red_coord
Position_Red_coin = Position_Red_coin
move_Red = move_Red
Six_overlap = Six_overlap
TakePermission = TakePermission
red_store_active = Active_Red_store
six_counter = Six_Counter
time_for = time_for
Robo = Robo
make_command() = Command_Maker()
delay_with_instrctions = delay_instruction
robo_judge = Robo_Judge
num_btns_state_controller - State_controller_Button
'''

class Ludo_Game:
    def __init__(self, root,Dice_side_one, Dice_side_two, Dice_side_three, Dice_side_four, Dice_side_five, Dice_side_six):
        self.window = root
        # Make board
        self.make_board = Canvas(self.window, bg="#1E1E1E", width=800, height=630)
        self.make_board.pack(fill=BOTH,expand=1)

        # Make some containers to store data
        self.Red_coin = []
        self.Green_coin = []
        self.Yellow_coin = []
        self.Blue_coin = []

        self.Red_label = []
        self.Green_label = []
        self.Yellow_label = []
        self.Blue_label = []

        self.Predict_BlockValue = []
        self.Total_player = []

        # Ludo block all side image store
        self.Dice_side = [Dice_side_one, Dice_side_two, Dice_side_three, Dice_side_four, Dice_side_five, Dice_side_six]

        # Use for store specific position of all coins
        self.Red_coord = [-1, -1, -1, -1]
        self.Green_coord = [-1, -1, -1, -1]
        self.Yellow_coord = [-1, -1, -1, -1]
        self.Blue_coord = [-1, -1, -1, -1]

        self.Position_Red_coin = [0, 1, 2, 3]
        self.Position_Green_coin = [0, 1, 2, 3]
        self.Position_Yellow_coin = [0, 1, 2, 3]
        self.Position_Blue_coin = [0, 1, 2, 3]

        for index in range(len(self.Position_Red_coin)):# Specific coin position set to -1 by default
            self.Position_Red_coin[index] = -1
            self.Position_Green_coin[index] = -1
            self.Position_Yellow_coin[index] = -1
            self.Position_Blue_coin[index] = -1

        # Number to room to be traverse by specific color coin, store in that variable
        self.move_Red = 0
        self.move_Green = 0
        self.move_Yellow = 0
        self.move_Blue = 0

        # Game state tracking
        self.TakePermission = 0
        self.time_for = -1
        
        # Fair play counters - apply to all players
        self.six_counts = {
            'red': 0,
            'blue': 0,
            'yellow': 0,
            'green': 0
        }
        
        # Turn management
        self.current_turn_sixes = 0  # Count sixes in current turn
        self.max_sixes_per_turn = 3  # Maximum allowed sixes per turn
        
        # AI Control
        self.Robo = 0
        self.ai = None
        
        # Import EasyAI when needed to avoid circular imports
        from easy_ai import EasyAI

        # By default some function call
        self.Board()

        self.Instructional_Button_Red()
        self.Instructional_Button_Blue()
        self.Instructional_Button_Yellow()
        self.Instructional_Button_Green()

        self.Initial_Control()

    def Board(self):
        # Cover Box made with colored paths
        self.make_board.create_rectangle(100, 15, 100 + (40 * 15), 15 + (40 * 15), width=6, fill="#F0F0F0")  # Light gray background

        # Colored paths for each quadrant
        # Red path (left)
        self.make_board.create_rectangle(100, 15+240, 100+240, 15+240+120, width=3, fill="#FFE6E6")
        # Green path (top)
        self.make_board.create_rectangle(100+240, 15, 100+240+120, 15+240, width=3, fill="#E6FFE6")
        # Blue path (bottom)
        self.make_board.create_rectangle(100+240, 15+240+120, 100+240+120, 15+240+240, width=3, fill="#E6E6FF")
        # Yellow path (right)
        self.make_board.create_rectangle(100+240+120, 15+240, 100+240+240, 15+240+120, width=3, fill="#FFFDE6")

        # Square box
        self.make_board.create_rectangle(100, 15, 100+240, 15+240, width=3, fill="red")# left up large square
        self.make_board.create_rectangle(100, (15+240)+(40*3), 100+240, (15+240)+(40*3)+(40*6), width=3, fill="blue")# left down large square
        self.make_board.create_rectangle(340+(40*3), 15, 340+(40*3)+(40*6), 15+240, width=3, fill="green")# right up large square
        self.make_board.create_rectangle(340+(40*3), (15+240)+(40*3), 340+(40*3)+(40*6), (15+240)+(40*3)+(40*6), width=3, fill="yellow")# right down large square

        # Left 3 box(In white region)
        self.make_board.create_rectangle(100, (15+240), 100+240, (15+240)+40, width=3)
        self.make_board.create_rectangle(100+40, (15 + 240)+40, 100 + 240, (15 + 240) + 40+40, width=3, fill="#F00000")
        self.make_board.create_rectangle(100, (15 + 240)+80, 100 + 240, (15 + 240) + 80+40, width=3)

        # right 3 box(In white region)
        self.make_board.create_rectangle(100+240, 15, 100 + 240+40, 15 + (40*6), width=3)
        self.make_board.create_rectangle(100+240+40, 15+40, 100+240+80, 15 + (40*6), width=3, fill="green")
        self.make_board.create_rectangle(100+240+80, 15, 100 + 240+80+40, 15 + (40*6), width=3)

        # up 3 box(In white region)
        self.make_board.create_rectangle(340+(40*3), 15+240, 340+(40*3)+(40*6), 15+240+40, width=3)
        self.make_board.create_rectangle(340+(40*3), 15+240+40, 340+(40*3)+(40*6)-40, 15+240+80, width=3, fill="yellow")
        self.make_board.create_rectangle(340+(40*3), 15+240+80, 340+(40*3)+(40*6), 15+240+120, width=3)

        # down 3 box(In white region)
        self.make_board.create_rectangle(100, (15 + 240)+(40*3), 100 + 240+40, (15 + 240)+(40*3)+(40*6), width=3)
        self.make_board.create_rectangle(100+240+40, (15 + 240)+(40*3), 100 + 240+40+40, (15 + 240)+(40*3)+(40*6)-40, width=3, fill="blue")
        self.make_board.create_rectangle(100 + 240+40+40, (15 + 240)+(40*3), 100 + 240+40+40+40, (15 + 240)+(40*3)+(40*6), width=3)

        # All left separation line
        X_Start = 100 + 40
        Y_Start = 15 + 240
        X_End = 100 + 40
        end_y = 15 + 240 + (40 * 3)
        for _ in range(5):
            self.make_board.create_line(X_Start, Y_Start, X_End, end_y, width=2)
            X_Start+=40
            X_End+= 40

        # All right separation line
        X_Start = 100+240+(40*3)+40
        Y_Start = 15 + 240
        X_End = 100+240+(40*3)+40
        Y_End = 15 + 240 + (40 * 3)
        for _ in range(5):
            self.make_board.create_line(X_Start, Y_Start, X_End, Y_End, width=2)
            X_Start += 40
            X_End += 40

        # All up separation done
        X_Start = 100+240
        Y_Start = 15+40
        X_End = 100+240+(40*3)
        Y_End = 15+40
        for _ in range(5):
            self.make_board.create_line(X_Start,Y_Start, X_End,Y_End, width=2)
            Y_Start += 40
            Y_End += 40

        # All down separation done
        X_Start = 100 + 240
        Y_Start = 15 + (40*6)+(40*3)+40
        X_End = 100 + 240 + (40 * 3)
        Y_End = 15 + (40*6)+(40*3)+40
        for _ in range(5):
            self.make_board.create_line(X_Start, Y_Start, X_End, Y_End, width=2)
            Y_Start += 40
            Y_End += 40

        # Square box(Coins containers) white region make
        self.make_board.create_rectangle(100+20, 15+40-20, 100 + 40 + 60 + 40 +60+20, 15+40+40+40+100-20, width=3, fill="white")
        self.make_board.create_rectangle(340+(40*3)+40 - 20, 15 + 40-20, 340+(40*3)+40 + 60 + 40 + 40+20+20, 15+40+40+40+100-20, width=3, fill="white")
        self.make_board.create_rectangle(100+20, 340+80-20+15, 100 + 40 + 60 + 40 +60+20, 340+80+60+40+40+20+15, width=3, fill="white")
        self.make_board.create_rectangle(340+(40*3)+40 - 20, 340 + 80 - 20+15, 340+(40*3)+40 + 60 + 40 + 40+20+20, 340 + 80 + 60 + 40 + 40 + 20+15, width=3, fill="white")

        # Left up square inside box made
        self.make_board.create_rectangle(100+40, 15+40, 100+40+40, 15+40+40, width=3, fill="red")
        self.make_board.create_rectangle(100+40+60+60, 15 + 40, 100+40+60+40+60, 15 + 40 + 40, width=3, fill="red")
        self.make_board.create_rectangle(100 + 40, 15 + 40+100, 100 + 40 + 40, 15 + 40 + 40+100, width=3, fill="red")
        self.make_board.create_rectangle(100 + 40 + 60 + 60, 15 + 40+100, 100 + 40 + 60 + 40 +60, 15 + 40 + 40+100, width=3, fill="red")

        # Right up square inside box made
        self.make_board.create_rectangle(340+(40*3)+40, 15 + 40, 340+(40*3)+40 + 40, 15 + 40 + 40, width=3, fill="green")
        self.make_board.create_rectangle(340+(40*3)+40+ 60 + 40+20, 15 + 40, 340+(40*3)+40 + 60 + 40 + 40+20, 15 + 40 + 40, width=3, fill="green")
        self.make_board.create_rectangle(340+(40*3)+40, 15 + 40 + 100, 340+(40*3)+40 + 40, 15 + 40 + 40 + 100, width=3, fill="green")
        self.make_board.create_rectangle(340+(40*3)+40+ 60 + 40+20, 15 + 40 + 100, 340+(40*3)+40 + 60 + 40 + 40+20, 15 + 40 + 40 + 100, width=3, fill="green")

        # Left down square inside box made
        self.make_board.create_rectangle(100 + 40, 340+80+15, 100 + 40 + 40, 340+80+40+15, width=3, fill="blue")
        self.make_board.create_rectangle(100 + 40 + 60 + 40+20, 340+80+15, 100 + 40 + 60 + 40 + 40+20, 340+80+40+15, width=3, fill="blue")
        self.make_board.create_rectangle(100 + 40, 340+80+60+40+15, 100 + 40 + 40, 340+80+60+40+40+15, width=3, fill="blue")
        self.make_board.create_rectangle(100 + 40 + 60 + 40+20, 340+80+60+40+15, 100 + 40 + 60 + 40 + 40+20, 340+80+60+40+40+15, width=3, fill="blue")

        # Right down square inside box made
        self.make_board.create_rectangle(340 + (40 * 3) + 40, 340+80+15, 340 + (40 * 3) + 40 + 40, 340+80+40+15, width=3, fill="yellow")
        self.make_board.create_rectangle(340 + (40 * 3) + 40 + 60 + 40+20, 340+80+15, 340 + (40 * 3) + 40 + 60 + 40 + 40+20, 340+80+40+15, width=3, fill="yellow")
        self.make_board.create_rectangle(340 + (40 * 3) + 40, 340+80+60+40+15, 340 + (40 * 3) + 40 + 40,340+80+60+40+40+15, width=3, fill="yellow")
        self.make_board.create_rectangle(340 + (40 * 3) + 40 + 60 + 40+20, 340+80+60+40+15,340 + (40 * 3) + 40 + 60 + 40 + 40+20, 340+80+60+40+40+15, width=3, fill="yellow")

        # Red start position
        self.make_board.create_rectangle(100 + 40, 15+(40*6), 100 +40 + 40, 15+(40*6)+40, fill="red", width=3)
        # Green start position
        self.make_board.create_rectangle(100 + (40*8), 15 + 40, 100 +(40*9), 15 + 40+ 40, fill="green", width=3)
        # Yellow start position
        self.make_board.create_rectangle(100 + (40 * 6)+(40*3)+(40*4), 15 + (40*8), 100 + (40 * 6)+(40*3)+(40*5), 15 + (40*9), fill="yellow", width=3)
        # blue start position
        self.make_board.create_rectangle(100+240,340+(40*5)-5,100+240+40,340+(40*6)-5,fill="blue",width=3)

        # Traingle in middle
        self.make_board.create_polygon(100+240, 15+240, 100+240+60, 15+240+60, 100+240, 15+240+(40*3), width=3,fill="red",outline="black")
        self.make_board.create_polygon(100 + 240+(40*3), 15 + 240, 100 + 240 + 60, 15 + 240 + 60, 100 + 240+(40*3), 15 + 240 + (40 * 3), width=3, fill="yellow",outline="black")
        self.make_board.create_polygon(100 + 240, 15 + 240, 100 + 240 + 60, 15 + 240 + 60, 100 + 240 + (40 * 3), 15 + 240, width=3, fill="green",outline="black")
        self.make_board.create_polygon(100 + 240, 15 + 240+(40*3), 100 + 240 + 60, 15 + 240 + 60, 100 + 240 + (40 * 3), 15 + 240+(40*3), width=3, fill="blue",outline="black")

        # Make coin for red left up block - improved styling
        Red1_Coin = self.make_board.create_oval(100+40, 15+40, 100+40+40, 15+40+40, width=3, fill="#FF3333", outline="black")
        Red2_Coin = self.make_board.create_oval(100+40+60+60, 15 + 40, 100+40+60+60+40, 15 + 40 + 40, width=3, fill="#FF3333", outline="black")
        Red3_Coin = self.make_board.create_oval(100 + 40 + 60 + 60, 15 + 40 + 100, 100 + 40 + 60 + 60 + 40, 15 + 40 + 40 + 100, width=3, fill="#FF3333", outline="black")
        Red4_Coin = self.make_board.create_oval(100 + 40, 15 + 40+100, 100 + 40 + 40, 15 + 40 + 40+100, width=3, fill="#FF3333", outline="black")
        self.Red_coin.append(Red1_Coin)
        self.Red_coin.append(Red2_Coin)
        self.Red_coin.append(Red3_Coin)
        self.Red_coin.append(Red4_Coin)

        # Make coin under number label for red left up block
        Red1_label = Label(self.make_board, text="1", font=("Arial", 15, "bold"), bg="red", fg="black")
        Red1_label.place(x=100 + 40 + 10, y=15 + 40 + 5)
        Red2_label = Label(self.make_board, text="2", font=("Arial", 15, "bold"), bg="red", fg="black")
        Red2_label.place(x=100 + 40 + 60 + 60 + 10, y=15 + 40 + 5)
        Red3_label = Label(self.make_board, text="3", font=("Arial", 15, "bold"), bg="red", fg="black")
        Red3_label.place(x=100 + 40 + 60 + 60 + 10, y=15 + 40 + 100 + 5)
        Red4_label = Label(self.make_board, text="4", font=("Arial", 15, "bold"), bg="red", fg="black")
        Red4_label.place(x=100 + 40 + 10, y=15 + 40 + 100 + 5)
        self.Red_label.append(Red1_label)
        self.Red_label.append(Red2_label)
        self.Red_label.append(Red3_label)
        self.Red_label.append(Red4_label)

        # Make coin for green right up block - improved styling
        Green1_Coin = self.make_board.create_oval(340+(40*3)+40, 15 + 40, 340+(40*3)+40 + 40, 15 + 40 + 40, width=3, fill="#33CC33", outline="black")
        Green2_Coin = self.make_board.create_oval(340+(40*3)+40+ 60 + 40+20, 15 + 40, 340+(40*3)+40 + 60 + 40 + 40+20, 15 + 40 + 40, width=3, fill="#33CC33", outline="black")
        Green3_Coin = self.make_board.create_oval(340 + (40 * 3) + 40 + 60 + 40 + 20, 15 + 40 + 100, 340 + (40 * 3) + 40 + 60 + 40 + 40 + 20, 15 + 40 + 40 + 100, width=3, fill="#33CC33", outline="black")
        Green4_Coin = self.make_board.create_oval(340+(40*3)+40, 15 + 40 + 100, 340+(40*3)+40 + 40, 15 + 40 + 40 + 100, width=3, fill="#33CC33", outline="black")
        self.Green_coin.append(Green1_Coin)
        self.Green_coin.append(Green2_Coin)
        self.Green_coin.append(Green3_Coin)
        self.Green_coin.append(Green4_Coin)

        # Make coin under number label for green right up block
        Green1_label = Label(self.make_board, text="1", font=("Arial", 15, "bold"), bg="green", fg="black")
        Green1_label.place(x=340 + (40 * 3) + 40 + 10, y=15 + 40 + 5)
        Green2_label = Label(self.make_board, text="2", font=("Arial", 15, "bold"), bg="green", fg="black")
        Green2_label.place(x=340 + (40 * 3) + 40 + 40 + 60 + 30, y=15 + 40 + 5)
        Green3_label = Label(self.make_board, text="3", font=("Arial", 15, "bold"), bg="green", fg="black")
        Green3_label.place(x=340 + (40 * 3) + 40 + 40 + 60 + 30, y=15 + 40 + 100 + 5)
        Green4_label = Label(self.make_board, text="4", font=("Arial", 15, "bold"), bg="green", fg="black")
        Green4_label.place(x=340 + (40 * 3) + 40 + 10, y=15 + 40 + 100 + 5)
        self.Green_label.append(Green1_label)
        self.Green_label.append(Green2_label)
        self.Green_label.append(Green3_label)
        self.Green_label.append(Green4_label)

        # Make coin for blue left down block - improved styling
        Blue1_Coin = self.make_board.create_oval(100 + 40, 340+80+15, 100 + 40 + 40, 340+80+40+15, width=3, fill="#3333FF", outline="black")
        Blue2_Coin = self.make_board.create_oval(100 + 40 + 60 + 40+20, 340+80+15, 100 + 40 + 60 + 40 + 40+20, 340+80+40+15, width=3, fill="#3333FF", outline="black")
        Blue3_Coin = self.make_board.create_oval(100 + 40 + 60 + 40 + 20, 340 + 80 + 60 + 40 + 15, 100 + 40 + 60 + 40 + 40 + 20, 340 + 80 + 60 + 40 + 40 + 15, width=3, fill="#3333FF", outline="black")
        Blue4_Coin = self.make_board.create_oval( 100 + 40, 340+80+60+40+15, 100 + 40 + 40, 340+80+60+40+40+15, width=3, fill="#3333FF", outline="black")
        self.Blue_coin.append(Blue1_Coin)
        self.Blue_coin.append(Blue2_Coin)
        self.Blue_coin.append(Blue3_Coin)
        self.Blue_coin.append(Blue4_Coin)

        # Make coin under number label for blue left down block
        Blue1_label = Label(self.make_board, text="1", font=("Arial", 15, "bold"), bg="blue", fg="black")
        Blue1_label.place(x=100 + 40 + 10, y=30 + (40 * 6) + (40 * 3) + 40 + 10)
        Blue2_label = Label(self.make_board, text="2", font=("Arial", 15, "bold"), bg="blue", fg="black")
        Blue2_label.place(x=100 + 40 + 60 + 60 + 10, y=30 + (40 * 6) + (40 * 3) + 40 + 10)
        Blue3_label = Label(self.make_board, text="3", font=("Arial", 15, "bold"), bg="blue", fg="black")
        Blue3_label.place(x=100 + 40 + 60 + 60 + 10, y=30 + (40 * 6) + (40 * 3) + 40 + 60 + 40 + 10)
        Blue4_label = Label(self.make_board, text="4", font=("Arial", 15, "bold"), bg="blue", fg="black")
        Blue4_label.place(x=100 + 40 + 10, y=30 + (40 * 6) + (40 * 3) + 40 + 60 + 40 + 10)
        self.Blue_label.append(Blue1_label)
        self.Blue_label.append(Blue2_label)
        self.Blue_label.append(Blue3_label)
        self.Blue_label.append(Blue4_label)

        # Make coin for yellow right down block - improved styling  
        Yellow1_Coin = self.make_board.create_oval(340 + (40 * 3) + 40, 340+80+15, 340 + (40 * 3) + 40 + 40, 340+80+40+15, width=3, fill="#FFCC00", outline="black")
        Yellow2_Coin = self.make_board.create_oval(340 + (40 * 3) + 40 + 60 + 40 + 20, 340+80+15, 340 + (40 * 3) + 40 + 60 + 40 + 40+20, 340+80+40+15, width=3, fill="#FFCC00", outline="black")
        Yellow3_Coin = self.make_board.create_oval(340 + (40 * 3) + 40 + 60 + 40 + 20, 340 + 80 + 60 + 40 + 15, 340 + (40 * 3) + 40 + 60 + 40 + 40 + 20, 340 + 80 + 60 + 40 + 40 + 15, width=3, fill="#FFCC00", outline="black")
        Yellow4_Coin = self.make_board.create_oval(340 + (40 * 3) + 40, 340+80+60+40+15, 340 + (40 * 3) + 40 + 40,340+80+60+40+40+15, width=3, fill="#FFCC00", outline="black")
        self.Yellow_coin.append(Yellow1_Coin)
        self.Yellow_coin.append(Yellow2_Coin)
        self.Yellow_coin.append(Yellow3_Coin)
        self.Yellow_coin.append(Yellow4_Coin)

        # Make coin under number label for yellow right down block
        Yellow1_label = Label(self.make_board, text="1", font=("Arial", 15, "bold"), bg="yellow", fg="black")
        Yellow1_label.place(x=340 + (40 * 3) + 40 + 10, y=30 + (40 * 6) + (40 * 3) + 40 + 10)
        Yellow2_label = Label(self.make_board, text="2", font=("Arial", 15, "bold"), bg="yellow", fg="black")
        Yellow2_label.place(x=340 + (40 * 3) + 40 + 40 + 60 + 30, y=30 + (40 * 6) + (40 * 3) + 40 + 10)
        Yellow3_label = Label(self.make_board, text="3", font=("Arial", 15, "bold"), bg="yellow", fg="black")
        Yellow3_label.place(x=340 + (40 * 3) + 40 + 40 + 60 + 30, y=30 + (40 * 6) + (40 * 3) + 40 + 100 + 10)
        Yellow4_label = Label(self.make_board, text="4", font=("Arial", 15, "bold"), bg="yellow", fg="black")
        Yellow4_label.place(x=340 + (40 * 3) + 40 + 10, y=30 + (40 * 6) + (40 * 3) + 40 + 100 + 10)
        self.Yellow_label.append(Yellow1_label)
        self.Yellow_label.append(Yellow2_label)
        self.Yellow_label.append(Yellow3_label)
        self.Yellow_label.append(Yellow4_label)
        # Add safe position markers last (after all other elements are drawn)
#         safe_positions = [
#     (100 + 40, 15+(40*6)),  # pos 1 (start red)
#     (100 + (40*8), 15 + 40),  # pos 9 (safe position)  
#     (340+(40*3)+40, 15 + 40),  # pos 14 (safe position)
#     (340+(40*3)+40, 15 + (40*8)),  # pos 22 (safe position)
#     (100 + (40 * 6)+(40*3)+(40*4), 15 + (40*8)),  # pos 27 (start yellow)
#     (100 + 40, 340+80+15),  # pos 35 (safe position)
#     (100+240, 340+(40*5)-5),  # pos 40 (start blue)
#     (100 + 40, 15 + 40)  # pos 48 (safe position)
# ]
        
#         # Create star markers that appear on top
#         for x, y in safe_positions:
#             self.make_board.create_text(x+20, y+20, text="★", font=("Arial", 25, "bold"), fill="gold", tags="safe_spot")


    # Total number of players: Control take at first
    def Initial_Control(self):
        for i in range(4):
            self.Predict_BlockValue[i][1]['state'] = DISABLED

        # Make other window to control take
        Top = Toplevel()
        Top.geometry("530x300")
        Top.maxsize(530,300)
        Top.minsize(530,300)
        Top.config(bg="white")
        # No icon needed

        Head = Label(Top,text="Total number of players",font=("Times new roman",30,"bold","italic"))
        Head.place(x=50,y=30)
        Entry_take = Entry(Top,font=("Times new roman",18,"bold","italic"),relief=SUNKEN,bd=5,width=12, state=DISABLED)
        Entry_take.place(x=130,y=85)
        Entry_take.focus()

        def Filter_value():# Total player input value filtering
            def input_filter_value(Coin_num):# Input value Filtering
                try:
                    return True if (4>=int(Coin_num)>=2) or type(Coin_num) == int else False
                except:
                    return False

            take_Response = input_filter_value(Entry_take.get())
            if take_Response:
                for player_index in range(int(Entry_take.get())):
                    self.Total_player.append(player_index)
                print(self.Total_player)
                self.Command_Maker()
                Top.destroy()
            else:
                messagebox.showerror("Input Error", "Please input number of players between 2 and 4")
                Top.destroy()
                self.Initial_Control()

        btn_Submit = Button(Top,text="Submit",bg="#262626",fg="white",font=("Times new roman",13,"bold"),relief=RAISED,bd=3,command=Filter_value,state=DISABLED)
        btn_Submit.place(x=330,y=87)

        def Operate_computer(ind):
            if ind:
                self.Robo = 1
                # Initialize AI when choosing to play with computer
                from easy_ai import EasyAI
                self.ai = EasyAI()
                
                for player_index in range(2):
                    self.Total_player.append(player_index)
                print(self.Total_player)
                def delay_instrctions(Time_is):
                    if Place_ins['text'] != "":
                        Place_ins.place_forget()
                    if Play_Command['text'] != "":
                        Play_Command.place_forget()
                
                    Place_ins['text'] = f"    Your game will start within {Time_is} sec         "
                    Place_ins.place(x=20, y=220)

                    if Time_is > 5:
                        Play_Command['text'] = f"             Machine Play With Red and You Play With Sky Blue"
                    elif Time_is>= 2 and Time_is<5:
                        Play_Command['text'] = f"                       You Will Get the First Chance to play"
                    else: 
                        Play_Command['text'] = f"                                        Enjoy this Game"
                    Play_Command.place(x=10, y=260)

                Time_is = 5
                Place_ins = Label(Top, text="", font=("Times new roman", 20, "bold"), fg="#FF0000")
                Play_Command = Label(Top, text="", font=("Helvetica", 12, "bold"), fg="blue")

                try:
                    while Time_is:
                        delay_instrctions(Time_is)
                        Time_is-=1
                        self.window.update()
                        time.sleep(1)
                    Top.destroy()
                except:
                    print("Force Stop Error in Operate computer")
                self.Predict_BlockValue[1][1]['state'] = NORMAL
            else:
                btn_Submit['state'] = NORMAL
                Entry_take['state'] = NORMAL

        
        btn_PC = Button(Top,text="Play With Computer",bg="#e8c1c7",fg="black",font=("Helvetica",15,"bold"),relief=RAISED,bd=3,command=lambda: Operate_computer(1), activebackground="#e3f4f1")
        btn_PC.place(x=30,y=160)

        btn_PF = Button(Top,text="Play With Friends",bg="#e8c1c7",fg="black",font=("Helvetica",15,"bold"),relief=RAISED,bd=3,command=lambda: Operate_computer(0), activebackground="#e3f4f1")
        btn_PF.place(x=260,y=160)

        Top.mainloop()

    # Get block value after prediction based on probability
    def Prediction_Maker(self,color_indicator):
        try:
            # Get the corresponding predict block value based on color
            if color_indicator == "red":
                Predict_BlockValue = self.Predict_BlockValue[0]
                Permanent_Dice_num = self.move_Red = randint(1, 6)
            elif color_indicator == "blue":
                Predict_BlockValue = self.Predict_BlockValue[1]
                Permanent_Dice_num = self.move_Blue = randint(1, 6)
            elif color_indicator == "yellow":
                Predict_BlockValue = self.Predict_BlockValue[2]
                Permanent_Dice_num = self.move_Yellow = randint(1, 6)
            else:  # green
                Predict_BlockValue = self.Predict_BlockValue[3]
                Permanent_Dice_num = self.move_Green = randint(1, 6)

            Predict_BlockValue[1]['state'] = DISABLED

            # Illusion of coin floating
            Temp_Counter = 12
            while Temp_Counter>0:
                move_Temp_Counter = randint(1, 6)
                Predict_BlockValue[0]['image'] = self.Dice_side[move_Temp_Counter - 1]
                self.window.update()
                time.sleep(0.1)
                Temp_Counter-=1

            print("Prediction result: ", Permanent_Dice_num)

            # Permanent predicted value containing image set
            Predict_BlockValue[0]['image'] = self.Dice_side[Permanent_Dice_num-1]
            if self.Robo == 1 and color_indicator == "red":
                self.window.update()
                time.sleep(0.4)
            self.Instructional_Button(color_indicator,Permanent_Dice_num,Predict_BlockValue)
        except:
            print("Force Stop Error in Prediction")


    def Instructional_Button(self,color_indicator,Permanent_Dice_num, Predict_BlockValue):
        Robo_Operator = None
        if color_indicator == "red":
            Temp_CoinPosition = self.Position_Red_coin
        elif color_indicator == "green":
            Temp_CoinPosition = self.Position_Green_coin
        elif color_indicator == "yellow":
            Temp_CoinPosition = self.Position_Yellow_coin
        else:
            Temp_CoinPosition = self.Position_Blue_coin

        all_in = 1
        for i in range(4):
            if Temp_CoinPosition[i] == -1:
                all_in = 1
            else:
                all_in = 0
                break

        # Handle sixes fairly for all players
        if Permanent_Dice_num == 6:
            self.current_turn_sixes += 1
            self.six_counts[color_indicator] += 1
        else:
            self.current_turn_sixes = 0
            self.six_counts[color_indicator] = 0

        # Check if move is allowed due to excessive sixes
        if self.current_turn_sixes >= self.max_sixes_per_turn:
            print(f"Max sixes ({self.max_sixes_per_turn}) reached for {color_indicator}. Passing turn.") # Optional: Add logging
            # Resetting current_turn_sixes is handled within Command_Maker now.
            self.Command_Maker() # Advance to the next player
            return # Stop further processing for this invalid move

        # Original permission logic continues here...
        permission = 1 # Assume permission initially for other checks
        # Allow move if either:
        # 1. All pieces are home and rolled a 6
        # 2. Has pieces on board
        if not ((all_in == 1 and Permanent_Dice_num == 6) or (all_in == 0)):
            permission = 0
            
        # Get coordinate reference for current player
        if color_indicator == "red":
            temp = self.Red_coord
        elif color_indicator == "green":
            temp = self.Green_coord
        elif color_indicator == "yellow":
            temp = self.Yellow_coord
        else:
            temp = self.Blue_coord

        # Check move validity based on dice roll
        if permission:
            # For non-6 rolls, check if any valid moves exist
            if Permanent_Dice_num < 6:
                permission = 0  # Reset permission
                for i in range(4):
                    # Check if piece can move
                    if temp[i] == -1:  # Piece in home
                        continue
                    elif temp[i] > 100:  # Piece in final stretch
                        if temp[i] + Permanent_Dice_num <= 106:
                            permission = 1
                            break
                    else:  # Piece on main board
                        permission = 1
                        break
            else:  # For roll of 6
                permission = 1
                # Check if any piece can complete journey
                for i in range(4):
                    if temp[i] > 100 and temp[i] + Permanent_Dice_num <= 106:
                        permission = 1
                        break

        # Handle result of permission check
        if permission == 0: # No valid moves possible
            # Advance turn immediately
            self.Command_Maker()
            # Re-enable the next player's button if the game is still going
            if self.time_for >= 0 and self.time_for < len(self.Total_player):
                curr_player = self.Total_player[self.time_for]
                self.Predict_BlockValue[curr_player][1]['state'] = NORMAL
                # Disable other players' predict buttons
                for i in range(len(self.Predict_BlockValue)):
                    if i != curr_player:
                        self.Predict_BlockValue[i][1]['state'] = DISABLED
        else:
            # Enable move buttons and update states
            self.State_controller_Button(Predict_BlockValue[2])
            Predict_BlockValue[1]['state'] = DISABLED

            # Handle AI turn if needed
            if self.Robo == 1 and Predict_BlockValue == self.Predict_BlockValue[0]:
                Robo_Operator = "give"

            # Turn logic is now handled at the end of Main_Controller after a move is completed.

        # Execute AI move decision if applicable
        if self.Robo == 1 and Robo_Operator:
            self.Robo_Judge(Robo_Operator)
            
    # Player Scope controller
    def Command_Maker(self, Robo_Operator = None):
        """Handle turn transitions and player control"""
        # Disable current player's controls if not -1
        if self.time_for != -1:
            self.Predict_BlockValue[self.Total_player[self.time_for]][1]['state'] = DISABLED
            # Reset six count for player ending their turn
            current_color = ['red', 'blue', 'yellow', 'green'][self.Total_player[self.time_for]]
            self.six_counts[current_color] = 0
            self.current_turn_sixes = 0

        # Cycle to next player
        if self.time_for == len(self.Total_player)-1:
            self.time_for = -1
        self.time_for += 1

        # Enable next player's controls and disable others
        for i in range(len(self.Predict_BlockValue)):
            if i == self.Total_player[self.time_for]:
                self.Predict_BlockValue[i][1]['state'] = NORMAL
            else:
                self.Predict_BlockValue[i][1]['state'] = DISABLED
        
        # Handle AI turn if applicable
        if self.Robo == 1 and self.time_for == 0:
            Robo_Operator = "predict"
        if Robo_Operator:
            self.Robo_Judge(Robo_Operator)

    def Instructional_Button_Red(self):
        Block_Predict_Red = Label(self.make_board,image=self.Dice_side[0])
        Block_Predict_Red.place(x=34,y=15)
        Predict_Red = Button(self.make_board, bg="black", fg="green", relief=RAISED, bd=5, text="Predict", font=("Times new roman", 8, "bold"), command=lambda: self.Prediction_Maker("red"))
        Predict_Red.place(x=25, y=15 + 50)
        
        btn_1 = Button(self.make_board,bg="#262626",fg="#00eb00",text="1",font=("Times new roman",13,"bold","italic"),relief=RAISED,bd=3,command=lambda: self.Main_Controller("red",'1'), state=DISABLED, disabledforeground="red")
        btn_1.place(x=20,y=15+100)
        btn_2 = Button(self.make_board,bg="#262626",fg="#00eb00",text="2",font=("Times new roman",13,"bold","italic"),relief=RAISED,bd=3,command=lambda: self.Main_Controller("red",'2'), state=DISABLED, disabledforeground="red")
        btn_2.place(x=60,y=15+100)
        btn_3 = Button(self.make_board,bg="#262626",fg="#00eb00",text="3",font=("Times new roman",13,"bold","italic"),relief=RAISED,bd=3,command=lambda: self.Main_Controller("red",'3'), state=DISABLED, disabledforeground="red")
        btn_3.place(x=20,y=15+100+40)
        btn_4 = Button(self.make_board,bg="#262626",fg="#00eb00",text="4",font=("Times new roman",13,"bold","italic"),relief=RAISED,bd=3,command=lambda: self.Main_Controller("red",'4'), state=DISABLED, disabledforeground="red")
        btn_4.place(x=60,y=15+100+40)

        Label(self.make_board,text="Player 1",bg="#141414",fg="gold",font=("Times new roman",15,"bold")).place(x=15,y=15+140+50)
        self.Instructional_Button_Store(Block_Predict_Red,Predict_Red,[btn_1,btn_2,btn_3,btn_4])

    def Instructional_Button_Blue(self):
        Block_Predict_Blue = Label(self.make_board, image=self.Dice_side[0])
        Block_Predict_Blue.place(x=34, y=15+(40*6+40*3)+10)
        Predict_Blue = Button(self.make_board, bg="black", fg="green", relief=RAISED, bd=5, text="Predict",font=("Times new roman", 8, "bold"), command=lambda: self.Prediction_Maker("blue"))
        Predict_Blue.place(x=25, y=15+(40*6+40*3)+40 + 20)

        btn_1 = Button(self.make_board,bg="#262626",fg="#00eb00",text="1",font=("Times new roman",13,"bold","italic"),relief=RAISED,bd=3,command=lambda: self.Main_Controller("blue",'1'), state=DISABLED, disabledforeground="red")
        btn_1.place(x=20,y=15+(40*6+40*3)+40 + 70)
        btn_2 = Button(self.make_board,bg="#262626",fg="#00eb00",text="2",font=("Times new roman",13,"bold","italic"),relief=RAISED,bd=3,command=lambda: self.Main_Controller("blue",'2'), state=DISABLED, disabledforeground="red")
        btn_2.place(x=60,y=15+(40*6+40*3)+40 + 70)
        btn_3 = Button(self.make_board,bg="#262626",fg="#00eb00",text="3",font=("Times new roman",13,"bold","italic"),relief=RAISED,bd=3,command=lambda: self.Main_Controller("blue",'3'), state=DISABLED, disabledforeground="red")
        btn_3.place(x=20,y=15+(40*6+40*3)+40 + 70+ 40)
        btn_4 = Button(self.make_board,bg="#262626",fg="#00eb00",text="4",font=("Times new roman",13,"bold","italic"),relief=RAISED,bd=3,command=lambda: self.Main_Controller("blue",'4'), state=DISABLED, disabledforeground="red")
        btn_4.place(x=60,y=15+(40*6+40*3)+40 + 70+ 40)

        Label(self.make_board, text="Player 2", bg="#141414", fg="gold", font=("Times new roman", 15, "bold")).place(x=12,y=15+(40*6+40*3)+40 + 110+50)
        self.Instructional_Button_Store(Block_Predict_Blue, Predict_Blue, [btn_1,btn_2,btn_3,btn_4])

    def Instructional_Button_Yellow(self):
        Block_Predict_Yellow = Label(self.make_board, image=self.Dice_side[0])
        Block_Predict_Yellow.place(x=100 + (40 * 6 + 40 * 3 + 40 * 6 + 10)+20, y=15 + (40 * 6 + 40 * 3) + 10)
        Predict_Yellow = Button(self.make_board, bg="black", fg="green", relief=RAISED, bd=5, text="Predict",font=("Times new roman", 8, "bold"), command=lambda: self.Prediction_Maker("yellow"))
        Predict_Yellow.place(x=100 + (40 * 6 + 40 * 3 + 40 * 6 + 2)+20, y=15 + (40 * 6 + 40 * 3) + 40 + 20)
        
        btn_1 = Button(self.make_board,bg="#262626",fg="#00eb00",text="1",font=("Times new roman",13,"bold","italic"),relief=RAISED,bd=3,command=lambda: self.Main_Controller("yellow",'1'), state=DISABLED, disabledforeground="red")
        btn_1.place(x=100 + (40 * 6 + 40 * 3 + 40 * 6 + 2)+15, y=15 + (40 * 6 + 40 * 3) + 40 + 70)
        btn_2 = Button(self.make_board,bg="#262626",fg="#00eb00",text="2",font=("Times new roman",13,"bold","italic"),relief=RAISED,bd=3,command=lambda: self.Main_Controller("yellow",'2'), state=DISABLED, disabledforeground="red")
        btn_2.place(x=100 + (40 * 6 + 40 * 3 + 40 * 6 + 2)+15 + 40, y=15 + (40 * 6 + 40 * 3) + 40 + 70)
        btn_3 = Button(self.make_board,bg="#262626",fg="#00eb00",text="3",font=("Times new roman",13,"bold","italic"),relief=RAISED,bd=3,command=lambda: self.Main_Controller("yellow",'3'), state=DISABLED, disabledforeground="red")
        btn_3.place(x=100 + (40 * 6 + 40 * 3 + 40 * 6 + 2)+15, y=15 + (40 * 6 + 40 * 3) + 40 + 70+ 40)
        btn_4 = Button(self.make_board,bg="#262626",fg="#00eb00",text="4",font=("Times new roman",13,"bold","italic"),relief=RAISED,bd=3,command=lambda: self.Main_Controller("yellow",'4'), state=DISABLED, disabledforeground="red")
        btn_4.place(x=100 + (40 * 6 + 40 * 3 + 40 * 6 + 2)+15 + 40, y=15 + (40 * 6 + 40 * 3) + 40 + 70+ 40)
        
        Label(self.make_board, text="Player 3", bg="#141414", fg="gold", font=("Times new roman", 15, "bold")).place(x=100 + (40 * 6 + 40 * 3 + 40 * 6 +7),y=15+(40*6+40*3)+40 + 110+50)
        self.Instructional_Button_Store(Block_Predict_Yellow, Predict_Yellow, [btn_1,btn_2,btn_3,btn_4])

    def Instructional_Button_Green(self):
        Block_Predict_Green = Label(self.make_board, image=self.Dice_side[0])
        Block_Predict_Green.place(x=100+(40*6+40*3+40*6+10)+20, y=15)
        Predict_Green = Button(self.make_board, bg="black", fg="green", relief=RAISED, bd=5, text="Predict", font=("Times new roman", 8, "bold"), command=lambda: self.Prediction_Maker("green"))
        Predict_Green.place(x=100+(40*6+40*3+40*6+2)+20, y=15 + 50)
        
        btn_1 = Button(self.make_board,bg="#262626",fg="#00eb00",text="1",font=("Times new roman",13,"bold","italic"),relief=RAISED,bd=3,command=lambda: self.Main_Controller("green",'1'), state=DISABLED, disabledforeground="red")
        btn_1.place(x=100 + (40 * 6 + 40 * 3 + 40 * 6 + 2)+15,y=15+100)
        btn_2 = Button(self.make_board,bg="#262626",fg="#00eb00",text="2",font=("Times new roman",13,"bold","italic"),relief=RAISED,bd=3,command=lambda: self.Main_Controller("green",'2'), state=DISABLED, disabledforeground="red")
        btn_2.place(x=100 + (40 * 6 + 40 * 3 + 40 * 6 + 2)+15 + 40,y=15+100)
        btn_3 = Button(self.make_board,bg="#262626",fg="#00eb00",text="3",font=("Times new roman",13,"bold","italic"),relief=RAISED,bd=3,command=lambda: self.Main_Controller("green",'3'), state=DISABLED, disabledforeground="red")
        btn_3.place(x=100 + (40 * 6 + 40 * 3 + 40 * 6 + 2)+15,y=15+100+40)
        btn_4 = Button(self.make_board,bg="#262626",fg="#00eb00",text="4",font=("Times new roman",13,"bold","italic"),relief=RAISED,bd=3,command=lambda: self.Main_Controller("green",'4'), state=DISABLED, disabledforeground="red")
        btn_4.place(x=100 + (40 * 6 + 40 * 3 + 40 * 6 + 2)+15 + 40,y=15+100+40)
        
        Label(self.make_board, text="Player 4", bg="#141414", fg="gold", font=("Times new roman", 15, "bold")).place(x=100+(40*6+40*3+40*6+7), y=15+140+50)
        self.Instructional_Button_Store(Block_Predict_Green, Predict_Green, [btn_1,btn_2,btn_3,btn_4])


    def Instructional_Button_Store(self, Block_Indicator, Predictor, Entry_Controller):
        temp = []
        temp.append(Block_Indicator)
        temp.append(Predictor)
        temp.append(Entry_Controller)
        self.Predict_BlockValue.append(temp)


    def Start_position_RedCircle(self, Coin_num):
        self.make_board.delete(self.Red_coin[int(Coin_num)-1])
        self.Red_coin[int(Coin_num)-1] = self.make_board.create_oval(100 + 40, 15+(40*6), 100 +40 + 40, 15+(40*6)+40, fill="red", width=3, outline="black")

        self.Red_label[int(Coin_num)-1].place_forget()
        Red_label_X = 100 + 40 + 10
        Red_label_Y = 15 + (40 * 6) + 5
        self.Red_label[int(Coin_num)-1].place(x=Red_label_X, y=Red_label_Y)

        self.Position_Red_coin[int(Coin_num)-1] = 1
        self.window.update()
        time.sleep(0.2)

    def Start_position_BlueCircle(self,Coin_num):
        self.make_board.delete(self.Blue_coin[int(Coin_num)-1])
        self.Blue_coin[int(Coin_num)-1] = self.make_board.create_oval(100+240,340+(40*5)-5,100+240+40,340+(40*6)-5,fill="blue",width=3)

        self.Blue_label[int(Coin_num)-1].place_forget()
        Blue_label_X = 100+240 + 10
        Blue_label_Y = 340+(40*5)-5 + 5
        self.Blue_label[int(Coin_num) - 1].place(x=Blue_label_X, y=Blue_label_Y)

        self.Position_Blue_coin[int(Coin_num) - 1] = 40
        self.window.update()
        time.sleep(0.2)
    
    def Start_position_GreenCircle(self,Coin_num):
        self.make_board.delete(self.Green_coin[int(Coin_num)-1])
        self.Green_coin[int(Coin_num)-1] = self.make_board.create_oval(100 + (40*8), 15 + 40, 100 +(40*9), 15 + 40+ 40, fill="green", width=3)

        self.Green_label[int(Coin_num)-1].place_forget()
        Green_label_X = 100 + (40*8) + 10
        Green_label_Y = 15 + 40 + 5
        self.Green_label[int(Coin_num)-1].place(x=Green_label_X, y=Green_label_Y)

        self.Position_Green_coin[int(Coin_num)-1] = 14
        self.window.update()
        time.sleep(0.2)

    def Start_position_YellowCircle(self,Coin_num):
        self.make_board.delete(self.Yellow_coin[int(Coin_num)-1])
        self.Yellow_coin[int(Coin_num)-1] = self.make_board.create_oval(100 + (40 * 6)+(40*3)+(40*4), 15 + (40*8), 100 + (40 * 6)+(40*3)+(40*5), 15 + (40*9), fill="yellow", width=3)

        self.Yellow_label[int(Coin_num)-1].place_forget()
        Yellow_label_X = 100 + (40 * 6)+(40*3)+(40*4) + 10
        Yellow_label_Y = 15 + (40*8) + 5
        self.Yellow_label[int(Coin_num) - 1].place(x=Yellow_label_X, y=Yellow_label_Y)

        self.Position_Yellow_coin[int(Coin_num) - 1] = 27
        self.window.update()
        time.sleep(0.2)



    def State_controller_Button(self, nums_btn_List, State_Control = 1):
        if State_Control:
            for num_btn in nums_btn_List:
                num_btn['state'] = NORMAL
        else:
            for num_btn in nums_btn_List:
                num_btn['state'] = DISABLED


    def Main_Controller(self, Coin_Color, Coin_num):
        Robo_Operator = None

        if  Coin_Color == "red":
            self.State_controller_Button(self.Predict_BlockValue[0][2], 0)

            if self.move_Red == 106:
                messagebox.showwarning("Destination reached","Reached at the destination")

            elif self.Position_Red_coin[int(Coin_num)-1] == -1 and self.move_Red == 6:
                self.Start_position_RedCircle(Coin_num)
                self.Red_coord[int(Coin_num) - 1] = 1
                # Player gets another turn after unlocking pawn
                # Player gets another turn after unlocking pawn - Mark for later check
                unlocked_with_six = True # Flag this event
                if self.current_turn_sixes < self.max_sixes_per_turn:
                    self.current_turn_sixes += 1
                    # Don't return here, let the end logic handle turn
                else:
                    unlocked_with_six = False # Max sixes reached

            elif self.Position_Red_coin[int(Coin_num)-1] > -1:
                Take_coord = self.make_board.coords(self.Red_coin[int(Coin_num)-1])
                Red_label_X = Take_coord[0] + 10
                Red_label_Y = Take_coord[1] + 5
                self.Red_label[int(Coin_num) - 1].place(x=Red_label_X, y=Red_label_Y)

                if self.Position_Red_coin[int(Coin_num)-1]+self.move_Red<=106:
                    self.Position_Red_coin[int(Coin_num)-1] = self.Coin_Motion(self.Position_Red_coin[int(Coin_num) - 1],self.Red_coin[int(Coin_num)-1],self.Red_label[int(Coin_num)-1],Red_label_X,Red_label_Y,"red",self.move_Red)
                    if self.Robo and self.Position_Red_coin[int(Coin_num)-1] == 106 and Coin_Color == "red":
                        print(f"Red coin {Coin_num} reached destination")

                else:
                    if not self.Robo:
                            messagebox.showerror("Not possible","Sorry, not permitted")
                    self.State_controller_Button(self.Predict_BlockValue[0][2])

                    if self.Robo:
                        self.Robo_Judge("give")
                    return

                if  self.Position_Red_coin[int(Coin_num)-1]==22 or self.Position_Red_coin[int(Coin_num)-1]==9 or self.Position_Red_coin[int(Coin_num)-1]==48 or self.Position_Red_coin[int(Coin_num)-1]==35 or self.Position_Red_coin[int(Coin_num)-1]==14 or self.Position_Red_coin[int(Coin_num)-1]==27 or self.Position_Red_coin[int(Coin_num)-1]==40 or self.Position_Red_coin[int(Coin_num)-1]==1:
                    pass
                else:
                    if self.Position_Red_coin[int(Coin_num) - 1] < 100:
                        self.coord_overlap(self.Position_Red_coin[int(Coin_num)-1],Coin_Color, self.move_Red)

                self.Red_coord[int(Coin_num)-1] = self.Position_Red_coin[int(Coin_num)-1]

            else:
                messagebox.showerror("Wrong choice","Sorry, Your coin in not permitted to travel")
                self.State_controller_Button(self.Predict_BlockValue[0][2])

                if self.Robo == 1:
                    Robo_Operator = "give"
                    self.Robo_Judge(Robo_Operator)
                # Don't re-enable predict here, handle at the end
                # self.Predict_BlockValue[0][1]['state'] = NORMAL
                # return # Let the final turn logic execute


        elif Coin_Color == "green":
            self.State_controller_Button(self.Predict_BlockValue[3][2], 0)

            if self.move_Green == 106:
                messagebox.showwarning("Destination reached","Reached at the destination")

            elif self.Position_Green_coin[int(Coin_num) - 1] == -1 and self.move_Green == 6:
                self.Start_position_GreenCircle(Coin_num)
                self.Green_coord[int(Coin_num) - 1] = 14
                # Player gets another turn after unlocking pawn
                # Player gets another turn after unlocking pawn - Mark for later check
                unlocked_with_six = True # Flag this event
                if self.current_turn_sixes < self.max_sixes_per_turn:
                    self.current_turn_sixes += 1
                    # Don't return here, let the end logic handle turn
                else:
                    unlocked_with_six = False # Max sixes reached

            elif self.Position_Green_coin[int(Coin_num) - 1] > -1:
                Take_coord = self.make_board.coords(self.Green_coin[int(Coin_num) - 1])
                green_start_label_x = Take_coord[0] + 10
                green_start_label_y = Take_coord[1] + 5
                self.Green_label[int(Coin_num) - 1].place(x=green_start_label_x, y=green_start_label_y)


                if  self.Position_Green_coin[int(Coin_num) - 1] + self.move_Green <= 106:
                    self.Position_Green_coin[int(Coin_num) - 1] = self.Coin_Motion(self.Position_Green_coin[int(Coin_num) - 1], self.Green_coin[int(Coin_num) - 1], self.Green_label[int(Coin_num) - 1], green_start_label_x, green_start_label_y, "green", self.move_Green)
                else:
                   messagebox.showerror("Not possible","No path available")
                   self.State_controller_Button(self.Predict_BlockValue[3][2])
                   return


                if  self.Position_Green_coin[int(Coin_num)-1]==22 or self.Position_Green_coin[int(Coin_num)-1]==9 or self.Position_Green_coin[int(Coin_num)-1]==48 or self.Position_Green_coin[int(Coin_num)-1]==35 or self.Position_Green_coin[int(Coin_num)-1]==1 or self.Position_Green_coin[int(Coin_num)-1]==27 or self.Position_Green_coin[int(Coin_num)-1]==40 or self.Position_Green_coin[int(Coin_num)-1]==14:
                    pass
                else:
                    if self.Position_Green_coin[int(Coin_num) - 1] < 100:
                        self.coord_overlap(self.Position_Green_coin[int(Coin_num) - 1],Coin_Color, self.move_Green)

                self.Green_coord[int(Coin_num) - 1] = self.Position_Green_coin[int(Coin_num) - 1]

            else:
                messagebox.showerror("Wrong choice", "Sorry, Your coin in not permitted to travel")
                self.State_controller_Button(self.Predict_BlockValue[3][2])
                # Don't re-enable predict here, handle at the end
                # self.Predict_BlockValue[3][1]['state'] = NORMAL
                # return # Let the final turn logic execute

        elif Coin_Color == "yellow":
            self.State_controller_Button(self.Predict_BlockValue[2][2], 0)

            if self.move_Yellow == 106:
                messagebox.showwarning("Destination reached","Reached at the destination")

            elif self.Position_Yellow_coin[int(Coin_num) - 1] == -1 and self.move_Yellow == 6:
                self.Start_position_YellowCircle(Coin_num)
                self.Yellow_coord[int(Coin_num) - 1] = 27
                # Player gets another turn after unlocking pawn
                # Player gets another turn after unlocking pawn - Mark for later check
                unlocked_with_six = True # Flag this event
                if self.current_turn_sixes < self.max_sixes_per_turn:
                    self.current_turn_sixes += 1
                    # Don't return here, let the end logic handle turn
                else:
                    unlocked_with_six = False # Max sixes reached

            elif self.Position_Yellow_coin[int(Coin_num) - 1] > -1:
                Take_coord = self.make_board.coords(self.Yellow_coin[int(Coin_num) - 1])
                yellow_start_label_x = Take_coord[0] + 10
                yellow_start_label_y = Take_coord[1] + 5
                self.Yellow_label[int(Coin_num) - 1].place(x=yellow_start_label_x, y=yellow_start_label_y)

                if  self.Position_Yellow_coin[int(Coin_num) - 1] + self.move_Yellow <= 106:
                    self.Position_Yellow_coin[int(Coin_num) - 1] = self.Coin_Motion(self.Position_Yellow_coin[int(Coin_num) - 1], self.Yellow_coin[int(Coin_num) - 1], self.Yellow_label[int(Coin_num) - 1], yellow_start_label_x, yellow_start_label_y, "yellow", self.move_Yellow)
                else:
                   messagebox.showerror("Not possible","No path available")
                   
                   self.State_controller_Button(self.Predict_BlockValue[2][2])
                   return

                if  self.Position_Yellow_coin[int(Coin_num)-1]==22 or self.Position_Yellow_coin[int(Coin_num)-1]==9 or self.Position_Yellow_coin[int(Coin_num)-1]==48 or self.Position_Yellow_coin[int(Coin_num)-1]==35 or self.Position_Yellow_coin[int(Coin_num)-1]==1 or self.Position_Yellow_coin[int(Coin_num)-1]==14 or self.Position_Yellow_coin[int(Coin_num)-1]==40 or self.Position_Yellow_coin[int(Coin_num)-1]==27:
                    pass
                else:
                    if self.Position_Yellow_coin[int(Coin_num) - 1] < 100:
                        self.coord_overlap(self.Position_Yellow_coin[int(Coin_num) - 1],Coin_Color, self.move_Yellow)

                self.Yellow_coord[int(Coin_num) - 1] = self.Position_Yellow_coin[int(Coin_num) - 1]

            else:
                messagebox.showerror("Wrong choice", "Sorry, Your coin in not permitted to travel")
                self.State_controller_Button(self.Predict_BlockValue[2][2])
                # Don't re-enable predict here, handle at the end
                # self.Predict_BlockValue[2][1]['state'] = NORMAL
                # return # Let the final turn logic execute

 
        elif Coin_Color == "blue":
            self.State_controller_Button(self.Predict_BlockValue[1][2], 0)

            if self.move_Blue == 106:
                messagebox.showwarning("Destination reached","Reached at the destination")

            elif self.Position_Blue_coin[int(Coin_num) - 1] == -1 and self.move_Blue == 6:
                self.Start_position_BlueCircle(Coin_num)
                self.Blue_coord[int(Coin_num) - 1] = 40
                # Player gets another turn after unlocking pawn
                # Player gets another turn after unlocking pawn - Mark for later check
                unlocked_with_six = True # Flag this event
                if self.current_turn_sixes < self.max_sixes_per_turn:
                    self.current_turn_sixes += 1
                    # Don't return here, let the end logic handle turn
                else:
                    unlocked_with_six = False # Max sixes reached

            elif self.Position_Blue_coin[int(Coin_num) - 1] > -1:
                Take_coord = self.make_board.coords(self.Blue_coin[int(Coin_num) - 1])
                blue_start_label_x = Take_coord[0] + 10
                blue_start_label_y = Take_coord[1] + 5
                self.Blue_label[int(Coin_num) - 1].place(x=blue_start_label_x, y=blue_start_label_y)

                if  self.Position_Blue_coin[int(Coin_num) - 1] + self.move_Blue <= 106:
                    self.Position_Blue_coin[int(Coin_num) - 1] = self.Coin_Motion(self.Position_Blue_coin[int(Coin_num) - 1], self.Blue_coin[int(Coin_num) - 1], self.Blue_label[int(Coin_num) - 1], blue_start_label_x, blue_start_label_y, "blue", self.move_Blue)
                else:
                   messagebox.showerror("Not possible","No path available")
                   
                   self.State_controller_Button(self.Predict_BlockValue[1][2])
                   return

                if  self.Position_Blue_coin[int(Coin_num)-1]==22 or self.Position_Blue_coin[int(Coin_num)-1]==9 or self.Position_Blue_coin[int(Coin_num)-1]==48 or self.Position_Blue_coin[int(Coin_num)-1]==35 or self.Position_Blue_coin[int(Coin_num)-1]==1 or self.Position_Blue_coin[int(Coin_num)-1]==14 or self.Position_Blue_coin[int(Coin_num)-1]==27 or self.Position_Blue_coin[int(Coin_num)-1]==40:
                    pass
                else:
                    if self.Position_Blue_coin[int(Coin_num) - 1] < 100:
                        self.coord_overlap(self.Position_Blue_coin[int(Coin_num) - 1],Coin_Color, self.move_Blue)

                self.Blue_coord[int(Coin_num) - 1] = self.Position_Blue_coin[int(Coin_num) - 1]

            else:
                messagebox.showerror("Wrong choice", "Sorry, Your coin in not permitted to travel")
                self.State_controller_Button(self.Predict_BlockValue[1][2])
                # Don't re-enable predict here, handle at the end
                # self.Predict_BlockValue[1][1]['state'] = NORMAL
                # return # Let the final turn logic execute

        print(self.Red_coord)
        print(self.Green_coord)
        print(self.Yellow_coord)
        print(self.Blue_coord)
        # if self.Robo == 1: # Commented out due to AttributeError: 'Ludo_Game' object has no attribute 'Store_Robo'
            # print("Robo Store is: ", self.Store_Robo)
        
        Permission_Granted = True

        if  Coin_Color == "red" and self.Position_Red_coin[int(Coin_num)-1] == 106:
            Permission_Granted = self.Check_Win_Runnerup(Coin_Color)
        elif  Coin_Color == "green" and self.Position_Green_coin[int(Coin_num)-1] == 106:
            Permission_Granted = self.Check_Win_Runnerup(Coin_Color)
        elif  Coin_Color == "yellow" and self.Position_Yellow_coin[int(Coin_num)-1] == 106:
            Permission_Granted = self.Check_Win_Runnerup(Coin_Color)
        elif  Coin_Color == "blue" and self.Position_Blue_coin[int(Coin_num)-1] == 106:
            Permission_Granted = self.Check_Win_Runnerup(Coin_Color)

        # --- Centralized Turn Logic ---
        if Permission_Granted: # Check if the game should continue for this player
            # Determine the dice roll for the current player
            dice_roll = 0
            player_index = -1
            if Coin_Color == "red":
                dice_roll = self.move_Red
                player_index = 0
            elif Coin_Color == "green":
                dice_roll = self.move_Green
                player_index = 3
            elif Coin_Color == "yellow":
                dice_roll = self.move_Yellow
                player_index = 2
            elif Coin_Color == "blue":
                dice_roll = self.move_Blue
                player_index = 1

            # Check for extra turn conditions (rolled a 6, haven't hit max sixes)
            gets_another_turn = (dice_roll == 6 and self.current_turn_sixes < self.max_sixes_per_turn)

            if gets_another_turn:
                # Re-enable the current player's Predict button for another turn
                if player_index != -1:
                     self.Predict_BlockValue[player_index][1]['state'] = NORMAL
                # If it's the AI's turn, trigger its prediction again
                if self.Robo == 1 and Coin_Color == "red":
                     self.Robo_Judge("predict") # AI predicts again
            else:
                # Advance to the next player
                self.Command_Maker(Robo_Operator)
        # --- End Centralized Turn Logic ---


    def Coin_Motion(self,Coin_Counter,Specific_Coin,num_label,num_label_X ,num_label_Y,Coin_Color, Path_Counter):
        try:
            num_label.place(x=num_label_X,y=num_label_Y)
            while True:
                if Path_Counter == 0:
                    break
                elif (Coin_Counter == 51 and Coin_Color == "red") or (Coin_Counter==12 and Coin_Color == "green") or (Coin_Counter == 25 and Coin_Color == "yellow") or (Coin_Counter == 38 and Coin_Color == "blue") or Coin_Counter>=100:
                    if Coin_Counter<100:
                        Coin_Counter=100

                    Coin_Counter = self.Traversal_Control(Specific_Coin, num_label, num_label_X, num_label_Y, Path_Counter, Coin_Counter, Coin_Color)

                    if  Coin_Counter == 106:
                        
                        if self.Robo == 1 and Coin_Color == "red":
                            messagebox.showinfo("Destination reached","Hey! I am at the destination")
                        else:
                            messagebox.showinfo("Destination reached","Congrats! You now at the destination")
                        if Path_Counter == 6:
                            self.Six_overlap = 1
                        else:
                            self.time_for -= 1
                    break

                Coin_Counter += 1
                Path_Counter -=1
                num_label.place_forget()

                print(Coin_Counter)

                if Coin_Counter<=5:
                    self.make_board.move(Specific_Coin, 40, 0)
                    num_label_X+=40
                elif Coin_Counter == 6:
                    self.make_board.move(Specific_Coin, 40, -40)
                    num_label_X += 40
                    num_label_Y-=40
                elif 6< Coin_Counter <=11:
                    self.make_board.move(Specific_Coin, 0, -40)
                    num_label_Y -= 40
                elif Coin_Counter <=13:
                    self.make_board.move(Specific_Coin, 40, 0)
                    num_label_X += 40
                elif Coin_Counter <=18:
                    self.make_board.move(Specific_Coin, 0, 40)
                    num_label_Y += 40
                elif Coin_Counter == 19:
                    self.make_board.move(Specific_Coin, 40, 40)
                    num_label_X += 40
                    num_label_Y += 40
                elif Coin_Counter <=24:
                    self.make_board.move(Specific_Coin, 40, 0)
                    num_label_X += 40
                elif Coin_Counter <=26:
                    self.make_board.move(Specific_Coin, 0, 40)
                    num_label_Y += 40
                elif Coin_Counter <=31:
                    self.make_board.move(Specific_Coin, -40, 0)
                    num_label_X -= 40
                elif Coin_Counter == 32:
                    self.make_board.move(Specific_Coin, -40, 40)
                    num_label_X -= 40
                    num_label_Y += 40
                elif Coin_Counter <= 37:
                    self.make_board.move(Specific_Coin, 0, 40)
                    num_label_Y += 40
                elif Coin_Counter <= 39:
                    self.make_board.move(Specific_Coin, -40, 0)
                    num_label_X -= 40
                elif Coin_Counter <= 44:
                    self.make_board.move(Specific_Coin, 0, -40)
                    num_label_Y -= 40
                elif Coin_Counter == 45:
                    self.make_board.move(Specific_Coin, -40, -40)
                    num_label_X -= 40
                    num_label_Y -= 40
                elif Coin_Counter <= 50:
                    self.make_board.move(Specific_Coin, -40, 0)
                    num_label_X -= 40
                elif 50< Coin_Counter <=52:
                    self.make_board.move(Specific_Coin, 0, -40)
                    num_label_Y -= 40
                elif Coin_Counter == 53:
                    self.make_board.move(Specific_Coin, 40, 0)
                    num_label_X += 40
                    Coin_Counter = 1

                num_label.place_forget()
                num_label.place(x=num_label_X, y=num_label_Y)

                self.window.update()
                time.sleep(0.2)

            return Coin_Counter
        except:
            print("Force Stop Error Came in motion of coin")

    # For same position, previous coin deleted and set to the room
    def coord_overlap(self, Coin_Counter, Coin_Color, path_to_traverse_before_overlap): # path_to_traverse_before_overlap seems unused now
        if Coin_Color != "red":
            for Coin_num in range(len(self.Red_coord)):
                if self.Red_coord[Coin_num] == Coin_Counter:
                    # Reset the captured piece
                    self.make_board.delete(self.Red_coin[Coin_num])
                    self.Red_label[Coin_num].place_forget()
                    self.Position_Red_coin[Coin_num] = -1
                    self.Red_coord[Coin_num] = -1
                    if self.Robo == 1:
                        # Simply update AI about the coin being sent home
                        if self.Position_Red_coin.count(-1) >= 1: # Check if any red coins are home
                            print(f"Red coin {Coin_num+1} sent back home by {Coin_Color}") # Added context

                    # Remake the coin in its home position
                    if Coin_num == 0:
                       remade_coin = self.make_board.create_oval(100+40, 15+40, 100+40+40, 15+40+40, width=3, fill="red", outline="black")
                       self.Red_label[Coin_num].place(x=100 + 40 + 10, y=15 + 40 + 5)
                    elif Coin_num == 1:
                        remade_coin = self.make_board.create_oval(100+40+60+60, 15 + 40, 100+40+60+60+40, 15 + 40 + 40, width=3, fill="red", outline="black")
                        self.Red_label[Coin_num].place(x=100 + 40 + 60 +60 + 10, y=15 + 40 + 5)
                    elif Coin_num == 2:
                        remade_coin = self.make_board.create_oval(100 + 40 + 60 + 60, 15 + 40 + 100, 100 + 40 + 60 + 60 + 40, 15 + 40 + 40 + 100, width=3, fill="red", outline="black")
                        self.Red_label[Coin_num].place(x=100 + 40 + 60 + 60 + 10, y=15 + 40 + 100 + 5)
                    else:
                        remade_coin = self.make_board.create_oval(100 + 40, 15 + 40+100, 100 + 40 + 40, 15 + 40 + 40+100, width=3,fill="red", outline="black")
                        self.Red_label[Coin_num].place(x=100 + 40 + 10, y=15 + 40 + 100 + 5)
                    self.Red_coin[Coin_num]=remade_coin
                    # No turn logic modification here

        if Coin_Color != "green":
            for Coin_num in range(len(self.Green_coord)):
                if self.Green_coord[Coin_num] == Coin_Counter:
                    # Reset the captured piece
                    self.make_board.delete(self.Green_coin[Coin_num])
                    self.Green_label[Coin_num].place_forget()
                    self.Position_Green_coin[Coin_num] = -1
                    self.Green_coord[Coin_num] = -1
                    print(f"Green coin {Coin_num+1} sent back home by {Coin_Color}") # Added context

                    # Remake the coin in its home position
                    if Coin_num == 0:
                        remade_coin = self.make_board.create_oval(340+(40*3)+40, 15 + 40, 340+(40*3)+40 + 40, 15 + 40 + 40, width=3, fill="green", outline="black")
                        self.Green_label[Coin_num].place(x=340 + (40 * 3) + 40 + 10, y=15 + 40 + 5)
                    elif Coin_num == 1:
                        remade_coin = self.make_board.create_oval(340+(40*3)+40+ 60 + 40+20, 15 + 40, 340+(40*3)+40 + 60 + 40 + 40+20, 15 + 40 + 40, width=3, fill="green", outline="black")
                        self.Green_label[Coin_num].place(x=340 + (40 * 3) + 40 + 40 + 60 + 30, y=15 + 40 + 5)
                    elif Coin_num == 2:
                        remade_coin = self.make_board.create_oval(340 + (40 * 3) + 40 + 60 + 40 + 20, 15 + 40 + 100, 340 + (40 * 3) + 40 + 60 + 40 + 40 + 20, 15 + 40 + 40 + 100, width=3, fill="green", outline="black")
                        self.Green_label[Coin_num].place(x=340 + (40 * 3) + 40 + 40 + 60 + 30, y=15 + 40 + 100 + 5)
                    else:
                        remade_coin = self.make_board.create_oval(340+(40*3)+40, 15 + 40 + 100, 340+(40*3)+40 + 40, 15 + 40 + 40 + 100, width=3, fill="green", outline="black")
                        self.Green_label[Coin_num].place(x=340+(40*3) + 40 + 10, y=15 + 40 + 100 + 5)
                    self.Green_coin[Coin_num] = remade_coin
                    # No turn logic modification here

        if Coin_Color != "yellow":
            for Coin_num in range(len(self.Yellow_coord)):
                if self.Yellow_coord[Coin_num] == Coin_Counter:
                    # Reset the captured piece
                    self.make_board.delete(self.Yellow_coin[Coin_num])
                    self.Yellow_label[Coin_num].place_forget()
                    self.Position_Yellow_coin[Coin_num] = -1
                    self.Yellow_coord[Coin_num] = -1
                    print(f"Yellow coin {Coin_num+1} sent back home by {Coin_Color}") # Added context

                    # Remake the coin in its home position
                    if Coin_num == 0:
                        remade_coin = self.make_board.create_oval(340 + (40 * 3) + 40, 340+80+15, 340 + (40 * 3) + 40 + 40, 340+80+40+15, width=3, fill="yellow", outline="black")
                        self.Yellow_label[Coin_num].place(x=340+(40*3) + 40 + 10, y=30 + (40*6)+(40*3)+40+10)
                    elif Coin_num == 1:
                        remade_coin = self.make_board.create_oval(340 + (40 * 3) + 40 + 60 + 40 + 20, 340+80+15, 340 + (40 * 3) + 40 + 60 + 40 + 40+20, 340+80+40+15, width=3, fill="yellow", outline="black")
                        self.Yellow_label[Coin_num].place(x=340+(40*3)+ 40 + 40+ 60 + 30, y=30 + (40*6)+(40*3)+40+10)
                    elif Coin_num == 2:
                        remade_coin = self.make_board.create_oval(340 + (40 * 3) + 40 + 60 + 40 + 20, 340 + 80 + 60 + 40 + 15, 340 + (40 * 3) + 40 + 60 + 40 + 40 + 20, 340 + 80 + 60 + 40 + 40 + 15, width=3, fill="yellow", outline="black")
                        self.Yellow_label[Coin_num].place(x=340+(40*3)+ 40 + 40+ 60 + 30, y=30 + (40*6)+(40*3)+40+100+10)
                    else:
                        remade_coin = self.make_board.create_oval(340 + (40 * 3) + 40, 340+80+60+40+15, 340 + (40 * 3) + 40 + 40,340+80+60+40+40+15, width=3, fill="yellow", outline="black")
                        self.Yellow_label[Coin_num].place(x=340 + (40 * 3) + 40 + 10, y=30 + (40 * 6) + (40 * 3) + 40 + 100 + 10)
                    self.Yellow_coin[Coin_num] = remade_coin
                    # No turn logic modification here

        if Coin_Color != "blue":
            for Coin_num in range(len(self.Blue_coord)):
                if self.Blue_coord[Coin_num] == Coin_Counter:
                    # Reset the captured piece
                    self.make_board.delete(self.Blue_coin[Coin_num])
                    self.Blue_label[Coin_num].place_forget()
                    self.Position_Blue_coin[Coin_num] = -1
                    self.Blue_coord[Coin_num]=-1
                    print(f"Blue coin {Coin_num+1} sent back home by {Coin_Color}") # Added context

                    # Remake the coin in its home position
                    if Coin_num == 0:
                        remade_coin = self.make_board.create_oval(100 + 40, 340+80+15, 100 + 40 + 40, 340+80+40+15, width=3, fill="blue", outline="black")
                        self.Blue_label[Coin_num].place(x=100+40+10, y=30 + (40*6)+(40*3)+40+10)
                    elif Coin_num == 1:
                        remade_coin = self.make_board.create_oval(100 + 40 + 60 + 40+20, 340+80+15, 100 + 40 + 60 + 40 + 40+20, 340+80+40+15, width=3, fill="blue", outline="black")
                        self.Blue_label[Coin_num].place(x=100 + 40 + 60 +60 + 10, y=30 + (40*6)+(40*3)+40+10)
                    elif Coin_num == 2:
                        remade_coin = self.make_board.create_oval(100 + 40 + 60 + 40 + 20, 340 + 80 + 60 + 40 + 15, 100 + 40 + 60 + 40 + 40 + 20, 340 + 80 + 60 + 40 + 40 + 15, width=3, fill="blue", outline="black")
                        self.Blue_label[Coin_num].place(x=100 + 40 + 60 + 60 + 10, y=30 + (40 * 6) + (40 * 3) + 40 + 60 + 40 + 10)
                    else:
                        remade_coin = self.make_board.create_oval( 100 + 40, 340+80+60+40+15, 100 + 40 + 40, 340+80+60+40+40+15, width=3, fill="blue", outline="black")
                        self.Blue_label[Coin_num].place(x=100+40+10, y=30 + (40*6)+(40*3)+40+60+40+10)
                    self.Blue_coin[Coin_num] = remade_coin
                    # No turn logic modification here


    def Traversal_Control(self,Specific_Coin,num_label,num_label_X,num_label_Y,Path_Counter,Coin_Counter,Coin_Color):
        if Coin_Color == "red" and Coin_Counter >= 100:
            if int(Coin_Counter)+int(Path_Counter)<=106:
               Coin_Counter = self.Traversal_Red(Specific_Coin, num_label, num_label_X, num_label_Y, Path_Counter, Coin_Counter)

        elif Coin_Color == "green" and Coin_Counter >= 100:
            if  int(Coin_Counter) + int(Path_Counter) <= 106:
                Coin_Counter = self.Traversal_Green(Specific_Coin, num_label, num_label_X, num_label_Y,Path_Counter,Coin_Counter)

        elif Coin_Color == "yellow" and Coin_Counter >= 100:
            if  int(Coin_Counter) + int(Path_Counter) <= 106:
                Coin_Counter = self.Traversal_Yellow(Specific_Coin, num_label, num_label_X, num_label_Y,Path_Counter,Coin_Counter)

        elif Coin_Color == "blue" and Coin_Counter >= 100:
            if  int(Coin_Counter) + int(Path_Counter) <= 106:
                Coin_Counter = self.Traversal_Blue(Specific_Coin, num_label, num_label_X, num_label_Y,Path_Counter,Coin_Counter)

        return Coin_Counter


    def Traversal_Red(self, Specific_Coin, num_label, num_label_X, num_label_Y, Path_Counter, Coin_Counter):
        while Path_Counter>0:
            Coin_Counter += 1
            Path_Counter -= 1
            self.make_board.move(Specific_Coin, 40, 0)
            num_label_X+=40
            num_label.place(x=num_label_X,y=num_label_Y)
            self.window.update()
            time.sleep(0.2)
        return Coin_Counter

    def Traversal_Green(self, Specific_Coin, num_label, num_label_X, num_label_Y, Path_Counter, Coin_Counter):
        while Path_Counter > 0:
            Coin_Counter += 1
            Path_Counter -= 1
            self.make_board.move(Specific_Coin, 0, 40)
            num_label_Y += 40
            num_label.place(x=num_label_X, y=num_label_Y)
            self.window.update()
            time.sleep(0.2)
        return Coin_Counter

    def Traversal_Yellow(self, Specific_Coin, num_label, num_label_X, num_label_Y,Path_Counter,Coin_Counter):
        while Path_Counter > 0:
            Coin_Counter += 1
            Path_Counter -= 1
            self.make_board.move(Specific_Coin, -40, 0)
            num_label_X -= 40
            num_label.place(x=num_label_X, y=num_label_Y)
            self.window.update()
            time.sleep(0.2)
        return Coin_Counter

    def Traversal_Blue(self, Specific_Coin, num_label, num_label_X, num_label_Y,Path_Counter,Coin_Counter):
        while Path_Counter > 0:
            Coin_Counter += 1
            Path_Counter -= 1
            self.make_board.move(Specific_Coin, 0, -40)
            num_label_Y -= 40
            num_label.place(x=num_label_X, y=num_label_Y)
            self.window.update()
            time.sleep(0.2)
        return Coin_Counter

    def Check_Win_Runnerup(self,Coin_Color):
        Destination_Reached = 0 # Check for all specific color coins
        if Coin_Color == "red":
            Temp_store = self.Red_coord
            Temp_Delete = 0# Player index
        elif Coin_Color == "green":
            Temp_store = self.Green_coord
            Temp_Delete = 3# Player index
        elif Coin_Color == "yellow":
            Temp_store = self.Yellow_coord
            Temp_Delete = 2# Player index
        else:
            Temp_store = self.Blue_coord
            Temp_Delete = 1# Player index

        for take in Temp_store:
            if take == 106:
                Destination_Reached = 1
            else:
                Destination_Reached = 0
                break

        if  Destination_Reached == 1:# If all coins in block reach to the destination, winner and runner check
            self.TakePermission += 1
            if self.TakePermission == 1:# Winner check  
                if self.Robo == 1 and Coin_Color == "red":
                    messagebox.showinfo("YOU WIN!!")
                else:
                    messagebox.showinfo("Winner","Congrats! You are the winner")
            elif self.TakePermission == 2:# 1st runner check
                if self.Robo == 1 and Coin_Color == "red":
                    messagebox.showinfo("Winner", "Hurrah! I am 1st runner")
                else:
                    messagebox.showinfo("Winner", "Wow! You are 1st runner")
            elif self.TakePermission == 3:# 2nd runner check
                if self.Robo == 1 and Coin_Color == "red":
                    messagebox.showinfo("Result", "I am 2nd runner....Not bad at all")
                else:
                    messagebox.showinfo("Result", "You are 2nd runner....Better Luck next time")

            self.Predict_BlockValue[Temp_Delete][1]['state'] = DISABLED
            self.Total_player.remove(Temp_Delete)

            if len(self.Total_player) == 1:
                messagebox.showinfo("GAME OVER")
                self.Predict_BlockValue[0][1]['state'] = DISABLED
                return False
            else:
                self.time_for-=1
        else:
            print("Winner not decided")

        return True

    def Robo_Judge(self, ind="give"):
        """New AI-based decision making"""
        if ind == "give":  # For giving the value
            # Initialize AI if not already done
            if not self.ai:
                self.ai = EasyAI()
            
            # Get AI's move decision
            chosen_coin = self.ai.make_move(self.move_Red,
                                          self.Position_Red_coin,
                                          self.Position_Blue_coin)
            
            # If AI found a valid move, execute it
            if chosen_coin is not None:
                self.Main_Controller("red", chosen_coin)
        else:
            self.Prediction_Maker("red")  # Prediction Function Call


if __name__ == '__main__':
    window = Tk()
    window.geometry("800x630")
    window.maxsize(800,630)
    window.minsize(800,630)
    window.title("LUDO Game by DataFlair")
    block_one_side = ImageTk.PhotoImage(Image.open("images/Dice_1.jpg"))
    block_two_side = ImageTk.PhotoImage(Image.open("images/Dice_2.jpg"))
    block_three_side = ImageTk.PhotoImage(Image.open("images/Dice_3.jpg"))
    block_four_side = ImageTk.PhotoImage(Image.open("images/Dice_4.jpg"))
    block_five_side = ImageTk.PhotoImage(Image.open("images/Dice_5.jpg"))
    block_six_side = ImageTk.PhotoImage(Image.open("images/Dice_6.jpg"))
    Ludo_Game(window,block_one_side,block_two_side,block_three_side,block_four_side,block_five_side,block_six_side)
    window.mainloop()
