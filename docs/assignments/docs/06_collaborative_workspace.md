---
theme: gaia
_class: lead
paginate: true
backgroundColor: #fff
backgroundImage: url('https://marp.app/assets/hero-background.svg')
---

![bg left:40% 80%](https://oppkey.com/static/logo.jpg)

# **Collaborative Workspace Assignment**
## Real-Time Team Collaboration

**Build a collaborative workspace for FastOpp**

---

# Assignment Overview

## What You'll Build

A collaborative workspace application that enables real-time team collaboration on FastOpp conversations, featuring:
- **Real-time collaboration** - Live updates when team members make changes
- **User presence** - See who's online and what they're working on
- **Shared workspaces** - Team-based conversation organization
- **Comment system** - Discuss conversations with team members
- **Permission management** - Control who can access what

---

# Problem Statement

## Team Collaboration Challenges

The current FastOpp system, while powerful, lacks team collaboration features:
- **No real-time updates** - Changes aren't reflected immediately
- **No user presence** - Can't see who's online or working on what
- **No shared workspaces** - Conversations are isolated per user
- **No commenting system** - Can't discuss conversations with team
- **No permission control** - All users have the same access level

---

# Your Solution

## Collaborative Workspace

Create a collaborative workspace that addresses these limitations:

1. **Real-time Updates** - WebSocket-based live collaboration
2. **User Presence** - Show online status and current activity
3. **Shared Workspaces** - Team-based conversation organization
4. **Comment System** - Threaded discussions on conversations
5. **Permission Management** - Role-based access control

---

# Technical Requirements

## Tech Stack

- **Frontend Framework** - React, Vue, or Angular
- **Real-time Communication** - Socket.io or WebSocket
- **State Management** - Redux, Pinia, or NgRx
- **Authentication** - JWT with role-based permissions
- **Database** - PostgreSQL with real-time subscriptions
- **Backend** - FastAPI with WebSocket support

---

# Project Structure

## Recommended Architecture

```
src/
├── components/
│   ├── collaboration/
│   │   ├── UserPresence.tsx
│   │   ├── CommentThread.tsx
│   │   ├── SharedWorkspace.tsx
│   │   └── PermissionManager.tsx
│   ├── realtime/
│   │   ├── RealtimeProvider.tsx
│   │   ├── PresenceIndicator.tsx
│   │   └── ActivityFeed.tsx
│   └── shared/
├── hooks/
│   ├── useWebSocket.ts
│   ├── usePresence.ts
│   ├── useComments.ts
│   └── usePermissions.ts
├── services/
│   ├── websocket.ts
│   ├── collaboration.ts
│   └── permissions.ts
└── stores/
    ├── collaboration.ts
    ├── presence.ts
    └── comments.ts
```

---

# Core Components

## 1. User Presence Component

```tsx
// components/collaboration/UserPresence.tsx
import React from 'react'
import { usePresence } from '@/hooks/usePresence'

interface UserPresenceProps {
  conversationId: string
}

const UserPresence: React.FC<UserPresenceProps> = ({ conversationId }) => {
  const { onlineUsers, currentUser } = usePresence(conversationId)

  return (
    <div className="flex items-center space-x-2">
      <span className="text-sm text-gray-500">Online:</span>
      <div className="flex -space-x-2">
        {onlineUsers.map((user) => (
          <div
            key={user.id}
            className="relative"
            title={`${user.name} - ${user.activity}`}
          >
            <div className="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center text-white text-xs font-medium">
              {user.name[0].toUpperCase()}
            </div>
            <div className="absolute -bottom-1 -right-1 w-3 h-3 bg-green-500 rounded-full border-2 border-white" />
          </div>
        ))}
      </div>
      {onlineUsers.length > 3 && (
        <span className="text-sm text-gray-500">
          +{onlineUsers.length - 3} more
        </span>
      )}
    </div>
  )
}
```

---

# Core Components

## 2. Comment Thread Component

```tsx
// components/collaboration/CommentThread.tsx
import React, { useState } from 'react'
import { useComments } from '@/hooks/useComments'
import { useAuth } from '@/hooks/useAuth'

interface CommentThreadProps {
  conversationId: string
  parentId?: string
}

const CommentThread: React.FC<CommentThreadProps> = ({
  conversationId,
  parentId
}) => {
  const { comments, addComment, updateComment, deleteComment } = useComments(conversationId, parentId)
  const { user } = useAuth()
  const [newComment, setNewComment] = useState('')
  const [editingComment, setEditingComment] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!newComment.trim()) return

    try {
      await addComment({
        content: newComment,
        conversationId,
        parentId
      })
      setNewComment('')
    } catch (error) {
      console.error('Failed to add comment:', error)
    }
  }

  const handleEdit = async (commentId: string, content: string) => {
    try {
      await updateComment(commentId, { content })
      setEditingComment(null)
    } catch (error) {
      console.error('Failed to update comment:', error)
    }
  }

  const handleDelete = async (commentId: string) => {
    if (confirm('Are you sure you want to delete this comment?')) {
      try {
        await deleteComment(commentId)
      } catch (error) {
        console.error('Failed to delete comment:', error)
      }
    }
  }

  return (
    <div className="space-y-4">
      {/* Comment Form */}
      <form onSubmit={handleSubmit} className="flex space-x-2">
        <input
          type="text"
          value={newComment}
          onChange={(e) => setNewComment(e.target.value)}
          placeholder="Add a comment..."
          className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          type="submit"
          disabled={!newComment.trim()}
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
        >
          Comment
        </button>
      </form>

      {/* Comments List */}
      <div className="space-y-3">
        {comments.map((comment) => (
          <div key={comment.id} className="bg-gray-50 rounded-lg p-3">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center space-x-2">
                  <span className="font-medium text-sm">{comment.author.name}</span>
                  <span className="text-xs text-gray-500">
                    {formatDate(comment.createdAt)}
                  </span>
                  {comment.updatedAt !== comment.createdAt && (
                    <span className="text-xs text-gray-400">(edited)</span>
                  )}
                </div>
                {editingComment === comment.id ? (
                  <EditCommentForm
                    comment={comment}
                    onSave={(content) => handleEdit(comment.id, content)}
                    onCancel={() => setEditingComment(null)}
                  />
                ) : (
                  <p className="text-sm text-gray-700 mt-1">{comment.content}</p>
                )}
              </div>
              {comment.author.id === user?.id && (
                <div className="flex space-x-1">
                  <button
                    onClick={() => setEditingComment(comment.id)}
                    className="text-xs text-blue-600 hover:text-blue-800"
                  >
                    Edit
                  </button>
                  <button
                    onClick={() => handleDelete(comment.id)}
                    className="text-xs text-red-600 hover:text-red-800"
                  >
                    Delete
                  </button>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
```

---

# Real-time Communication

## WebSocket Hook

```typescript
// hooks/useWebSocket.ts
import { useEffect, useRef, useState } from 'react'
import { io, Socket } from 'socket.io-client'

interface WebSocketHook {
  socket: Socket | null
  isConnected: boolean
  emit: (event: string, data: any) => void
  on: (event: string, callback: (data: any) => void) => void
  off: (event: string, callback: (data: any) => void) => void
}

export const useWebSocket = (url: string): WebSocketHook => {
  const [socket, setSocket] = useState<Socket | null>(null)
  const [isConnected, setIsConnected] = useState(false)
  const socketRef = useRef<Socket | null>(null)

  useEffect(() => {
    const newSocket = io(url, {
      auth: {
        token: localStorage.getItem('auth_token')
      }
    })

    newSocket.on('connect', () => {
      setIsConnected(true)
      console.log('Connected to WebSocket')
    })

    newSocket.on('disconnect', () => {
      setIsConnected(false)
      console.log('Disconnected from WebSocket')
    })

    newSocket.on('error', (error) => {
      console.error('WebSocket error:', error)
    })

    setSocket(newSocket)
    socketRef.current = newSocket

    return () => {
      newSocket.close()
    }
  }, [url])

  const emit = (event: string, data: any) => {
    if (socketRef.current) {
      socketRef.current.emit(event, data)
    }
  }

  const on = (event: string, callback: (data: any) => void) => {
    if (socketRef.current) {
      socketRef.current.on(event, callback)
    }
  }

  const off = (event: string, callback: (data: any) => void) => {
    if (socketRef.current) {
      socketRef.current.off(event, callback)
    }
  }

  return {
    socket,
    isConnected,
    emit,
    on,
    off
  }
}
```

---

# Presence Management

## Presence Hook

```typescript
// hooks/usePresence.ts
import { useState, useEffect } from 'react'
import { useWebSocket } from './useWebSocket'
import { useAuth } from './useAuth'

interface User {
  id: string
  name: string
  email: string
  avatar?: string
  activity: string
  lastSeen: Date
}

export const usePresence = (conversationId: string) => {
  const [onlineUsers, setOnlineUsers] = useState<User[]>([])
  const [currentUser, setCurrentUser] = useState<User | null>(null)
  const { socket, isConnected, emit, on, off } = useWebSocket(process.env.REACT_APP_WS_URL || 'ws://localhost:8000')
  const { user } = useAuth()

  useEffect(() => {
    if (!socket || !isConnected) return

    // Join conversation room
    emit('join_conversation', { conversationId })

    // Listen for presence updates
    const handlePresenceUpdate = (data: { users: User[] }) => {
      setOnlineUsers(data.users)
    }

    const handleUserJoined = (data: { user: User }) => {
      setOnlineUsers(prev => [...prev.filter(u => u.id !== data.user.id), data.user])
    }

    const handleUserLeft = (data: { userId: string }) => {
      setOnlineUsers(prev => prev.filter(u => u.id !== data.userId))
    }

    const handleActivityUpdate = (data: { userId: string, activity: string }) => {
      setOnlineUsers(prev => 
        prev.map(u => u.id === data.userId ? { ...u, activity: data.activity } : u)
      )
    }

    on('presence_update', handlePresenceUpdate)
    on('user_joined', handleUserJoined)
    on('user_left', handleUserLeft)
    on('activity_update', handleActivityUpdate)

    // Set current user
    if (user) {
      setCurrentUser({
        id: user.id,
        name: user.name,
        email: user.email,
        activity: 'viewing conversation',
        lastSeen: new Date()
      })
    }

    return () => {
      emit('leave_conversation', { conversationId })
      off('presence_update', handlePresenceUpdate)
      off('user_joined', handleUserJoined)
      off('user_left', handleUserLeft)
      off('activity_update', handleActivityUpdate)
    }
  }, [socket, isConnected, conversationId, user, emit, on, off])

  const updateActivity = (activity: string) => {
    if (socket && isConnected) {
      emit('update_activity', { conversationId, activity })
    }
  }

  return {
    onlineUsers,
    currentUser,
    updateActivity
  }
}
```

---

# Permission Management

## Permission Hook

```typescript
// hooks/usePermissions.ts
import { useState, useEffect } from 'react'
import { useAuth } from './useAuth'

export type Permission = 
  | 'read_conversation'
  | 'write_conversation'
  | 'delete_conversation'
  | 'add_comment'
  | 'edit_comment'
  | 'delete_comment'
  | 'manage_permissions'
  | 'invite_users'

export type Role = 'owner' | 'admin' | 'editor' | 'viewer'

interface PermissionMap {
  [key: string]: Permission[]
}

const ROLE_PERMISSIONS: PermissionMap = {
  owner: [
    'read_conversation',
    'write_conversation',
    'delete_conversation',
    'add_comment',
    'edit_comment',
    'delete_comment',
    'manage_permissions',
    'invite_users'
  ],
  admin: [
    'read_conversation',
    'write_conversation',
    'delete_conversation',
    'add_comment',
    'edit_comment',
    'delete_comment',
    'invite_users'
  ],
  editor: [
    'read_conversation',
    'write_conversation',
    'add_comment',
    'edit_comment'
  ],
  viewer: [
    'read_conversation',
    'add_comment'
  ]
}

export const usePermissions = (conversationId: string) => {
  const [userRole, setUserRole] = useState<Role | null>(null)
  const [permissions, setPermissions] = useState<Permission[]>([])
  const { user } = useAuth()

  useEffect(() => {
    if (!user || !conversationId) return

    // Fetch user role for this conversation
    fetchUserRole(conversationId)
      .then(role => {
        setUserRole(role)
        setPermissions(ROLE_PERMISSIONS[role] || [])
      })
      .catch(error => {
        console.error('Failed to fetch user role:', error)
        setUserRole('viewer')
        setPermissions(ROLE_PERMISSIONS.viewer)
      })
  }, [user, conversationId])

  const hasPermission = (permission: Permission): boolean => {
    return permissions.includes(permission)
  }

  const canRead = () => hasPermission('read_conversation')
  const canWrite = () => hasPermission('write_conversation')
  const canDelete = () => hasPermission('delete_conversation')
  const canComment = () => hasPermission('add_comment')
  const canManagePermissions = () => hasPermission('manage_permissions')

  return {
    userRole,
    permissions,
    hasPermission,
    canRead,
    canWrite,
    canDelete,
    canComment,
    canManagePermissions
  }
}
```

---

# Shared Workspace

## Workspace Component

```tsx
// components/collaboration/SharedWorkspace.tsx
import React, { useState } from 'react'
import { usePermissions } from '@/hooks/usePermissions'
import { usePresence } from '@/hooks/usePresence'
import { CommentThread } from './CommentThread'

interface SharedWorkspaceProps {
  conversationId: string
  conversation: Conversation
}

const SharedWorkspace: React.FC<SharedWorkspaceProps> = ({
  conversationId,
  conversation
}) => {
  const { canRead, canWrite, canComment } = usePermissions(conversationId)
  const { onlineUsers, updateActivity } = usePresence(conversationId)
  const [activeTab, setActiveTab] = useState<'conversation' | 'comments'>('conversation')

  useEffect(() => {
    updateActivity('viewing conversation')
  }, [updateActivity])

  if (!canRead()) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <h3 className="text-lg font-medium text-gray-900">Access Denied</h3>
          <p className="text-gray-500">You don't have permission to view this conversation.</p>
        </div>
      </div>
    )
  }

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="bg-white border-b px-6 py-4">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-xl font-semibold text-gray-900">
              {conversation.title}
            </h1>
            <UserPresence conversationId={conversationId} />
          </div>
          <div className="flex items-center space-x-4">
            <div className="flex space-x-1">
              <button
                onClick={() => setActiveTab('conversation')}
                className={`px-3 py-2 text-sm font-medium rounded-md ${
                  activeTab === 'conversation'
                    ? 'bg-blue-100 text-blue-700'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                Conversation
              </button>
              <button
                onClick={() => setActiveTab('comments')}
                className={`px-3 py-2 text-sm font-medium rounded-md ${
                  activeTab === 'comments'
                    ? 'bg-blue-100 text-blue-700'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                Comments ({conversation.commentCount || 0})
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-hidden">
        {activeTab === 'conversation' ? (
          <ConversationView
            conversation={conversation}
            canWrite={canWrite()}
            canDelete={canDelete()}
          />
        ) : (
          <div className="h-full overflow-y-auto p-6">
            <CommentThread conversationId={conversationId} />
          </div>
        )}
      </div>
    </div>
  )
}
```

---

# Activity Feed

## Activity Component

```tsx
// components/realtime/ActivityFeed.tsx
import React from 'react'
import { useActivity } from '@/hooks/useActivity'

interface Activity {
  id: string
  type: 'conversation_created' | 'conversation_updated' | 'comment_added' | 'user_joined'
  user: {
    id: string
    name: string
    avatar?: string
  }
  data: any
  timestamp: Date
}

const ActivityFeed: React.FC = () => {
  const { activities, isLoading } = useActivity()

  if (isLoading) {
    return (
      <div className="space-y-4">
        {[...Array(5)].map((_, i) => (
          <div key={i} className="animate-pulse">
            <div className="h-4 bg-gray-200 rounded w-3/4 mb-2" />
            <div className="h-3 bg-gray-200 rounded w-1/2" />
          </div>
        ))}
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {activities.map((activity) => (
        <div key={activity.id} className="flex items-start space-x-3">
          <div className="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center text-white text-xs font-medium">
            {activity.user.name[0].toUpperCase()}
          </div>
          <div className="flex-1">
            <p className="text-sm text-gray-900">
              <span className="font-medium">{activity.user.name}</span>{' '}
              {getActivityText(activity)}
            </p>
            <p className="text-xs text-gray-500">
              {formatRelativeTime(activity.timestamp)}
            </p>
          </div>
        </div>
      ))}
    </div>
  )
}

const getActivityText = (activity: Activity): string => {
  switch (activity.type) {
    case 'conversation_created':
      return 'created a new conversation'
    case 'conversation_updated':
      return 'updated the conversation'
    case 'comment_added':
      return 'added a comment'
    case 'user_joined':
      return 'joined the workspace'
    default:
      return 'performed an action'
  }
}
```

---

# Testing

## Collaboration Tests

```typescript
// tests/collaboration/UserPresence.test.tsx
import { render, screen, waitFor } from '@testing-library/react'
import { UserPresence } from '@/components/collaboration/UserPresence'
import { WebSocketProvider } from '@/contexts/WebSocketContext'

const mockWebSocket = {
  emit: jest.fn(),
  on: jest.fn(),
  off: jest.fn(),
  connected: true
}

describe('UserPresence', () => {
  it('displays online users', async () => {
    const mockUsers = [
      { id: '1', name: 'John Doe', activity: 'viewing conversation' },
      { id: '2', name: 'Jane Smith', activity: 'editing conversation' }
    ]

    render(
      <WebSocketProvider value={mockWebSocket}>
        <UserPresence conversationId="test-conversation" />
      </WebSocketProvider>
    )

    // Simulate presence update
    const presenceHandler = mockWebSocket.on.mock.calls.find(
      call => call[0] === 'presence_update'
    )?.[1]
    
    if (presenceHandler) {
      presenceHandler({ users: mockUsers })
    }

    await waitFor(() => {
      expect(screen.getByText('John Doe')).toBeInTheDocument()
      expect(screen.getByText('Jane Smith')).toBeInTheDocument()
    })
  })
})
```

---

# Success Criteria

## Must-Have Features

- [ ] **Real-time Updates** - Live collaboration on conversations
- [ ] **User Presence** - Show online users and their activity
- [ ] **Comment System** - Threaded discussions on conversations
- [ ] **Permission Management** - Role-based access control
- [ ] **Shared Workspaces** - Team-based conversation organization
- [ ] **Activity Feed** - Real-time activity updates
- [ ] **WebSocket Integration** - Stable real-time communication
- [ ] **Error Handling** - Graceful handling of connection issues

---

# Bonus Challenges

## Advanced Features

- [ ] **Video Calls** - Integrated video conferencing
- [ ] **Screen Sharing** - Share screens during collaboration
- [ ] **File Sharing** - Upload and share files in conversations
- [ ] **Notifications** - Push notifications for important events
- [ ] **Conflict Resolution** - Handle simultaneous edits
- [ ] **Version History** - Track changes over time
- [ ] **Advanced Permissions** - Granular permission control
- [ ] **Team Analytics** - Usage and collaboration metrics

---

# Getting Started

## Setup Instructions

1. **Set up WebSocket server** - Add WebSocket support to FastAPI
2. **Choose your frontend framework** - React, Vue, or Angular
3. **Implement real-time communication** - Socket.io or native WebSocket
4. **Add presence management** - Track user online status
5. **Build comment system** - Threaded discussions
6. **Implement permissions** - Role-based access control
7. **Add shared workspaces** - Team-based organization
8. **Test collaboration** - Multi-user testing

---

# Resources

## Helpful Links

- **Socket.io** - https://socket.io/
- **WebSocket API** - https://developer.mozilla.org/en-US/docs/Web/API/WebSocket
- **Real-time Collaboration** - https://web.dev/real-time-collaboration/
- **Presence Systems** - https://pusher.com/guides/presence-channels
- **Permission Management** - https://auth0.com/blog/role-based-access-control-rbac/

---

# Let's Build!

## Ready to Start?

**This assignment will teach you:**
- Real-time web application development
- WebSocket communication
- User presence management
- Collaborative editing
- Permission systems
- Team workspace design

**Start with basic WebSocket integration and build up from there!**

---

# Next Steps

## After Completing This Assignment

1. **Test with multiple users** - Ensure real-time features work correctly
2. **Deploy your app** - Use a platform that supports WebSockets
3. **Share your code** - Create a GitHub repository
4. **Document your approach** - Write a comprehensive README
5. **Move to the next track** - Try advanced UI patterns or mobile development next!

**Happy coding! 🚀**
