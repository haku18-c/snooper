from ftplib import FTP


banner = r'''

                               ,        ,
                              /(        )`
                              \ \___   / |
                              /- _  `-/  '
                             (/\/ \ \   /\
                             / /   | `    \
                             O O   ) /    |
                             `-^--'`<     '
                            (_.)  _  )   /
                             `.___/`    /
                               `-----' /
FTPClient         <----.     __ / __   \
                  <----|====O)))==) \) /====
1. Daftar         <----'    `--' `.__,' \
2. Unggah                     |        |
3. Unduh                      \       /
4. Hapus                ______( (_  / \______
5. Kembali             ,'  ,-----'   |        \
6. Keluar              `--{__________)        \/

'''


def fbanner():
    return banner


class FTPClient:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.ftp = FTP(self.host)

    def login(self):
        try:
            self.ftp.login(self.username, self.password)
            print(f"Masuk sebagai {self.username}")
        except Exception as e:
            print(f"Gagal masuk : {str(e)}")

    def list_files(self):
        try:
            self.ftp.dir()
        except Exception as e:
            print(f"Gagal mendapatkan daftar file : {str(e)}")

    def download_file(self, remote_filepath, local_filepath):
        try:
            with open(local_filepath, 'wb') as local_file:
                self.ftp.retrbinary(f"RETR {remote_filepath}", local_file.write)
            print(f"terunduh {remote_filepath} to {local_filepath}")
        except Exception as e:
            print(f"Gagal mengunduh file: {str(e)}")

    def upload_file(self, local_filepath, remote_filepath):
        try:
            with open(local_filepath, 'rb') as local_file:
                self.ftp.storbinary(f"STOR {remote_filepath}", local_file)
            print(f"Terunggah {local_filepath} ke {remote_filepath}")
        except Exception as e:
            print(f"Gagal unggah file: {str(e)}")

    def delete_file(self, remote_filepath):
        try:
            self.ftp.delete(remote_filepath)
            print(f"{remote_filepath} berhasil dihapus")
        except Exception as e:
            print(f"Gagal menghapus file: {str(e)}")

    def close(self):
        try:
            self.ftp.quit()
            print("Koneksi terputus")
        except Exception as e:
            print(f"Gagal memutuskan koneksi: {str(e)}")

