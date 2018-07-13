# webvn

This is the tool that created the Endgames Visual Novel feated on Megatokyo.com in 2015. It generates pure HTML+CSS "linear" visual novels, though in theory it can be adapted for branching storylines.


## Usage

I'm not entirely sure this is in a working state, but generally:

- Write your script in the [webvn](https://megatokyo.com/endgames-vn/part1.webvn) format.
- Build a bunch of PNG assets.
- Run `genweb.py` to build HTML assets.
- Write the CSS for [scene descriptions](https://megatokyo.com/endgames-vn/scenes.css).
