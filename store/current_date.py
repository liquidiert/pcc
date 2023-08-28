class CurrentDateStore():
    current_date = None

    @property
    def has_date(self):
        return self.current_date is not None