# Draw polygons!
# Use A to add a point
# Use Space to add the final point in a group, starting a new one.
# Use C to delete the latest group and go back to the previous one
# Use R to completely reset the canvas
# Use Z to delete the latest point
# Use P to print the points normalised to the screen size
# Use F to print the normalised points, but flipped vertically

# I love pygame !!
import pygame


def screen_size():
    return 500, 500


def normalise(pts, flip: bool = False):
    """Takes in a list of lists of points,
    returns it in the same shape but normalised to the screen size.
    flip=True if you want to flip the image vertically."""
    ret = []
    w, h = screen_size()

    for ls in pts:
        # Ignore empty lists
        # We'll get one at the end if the user presses p after space
        if not ls:
            continue

        new_ls = []
        for (x, y) in ls:
            if flip:
                new_ls.append((x/w, y/h))
            else:
                new_ls.append((x/w, 1 - y/h))

        ret.append(new_ls)

    return ret


def main():
    pygame.init()

    screen = pygame.display.set_mode(screen_size())
    clock = pygame.time.Clock()

    pts = [[]]

    running = True
    while running:
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYUP:
                # Add a group
                if e.key == pygame.K_SPACE:
                    pts[-1].append(pygame.mouse.get_pos())
                    pts.append([])

                # Add a point
                elif e.key == pygame.K_a:
                    pts[-1].append(pygame.mouse.get_pos())

                # Reset the whole list
                elif e.key == pygame.K_r:
                    pts.clear()
                    pts.append([])

                # delete last point
                elif e.key == pygame.K_z:
                    if len(pts[-1]) > 0:
                        del pts[-1][-1]

                # delete last group
                elif e.key == pygame.K_c:
                    if len(pts) > 1:
                        del pts[-1]

                    # Let's keep at least one group
                    elif len(pts) == 1:
                        pts[-1].clear()

                # print points normalised
                elif e.key == pygame.K_p:
                    print(normalise(pts, flip=False))

                # print points normalised but flipped on the y axis
                elif e.key == pygame.K_f:
                    print(normalise(pts, flip=True))

        screen.fill(0xffffff)

        for idx in range(len(pts)):
            # This is inefficient. Too bad!
            inner_pts = pts[idx].copy()

            # Draw what the poly would look like if
            # the mouse was the last point on the polygon
            if idx == len(pts) - 1:
                inner_pts.append(pygame.mouse.get_pos())

            match len(inner_pts):
                # Don't draw if empty
                case 0:
                    pass
                # Draw just the point
                case 1:
                    pygame.draw.circle(screen, 0x000000, inner_pts[0], 2)

                # Can now use polygon
                case _:
                    pygame.draw.polygon(screen, 0x000000, inner_pts, 4)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
