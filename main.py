import subprocess
import signal
import threading


class MediaPlayer:

    def __init__(self):
        self.player_process = None
        self.ytdlp_process = None
        self.is_paused = False

    def play(self, query):
        self.stop()

        cmd = [
            "yt-dlp",
            f"ytsearch1:{query}",
            "-f",
            "bestaudio",
            "-o",
            "-"
        ]

        player = [
            "ffplay",
            "-nodisp",
            "-autoexit",
            "-i",
            "-"
        ]

        self.ytdlp_process = subprocess.Popen(cmd, stdout=subprocess.PIPE)

        self.player_process = subprocess.Popen(
            player,
            stdin=self.ytdlp_process.stdout,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        print(f"▶ Playing: {query}")

    def pause(self):
        if self.player_process and not self.is_paused:
            self.player_process.send_signal(signal.SIGSTOP)
            self.is_paused = True
            print("⏸ Paused")

    def resume(self):
        if self.player_process and self.is_paused:
            self.player_process.send_signal(signal.SIGCONT)
            self.is_paused = False
            print("▶ Resumed")

    def stop(self):
        if self.player_process:
            self.player_process.terminate()
            self.player_process = None

        if self.ytdlp_process:
            self.ytdlp_process.terminate()
            self.ytdlp_process = None

        self.is_paused = False

    def is_playing(self):
        return self.player_process and self.player_process.poll() is None


def command_loop(player):

    while True:

        cmd = input("\nCommand (p=pause, r=resume, s=stop, n=next, q=quit): ")

        if cmd == "p":
            player.pause()

        elif cmd == "r":
            player.resume()

        elif cmd == "s":
            player.stop()

        elif cmd == "n":
            player.stop()
            song = input("Next song: ")
            player.play(song)

        elif cmd == "q":
            player.stop()
            break


if __name__ == "__main__":

    player = MediaPlayer()

    first_song = input("Enter song: ")
    player.play(first_song)

    command_loop(player)