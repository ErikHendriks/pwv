import gnupg

gpg_home = "$HOME/.gnupg"
gpg = gnupg.GPG(gnupghome=gpg_home)
data = "$HOME/pwv/database/oaslkd/oaslkd.asc"
savefile = "my-unencrypted.txt"
passwd = raw_input("Enter key IDs separated by spaces: ")
afile = open(data, "rb")
encrypted_ascii_data = gpg.decrypt_file(afile, passphrase=passwd)
print encrypted_ascii_data
afile.close()
