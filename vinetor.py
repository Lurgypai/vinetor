#!/bin/python3

from PIL import Image
import sys, random

compression_factor = 32 

sprites = Image.open("sprites_palette.png")
sprites = sprites.convert("RGB")
palette = Image.new("RGB", (256, 1))

sprite_num = 0
palette_to_sprite = {}

for row in range(0, 16):
    for col in range(0, 16):
        x, y = row*12, col*12
        avg_r, avg_g, avg_b = 0, 0, 0
        pixels_used = 0
        for x_offset in range(0, 8):
            for y_offset in range(0, 8):
                i = y_offset
                r, g, b = sprites.getpixel((x + x_offset, y + y_offset))
                if not (r == 255 and b == 255 and g == 0):
                    avg_r += r
                    avg_g += g
                    avg_b += b
                    pixels_used += 1

        # I dont' know anything about image processing,
        # so here's a really lazy way to compress colors so that more things will share the same colors.
        avg_r /= pixels_used * compression_factor
        avg_g /= pixels_used * compression_factor
        avg_b /= pixels_used * compression_factor

        avg_r = int(avg_r) * compression_factor
        avg_g = int(avg_g) * compression_factor
        avg_b = int(avg_b) * compression_factor

        color = (avg_r, avg_g, avg_b)
        if color == (0, 0, 0):
            print('black found')

        if color in palette_to_sprite:
            palette_to_sprite[color] += [(x, y)]
        else:
            palette_to_sprite[color] = [(x, y)]
            palette.putpixel((sprite_num, 0), color)

        
        sprite_num += 1

# for some reason, it inserts black pixels into the output. I'm too tired to figure out why
palette_to_sprite[(0, 0, 0)] = [(84, 180), (72, 168)]

palette = palette.convert("P", palette=Image.Palette.ADAPTIVE)
# palette.save("pallete.png")

target_image = Image.open(sys.argv[1])
target_image = target_image.quantize(palette=palette, dither=Image.Dither.NONE)
# target_image = target_image.quantize(palette=palette)
# target_image.save("test_save.png")
target_image = target_image.convert("RGB")

output_image = Image.new("RGB", (target_image.width * 9 + 1, target_image.height * 9 + 1), (0, 0, 0))

sprites_to_be_pasted = Image.open("sprites.png")

for x in range(0, target_image.width):
    for y in range(0, target_image.height):
        color = target_image.getpixel((x, y))
        if not color in palette_to_sprite:
            continue
        palette_x, palette_y = random.choice(palette_to_sprite[color])
        cropped = sprites_to_be_pasted.crop((palette_x, palette_y, palette_x + 8, palette_y + 8))
        output_x, output_y = x * 9 + 1, y * 9 + 1 
        output_image.paste(cropped, (output_x, output_y, output_x + 8, output_y + 8))

output_image.save(sys.argv[1].split('.')[0] + "_output.png")
