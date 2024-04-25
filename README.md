# Intro to AI

# README

## Running the Program

To run the program, simply execute the `game.py` file. This will launch the game interface.

## Interface Overview

Upon running the program, a window will appear with several buttons under the title "Choose game mode." Here's what each button does:

- **Human Player**: Allows you to play the game manually using the arrow keys on your keyboard.
- **Ai player minimax**: Initiates a game where the AI player uses the Minimax algorithm.
- **Ai player expectimax**: Initiates a game where the AI player uses the Expectimax algorithm.
- **Ai player expectimax epsilon**: Initiates a game where the AI player uses the Expectimax with Epsilon algorithm.
- **Ai player expectibetter**: Initiates a game where the AI player uses the Expectibetter algorithm.

## Game Statistics

When playing against one of the AI players, the game will generate a file named `game_stats.csv`. This file contains statistics regarding the gameplay, including:

- Algorithm used
- Number of moves made
- Final score achieved
- Number of nodes expanded during gameplay
- Number of 2048 tiles obtained
- Number of 1024 tiles obtained
- Number of 512 tiles obtained
- Number of 128 tiles obtained
- Number of 64 tiles obtained

These statistics can be useful for analyzing the performance of different AI algorithms.