#!/usr/bin/env python
import os
import zipfile
import shutil
import logging

logging.basicConfig(level=logging.INFO)

def zipdir(path, ziph, name):
    # ziph is zipfile handle

    # This method only copy all *files*
    for root, dirs, files in os.walk(path):
        os.chdir(name)
        ziph.write('META-INF/container.xml')
        for file in files:
            ziph.write(file)

def compress(name):
    epub_name = name + '.epub'
    logging.info("Compressing all files and convert to epub...")
    zipf = zipfile.ZipFile(epub_name, 'w', zipfile.ZIP_DEFLATED)
    zipdir(name, zipf, name)
    zipf.close()
    logging.info("Delete the unneeded folder...")
    os.chdir("..")
    shutil.rmtree(name)
    logging.info("Done")

if __name__ == '__main__':
    pass