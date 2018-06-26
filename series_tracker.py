import npyscreen
from os import listdir
from os.path import isfile, join

TRACKER_FILENAME = ".watched"


class dir_selector_form(npyscreen.Form):
    def afterEditing(self):
        self.selected_dir = self.dir_selector.get_value()
        with open("./.lastdir", "w+") as f:
            f.write(self.selected_dir)
        self.files_in_dir = [
            f for f in listdir(self.selected_dir)
            if isfile(join(self.selected_dir, f)) and f != TRACKER_FILENAME
        ]
        self.parentApp.getForm("EPI_SEL_FORM").update(self.files_in_dir)
        self.parentApp.setNextForm("EPI_SEL_FORM")

    def create(self):
        self.dir_selector = self.add(
            npyscreen.TitleFilenameCombo,
            select_dir=True,
            exit_right=True,
            name="Select directory:")
        try:
            with open("./.lastdir", "r") as f:
                self.dir_selector.value = f.read()
        except FileNotFoundError:
            pass


class episode_selector_form(npyscreen.Form):
    def afterEditing(self):
        file_path = self.prev_form.selected_dir + "\\" + TRACKER_FILENAME
        with open(file_path, "w+") as f:
            selected_episodes = self.episode_selector.get_selected_objects()
            f.writelines("%s\n" % l for l in selected_episodes)
        self.parentApp.setNextForm(None)

    def update(self, files):
        self.episode_selector.values = files
        try:
            file_path = self.prev_form.selected_dir + "\\" + TRACKER_FILENAME
            with open(file_path, "r") as f:
                self.watched_episodes = f.read().splitlines()
                self.episode_selector.value = [
                    i for i, f in enumerate(files)
                    if f in self.watched_episodes
                ]
        except FileNotFoundError:
            pass

    def create(self):
        self.prev_form = self.parentApp.getForm("MAIN")
        self.episode_selector = self.add(
            npyscreen.MultiSelect,
            scroll_exit=True,
            slow_scroll=True)


class series_tracker_app(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", dir_selector_form)
        self.addForm("EPI_SEL_FORM", episode_selector_form)


if __name__ == "__main__":
    series_tracker_app = series_tracker_app().run()
