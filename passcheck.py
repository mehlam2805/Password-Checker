import requests
import hashlib

def request_api(query):
    url = f'https://api.pwnedpasswords.com/range/'  + query
    res = requests.get(url)
    if res.status_code!=200:
        raise RuntimeError (f'error {res.status_code}')
    return res

def check_pass_leaks(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h,count in hashes: 
        if h == hash_to_check:
            return count
    return 0

def pwned_hashing(password):
    sha1pass = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5, tail = sha1pass[:5],sha1pass[5:]
    response = request_api(first5)
    return check_pass_leaks(response, tail)

def main(args):
    count = pwned_hashing(args)
    if count:
        print(f'{args} has been found {count} times. UNSAFE')
    else:
        print('{args} is SAFE')

main('123')
