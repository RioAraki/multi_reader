#!/usr/bin/env python
import os
import zipfile

def zipdir(path, ziph):
    # ziph is zipfile handle

    # This method only copy all *files*
    for root, dirs, files in os.walk(path):
        os.chdir('SDYXZ')
        ziph.write('META-INF/container.xml')
        for file in files:
            ziph.write(file)


def main():
    pass

if __name__ == '__main__':
    zipf = zipfile.ZipFile('射雕英雄传.epub', 'w', zipfile.ZIP_DEFLATED)
    zipdir('SDYXZ', zipf)
    zipf.close()
