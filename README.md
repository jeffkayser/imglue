# Imglue

## What is it

Create a single CSS "sprite" from a set of images, and output some reasonable CSS code to bootstrap it to stdout.

- See [this article](http://www.alistapart.com/articles/sprites) for an introduction on CSS sprites.

It can also be used as a utility to quickly concatenate images in general.


## How to use it

Install [Python Imaging Library](http://www.pythonware.com/products/pil/) (PIL)

*Usage*:

```
python imglue.py h[orizontal] | v[ertical] | g[rid] FILE-1 [... FILE-n] OUTFILE
```

- horizontal: Place images side-by-side
- vertical:   Stack images on top of each other
- grid:       Align images into a grid


## Examples

$ python imglue.py horizontal a.png b.png c.png d.png sprite.png

Will yield a sprite.png consisting of:

    [a][b][c][d]

$ python imglue.py vertical a.png b.png c.png d.png sprite.png

Will yield a sprite.png consisting of:

    [a]
    [b]
    [c]
    [d]

$ python imglue.py grid a.png b.png c.png d.png sprite.png

Will yield a sprite.png consisting of:

    [a][b]
    [c][d]

