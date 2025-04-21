
from campy.graphics.gobjects import GLabel
from campy.gui.events.timer import pause
from breakoutgraphics import BreakoutGraphics
from leaderboard import load_scores, save_scores
from leaderboardgraphics import LeaderboardGraphics

FRAME_RATE = 10  # 100 frames per second
NUM_LIVES = 3  # Number of attempts


def main():
    graphics = BreakoutGraphics()
    lives = NUM_LIVES

    while True:
        dx = graphics.get_dx()
        dy = graphics.get_dy()
        graphics.ball.move(dx, dy)
        pause(FRAME_RATE)
        graphics.update()

        if graphics.ball.y + graphics.ball.height > graphics.window.height:
            graphics.restart()
            lives -= 1

        if lives == 0:
            game_over = GLabel('Game Over.')
            game_over.font = 'Times-40'
            graphics.window.add(game_over, graphics.window.width / 2 - game_over.width / 2,
                                graphics.window.height / 2 + game_over.height)
            save_scores(graphics.score)
            leaderboard_graphics = LeaderboardGraphics(graphics.window.width, graphics.window.height)
            break

        if not graphics.bricks:
            win = GLabel("You win")
            win.font = "Times-40"
            graphics.window.add(win, (graphics.window.width - win.width), (graphics.window.height + win.height))
            graphics.window.remove(graphics.paddle)
            graphics.window.remove(graphics.ball)
            save_scores(graphics.score)
            leaderboard_graphics = LeaderboardGraphics(graphics.window.width, graphics.window.height)
            break

        if graphics.ball.x <= 0 or graphics.ball.x + graphics.ball.width >= graphics.window.width:
            graphics.set_dx(-dx)
        if graphics.ball.y <= 0:
            graphics.set_dy(-dy)
        if graphics.ball.y + graphics.ball.height > graphics.window.height:
            graphics.restart()

        graphics.check_collisions()


if __name__ == '__main__':
    main()
