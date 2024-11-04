import streamlit as st
import numpy as np
import random

# 棋盘的大小
SIZE = 6

# 初始化棋盘
def init_game():
    board = np.zeros((SIZE, SIZE), dtype=int)
    add_new_number(board)
    add_new_number(board)
    return board

# 随机添加数字 2 或 4
def add_new_number(board):
    empty_cells = [(i, j) for i in range(SIZE) for j in range(SIZE) if board[i][j] == 0]
    if empty_cells:
        x, y = random.choice(empty_cells)
        board[x][y] = random.choice([2, 4])

# 滑动并合并
def slide_and_merge(row):
    new_row = [i for i in row if i != 0]
    for i in range(len(new_row)-1):
        if new_row[i] == new_row[i+1]:  # 合并相邻相同数字
            new_row[i] *= 2
            new_row[i+1] = 0
    new_row = [i for i in new_row if i != 0]
    return new_row + [0] * (SIZE - len(new_row))

# 上下左右移动的逻辑
def move_left(board):
    new_board = np.zeros((SIZE, SIZE), dtype=int)
    for i in range(SIZE):
        new_board[i] = slide_and_merge(board[i])
    return new_board

def move_right(board):
    new_board = np.zeros((SIZE, SIZE), dtype=int)
    for i in range(SIZE):
        new_board[i] = slide_and_merge(board[i][::-1])[::-1]
    return new_board

def move_up(board):
    return np.transpose(move_left(np.transpose(board)))

def move_down(board):
    return np.transpose(move_right(np.transpose(board)))

# 检查是否可以继续游戏
def is_game_over(board):
    if np.any(board == 0):  # 仍有空位
        return False
    for i in range(SIZE):
        for j in range(SIZE - 1):
            if board[i][j] == board[i][j + 1] or board[j][i] == board[j + 1][i]:
                return False
    return True

# Streamlit 界面
st.title("2048 Game - 6x6 Grid")
if 'board' not in st.session_state:
    st.session_state.board = init_game()

# 显示棋盘
def display_board(board):
    for row in board:
        st.write(" | ".join([str(int(cell)).center(4) if cell != 0 else " " for cell in row]))

# 控制游戏的按钮
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("Left"):
        new_board = move_left(st.session_state.board)
        if not np.array_equal(st.session_state.board, new_board):
            st.session_state.board = new_board
            add_new_number(st.session_state.board)

with col2:
    if st.button("Right"):
        new_board = move_right(st.session_state.board)
        if not np.array_equal(st.session_state.board, new_board):
            st.session_state.board = new_board
            add_new_number(st.session_state.board)

with col3:
    if st.button("Up"):
        new_board = move_up(st.session_state.board)
        if not np.array_equal(st.session_state.board, new_board):
            st.session_state.board = new_board
            add_new_number(st.session_state.board)

with col4:
    if st.button("Down"):
        new_board = move_down(st.session_state.board)
        if not np.array_equal(st.session_state.board, new_board):
            st.session_state.board = new_board
            add_new_number(st.session_state.board)

# 显示当前棋盘
display_board(st.session_state.board)

# 检查游戏是否结束
if is_game_over(st.session_state.board):
    st.write("Game Over!")
else:
    st.write("Keep going!")
