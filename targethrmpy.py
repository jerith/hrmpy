from hrmpy.main import entry_point


def target(driver, args):
    driver.exe_name = 'hrmpy-%(backend)s'
    return entry_point, None
