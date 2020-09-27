import sqlite3
import cryptography
import base64
import sys
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

print(len(sys.argv))
if len(sys.argv) == 1:
    con = sqlite3.connect("db.sqlite3")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM auth_user;")

    #contains algorithm and iteration
    algo_iterations = []
    #contains salt, hash
    salt_hash = []
    #contains a username, salt_hash[0] corresponds to users[0] and so on
    users = []
    for x in cursor.fetchall():
        entry_list = x[1].rsplit('$')
    
        #algo and iteration
        ai_entry = entry_list[0] + '$' + entry_list[1]
        if ai_entry not in algo_iterations:
            algo_iterations.append(ai_entry)

        sh_entry = entry_list[2] + '$' + entry_list[3]
        if sh_entry not in salt_hash:
            salt_hash.append(sh_entry)
            users.append(x[4])

    print(users)
    common_list = ["123456", "123456789", "qwerty", "password", "1234567", "12345678", "12345", "iloveyou", "111111",
                "123123", "abc123", "qwerty123", "1q2w3e4r", "admin", "qwertyuiop", "654321", "555555", "lovely",
                "7777777", "welcome", "888888", "princess", "dragon", "password1", "123qwe"]

    #for every algo/iter combination, test the common passwords
    for y in algo_iterations:
        #algo in entry_list[0] iter in entry_list[1]
        entry_list = y.rsplit('$')

        if entry_list[0] == 'pbkdf2_sha256':
            #this should always be the case for our purposes
            #get iter and do algo

            #print('running common passwords for ' + entry_list[0] + ' iter ' + entry_list[1])
            counter = 0
            for z in salt_hash:
                #sh_list[0] has salt [1] has hash
                sh_list = z.rsplit('$')
                #print('running with salt ' + sh_list[0] + ' and hash ' + sh_list[1])

                for common in common_list:
                    enc = PBKDF2HMAC(
                        algorithm = hashes.SHA256(),
                        length = 32,
                        salt = sh_list[0].encode(),
                        iterations = int(entry_list[1])
                    )
                    zhash = enc.derive(common.encode('utf-8'))
                    if(zhash == base64.b64decode(sh_list[1])):
                        #print("CRACKED hash " + sh_list[1] + " with salt " + sh_list[0] + " is " + common)
                        print(users[counter] + ", " + common)
                        counter += 1
                        break
            counter += 1
    
        else:
            print('UH OH WE SHOULDNT BE HERE!')

else:
    alphabet = 'abcdefghijklmnopqrstuvwxyz'

    param = sys.argv[1]
    print(param)

    entry_list = param.rsplit('$')
    
    if entry_list[1] != '1':
        print('Cannot brute-force password in time')
    else:

        for letter in alphabet:
            attempt = letter
            enc = PBKDF2HMAC(
                algorithm = hashes.SHA256(),
                length = 32,
                salt = entry_list[2].encode(),
                iterations = int(entry_list[1])
            )
            zhash = enc.derive(attempt.encode('utf-8'))
            if(zhash == base64.b64decode(entry_list[3])):
                print("Password cracked: " + attempt)
                break

            for letter2 in alphabet:
                attempt2 = letter + '' + letter2
                enc2 = PBKDF2HMAC(
                    algorithm = hashes.SHA256(),
                    length = 32,
                    salt = entry_list[2].encode(),
                    iterations = int(entry_list[1])
                )
                zhash2 = enc2.derive(attempt2.encode('utf-8'))
                if(zhash2 == base64.b64decode(entry_list[3])):
                    print("Password cracked: " + attempt2)
                    break

                for letter3 in alphabet:
                    attempt3 = letter + '' + letter2 + '' + letter3
                    enc3 = PBKDF2HMAC(
                        algorithm = hashes.SHA256(),
                        length = 32,
                        salt = entry_list[2].encode(),
                        iterations = int(entry_list[1])
                    )
                    zhash3 = enc3.derive(attempt3.encode('utf-8'))
                    if(zhash3 == base64.b64decode(entry_list[3])):
                        print("Password cracked: " + attempt3)
                        break

                    for letter4 in alphabet:
                        attempt4 = letter + '' + letter2 + '' + letter3 + '' + letter4
                        enc4 = PBKDF2HMAC(
                            algorithm = hashes.SHA256(),
                            length = 32,
                            salt = entry_list[2].encode(),
                            iterations = int(entry_list[1])
                        )
                        zhash4 = enc4.derive(attempt4.encode('utf-8'))
                        if(zhash4 == base64.b64decode(entry_list[3])):
                            print("Password cracked: " + attempt4)
                            break
        
        #for each possible combination, encode the combo and compare to hash
