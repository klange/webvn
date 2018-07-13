# webvn

This is the tool that created the Endgames Visual Novel featured on Megatokyo.com in 2015. It generates pure HTML+CSS "linear" visual novels, though in theory it can be adapted for branching storylines.


## Usage

Examine the `demo.webvn` to understand the syntax of the input files, and create assets for your characters and background scenes. Edit `scenes.css` to add new scene descriptions, and edit `vn.css` to change the look and feel of the text boxes.

Running `python2 genweb.py demo.webvn` will create a series of files `demo_0.htm` (and so on) for each of the music segments in your source file. `index.htm` is configured to load the first frame of the demo script.
