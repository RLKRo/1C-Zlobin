# 1C-Zlobin

Not ready yet.

Usage:
python <main.py path> <filename>
 
The idea of the method:
1) find a stroke
2) find a corresponding line
3) if there are enough strokes intersecting that line then it is a straight line of a figure
4) find all the lines
5) define the type of the shape
6) find_line method returns two points of a line ---> calculate the length of it and the angle
7) for a triangle calculate the angle between the lines
8) for a circle (no lines found) find the most right and most left black points. Its radius is the half of their x difference
