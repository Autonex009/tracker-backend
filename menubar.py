import rumps
import subprocess
import os

class TrackerApp(rumps.App):
    def __init__(self):
        super(TrackerApp, self).__init__("WorkWise", icon="icon.icns", menu=["Start Tracking", "Stop Tracking", "Preferences", None, "Quit"])

    def on_start_tracking(self, _):
        rumps.notification("WorkWise", "Tracking Started", "Your activity tracking is now active.")

    def on_stop_tracking(self, _):
        rumps.notification("WorkWise", "Tracking Stopped", "Your activity tracking is now paused.")

    def on_preferences(self, _):
        rumps.alert("Preferences are not configured yet — we will add UI fields next.")

    def on_quit(self, _):
        rumps.quit_application()

    @rumps.clicked("Start Tracking")
    def start_clicked(self, _):
        self.on_start_tracking(_)

    @rumps.clicked("Stop Tracking")
    def stop_clicked(self, _):
        self.on_stop_tracking(_)

    @rumps.clicked("Preferences")
    def prefs_clicked(self, _):
        self.on_preferences(_)

    @rumps.clicked("Quit")
    def quit_clicked(self, _):
        self.on_quit(_)

if __name__ == "__main__":
    TrackerApp().run()
