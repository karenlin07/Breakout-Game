# 202411
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GRect, GLabel
from leaderboard import get_sorted_scores


class LeaderboardGraphics:
    def __init__(self, window_width, window_height):
        # Only pass the window width and height
        self.window_width = window_width
        self.window_height = window_height

        # Create a transparent background rectangle to hold the leaderboard
        self.leaderboard = GRect(self.window_width * 0.8, self.window_height * 0.8)
        self.leaderboard.filled = True
        self.leaderboard.fill_color = 'white'

        # Create a graphical window to display the leaderboard
        self.window = GWindow(self.window_width, self.window_height)
        self.window.add(self.leaderboard, self.window_width * 0.1, self.window_height * 0.1)

        title = GLabel("Leaderboard")
        title.font = "Times-36"
        self.window.add(title, self.window_width / 2 - title.width / 2, self.window_height * 0.2)

        # Display the scores
        self.show_scores()

    def show_scores(self):
        # Get the sorted scores
        scores = get_sorted_scores()
        y_offset = self.window_height * 0.25

        for i, score in enumerate(scores[:10], start=1):  # Only display the top 10 scores
            score_label = GLabel(f"{i}. {score}")
            score_label.font = "Times-24"
            self.window.add(score_label, self.window_width / 2 - score_label.width / 2, y_offset)
            y_offset += 30  # Adjust the vertical position for the next score
