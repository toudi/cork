class transaction(object):
    def __init__(self, db, exception_on_failure=None):
        self.db = db
        self.exception_on_failure = exception_on_failure

    def __enter__(self):
        return self.db

    def __exit__(self, type, value, traceback):
        try:
            self.db.session.commit()
        except:
            self.db.session.rollback()
            if self.exception_on_failure:
                raise self.exception_on_failure()
            raise
