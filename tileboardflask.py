#!/usr/bin/env python

#------------------------------------------------------------------------
# 8Board.py
# Author: Vedant Dhopte
#------------------------------------------------------------------------

from flask import Flask, request, make_response, redirect, url_for
from flask import render_template
from sys import stderr
from BoardSolver import Solver, Board

#------------------------------------------------------------------------

app = Flask(__name__, template_folder='webpages')

#------------------------------------------------------------------------

@app.route('/', methods=['GET'])
def home():
    html = render_template('index.html')
    response = make_response(html)
    return response

#------------------------------------------------------------------------

@app.route('/solveBoard', methods=['GET'])
def solveBoard():
    tiles = request.args.get('board')
    boardSize = int(request.args.get('boardSize'))
    algorithm = request.args.get('algorithm')
    iterations = int(request.args.get('iterations'))

    temp = [[0 for i in range(boardSize)] for j in range(boardSize)]
    tiles = tiles.strip(" ")
    tiles = tiles.split(',')
    counter = 0
    for i in range(boardSize):
        for j in range(boardSize):
            temp[i][j] = tiles[counter]
            counter += 1
    tiles = temp

    ogboard = Board(tiles)

    solvable = ogboard.isSolvable()

    if solvable:
        solution = Solver(ogboard, algorithm, iterations)
        solutionTree = []
        for board in solution.solution():
            solutionTree.append(board.tilescopy)

    else:
        solutionTree = None

    html = render_template('index.html', initialBoard = ogboard.tilescopy, solutionTree = solutionTree, solvable = solvable)
    response = make_response(html)
    return response