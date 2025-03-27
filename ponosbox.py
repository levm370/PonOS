#!/usr/bin/python3
import time, os, struct

def create_disk_image():
    if not os.path.exists("ponos.img"):
        print("creating virtual disk...")
        with open("ponos.img", "wb") as f:
            f.write(struct.pack("III16s", 0x706F6E6F, 1, 1024, b"PonOS_Disk"))
            f.write(b"\x00" * (1024 * 1024 - 32))
        print("created ponos.img")

print('Welcome to PonosBox')
ip = '127.0.0.1'
mem = '4096'
proc = 'Ponos Core 16X2'

print('\nhw:')
print(f'  CPU: {proc}')
print(f'  RAM: {mem} MB')
print(f'  IP: {ip}')

create_disk_image()

print('\nbooting up...')
time.sleep(1)
os.system('clear')
os.system(f"python3 ponos.py ponosbox {mem} '{proc}' {ip}")
print('exiting ponosbox...')
