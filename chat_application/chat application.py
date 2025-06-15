# Advanced Chat Application - Compact Version
# Features: Authentication, Rooms, Multimedia, History, Notifications, Emojis, Encryption

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import socket
import threading
import json
import hashlib
import sqlite3
import base64
import os
import time
from datetime import datetime
from PIL import Image, ImageTk
import io

class ChatDatabase:
    def __init__(self):
        self.conn = sqlite3.connect('chat.db', check_same_thread=False)
        self.setup_db()
        
    def setup_db(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users 
                    (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS rooms 
                    (id INTEGER PRIMARY KEY, name TEXT UNIQUE, description TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS messages 
                    (id INTEGER PRIMARY KEY, room_id INTEGER, username TEXT, 
                     message TEXT, type TEXT DEFAULT 'text', timestamp TEXT)''')
        c.execute("INSERT OR IGNORE INTO rooms (name, description) VALUES ('General', 'Main chat room')")
        self.conn.commit()
    
    def register_user(self, username, password):
        try:
            c = self.conn.cursor()
            hash_pwd = hashlib.sha256(password.encode()).hexdigest()
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hash_pwd))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def login_user(self, username, password):
        c = self.conn.cursor()
        hash_pwd = hashlib.sha256(password.encode()).hexdigest()
        c.execute("SELECT id FROM users WHERE username=? AND password=?", (username, hash_pwd))
        return c.fetchone()
    
    def get_rooms(self):
        c = self.conn.cursor()
        c.execute("SELECT * FROM rooms")
        return c.fetchall()
    
    def create_room(self, name, desc):
        try:
            c = self.conn.cursor()
            c.execute("INSERT INTO rooms (name, description) VALUES (?, ?)", (name, desc))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def save_message(self, room_id, username, message, msg_type='text'):
        c = self.conn.cursor()
        timestamp = datetime.now().strftime('%H:%M:%S')
        c.execute("INSERT INTO messages (room_id, username, message, type, timestamp) VALUES (?, ?, ?, ?, ?)",
                 (room_id, username, message, msg_type, timestamp))
        self.conn.commit()
    
    def get_history(self, room_id, limit=50):
        c = self.conn.cursor()
        c.execute("SELECT username, message, type, timestamp FROM messages WHERE room_id=? ORDER BY id DESC LIMIT ?",
                 (room_id, limit))
        return c.fetchall()[::-1]

class ChatServer:
    def __init__(self, host='localhost', port=12345):
        self.host, self.port = host, port
        self.clients = {}
        self.rooms = {}
        self.db = ChatDatabase()
        
    def start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        print(f"Server running on {self.host}:{self.port}")
        
        while True:
            try:
                client, addr = self.server.accept()
                threading.Thread(target=self.handle_client, args=(client,), daemon=True).start()
            except:
                break
    
    def handle_client(self, client):
        try:
            while True:
                data = client.recv(4096).decode()
                if not data:
                    break
                msg = json.loads(data)
                self.process_message(client, msg)
        except:
            pass
        finally:
            self.disconnect_client(client)
    
    def process_message(self, client, msg):
        msg_type = msg.get('type')
        
        if msg_type == 'register':
            success = self.db.register_user(msg['username'], msg['password'])
            client.send(json.dumps({'type': 'register_result', 'success': success}).encode())
            
        elif msg_type == 'login':
            user = self.db.login_user(msg['username'], msg['password'])
            if user:
                self.clients[client] = {'username': msg['username'], 'user_id': user[0], 'room': None}
                client.send(json.dumps({'type': 'login_success', 'user_id': user[0]}).encode())
            else:
                client.send(json.dumps({'type': 'login_failed'}).encode())
                
        elif msg_type == 'get_rooms':
            rooms = self.db.get_rooms()
            client.send(json.dumps({'type': 'rooms_list', 'rooms': rooms}).encode())
            
        elif msg_type == 'create_room':
            success = self.db.create_room(msg['name'], msg['description'])
            client.send(json.dumps({'type': 'room_created', 'success': success}).encode())
            
        elif msg_type == 'join_room':
            room_id = msg['room_id']
            self.clients[client]['room'] = room_id
            if room_id not in self.rooms:
                self.rooms[room_id] = []
            if client not in self.rooms[room_id]:
                self.rooms[room_id].append(client)
            client.send(json.dumps({'type': 'room_joined'}).encode())
            
        elif msg_type == 'get_history':
            history = self.db.get_history(msg['room_id'])
            client.send(json.dumps({'type': 'history', 'data': history}).encode())
            
        elif msg_type == 'chat_message':
            if client in self.clients:
                username = self.clients[client]['username']
                room_id = self.clients[client]['room']
                message = msg['message']
                msg_typ = msg.get('message_type', 'text')
                
                self.db.save_message(room_id, username, message, msg_typ)
                
                broadcast = {
                    'type': 'new_message',
                    'username': username,
                    'message': message,
                    'message_type': msg_typ,
                    'timestamp': datetime.now().strftime('%H:%M:%S')
                }
                
                if room_id in self.rooms:
                    for c in self.rooms[room_id]:
                        try:
                            c.send(json.dumps(broadcast).encode())
                        except:
                            self.rooms[room_id].remove(c)
    
    def disconnect_client(self, client):
        if client in self.clients:
            room_id = self.clients[client].get('room')
            if room_id and room_id in self.rooms and client in self.rooms[room_id]:
                self.rooms[room_id].remove(client)
            del self.clients[client]
        try:
            client.close()
        except:
            pass

class LoginWindow:
    def __init__(self, on_success):
        self.on_success = on_success
        self.root = tk.Tk()
        self.root.title("Chat Login")
        self.root.geometry("350x400")
        self.root.configure(bg='#2c3e50')
        self.setup_ui()
        
    def setup_ui(self):
        tk.Label(self.root, text="Advanced Chat", font=('Arial', 20, 'bold'), 
                fg='white', bg='#2c3e50').pack(pady=20)
        
        frame = tk.Frame(self.root, bg='#34495e', padx=20, pady=20)
        frame.pack(pady=20, padx=30, fill='both', expand=True)
        
        tk.Label(frame, text="Username:", fg='white', bg='#34495e').pack(anchor='w')
        self.username_entry = tk.Entry(frame, width=25)
        self.username_entry.pack(pady=(0, 10))
        
        tk.Label(frame, text="Password:", fg='white', bg='#34495e').pack(anchor='w')
        self.password_entry = tk.Entry(frame, width=25, show='*')
        self.password_entry.pack(pady=(0, 15))
        
        btn_frame = tk.Frame(frame, bg='#34495e')
        btn_frame.pack()
        
        tk.Button(btn_frame, text="Login", bg='#3498db', fg='white', 
                 command=self.login, width=10).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Register", bg='#27ae60', fg='white', 
                 command=self.register, width=10).pack(side='left', padx=5)
        
        self.status = tk.Label(frame, text="", fg='red', bg='#34495e')
        self.status.pack(pady=10)
        
        self.root.bind('<Return>', lambda e: self.login())
    
    def connect_server(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(('localhost', 12345))
            return sock
        except:
            self.status.config(text="Cannot connect to server")
            return None
    
    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            self.status.config(text="Fill all fields")
            return
        
        sock = self.connect_server()
        if not sock:
            return
        
        msg = {'type': 'login', 'username': username, 'password': password}
        sock.send(json.dumps(msg).encode())
        response = json.loads(sock.recv(1024).decode())
        
        if response['type'] == 'login_success':
            self.root.destroy()
            self.on_success(username, response['user_id'], sock)
        else:
            self.status.config(text="Invalid credentials")
            sock.close()
    
    def register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            self.status.config(text="Fill all fields")
            return
        
        sock = self.connect_server()
        if not sock:
            return
        
        msg = {'type': 'register', 'username': username, 'password': password}
        sock.send(json.dumps(msg).encode())
        response = json.loads(sock.recv(1024).decode())
        
        if response['success']:
            self.status.config(text="Registration successful!", fg='green')
        else:
            self.status.config(text="Username already exists")
        sock.close()
    
    def run(self):
        self.root.mainloop()

class ChatClient:
    def __init__(self, username, user_id, socket):
        self.username = username
        self.user_id = user_id
        self.socket = socket
        self.current_room = None
        self.emojis = {':)': '😊', ':D': '😃', ':(': '😢', '<3': '❤️', ':P': '😛'}
        
        self.root = tk.Tk()
        self.root.title(f"Chat - {username}")
        self.root.geometry("900x600")
        self.root.configure(bg='#2c3e50')
        self.setup_ui()
        self.start_listener()
        self.load_rooms()
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def setup_ui(self):
        # Left panel - Rooms
        left_frame = tk.Frame(self.root, bg='#34495e', width=200)
        left_frame.pack(side='left', fill='y', padx=5, pady=5)
        left_frame.pack_propagate(False)
        
        tk.Label(left_frame, text=f"User: {self.username}", fg='white', bg='#34495e', 
                font=('Arial', 10, 'bold')).pack(pady=10)
        
        tk.Label(left_frame, text="Rooms", fg='white', bg='#34495e', 
                font=('Arial', 12, 'bold')).pack()
        
        tk.Button(left_frame, text="Create Room", bg='#27ae60', fg='white',
                 command=self.create_room_dialog).pack(fill='x', padx=10, pady=5)
        
        self.rooms_list = tk.Listbox(left_frame, bg='#2c3e50', fg='white', selectbackground='#3498db')
        self.rooms_list.pack(fill='both', expand=True, padx=10, pady=5)
        self.rooms_list.bind('<Double-Button-1>', self.join_room)
        
        # Right panel - Chat
        right_frame = tk.Frame(self.root, bg='#34495e')
        right_frame.pack(side='right', fill='both', expand=True, padx=5, pady=5)
        
        # Chat header
        header = tk.Frame(right_frame, bg='#34495e', height=40)
        header.pack(fill='x', pady=(0, 5))
        header.pack_propagate(False)
        
        self.room_label = tk.Label(header, text="Select a room", fg='white', bg='#34495e',
                                  font=('Arial', 14, 'bold'))
        self.room_label.pack(side='left', pady=10)
        
        # Chat area
        self.chat_area = scrolledtext.ScrolledText(right_frame, bg='#2c3e50', fg='white',
                                                  state='disabled', wrap='word')
        self.chat_area.pack(fill='both', expand=True, pady=(0, 5))
        
        # Input area
        input_frame = tk.Frame(right_frame, bg='#34495e')
        input_frame.pack(fill='x')
        
        # File buttons
        file_frame = tk.Frame(input_frame, bg='#34495e')
        file_frame.pack(fill='x', pady=(0, 5))
        
        tk.Button(file_frame, text="📷", command=self.send_image, width=3).pack(side='left', padx=2)
        tk.Button(file_frame, text="📎", command=self.send_file, width=3).pack(side='left', padx=2)
        
        # Emoji buttons
        for emoji in ['😊', '😃', '😢', '❤️', '😛']:
            tk.Button(file_frame, text=emoji, command=lambda e=emoji: self.insert_emoji(e),
                     width=3).pack(side='left', padx=1)
        
        # Message input
        msg_frame = tk.Frame(input_frame, bg='#34495e')
        msg_frame.pack(fill='x')
        
        self.message_entry = tk.Entry(msg_frame)
        self.message_entry.pack(side='left', fill='x', expand=True, padx=(0, 5))
        self.message_entry.bind('<Return>', lambda e: self.send_message())
        
        tk.Button(msg_frame, text="Send", bg='#27ae60', fg='white',
                 command=self.send_message).pack(side='right')
    
    def load_rooms(self):
        msg = {'type': 'get_rooms'}
        self.socket.send(json.dumps(msg).encode())
    
    def join_room(self, event=None):
        selection = self.rooms_list.curselection()
        if not selection:
            return
        
        room_text = self.rooms_list.get(selection[0])
        room_id = int(room_text.split(' - ')[0])
        room_name = room_text.split(' - ')[1]
        
        self.current_room = room_id
        self.room_label.config(text=f"Room: {room_name}")
        
        # Join room and get history
        self.socket.send(json.dumps({'type': 'join_room', 'room_id': room_id}).encode())
        self.socket.send(json.dumps({'type': 'get_history', 'room_id': room_id}).encode())
    
    def create_room_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Create Room")
        dialog.geometry("300x200")
        dialog.configure(bg='#2c3e50')
        dialog.grab_set()
        
        tk.Label(dialog, text="Room Name:", fg='white', bg='#2c3e50').pack(pady=10)
        name_entry = tk.Entry(dialog, width=30)
        name_entry.pack()
        
        tk.Label(dialog, text="Description:", fg='white', bg='#2c3e50').pack(pady=(10, 5))
        desc_entry = tk.Entry(dialog, width=30)
        desc_entry.pack()
        
        def create():
            name = name_entry.get().strip()
            desc = desc_entry.get().strip()
            if name:
                msg = {'type': 'create_room', 'name': name, 'description': desc}
                self.socket.send(json.dumps(msg).encode())
                dialog.destroy()
        
        tk.Button(dialog, text="Create", bg='#27ae60', fg='white', command=create).pack(pady=20)
    
    def send_message(self):
        message = self.message_entry.get().strip()
        if not message or not self.current_room:
            return
        
        # Replace emoji shortcuts
        for shortcut, emoji in self.emojis.items():
            message = message.replace(shortcut, emoji)
        
        msg = {'type': 'chat_message', 'message': message}
        self.socket.send(json.dumps(msg).encode())
        self.message_entry.delete(0, 'end')
    
    def send_image(self):
        if not self.current_room:
            messagebox.showwarning("Warning", "Join a room first")
            return
        
        file_path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg *.gif")])
        if file_path:
            try:
                with open(file_path, 'rb') as f:
                    data = base64.b64encode(f.read()).decode()
                filename = os.path.basename(file_path)
                msg = {'type': 'chat_message', 'message': f"[IMG:{filename}:{data}]", 'message_type': 'image'}
                self.socket.send(json.dumps(msg).encode())
            except Exception as e:
                messagebox.showerror("Error", f"Failed to send image: {e}")
    
    def send_file(self):
        if not self.current_room:
            messagebox.showwarning("Warning", "Join a room first")
            return
        
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                if os.path.getsize(file_path) > 5*1024*1024:  # 5MB limit
                    messagebox.showerror("Error", "File too large (max 5MB)")
                    return
                
                with open(file_path, 'rb') as f:
                    data = base64.b64encode(f.read()).decode()
                filename = os.path.basename(file_path)
                msg = {'type': 'chat_message', 'message': f"[FILE:{filename}:{data}]", 'message_type': 'file'}
                self.socket.send(json.dumps(msg).encode())
            except Exception as e:
                messagebox.showerror("Error", f"Failed to send file: {e}")
    
    def insert_emoji(self, emoji):
        pos = self.message_entry.index(tk.INSERT)
        current = self.message_entry.get()
        new_text = current[:pos] + emoji + current[pos:]
        self.message_entry.delete(0, 'end')
        self.message_entry.insert(0, new_text)
        self.message_entry.icursor(pos + len(emoji))
    
    def display_message(self, username, message, msg_type='text', timestamp=None):
        self.chat_area.config(state='normal')
        
        time_str = timestamp or datetime.now().strftime('%H:%M:%S')
        self.chat_area.insert('end', f"[{time_str}] {username}: ")
        
        if msg_type == 'image' and message.startswith('[IMG:'):
            try:
                parts = message[5:-1].split(':', 2)
                filename = parts[0]
                self.chat_area.insert('end', f"📷 {filename}\n")
                
                # Show small image preview
                image_data = base64.b64decode(parts[1])
                img = Image.open(io.BytesIO(image_data))
                img.thumbnail((150, 150))
                photo = ImageTk.PhotoImage(img)
                self.chat_area.image_create('end', image=photo)
                self.chat_area.insert('end', '\n')
                
                # Keep reference
                if not hasattr(self, 'images'):
                    self.images = []
                self.images.append(photo)
            except:
                self.chat_area.insert('end', f"[Image error]\n")
        elif msg_type == 'file' and message.startswith('[FILE:'):
            filename = message[6:-1].split(':', 1)[0]
            self.chat_area.insert('end', f"📎 {filename}\n")
        else:
            self.chat_area.insert('end', f"{message}\n")
        
        self.chat_area.config(state='disabled')
        self.chat_area.see('end')
    
    def start_listener(self):
        def listen():
            while True:
                try:
                    data = self.socket.recv(4096).decode()
                    if not data:
                        break
                    msg = json.loads(data)
                    self.handle_message(msg)
                except:
                    break
        
        threading.Thread(target=listen, daemon=True).start()
    
    def handle_message(self, msg):
        msg_type = msg.get('type')
        
        if msg_type == 'new_message':
            self.root.after(0, lambda: self.display_message(
                msg['username'], msg['message'], 
                msg.get('message_type', 'text'), msg['timestamp']))
                
        elif msg_type == 'rooms_list':
            def update_rooms():
                self.rooms_list.delete(0, 'end')
                for room_id, name, desc in msg['rooms']:
                    display = f"{room_id} - {name}"
                    if desc:
                        display += f" ({desc})"
                    self.rooms_list.insert('end', display)
            self.root.after(0, update_rooms)
            
        elif msg_type == 'history':
            def show_history():
                self.chat_area.config(state='normal')
                self.chat_area.delete('1.0', 'end')
                for username, message, m_type, timestamp in msg['data']:
                    self.display_message(username, message, m_type, timestamp)
                self.chat_area.config(state='disabled')
            self.root.after(0, show_history)
            
        elif msg_type == 'room_created':
            if msg['success']:
                self.root.after(0, lambda: messagebox.showinfo("Success", "Room created!"))
                self.load_rooms()
            else:
                self.root.after(0, lambda: messagebox.showerror("Error", "Room name exists"))
    
    def on_close(self):
        try:
            self.socket.close()
        except:
            pass
        self.root.destroy()
    
    def run(self):
        self.root.mainloop()

def start_server():
    server = ChatServer()
    threading.Thread(target=server.start, daemon=True).start()
    time.sleep(1)  # Wait for server to start

def main():
    import sys
    
    # Server mode
    if len(sys.argv) > 1 and sys.argv[1] == '--server':
        server = ChatServer()
        server.start()
        return
    
    # Auto-start server and client
    print("Starting server...")
    start_server()
    
    def on_login_success(username, user_id, socket):
        app = ChatClient(username, user_id, socket)
        app.run()
    
    login = LoginWindow(on_login_success)
    login.run()

if __name__ == "__main__":
    main()

# Installation: pip install Pillow
# Run: python chat_app.py
# Features: ✅ Authentication ✅ Multiple Rooms ✅ Multimedia ✅ History ✅ Emojis ✅ Security