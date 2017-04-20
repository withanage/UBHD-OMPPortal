import logging, logging.handlers

class GAEHandler(logging.Handler):
    """
    Logging handler for GAE DataStore
    """
    def emit(self, record):

        from google.appengine.ext import db

        class Log(db.Model):
            name = db.StringProperty()
            level = db.StringProperty()
            module = db.StringProperty()
            func_name = db.StringProperty()
            line_no = db.IntegerProperty()
            thread = db.IntegerProperty()
            thread_name = db.StringProperty()
            process = db.IntegerProperty()
            message = db.StringProperty(multiline=True)
            args = db.StringProperty(multiline=True)
            date = db.DateTimeProperty(auto_now_add=True)

        log = Log()
        log.name = record.name
        log.level = record.levelname
        log.module = record.module
        log.func_name = record.funcName
        log.line_no = record.lineno
        log.thread = record.thread
        log.thread_name = record.threadName
        log.process = record.process
        log.message = record.msg
        log.args = str(record.args)
        log.put()

def get_configured_logger(name):
    logger = logging.getLogger(name)
    if (len(logger.handlers) == 0):
        # This logger has no handlers, so we can assume it hasn't yet been configured
        # (Configure logger)

        # Create default handler
        if request.env.web2py_runtime_gae:
            # Create GAEHandler
            handler = GAEHandler()
        else:
            # Create RotatingFileHandler
            import os
            formatter="%(asctime)s %(levelname)s %(process)s %(thread)s %(funcName)s():%(lineno)d %(message)s"
            handler = logging.handlers.RotatingFileHandler(os.path.join(request.folder,'private/app.log'),maxBytes=1024,backupCount=2)
            handler.setFormatter(logging.Formatter(formatter))

        handler.setLevel(logging.DEBUG)

        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

        # Test entry:
        logger.debug(name + ' logger created')
    else:
        # Test entry:
        logger.debug(name + ' already exists')

    return logger

# Assign application logger to a global var

logger = get_configured_logger(request.application)
