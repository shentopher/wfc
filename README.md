# Wave Function Collapse: a Python Interpretation 
## Project Information
**Author**: Christopher Shen | **Affiliation**: University of Pennsylvania | **Email**: christophershen32@gmail.com

## Introduction
Wave Function Collapse (WFC) is a beautiful algorithm devised by Maxim Gumin (Twitter @ExUtumno) and employed by the likes of Oskar Stålberg for procedural world and image generation. It draws inspiration from the quantum physics concept of the same name, which describes the 'collapse' of a wave function from a superposition of eigenstates into a single eigenstate. 

The scope of this project is to port the algorithm into Python, as well as tinker with alternative heuristics. 

## How it Works

Broadly, the algorithm works as follows:
1. Given an input image, divide it up into N x N patterns of tiles (for most cases, a tile will be a pixel. however, given larger image inputs it may be better practice to have a tile be a 2 x 2 grid of pixels). For example, if the size of the input image is 10 x 10, a tile is a pixel, and N x N, the image will be divided up into 25 2 x 2 patterns (assuming that all patterns are unique).
2. Create an array of a desired output dimension (which we will call a 'wave'). Each element in the array represents the *state* of a N x N region in the output. The *state* is a superposition of all possible N x N patterns that may exist, expressed in terms of boolean coefficients. So for example, if there are 9 different N x N patterns in total, the states would be a list of 9 booleans describing whether the corresponding pattern is allowed or forbidden in that particular element of the grid. 
3. Initialize the array in a completely unobserved state (all boolean coefficients are default set to False)
4. Repeat through the following steps
   1. *Observation*
      1. Find the element in the wave that has the lowest non-zero entropy. If there are no such elements, break the cycle.
      2. Collapse the element to a single definite state according to the distribution of N x N patterns in the input and the coefficients of the state.
   2. *Propogation* propogate the collapse and update the states in the rest of the wave.
5. All states are either collpased, or the wave exists in an unsolvable state (which is usually pretty rare). Return the result.

## Credits and Inspiration

To learn more about WFC, I would highly recommend watching [this video](https://www.youtube.com/watch?v=2SuvO4Gi7uY&ab_channel=MartinDonald) by Martin Donald, who introduces the concept using Sudoku. The [original repository](https://github.com/mxgmn/WaveFunctionCollapse) also contains a lot of general purpose information and interesting work that people have applied WFC to in the past. 

This work draws from the original repo, and it is deeply inspired by the work done by [Isaac Karth](https://github.com/ikarth/wfc_2019f) in terms of modularization of the codebase as well as best practices for method implementation.

## Running Wave Function Collapse
TODO
