import os
import zipfile
# import StringIO

def compress(folder):

    filenames = []

    # zip name before the extension
    zip_subdir = 'filename'

    # zip name with extension
    zip_filename = '%s.zip' % zip_subdir

    zf = zipfile.ZipFile("new_zip_files", "w")
    # Open StringIO to grab in-memory ZIP contents
    # s = StringIO.StringIO()

    for fpath in filenames:
        fdir, fname = os.path.split(fpath)
        zip_path = os.path.join(zip_subdir, fname)

        zf.write(fpath, zip_path)

if __name__ == '__main__':
