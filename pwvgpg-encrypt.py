import gnupg

gpg_home = "$HOME/.gnupg"
gpg = gnupg.GPG(gnupghome=gpg_home)
data = "my-unencrypted.txt"
savefile = data+".asc"
passph = raw_input("Enter key IDs separated by spaces: ")
afile = open(data, "rb")
encrypted_ascii_data = gpg.encrypt_file(afile, recipients=None, symmetric='AES256', passphrase=passph, output=savefile)
afile.close()
