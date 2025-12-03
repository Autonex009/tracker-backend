import rumps
import subprocess
import os

class TrackerApp(rumps.App):
    def __init__(self):
        super(TrackerApp, self).__init__("🟢", title="Activity Tracker")
        self.menu = [
            "Start Tracking",
            "Stop Tracking",
            None,
            "Quit"
        ]
        self.tracking_process = None

    @rumps.clicked("Start Tracking")
    def start_tracking(self, _):
        if self.tracking_process is None:
            self.tracking_process = subprocess.Popen(["python3", "main.py"])
            rumps.notification(
                "Tracking Started",
                "",
                "Your activity is being logged with consent."
            )

    @rumps.clicked("Stop Tracking")
    def stop_tracking(self, _):
        if self.tracking_process:
            self.tracking_process.terminate()
            self.tracking_process = None
            rumps.notification("Tracking Stopped", "", "Activity tracking stopped.")

    @rumps.clicked("Quit")
    def quit_app(self, _):
        if self.tracking_process:
            self.tracking_process.terminate()
        rumps.quit_application()


if __name__ == "__main__":
    TrackerApp().run()
