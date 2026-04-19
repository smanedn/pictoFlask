# 💬 PictoFlask - Real-time Chat Application

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-green?style=for-the-badge&logo=flask)
![Socket.IO](https://img.shields.io/badge/Socket.IO-4.7-black?style=for-the-badge&logo=socket.io)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**A real-time chat application inspired by Nintendo DS's PictoChat**

🎉 **Version 1.0 - Final Release** 🎉
Built with Flask, Socket.IO, and authentic Nintendo DS styling

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [Usage](#-usage) • [Contributing](#-contributing)

</div>

---

## ✨ Features

### 💬 **Real-time Messaging**
- Instant message delivery using WebSockets
- Message bubbles with authentic DS styling
- Last 100 messages loaded on connect
- Smooth scrolling and animations
- Message deletion (own messages + admin)
- Emoji picker with 24 popular emojis

### 👤 **User System**
- Secure registration and login
- Profile picture uploads
- 16 PictoChat-inspired color themes per user
- Public profile pages
- Single-session login (auto-logout on other devices)

### ✉️ **Private Messaging**
- Direct messaging between users
- Conversation-based inbox
- Unread message badges
- Real-time notifications
- Left sidebar menu for quick access
- Blocked users cannot message you

### 🎮 **Nintendo DS Aesthetic**
- Authentic PictoChat visual design
- Press Start 2P pixel font
- DS-style buttons and screens
- Light/Dark theme toggle (🌙)
- Retro sound effects
- **🎵 Background music support** (DS/3DS themed)

### 🔔 **Real-time Features**
- Online users panel with avatars
- Live typing indicators
- Connection status display
- Unread message counter in tab title
- Sound notifications (send/receive/join)

### 🛡️ **Security & Performance**
- Rate limiting (anti-spam)
- Password hashing (Werkzeug)
- Session management
- CSRF protection
- Efficient WebSocket handling
- User blocking system

### 👑 **Admin Panel**
- Admin dashboard with statistics
- User management (view, promote/demote admin, delete)
- Message management (view, search, delete)
- Admin-only access control

### 📱 **Responsive Design**
- Desktop optimized (1920x1080+)
- Tablet support (768px+)
- Mobile friendly (320px+)
- Landscape orientation support
- Touch-optimized controls

## 📸 Screenshots

*Coming soon - Will include chat interface, profile customization, and theme comparison*

## 🎨 Demo

<!-- Add demo GIF or video here -->
*Live demo coming soon*

## 🛠️ Tech Stack

### Backend
- **Framework**: Flask 3.0
- **Real-time**: Flask-SocketIO with Eventlet
- **Authentication**: Flask-Login
- **Database**: Flask-SQLAlchemy (SQLite default, PostgreSQL compatible)
- **Security**: Werkzeug password hashing

### Frontend
- **Styling**: Custom CSS with DS theme (no frameworks!)
- **JavaScript**: Vanilla JS with Socket.IO client
- **Icons**: Font Awesome 6.5
- **Font**: Press Start 2P (Google Fonts)

### Server
- **WSGI**: Eventlet for async WebSocket support
- **Development**: Flask built-in server
- **Production**: Eventlet WSGI server

## 📦 Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Git

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/smanedn/PictoFlask.git
   cd PictoFlask
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/macOS
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Windows
   copy .env.example .env
   
   # Linux/macOS
   cp .env.example .env
   
   # Edit .env with your settings (optional)
   ```

5. **Run the application**
   ```bash
   python run.py
   ```

6. **Open your browser**
   ```
   http://localhost:5000
   ```

7. **[Optional] Add background music** 🎵
   - See [Music Setup](#-music-setup) below for DS/3DS themed music

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root (use `.env.example` as template):

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `SECRET_KEY` | Flask secret key for sessions | Auto-generated | No |
| `DATABASE_URL` | Database connection string | `sqlite:///chat.db` | No |

**Example `.env` file:**
```env
SECRET_KEY=your-super-secret-key-here-change-this
DATABASE_URL=sqlite:///chat.db
```

### 🎵 Music Setup

The app supports DS/3DS themed background music!

**Quick Setup:**
1. Find or create DS-themed music
2. Name it `ds_theme.mp3`
3. Place in `static/music/` folder
4. Click the 🔊 button in the app to play!

**Free Music Resources:**
- [BeepBox.co](https://beepbox.co) - Create custom chiptune (2 minutes!)
- [FreePD.com](https://freepd.com/chiptune.php) - Public domain 8-bit music
- [OpenGameArt.org](https://opengameart.org) - Community game music

**Music Features:**
- Toggle with 🔊 button (top-right corner)
- Remembers your preference
- 30% volume (configurable in `base.html`)
- Seamless looping
- Pulse animation when playing

## 📁 Project Structure

```
pictoFlask/
├── app/
│   ├── __init__.py          # Application factory
│   ├── config.py            # Configuration settings
│   ├── extensions.py        # Flask extensions (DB, Login, SocketIO)
│   ├── models.py            # Database models (User, Message, PrivateMessage, BlockedUser)
│   ├── sockets.py           # WebSocket event handlers
│   ├── utils.py             # Utility functions
│   └── routes/
│       ├── __init__.py
│       ├── admin.py         # Admin panel routes
│       ├── auth.py          # Authentication routes
│       ├── main.py          # Main application routes
│       └── messages.py      # Private messaging routes
├── static/
│   ├── music/               # Background music files
│   │   ├── README.md        # Music setup guide
│   │   └── ds_theme.mp3     # (Add your own music file)
│   └── uploads/
│       └── profiles/        # User profile pictures
│           └── default.jpg
├── templates/
│   ├── admin/               # Admin panel templates
│   │   ├── dashboard.html   # Admin dashboard
│   │   ├── messages.html    # Message management
│   │   └── users.html       # User management
│   ├── messages/            # Private messaging templates
│   │   ├── inbox.html       # Conversations list
│   │   └── conversation.html # Chat with user
│   ├── base.html            # Base template with DS theme + sidebar
│   ├── index.html           # Chat room interface
│   ├── login.html           # Login page
│   ├── register.html        # Registration page
│   ├── profile.html         # User profile editor
│   └── public_profile.html  # Public user profiles
├── instance/                # Generated: Database
├── venv/                    # Virtual environment (not in git)
├── .env                     # Environment variables (not in git)
├── .env.example             # Environment template
├── .gitignore
├── CHANGELOG.md             # Version history
├── CONTRIBUTING.md          # Contribution guidelines
├── LICENSE
├── README.md
├── requirements.txt         # Python dependencies
└── run.py                   # Application entry point
```

## 🚀 Usage

### First Time Setup

1. **Register an account** at `/register`
2. **Choose a profile color** (16 PictoChat colors available)
3. **Upload a profile picture** (optional)
4. **Start chatting** at `/` (home page)

### Features Guide

| Feature | How to Use |
|---------|------------|
| **Send Message** | Type in the input box and press Enter or click Send |
| **Add Emoji** | Click 😀 button next to input to open emoji picker |
| **Delete Message** | Hover over your message, click X button |
| **Theme Toggle** | Click 🌙 button (top-right) for dark/light mode |
| **Music Toggle** | Click 🔊 button (top-right) for background music |
| **Open Menu** | Click ☰ button (top-left) for sidebar menu |
| **Private Message** | Click user profile → "INVIA MESSAGGIO" or use sidebar |
| **View Profile** | Click your username or "PROFILO" in header |
| **Edit Profile** | Go to profile page, update info, click Save |
| **See Online Users** | Check the panel above chat (auto-updates) |
| **View User Profile** | Click any username in the online users panel |

### Keyboard Shortcuts

- **Enter** - Send message
- **Ctrl + /** - Focus message input (coming soon)

## 🔌 API Endpoints

### HTTP Routes

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/register` | User registration |
| GET/POST | `/login` | User login |
| GET | `/logout` | User logout |
| GET | `/` | Chat room (requires auth) |
| GET/POST | `/profile` | Edit profile |
| GET | `/user/<username>` | Public profile |
| GET | `/admin` | Admin dashboard (admin only) |
| GET | `/admin/users` | User management (admin only) |
| POST | `/admin/users/<id>/toggle-admin` | Toggle admin status |
| POST | `/admin/users/<id>/delete` | Delete user |
| GET | `/admin/messages` | Message management (admin only) |
| POST | `/admin/messages/<id>/delete` | Delete message |
| GET | `/messages` | Private messages inbox |
| GET | `/messages/conversation/<user_id>` | Conversation with user |
| POST | `/messages/send/<user_id>` | Send private message |
| GET | `/messages/unread_count` | Get unread count (API) |
| POST | `/block/<user_id>` | Block a user |
| POST | `/unblock/<user_id>` | Unblock a user |

### WebSocket Events

| Event | Direction | Description |
|-------|-----------|-------------|
| `connect` | Client → Server | Join chat room |
| `disconnect` | Client → Server | Leave chat room |
| `message` | Bidirectional | Send/receive messages |
| `typing` | Bidirectional | Typing indicator |
| `online_users` | Server → Client | Online users list |
| `status` | Server → Client | System messages |
| `kicked` | Server → Client | Session invalidated |
| `private_message` | Client → Server | Send private message |
| `pm_sent` | Server → Client | Private message sent confirmation |
| `pm_received` | Server → Client | New private message received |
| `delete_message` | Client → Server | Delete a message |
| `message_deleted` | Server → Client | Message was deleted |

## 🎯 Roadmap

- [x] Private messaging
- [x] Message deletion
- [x] Drawing canvas (like real PictoChat!)
- [ ] Multiple chat rooms
- [ ] Image/file sharing
- [x] Emoji picker
- [x] Message search
- [x] User blocking
- [x] Admin panel
- [ ] Mobile app (React Native)

## 🤝 Contributing

Contributions are welcome! Here's how:

1. **Fork** the repository
2. **Create** a feature branch
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit** your changes
   ```bash
   git commit -m 'Add some amazing feature'
   ```
4. **Push** to the branch
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open** a Pull Request

### Development Guidelines

- Follow existing code style
- Keep the DS aesthetic consistent
- Test thoroughly before submitting
- Update documentation as needed
- Add comments for complex logic

### Reporting Bugs

Found a bug? Please open an issue with:
- Clear description
- Steps to reproduce
- Expected vs actual behavior
- Screenshots (if applicable)
- Your environment (OS, browser, Python version)

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Nintendo** - For the original PictoChat inspiration
- **Flask Team** - For the amazing web framework
- **Socket.IO** - For real-time communication
- **Press Start 2P** - For the authentic pixel font
- **Open Source Community** - For tools and libraries

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/smanedn/PictoFlask/issues)
- **Discussions**: [GitHub Discussions](https://github.com/smanedn/PictoFlask/discussions)
- **Documentation**: Check the `static/music/` folder for detailed guides

## ⚠️ Legal Notice

This project is a fan-made tribute to Nintendo DS's PictoChat. It is not affiliated with, endorsed by, or connected to Nintendo in any way. All trademarks belong to their respective owners.

---

<div align="center">

**Made with ❤️ and nostalgia for the Nintendo DS era**

⭐ Star this repo if you enjoyed chatting on your DS!

[⬆ Back to Top](#-PictoFlask---real-time-chat-application)

</div>
