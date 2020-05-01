#!/usr/bin/env python3
import argparse
import contextlib
import os.path

from selenium.webdriver.firefox.webdriver import WebDriver


SIZES = {
    '1080p': (1920, 1080),
    '720p': (1280, 720),
    'panel':  (320, 100),
}


@contextlib.contextmanager
def webdriver(*args, **kwargs):
    driver = WebDriver(*args, **kwargs)
    try:
        yield driver
    finally:
        driver.quit()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('html_file')
    parser.add_argument('--size', choices=SIZES, default='720p')
    args = parser.parse_args()

    # Put geckodriver on the PATH
    bindir = os.path.abspath('bin')
    path = os.environ['PATH']
    os.environ['PATH'] = f'{bindir}{os.pathsep}{path}'

    width, height = SIZES[args.size]
    filepath = os.path.abspath(args.html_file)
    basename, _ = os.path.splitext(args.html_file)
    screenshot = f'{basename}-{args.size}.png'

    with webdriver() as driver:
        driver.get(f'file://{filepath}')
        driver.execute_script(
            f'window.open('
            f'    "file://{filepath}", "test",'
            f'    "innerWidth={width},innerHeight={height}"'
            f');\n'
        )

        # Switch to our new window
        handle, = set(driver.window_handles) - {driver.current_window_handle}
        driver.switch_to.window(handle)

        driver.save_screenshot(screenshot)


if __name__ == '__main__':
    exit(main())
