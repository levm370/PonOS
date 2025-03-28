#!/usr/bin/python3
import sys, time, os, struct, json
import datetime
from system import ponosctrl
#try:
#    import ponosgraphics as pg
#except:
#    print('failed to import graphics module.')
# Параметры системы
ip_addr = sys.argv[4]
user = 'ponos'
host = sys.argv[1]
memory = sys.argv[2]
processor = sys.argv[3]

class VirtualDisk:
    def __init__(self, disk_file="ponos.img"):
        self.disk_file = disk_file
        self.block_size = 1024  # 1KB блоки
        if not os.path.exists(disk_file):
            print("disk image not found!")
        
        # Читаем суперблок
        with open(disk_file, "rb") as f:
            header = f.read(32)
            self.magic, self.version, self.total_blocks = struct.unpack_from("III", header, 0)
            self.label = header[12:28].decode().strip('\x00')
        
        # Корневой каталог в блоке 1
        self.root_block = 1
    
    def _read_block(self, block_num):
        with open(self.disk_file, "rb") as f:
            f.seek(block_num * self.block_size)
            return f.read(self.block_size)
    
    def _write_block(self, block_num, data):
        with open(self.disk_file, "r+b") as f:
            f.seek(block_num * self.block_size)
            f.write(data[:self.block_size].ljust(self.block_size, b'\x00'))
    
    def _get_metadata(self):
        data = self._read_block(self.root_block)
        try:
            return json.loads(data.decode().rstrip('\x00'))
        except:
            return {}
    
    def _save_metadata(self, metadata):
        self._write_block(self.root_block, json.dumps(metadata).encode())
    
    def create_file(self, filename, content):
        metadata = self._get_metadata()
        
        if filename in metadata:
            print(f"file {filename} already exists")
        
        # Находим свободные блоки (упрощённо)
        free_block = None
        for block in range(100, self.total_blocks):
            data = self._read_block(block)
            if data[0] == 0:
                free_block = block
                break
        
        if not free_block:
            print("no free space on disk")
        
        # Сохраняем данные
        self._write_block(free_block, content.encode())
        
        # Обновляем метаданные
        metadata[filename] = {
            "block": free_block,
            "size": len(content),
            "created": time.time()
        }
        self._save_metadata(metadata)
    
    def read_file(self, filename):
        metadata = self._get_metadata()
        if filename not in metadata:
            print(f"file {filename} not found")
        
        data = self._read_block(metadata[filename]["block"])
        return data.decode().rstrip('\x00')
    
    def delete_file(self, filename):
        metadata = self._get_metadata()
        if filename not in metadata:
            print(f"file {filename} not found")
        
        # Помечаем блок как свободный (записываем 0)
        self._write_block(metadata[filename]["block"], b'\x00')
        
        # Удаляем из метаданных
        del metadata[filename]
        self._save_metadata(metadata)

class Filesystem:
    def __init__(self):
        print('mounting virtual filesystem...')
        self.disk = VirtualDisk()
    
    def create(self, file, data):
        try:
            self.disk.create_file(file, data)
        except Exception as e:
            print(f"error: {e}")
    
    def rename(self, old, new):
        try:
            data = self.disk.read_file(old)
            self.disk.delete_file(old)
            self.disk.create_file(new, data)
        except Exception as e:
            print(f"error: {e}")
    
    def delete(self, file):
        try:
            self.disk.delete_file(file)
        except Exception as e:
            print(f"error: {e}")
    
    def read(self, file):
        try:
            return self.disk.read_file(file)
        except Exception as e:
            print(f"error: {e}")

def ponosfetch():
    global memory
    global user
    global host
    global processor
    os.system(f'python3 ./system/ponosfetch {memory} {user} {host} "{processor}"')

def ls():
    disk = VirtualDisk()
    metadata = disk._get_metadata()
    print("files in ponosfs:")
    for filename in metadata:
        print(f"- {filename} ({metadata[filename]['size']} bytes)")

def ip():
    global ip_addr
    print(ip_addr)

# Инициализация
fs = Filesystem()
print('PonOS 4.54 (ponosfs bulka edition)')

# Главный цикл (без изменений)
while True:
    term = input('ponos bulka -> ')
    if term.startswith('touch'):
        file = term[6:]
        fs.create(file, '')
    elif term.startswith('write'):
        file = term[6:]
        data = ''
        print(f'Editing {file}. Enter "exit" to exit.')
        while True:
            writer = input('')
            if writer != 'exit':
                data += f'{writer}\n'
            else:
                break
        fs.create(file, data)
    elif term.startswith('rm'):
        file = term[3:]
        fs.delete(file)
    elif term.startswith('export'):
        data = term[7:]
        fd = fs.read(data)
        with open(data, 'w') as fw:
            fw.write(fd)
    elif term.startswith('rnf'):
        old = term[4:]
        new = input('new file name: ')
        fs.rename(old, new)
    elif term.startswith('wfile'):
        file = term[6:]
        data = input('~ ')
        fs.create(file, data)
    elif term.startswith('cat'):
        data = term[4:]
        fs.read(data)
    elif term.startswith('ls -vfs'):
        ls()
    elif term.startswith('ip'):
        ip()
    elif term.startswith('ponosfetch'):
        ponosfetch()
    elif term.startswith('echo'):
        data = term[5:]
        print(data)
    elif term == 'exit':
        print('shutting down')
        exit()
    elif term == 'clear':
        print('\x1b[H\x1b[2J\x1b[3J')
    elif term == 'ponosgraphics':
        ponosctrl.circle()
    #elif term == 'ponosgraphics init':
    #    root = pg.ponoswin()
    #elif term == 'ponosgraphics loop':
    #    try:
    #        root.mainloop()
    #    except:
    #        print('enter ponosgraphics-init')
    elif term.startswith('python3'):
        script = term[8:]
        try:
            exec(script)
        except Exception as e:
            print('error:', e)
    elif term == 'ls':
        print('system files:')
        for item in os.listdir('./system'):
            print(item)
    else:
        print(f"command '{term}' not found.")
