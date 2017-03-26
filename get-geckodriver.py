#!/usr/bin/env python3.6
import argparse
import io
import tarfile
import urllib.request


URL = (
    'https://github.com/mozilla/geckodriver/releases/download/'
    '{tag}/geckodriver-{tag}-linux64.tar.gz'
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('tag')
    args = parser.parse_args()

    resp = urllib.request.urlopen(URL.format(tag=args.tag))
    fileobj = io.BytesIO(resp.read())
    with tarfile.open(fileobj=fileobj) as tar:
        geckodriver, = tar.members
        assert geckodriver.name == 'geckodriver', geckodriver.name
        tar.extract(geckodriver, 'bin')


if __name__ == '__main__':
    exit(main())
