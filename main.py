from node import Node
from plot import Plot
import time

# Parameters:
# n: the starting replication count
# i: replication count increment
Node.n = 2
Node.i = 0

# Codes
HEAD = 1
NECK = 2

# Dimensions
LINE_WIDTH = 2.0
HEAD_RADIUS = 6.0
OUTSIDE_RADIUS = HEAD_RADIUS + LINE_WIDTH

# Globals
paused = False
last_ordinal = None

# Methods
def motion(x, y):
    type, node = hit(hydra, x, y)
    if type == HEAD:
        plot.set_cursor('plus')
    elif type == NECK:
        plot.set_cursor('X_cursor')
    else:
        plot.set_cursor('arrow')

def click(x, y):
    type, node = hit(hydra, x, y)
    if type == HEAD:
        node.add(Node())
        update()

    elif type == NECK:
        node.chop_myself()
        update()

def play(delay):
    global paused
    paused = False
    while not hydra.is_head() and not paused:
        hydra.chop_child()
        update()
        plot.update()
        time.sleep(delay)

def pause():
    global paused
    paused = True

def button(option):
    global paused
    if option == 'SINGLE':
        hydra.chop_child()
        update()

    if option == 'PLAY':
        play(1.0)
            
    if option == 'FAST':
        play(0.1)
            
    elif option == 'PAUSE':
        pause()

    elif option == 'STOP':
        hydra.reset()
        update()

def resize():
    plot_hydra()

def plot_hydra():
    points.clear()
    plot.clear()
    depth = hydra.get_height()
    plot_node(
        hydra,
        plot.width / 2,
        OUTSIDE_RADIUS,
        plot.width - 2 * OUTSIDE_RADIUS,
        0 if depth == 0 else (plot.height - 2 * OUTSIDE_RADIUS) / (depth + 0.3)
    )
    plot_ordinal(plot.width/2 + HEAD_RADIUS + 14, 0, hydra.get_ordinal())

def plot_ordinal(x, y, ordinal):
    text = str(ordinal)
    x0 = x
    y0 = y
    dx = 0.7
    dy = 0.6
    size = 20
    scale = 0.7
    for char in text:
        if char == '↑':
            y += dy * size
            size *= scale
        elif char == '(':
            pass
        elif char == ')':
            size *= 1/scale
            y += -dy * size
        else:
            plot.text(x, y, char, int(size))
            x += dx * size

def plot_node(node, x, y, w, h):
    n = len(node.children)
    if not node.parent:
        points.append([node, x, y, None, None])

    if n:
        plot.circle(x, y, HEAD_RADIUS, fill='brown', outline='brown', width=0)
        for k, child in enumerate(node.children):
            x1, y1 = x - w*0.5 + (k + 0.5) * w / n, y + h
            plot.line(x, y, x1, y1, fill='brown', width=LINE_WIDTH)
            plot_node(child, x1, y1, w/n, h)
            points.append([child, x1, y1, x, y])
    else:
        plot.circle(x, y, HEAD_RADIUS, fill='green', outline='brown', width=LINE_WIDTH)

def hit(node, x, y):
    r = HEAD_RADIUS
    for node, x1, y1, x0, y0 in points:
        if (
            abs(x - x1) <= r and
            abs(y - y1) <= r
        ):
            return HEAD, node

        if node.is_head():
            if not x0 is None:
                if y0 + r < y and y1 - r > y:
                    xi = x1 + (y - y1) * (x0 - x1) / (y0 - y1)
                    if abs(x - xi) < r:
                        return NECK, node

    return None, None

def update():
    global last_ordinal

    plot_hydra()

    print(f'Height is {hydra.get_height()}')

    ordinal = hydra.get_ordinal()
    text1 = 'NEW'
    if last_ordinal:
        comparison = last_ordinal.compare(ordinal)
        text1 = 'LESS' if comparison > 0 else 'MORE' if comparison < 0 else 'EQUAL'
    print(f'Current is {text1}: {ordinal}')

    text2 = 'NEW'
    nines = ordinal.to_nines()
    if last_ordinal:
        last_nines = last_ordinal.to_nines()
        text2 = 'LESS' if nines > last_nines else 'MORE' if nines < last_nines else 'EQUAL'

    print(f'Previous was {text2}: {nines}')
    assert text1 == text2
    last_ordinal = ordinal

points = []
plot = Plot(motion, click, resize, button)

hydra = Node()
plot.loop() 

print('Finished')