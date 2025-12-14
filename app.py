import streamlit as st
import random

st.set_page_config(page_title="Tic Tac Toe", layout="centered")

# ---------- GAME LOGIC ----------

def check_winner(board):
    win_combinations = [
        [0,1,2], [3,4,5], [6,7,8],   # rows
        [0,3,6], [1,4,7], [2,5,8],   # columns
        [0,4,8], [2,4,6]             # diagonals
    ]
    for combo in win_combinations:
        a, b, c = combo
        if board[a] == board[b] == board[c] and board[a] != "":
            return board[a]
    if "" not in board:
        return "Draw"
    return None


def computer_move():
    empty_cells = [i for i, v in enumerate(st.session_state.board) if v == ""]
    if empty_cells:
        move = random.choice(empty_cells)
        st.session_state.board[move] = st.session_state.computer


def reset_game():
    st.session_state.board = [""] * 9
    st.session_state.winner = None
    st.session_state.game_started = False


# ---------- SESSION STATE ----------

if "board" not in st.session_state:
    reset_game()

if "player" not in st.session_state:
    st.session_state.player = "X"

if "computer" not in st.session_state:
    st.session_state.computer = "O"

# ---------- UI ----------

st.title("🎮 Tic Tac Toe")

if not st.session_state.game_started:
    st.subheader("Choose your symbol")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Play as X"):
            st.session_state.player = "X"
            st.session_state.computer = "O"
            st.session_state.game_started = True

    with col2:
        if st.button("Play as O"):
            st.session_state.player = "O"
            st.session_state.computer = "X"
            st.session_state.game_started = True

else:
    st.subheader(f"You are **{st.session_state.player}**")

    # Game Grid
    cols = st.columns(3)
    for i in range(9):
        with cols[i % 3]:
            if st.button(
                st.session_state.board[i] if st.session_state.board[i] != "" else " ",
                key=i,
                disabled=st.session_state.board[i] != "" or st.session_state.winner
            ):
                # Player move
                st.session_state.board[i] = st.session_state.player

                # Check winner after player move
                st.session_state.winner = check_winner(st.session_state.board)

                # Computer move if game not over
                if not st.session_state.winner:
                    computer_move()
                    st.session_state.winner = check_winner(st.session_state.board)

    # Result
    if st.session_state.winner:
        if st.session_state.winner == "Draw":
            st.info("It's a Draw!")
        elif st.session_state.winner == st.session_state.player:
            st.success("🎉 You Win!")
        else:
            st.error("💻 Computer Wins!")

        if st.button("Restart Game"):
            reset_game()
