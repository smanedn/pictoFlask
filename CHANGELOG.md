# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-19

### Added
- 🎵 **Background music support** with DS/3DS theme
  - Music toggle button with pulse animation
  - Volume control (30% default)
  - localStorage preference saving
  - Comprehensive music setup guides in `static/music/`
  - Free music source recommendations
- 💬 Real-time chat functionality with Socket.IO
- 👤 User authentication system (registration, login, logout)
- 🖼️ Profile customization (avatar upload, 16 color themes)
- 🎨 Authentic Nintendo DS PictoChat visual design
- 🌙 Light/Dark theme toggle
- 📱 Fully responsive design (mobile, tablet, desktop)
- 🔔 Sound effects (send, receive, join)
- 👥 Online users panel with live updates
- ⌨️ Typing indicators
- 📊 Connection status display
- 🔢 Unread message counter
- 📝 Message history (last 100 messages)
- 🛡️ Rate limiting (anti-spam protection)
- 🔐 Single-session login enforcement
- 🔗 Public user profile pages

### Technical Features
- Flask 3.0 application with application factory pattern
- Flask-SocketIO for WebSocket communication
- Flask-Login for session management
- Flask-SQLAlchemy for database ORM
- SQLite database (PostgreSQL compatible)
- Eventlet WSGI server for production
- Custom CSS with authentic DS styling (no frameworks)
- Vanilla JavaScript with Socket.IO client
- Press Start 2P pixel font from Google Fonts
- Font Awesome 6.5 icons

### Documentation
- Comprehensive README.md
- Music setup guide
- .env.example for configuration
- MIT License
- Project structure documentation
- API endpoint documentation

## [1.1.0] - 2026-01-19

### Added
- 👑 **Admin Panel** for moderation and management
  - Admin dashboard with statistics (user count, message count, admin count)
  - User management page with search, pagination
  - Promote/demote users to admin role
  - Delete users (and their messages)
  - Message management with search and deletion
  - Admin-only route protection with `admin_required` decorator
  - Admin link in navigation (visible only to admins)
- `is_admin` field added to User model

### Database Migration Required
If upgrading from v1.0.0, run:
```sql
ALTER TABLE user ADD COLUMN is_admin BOOLEAN DEFAULT 0;
```

## [Unreleased]

### Planned
- Private messaging between users
- Message editing and deletion
- Drawing canvas (like real PictoChat!)
- Multiple chat rooms
- Image/file sharing in chat
- Emoji picker
- Message search functionality
- User blocking feature
- Mobile app (React Native)

---

## Version History

### How to Read This Changelog

- **Added** - New features
- **Changed** - Changes to existing functionality
- **Deprecated** - Soon-to-be removed features
- **Removed** - Removed features
- **Fixed** - Bug fixes
- **Security** - Security improvements

### Version Numbering

This project uses [Semantic Versioning](https://semver.org/):
- **MAJOR** version for incompatible API changes
- **MINOR** version for backwards-compatible functionality additions
- **PATCH** version for backwards-compatible bug fixes

---

[1.1.0]: https://github.com/smanedn/PictoFlask/releases/tag/v1.1.0
[1.0.0]: https://github.com/smanedn/PictoFlask/releases/tag/v1.0.0
