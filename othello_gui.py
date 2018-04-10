# Kevin Hoang 76963024. ICS 32 Lab Section 11. Project # 5.

import math
import othello
import point
import tkinter

DEFAULT_FONT = ("Helvetica", 14)
HEADER_FONT  = ("Helvetica", 18)


class OptionsDialog:
    def __init__(self):
        """ Initialize the dialog object by setting up how it should look at
            first glance and handling the behind the scenes activity via
            binding.
        """
        self._options_dialog_window = tkinter.Toplevel()

        app_label = tkinter.Label(
            master = self._options_dialog_window,
            text = "Othello Options Menu",
            font = ("Helvetica", 24))
        app_label.grid(
            row = 0, column = 1, padx = 10, pady = 5,
            sticky = tkinter.E)
        
        # Game board dimensions header and label/entry boxes
        size_label = tkinter.Label(
            master = self._options_dialog_window,
            text = "What dimensions would you like for the game board?",
            font = HEADER_FONT)
        size_label.grid(
            row = 1, column = 0, columnspan = 2, padx = 10, pady = 10,
            sticky = tkinter.W)
        self._row_entry = self._make_label_entry("Row:", 2)
        self._column_entry = self._make_label_entry("Column:", 3)

        # First player header and label/entry box
        first_player_instructions_label = tkinter.Label(
            master = self._options_dialog_window,
            text = "Which color should go first? White or black?",
            font = HEADER_FONT)
        first_player_instructions_label.grid(
            row = 4, column = 0, columnspan = 2, padx = 10, pady = 10,
            sticky = tkinter.W)
        self._first_player_entry = self._make_label_entry("First Player:", 5)

        # Win style header, options, and label/entry box
        win_style_instructions_label = tkinter.Label(
            master = self._options_dialog_window,
            text = "Which win style do you prefer to play with?",
            font = HEADER_FONT, )
        win_style_instructions_label.grid(
            row = 6, column = 0, columnspan = 2, padx = 10, pady = 10,
            sticky = tkinter.W)
        win_style_instructions_label2 = tkinter.Label(
            master = self._options_dialog_window,
            text = "1) The player with the most discs on the board at the end of the game is the winner.",
            font = ("Times", 14))
        win_style_instructions_label2.grid(
            row = 7, column = 0, columnspan = 2, padx = 10, 
            sticky = tkinter.W)
        win_style_instructions_label3 = tkinter.Label(
            master = self._options_dialog_window,
            text = "2) The player with the fewest discs on the board at the end of the game is the winner.",
            font = ("Times", 14))
        win_style_instructions_label3.grid(
            row = 8, column = 0, columnspan = 2, padx = 10, 
            sticky = tkinter.W)
        self._win_style_entry = self._make_label_entry("Win Style:", 9)

        # Feedback listbox for user input
        self._output_listbox = tkinter.Listbox(
            self._options_dialog_window, width = 72, height = 4, font = ("Helvetica", 12))
        self._output_listbox.grid(
            row = 10, column = 0, columnspan = 2, padx = 10, pady = 10,
            sticky = tkinter.W)
        self._output_listbox.insert(tkinter.END, "Please fill in the entry boxes and press \"Enter\" to submit as you go.")
        self._output_listbox.insert(tkinter.END, "OK button will become enabled once all four entries have been submitted")
        self._output_listbox.insert(tkinter.END, "This box will provide feedback for your input.")
        
        # OK and CANCEL buttons
        button_frame = tkinter.Frame(
            master = self._options_dialog_window)
        button_frame.grid(
            row = 11, column = 0, columnspan = 2, padx = 10, pady = 10,
            sticky = tkinter.E + tkinter. S)
        
            # OK button
        self._ok_button = tkinter.Button(
            master = button_frame, text = "OK", font = DEFAULT_FONT,
            command = self._on_ok_button_clicked,
            state = tkinter.DISABLED)
        self._ok_button.grid(
            row = 0, column = 0, padx = 10, pady = 10)
        
            # CANCEL button
        self._cancel_button = tkinter.Button(
            master = button_frame, text = "CANCEL", font = DEFAULT_FONT,
            command = self._on_cancel_button_clicked)
        self._cancel_button.grid(
            row = 0, column = 1, padx = 10, pady = 10)

        # Class variables
        self._final_input_dict = { }
        self._ok_button_clicked = False

        # Binding widgets stage: Bind entry boxes with return event
        self._row_entry.bind("<Return>", self._row_returned)
        self._column_entry.bind("<Return>", self._column_returned)
        self._first_player_entry.bind("<Return>", self._first_player_returned)
        self._win_style_entry.bind("<Return>", self._win_style_returned)

        # Manage resize weight
        self._options_dialog_window.rowconfigure(11, weight = 1)
        self._options_dialog_window.columnconfigure(1, weight = 1)
        
    def show(self) -> None:
        """ This function turns control over to this options dialog window.
        """
        self._options_dialog_window.grab_set()
        self._options_dialog_window.wait_window()

    def get_final_input_dict(self) -> dict:
        """ This function returns the final input dictionary that holds all
            of the user's input. It should only be called in the case where
            all four entries have been submitted.
        """
        return self._final_input_dict

    def get_ok_button_clicked(self) -> bool:
        """ This function returns a boolean value that indicates whether or
            not the OK button has been clicked by the user. True implies that
            the OK button has been clicked, and False implies that the OK
            button has not been clicked.
        """
        return self._ok_button_clicked

    def _make_label_entry(self, input_field: str, row_num: int) -> None:
        """ This function does the tedious job of creating and placing labels
            and entry boxes that follow the headers. Also, it returns the
            entry box so that it can be assigned to a class variable and used
            later to be disabled after input submission by the user.
        """
        # Label
        label = tkinter.Label(
            master = self._options_dialog_window, text = input_field,
            font = DEFAULT_FONT)
        label.grid(
            row = row_num, column = 0, padx = 10, pady = 10,
            sticky = tkinter.W)

        # Entry box
        entry = tkinter.Entry(
            master = self._options_dialog_window, width = 20,
            font = DEFAULT_FONT)
        entry.grid(
            row = row_num, column = 1, padx = 10, pady = 1,
            sticky = tkinter.W + tkinter.E)
        
        return entry
    
    def _on_ok_button_clicked(self) -> None:
        """ This function handles the event in which the OK button has been
            clicked by the user. By clicking the OK button, the options dialog
            window will close and the boolean value of _ok_button_clicked will
            change to True to indicate that the OK button has been pressed.
        """
        self._ok_button_clicked = True
        self._options_dialog_window.destroy()

    def _on_cancel_button_clicked(self) -> None:
        """ This function handles the event in which the CANCEL button has been
            clicked by the user. By clicking the CANCEL button, the options
            dialog window will close and control will return to the root window.
            It will be as if nothing has happened.
        """
        self._options_dialog_window.destroy()

    def _enable_ok_button(self) -> None:
        """ This functino enables the OK button if and only if the user has
            submitted valid input to all four of the entry boxes. Otherwise,
            the OK button will remain disabled.
        """
        if len(self.get_final_input_dict()) == 4:
            self._ok_button.configure(state = tkinter.NORMAL)

    def _row_returned(self, event: tkinter.Event) -> None:
        """ This function handles the event in which the user submits input in
            the row entry box. If the input is valid, the function adds it to
            the final input dictionary and writes to the feedback listbox
            saying the input has been saved. Otherwise, the function writes to
            the feedback listbox saying it was invalid.
        """
        try:
            user_input = int(event.widget.get())
            if user_input % 2 == 0:
                if user_input >= 4 and user_input <= 16:
                    self._final_input_dict["row"] = user_input
                    self._valid_input_action(event, "Row option saved.")
                else:
                    self._write_output_feedback("Your even integer must be between 4 and 16.")
            else:
                self._write_output_feedback("Your integer must be even.")
        except:
            self._write_output_feedback("You must enter an integer.")
            
    def _column_returned(self, event: tkinter.Event) -> None:
        """ This function handles the event in which the user submits input in
            the column entry box. If the input is valid, the function adds it
            to the final input dictionary and writes to the feedback listbox
            saying the input has been saved. Otherwise, the function writes to
            the feedback listbox saying it was invalid.
        """
        try:
            user_input = int(event.widget.get())
            if user_input % 2 == 0:
                if user_input >= 4 and user_input <= 16:
                    self._final_input_dict["column"] = user_input
                    self._valid_input_action(event, "Column option saved.")
                else:
                    self._write_output_feedback("Your even integer must be between 4 and 16.")
            else:
                self._write_output_feedback("Your integer must be even.")
        except:
            self._write_output_feedback("You must enter an integer.")
    
    def _first_player_returned(self, event: tkinter.Event) -> None:
        """ This function handles the event in which the user submits input in
            the first player entry box. If the input is valid, the function adds
            it to the final input dictionary and writes to the feedback listbox
            saying the input has been saved. Otherwise, the function writes to
            the feedback listbox saying it was invalid.
        """
        user_input = event.widget.get().strip().lower()
        
        if user_input == "white":
            self._final_input_dict["first player"] = othello.WHITE
            self._valid_input_action(event, "First player option saved.")
        elif user_input == "black":
            self._final_input_dict["first player"] = othello.BLACK
            self._valid_input_action(event, "First player option saved.")
        else:
            self._write_output_feedback("Invalid first player option.")
    
    def _win_style_returned(self, event: tkinter.Event) -> None:
        """ This function handles the event in which the user submits input in
            the win style entry box. If the input is valid, the function adds
            it to the final input dictionary and writes to the feedback listbox
            saying the input has been saved. Otherwise, the function writes to
            the feedback listbox saying it was invalid.
        """
        user_input = event.widget.get().strip()
        
        if user_input == "1" or user_input == "2":
            self._final_input_dict["win style"] = int(user_input)
            self._valid_input_action(event, "Win style option saved.")
        else:
            self._write_output_feedback("You must enter either 1 or 2 as an option.")

    def _write_output_feedback(self, phrase: str) -> None:
        """ This function takes a given phrase and writes it to feedback listbox.
        """
        self._output_listbox.delete(0, tkinter.END)
        self._output_listbox.insert(tkinter.END, phrase)
    
    def _valid_input_action(self, event: tkinter.Event, phrase: str) -> None:
        """ This function handles the moment in which the user provides valid
            input to the entry boxes. This function will disable the entry box
            that has been filled out, write to the feedback listbox saying that
            the input has been saved, and check to see if there has been four
            submissions so that the OK button can be enabled.
        """
        event.widget.configure(state = tkinter.DISABLED)
        self._write_output_feedback(phrase)
        self._enable_ok_button()

class OthelloGame:
    def __init__(self):
        """ Initialize the game as a tiny window with an app label and a PLAY NOW
            button used to open up an options dialog window for the user to enter
            their desired options to fully boot the game.
        """
        self._root_window = tkinter.Tk()

        # Othello label
        self._othello_label = tkinter.Label(
            master = self._root_window, text = "OTHELLO GAME",
            font = DEFAULT_FONT)
        self._othello_label.grid(
            row = 0, column = 0, padx = 10, pady = 10,
            sticky = tkinter.S)

        # Play now button
        self._play_now_button = tkinter.Button(
            master = self._root_window, text = "PLAY NOW", font = DEFAULT_FONT,
            command = self._on_play_now_clicked)
        self._play_now_button.grid(
            row = 1, column = 0, padx = 10, pady = 10,
            sticky = tkinter.N)

        # Manage resizing weights
        self._root_window.rowconfigure(0, weight = 1)
        self._root_window.rowconfigure(1, weight = 1)
        self._root_window.columnconfigure(0, weight = 1)

    def start(self):
        """ This function infinitely loops the root window so that it can be
            governed by event-based programming.
        """
        self._root_window.mainloop()

    def _on_play_now_clicked(self):
        """ This function handles the event in which the "PLAY NOW" button is pressed. If the OK
            button was clicked in the options dialog window, this function will delete everything
            on the current root window in order to draw the Othello game board and game information.
        """
        options_dialog = OptionsDialog()
        options_dialog.show()

        if options_dialog.get_ok_button_clicked() == True:
            # Othello options and game state
            self._user_input_dict = options_dialog.get_final_input_dict()
            self._othello_game_state = othello.GameState(
                self._user_input_dict["row"], self._user_input_dict["column"],
                self._user_input_dict["first player"], self._user_input_dict["win style"])

            # Delete current widgets on window
            self._play_now_button.grid_forget()
            self._othello_label.grid_forget()

            # Othello logo
            othello_app_label = tkinter.Label(
                master = self._root_window,
                text = "Othello", font = ("Helvetica", 50), fg = "green")
            othello_app_label.grid(
                row = 0, column = 0, columnspan = 2, padx = 10, pady = 5,
                sticky = tkinter.N + tkinter.E + tkinter.S + tkinter.W)

            # Game board canvas
            self._game_board_canvas = tkinter.Canvas(
                master = self._root_window, width = 500, height = 500,
                background = "#1D7F3C")
            self._game_board_canvas.grid(
                row = 1, column = 0, padx = 10, pady = 10,
                sticky =  tkinter.N + tkinter.E + tkinter.S + tkinter.W)
            self._game_board_canvas.update()

            # Binding widgets stage
            self._game_board_canvas.bind("<Configure>", self._on_canvas_resized)
            self._game_board_canvas.bind("<Button-1>", self._on_canvas_clicked)

            # Game information area
            self._game_info_frame = tkinter.Frame(
                master = self._root_window)
            self._game_info_frame.grid(
                row = 2, column = 0, columnspan = 2, padx = 10, pady = 10,
                sticky =  tkinter.N + tkinter.E + tkinter.S + tkinter.W)

            # StringVar variables.
                # White score 
            self._white_score_text = tkinter.StringVar()
            white_score_label = tkinter.Label(
                master = self._game_info_frame, textvariable = self._white_score_text,
                font = HEADER_FONT)
            white_score_label.grid(
                row = 0, column = 0, padx = 10, pady = 5,
                sticky = tkinter.W)
            
                # Black score
            self._black_score_text = tkinter.StringVar()
            black_score_label = tkinter.Label(
                master = self._game_info_frame, textvariable = self._black_score_text,
                font = HEADER_FONT)
            black_score_label.grid(
                row = 1, column = 0, padx = 10, pady = 5,
                sticky = tkinter.W)
            
                # Current player
            self._current_player_text = tkinter.StringVar()
            current_player_label = tkinter.Label(
                master = self._game_info_frame, textvariable = self._current_player_text,
                font = HEADER_FONT)
            current_player_label.grid(
                row = 0, column = 2, padx = 10, pady = 5,
                sticky = tkinter.W)
            
                # Winner
            self._winner_text = tkinter.StringVar()
            winner_label = tkinter.Label(
                master = self._game_info_frame, textvariable = self._winner_text,
                font = HEADER_FONT)
            winner_label.grid(
                row = 1, column = 2, padx = 10, pady = 5,
                sticky = tkinter.W)

            # Display
            self._redraw_draw_board()
            self._get_game_info()

            # Manage resizing weights
            self._root_window.rowconfigure(0, weight = 0)

    def _on_canvas_resized(self, event: tkinter.Event) -> None:
        """ This function handles the event in which the root window is resized
            by the user. It will delete everything on the game board canvas and
            redraw it with respect to the new width and height of the resized
            window.
        """
        self._redraw_draw_board()

    def _on_canvas_clicked(self, event: tkinter.Event) -> None:
        """ This function handles the event in which the user clicks within the
            game board canvas. It will take the x, y coordinates of the user's
            click and convert it to row and coumn integer values such as (1, 1).
            Then, this function attempts to apply the user's row and column
            move to the othello game state.
        """
        # Convert (x, y) mouse click to (row, column)
        user_col_move = int(math.ceil(event.x/self.get_column_width())) - 1
        user_row_move = int(math.ceil(event.y/self.get_row_height())) - 1
        
        try:
            self._othello_game_state.apply_move((user_row_move, user_col_move))
            self._othello_game_state.check_possible_moves()
            
            self._redraw_draw_board()
            self._get_game_info()
            self._get_winner()
        except:
            pass
    
    def get_row_height(self) -> int:
        """ This function returns the proportionated height of an individual row.
        """
        row_height = self._game_board_canvas.winfo_height() / self._user_input_dict["row"]
        
        row_height_frac = point.from_pixel(
            0, row_height,
            self._game_board_canvas.winfo_width(),
            self._game_board_canvas.winfo_height())
        row_height_pixel = row_height_frac.frac()[1] * self._game_board_canvas.winfo_height()
        
        return row_height_pixel

    def get_column_width(self) -> int:
        """ This function returns the proportionated width of an individual
            column.
        """
        column_width = self._game_board_canvas.winfo_width() / self._user_input_dict["column"]
        
        column_width_frac = point.from_pixel(
            column_width, 0,
            self._game_board_canvas.winfo_width(),
            self._game_board_canvas.winfo_height())
        column_width_pixel = column_width_frac.frac()[0] * self._game_board_canvas.winfo_width()
        
        return column_width_pixel

    def _get_game_info(self) -> None:
        """ This function taps into the Othello game state in order to define
            corrent values for the current player as well as white and black
            score.
        """
        # White score
        self._white_score_text.set(
            "White Score: {}".format(self._othello_game_state.get_white_score()))
        
        # Black score
        self._black_score_text.set(
            "Black Score: {}".format(self._othello_game_state.get_black_score()))

        # Current player
        if self._othello_game_state.get_turn() == othello.WHITE:
            current_player = "White"
        if self._othello_game_state.get_turn() == othello.BLACK:
            current_player = "Black"
        self._current_player_text.set("Current Player: {}".format(current_player))
            
    def _get_winner(self) -> None:
        """ This function taps into the Othello game state in order to check
            whether or not the game is over. If so, this function defines the
            appropriate victory string for the _winner_text class variable.
        """
        if self._othello_game_state.game_over() == True:
            self._current_player_text.set("GAME OVER!")
            
            if self._othello_game_state.determine_winner() == othello.WHITE:
                self._winner_text.set("White is the winner!")
            elif self._othello_game_state.determine_winner() == othello.BLACK:
                self._winner_text.set("Black is the winner!")
            else:
                self._winner_text.set("The game ended in a tie!")
        
    def _redraw_draw_board(self) -> None:
        """ This function clears the current game board canvas. Then, it draws the
            proper amount of rows and columns with lines with respect to the current
            width and height of the window. Lastly, it draws all of the game pieces
            that are currently on the game board.
        """
        # Clear canvas
        self._game_board_canvas.delete(tkinter.ALL)

        # Get dimensions
        game_board_canvas_width  = self._game_board_canvas.winfo_width()   
        game_board_canvas_height = self._game_board_canvas.winfo_height()

        row_y_increment = self.get_row_height()
        col_x_increment = self.get_column_width()

        row_y = 0
        col_x = 0
        
        for row in range(self._user_input_dict["row"]):
            self._game_board_canvas.create_line(0, row_y, game_board_canvas_width, row_y)
            row_y += row_y_increment

        for col in range(self._user_input_dict["column"]):
            self._game_board_canvas.create_line(col_x, 0, col_x, game_board_canvas_height)
            col_x += col_x_increment

        self._draw_game_pieces()

    def _draw_game_pieces(self) -> None:
        """ This function taps into the Othello game state and traverses through
            the entire game board looking for game pieces. When the function
            encounters a game piece, it draws it onto the game board canvas with
            respect to the player color and current width and height of the current
            column and row, respectively.
        """
        canvas_width  = self._game_board_canvas.winfo_width()   
        canvas_height = self._game_board_canvas.winfo_height()
        
        for row_index in range(self._othello_game_state.get_rows()):
            for col_index in range(self._othello_game_state.get_columns()):
                if self._othello_game_state.get_game_board()[row_index][col_index] == othello.WHITE:
                    self._draw_game_piece(row_index, col_index, othello.WHITE)
                if self._othello_game_state.get_game_board()[row_index][col_index] == othello.BLACK:
                    self._draw_game_piece(row_index, col_index, othello.BLACK)

    def _draw_game_piece(self, row_index: int, col_index: int, player: str) -> None:
        """ This function draws a given game piece onto the game board canvas.
            It draws the game piece with respect to the player color and current
            width and height of the current column and row, respectively.
        """
        # Determine appropriate radius
        if self.get_row_height() > self.get_column_width():
            radius = self.get_column_width() * 0.4
        else:
            radius = self.get_row_height() * 0.4
            
        row_center = (row_index + 0.5) * self.get_row_height()
        col_center = (col_index + 0.5) * self.get_column_width()

        # Pick fill color 
        if player == othello.BLACK:
            fill_color = "black"
        if player == othello.WHITE:
            fill_color = "white"

        # Draw game piece
        self._game_board_canvas.create_oval(
            col_center - radius, row_center - radius,
            col_center + radius, row_center + radius,
            fill = fill_color)

if __name__ == "__main__":
    OthelloGame().start()
