---
theme: gaia
_class: lead
paginate: true
backgroundColor: #fff
backgroundImage: url('https://marp.app/assets/hero-background.svg')
---

![bg left:40% 80%](https://oppkey.com/static/logo.jpg)

# **Mobile-First Design Assignment**
## Touch-Optimized Conversation Management

**Build a mobile-first interface for FastOpp**

---

# Assignment Overview

## What You'll Build

A mobile-first web application that provides an optimized touch interface for FastOpp, featuring:
- **Touch-optimized interactions** - Swipe gestures, touch targets
- **Progressive Web App** - Installable, offline-capable
- **Responsive design** - Works on phones, tablets, and desktops
- **Gesture-based navigation** - Intuitive mobile patterns
- **Performance optimization** - Fast loading on mobile networks

---

# Problem Statement

## Mobile Usage Challenges

The current FastOpp UI, while responsive, has limitations for mobile users:
- **Desktop-first design** - Not optimized for touch interactions
- **Small touch targets** - Hard to tap on mobile devices
- **Complex navigation** - Too many clicks to access features
- **Poor offline experience** - Requires constant internet connection
- **Slow loading** - Not optimized for mobile networks

---

# Your Solution

## Mobile-First Interface

Create a mobile-first application that addresses these limitations:

1. **Touch-Optimized UI** - Large touch targets, swipe gestures
2. **Progressive Web App** - Installable, works offline
3. **Gesture Navigation** - Swipe to navigate, pull to refresh
4. **Mobile-First Layout** - Designed for small screens first
5. **Performance Focused** - Fast loading, smooth animations

---

# Technical Requirements

## Tech Stack Options

**Option 1: React Native Web**
- React Native with Expo
- Cross-platform mobile and web
- Native performance

**Option 2: Flutter Web**
- Flutter with web support
- Single codebase for all platforms
- Material Design components

**Option 3: PWA with Framework**
- React, Vue, or Angular
- Service Worker for offline support
- Web App Manifest for installation

---

# Project Structure

## Recommended Architecture

```
src/
├── components/
│   ├── mobile/
│   │   ├── ConversationCard.tsx
│   │   ├── SwipeableCard.tsx
│   │   ├── BottomSheet.tsx
│   │   └── TouchableList.tsx
│   ├── gestures/
│   │   ├── SwipeGesture.tsx
│   │   ├── PullToRefresh.tsx
│   │   └── PinchToZoom.tsx
│   └── shared/
├── hooks/
│   ├── useSwipeGesture.ts
│   ├── usePullToRefresh.ts
│   └── useOfflineSync.ts
├── services/
│   ├── pwa.ts
│   ├── offline.ts
│   └── push-notifications.ts
└── styles/
    ├── mobile.css
    └── animations.css
```

---

# Core Components

## 1. Swipeable Conversation Card

```tsx
// components/mobile/SwipeableCard.tsx
import React, { useRef } from 'react'
import { useSwipeGesture } from '@/hooks/useSwipeGesture'

interface SwipeableCardProps {
  conversation: Conversation
  onSwipeLeft: () => void
  onSwipeRight: () => void
  onTap: () => void
}

const SwipeableCard: React.FC<SwipeableCardProps> = ({
  conversation,
  onSwipeLeft,
  onSwipeRight,
  onTap
}) => {
  const cardRef = useRef<HTMLDivElement>(null)
  
  const { swipeDirection, isDragging } = useSwipeGesture(cardRef, {
    onSwipeLeft,
    onSwipeRight,
    threshold: 100
  })

  return (
    <div
      ref={cardRef}
      className={`
        relative bg-white rounded-lg shadow-md p-4 mb-2
        transition-transform duration-200 ease-out
        ${isDragging ? 'scale-105 shadow-lg' : ''}
        ${swipeDirection === 'left' ? 'bg-red-50' : ''}
        ${swipeDirection === 'right' ? 'bg-green-50' : ''}
      `}
      onClick={onTap}
    >
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-gray-900">
            {conversation.title}
          </h3>
          <p className="text-sm text-gray-500 mt-1">
            {formatDate(conversation.updatedAt)}
          </p>
        </div>
        <div className="flex items-center space-x-2">
          {swipeDirection === 'left' && (
            <span className="text-red-500 text-sm">Delete</span>
          )}
          {swipeDirection === 'right' && (
            <span className="text-green-500 text-sm">Archive</span>
          )}
        </div>
      </div>
    </div>
  )
}
```

---

# Core Components

## 2. Bottom Sheet Modal

```tsx
// components/mobile/BottomSheet.tsx
import React, { useEffect, useRef } from 'react'
import { createPortal } from 'react-dom'

interface BottomSheetProps {
  isOpen: boolean
  onClose: () => void
  children: React.ReactNode
  title?: string
}

const BottomSheet: React.FC<BottomSheetProps> = ({
  isOpen,
  onClose,
  children,
  title
}) => {
  const sheetRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden'
    } else {
      document.body.style.overflow = 'unset'
    }

    return () => {
      document.body.style.overflow = 'unset'
    }
  }, [isOpen])

  if (!isOpen) return null

  return createPortal(
    <div className="fixed inset-0 z-50 flex items-end">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black bg-opacity-50"
        onClick={onClose}
      />
      
      {/* Sheet */}
      <div
        ref={sheetRef}
        className="relative bg-white rounded-t-lg w-full max-h-[80vh] overflow-hidden"
        style={{
          animation: 'slideUp 0.3s ease-out'
        }}
      >
        {/* Handle */}
        <div className="flex justify-center py-2">
          <div className="w-12 h-1 bg-gray-300 rounded-full" />
        </div>
        
        {/* Header */}
        {title && (
          <div className="px-4 py-3 border-b">
            <h2 className="text-lg font-semibold text-gray-900">{title}</h2>
          </div>
        )}
        
        {/* Content */}
        <div className="px-4 py-4 overflow-y-auto">
          {children}
        </div>
      </div>
    </div>,
    document.body
  )
}
```

---

# Gesture Hooks

## Swipe Gesture Hook

```typescript
// hooks/useSwipeGesture.ts
import { useRef, useCallback } from 'react'

interface SwipeGestureOptions {
  onSwipeLeft?: () => void
  onSwipeRight?: () => void
  onSwipeUp?: () => void
  onSwipeDown?: () => void
  threshold?: number
}

export const useSwipeGesture = (
  elementRef: React.RefObject<HTMLElement>,
  options: SwipeGestureOptions
) => {
  const startPos = useRef({ x: 0, y: 0 })
  const currentPos = useRef({ x: 0, y: 0 })
  const isDragging = useRef(false)

  const handleTouchStart = useCallback((e: TouchEvent) => {
    const touch = e.touches[0]
    startPos.current = { x: touch.clientX, y: touch.clientY }
    currentPos.current = { x: touch.clientX, y: touch.clientY }
    isDragging.current = true
  }, [])

  const handleTouchMove = useCallback((e: TouchEvent) => {
    if (!isDragging.current) return
    
    const touch = e.touches[0]
    currentPos.current = { x: touch.clientX, y: touch.clientY }
  }, [])

  const handleTouchEnd = useCallback(() => {
    if (!isDragging.current) return

    const deltaX = currentPos.current.x - startPos.current.x
    const deltaY = currentPos.current.y - startPos.current.y
    const threshold = options.threshold || 50

    if (Math.abs(deltaX) > Math.abs(deltaY)) {
      // Horizontal swipe
      if (deltaX > threshold && options.onSwipeRight) {
        options.onSwipeRight()
      } else if (deltaX < -threshold && options.onSwipeLeft) {
        options.onSwipeLeft()
      }
    } else {
      // Vertical swipe
      if (deltaY > threshold && options.onSwipeDown) {
        options.onSwipeDown()
      } else if (deltaY < -threshold && options.onSwipeUp) {
        options.onSwipeUp()
      }
    }

    isDragging.current = false
  }, [options])

  useEffect(() => {
    const element = elementRef.current
    if (!element) return

    element.addEventListener('touchstart', handleTouchStart)
    element.addEventListener('touchmove', handleTouchMove)
    element.addEventListener('touchend', handleTouchEnd)

    return () => {
      element.removeEventListener('touchstart', handleTouchStart)
      element.removeEventListener('touchmove', handleTouchMove)
      element.removeEventListener('touchend', handleTouchEnd)
    }
  }, [elementRef, handleTouchStart, handleTouchMove, handleTouchEnd])

  return {
    isDragging: isDragging.current,
    swipeDirection: isDragging.current ? 
      (Math.abs(currentPos.current.x - startPos.current.x) > Math.abs(currentPos.current.y - startPos.current.y) ?
        (currentPos.current.x > startPos.current.x ? 'right' : 'left') :
        (currentPos.current.y > startPos.current.y ? 'down' : 'up')
      ) : null
  }
}
```

---

# PWA Features

## Service Worker

```typescript
// public/sw.js
const CACHE_NAME = 'fastopp-v1'
const urlsToCache = [
  '/',
  '/static/js/bundle.js',
  '/static/css/main.css',
  '/manifest.json'
]

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(urlsToCache))
  )
})

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((response) => {
        // Return cached version or fetch from network
        return response || fetch(event.request)
      })
  )
})

self.addEventListener('sync', (event) => {
  if (event.tag === 'background-sync') {
    event.waitUntil(doBackgroundSync())
  }
})

async function doBackgroundSync() {
  // Sync offline data when connection is restored
  const offlineData = await getOfflineData()
  for (const item of offlineData) {
    try {
      await syncItem(item)
    } catch (error) {
      console.error('Sync failed:', error)
    }
  }
}
```

---

# PWA Features

## Web App Manifest

```json
// public/manifest.json
{
  "name": "FastOpp Mobile",
  "short_name": "FastOpp",
  "description": "Mobile conversation management for FastOpp",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#3B82F6",
  "orientation": "portrait",
  "icons": [
    {
      "src": "/icons/icon-192x192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-512x512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ],
  "categories": ["productivity", "business"],
  "screenshots": [
    {
      "src": "/screenshots/mobile-1.png",
      "sizes": "390x844",
      "type": "image/png",
      "form_factor": "narrow"
    }
  ]
}
```

---

# Offline Support

## Offline Sync Hook

```typescript
// hooks/useOfflineSync.ts
import { useState, useEffect } from 'react'
import { useConversationStore } from '@/stores/conversation'

export const useOfflineSync = () => {
  const [isOnline, setIsOnline] = useState(navigator.onLine)
  const [pendingChanges, setPendingChanges] = useState<any[]>([])
  const conversationStore = useConversationStore()

  useEffect(() => {
    const handleOnline = () => {
      setIsOnline(true)
      syncPendingChanges()
    }

    const handleOffline = () => {
      setIsOnline(false)
    }

    window.addEventListener('online', handleOnline)
    window.addEventListener('offline', handleOffline)

    return () => {
      window.removeEventListener('online', handleOnline)
      window.removeEventListener('offline', handleOffline)
    }
  }, [])

  const syncPendingChanges = async () => {
    if (pendingChanges.length === 0) return

    try {
      for (const change of pendingChanges) {
        await conversationStore.syncChange(change)
      }
      setPendingChanges([])
    } catch (error) {
      console.error('Sync failed:', error)
    }
  }

  const queueChange = (change: any) => {
    if (isOnline) {
      // Try to sync immediately
      conversationStore.syncChange(change).catch(() => {
        setPendingChanges(prev => [...prev, change])
      })
    } else {
      // Queue for later sync
      setPendingChanges(prev => [...prev, change])
    }
  }

  return {
    isOnline,
    pendingChanges: pendingChanges.length,
    queueChange
  }
}
```

---

# Mobile Layout

## Responsive Grid

```tsx
// components/mobile/ConversationGrid.tsx
import React from 'react'
import { SwipeableCard } from './SwipeableCard'

interface ConversationGridProps {
  conversations: Conversation[]
  onConversationTap: (id: string) => void
  onConversationSwipeLeft: (id: string) => void
  onConversationSwipeRight: (id: string) => void
}

const ConversationGrid: React.FC<ConversationGridProps> = ({
  conversations,
  onConversationTap,
  onConversationSwipeLeft,
  onConversationSwipeRight
}) => {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 p-4">
      {conversations.map((conversation) => (
        <SwipeableCard
          key={conversation.id}
          conversation={conversation}
          onTap={() => onConversationTap(conversation.id)}
          onSwipeLeft={() => onConversationSwipeLeft(conversation.id)}
          onSwipeRight={() => onConversationSwipeRight(conversation.id)}
        />
      ))}
    </div>
  )
}
```

---

# Performance Optimization

## Lazy Loading

```tsx
// components/mobile/LazyConversationList.tsx
import React, { useState, useEffect, useRef } from 'react'
import { useInView } from 'react-intersection-observer'

interface LazyConversationListProps {
  conversations: Conversation[]
  onLoadMore: () => void
  hasMore: boolean
}

const LazyConversationList: React.FC<LazyConversationListProps> = ({
  conversations,
  onLoadMore,
  hasMore
}) => {
  const [visibleConversations, setVisibleConversations] = useState<Conversation[]>([])
  const [page, setPage] = useState(0)
  const itemsPerPage = 20

  const { ref: loadMoreRef, inView } = useInView({
    threshold: 0.1,
    triggerOnce: false
  })

  useEffect(() => {
    const startIndex = page * itemsPerPage
    const endIndex = startIndex + itemsPerPage
    const newConversations = conversations.slice(0, endIndex)
    setVisibleConversations(newConversations)
  }, [conversations, page])

  useEffect(() => {
    if (inView && hasMore) {
      setPage(prev => prev + 1)
      onLoadMore()
    }
  }, [inView, hasMore, onLoadMore])

  return (
    <div className="space-y-4">
      {visibleConversations.map((conversation) => (
        <ConversationCard
          key={conversation.id}
          conversation={conversation}
        />
      ))}
      {hasMore && (
        <div ref={loadMoreRef} className="flex justify-center py-4">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600" />
        </div>
      )}
    </div>
  )
}
```

---

# Testing

## Mobile Testing

```typescript
// tests/mobile/ConversationCard.test.tsx
import { render, fireEvent, waitFor } from '@testing-library/react'
import { SwipeableCard } from '@/components/mobile/SwipeableCard'

describe('SwipeableCard', () => {
  it('handles swipe left gesture', async () => {
    const onSwipeLeft = jest.fn()
    const conversation = {
      id: '1',
      title: 'Test Conversation',
      updatedAt: '2024-01-01T00:00:00Z'
    }

    const { getByText } = render(
      <SwipeableCard
        conversation={conversation}
        onSwipeLeft={onSwipeLeft}
        onSwipeRight={jest.fn()}
        onTap={jest.fn()}
      />
    )

    const card = getByText('Test Conversation').closest('div')
    
    // Simulate swipe left
    fireEvent.touchStart(card!, { touches: [{ clientX: 100, clientY: 0 }] })
    fireEvent.touchMove(card!, { touches: [{ clientX: 0, clientY: 0 }] })
    fireEvent.touchEnd(card!)

    await waitFor(() => {
      expect(onSwipeLeft).toHaveBeenCalled()
    })
  })
})
```

---

# Success Criteria

## Must-Have Features

- [ ] **Touch-Optimized UI** - Large touch targets, swipe gestures
- [ ] **PWA Features** - Installable, offline-capable
- [ ] **Responsive Design** - Works on all screen sizes
- [ ] **Gesture Navigation** - Swipe, pull-to-refresh
- [ ] **Performance** - Fast loading, smooth animations
- [ ] **Offline Support** - Works without internet connection
- [ ] **Mobile-First Layout** - Designed for small screens first
- [ ] **Accessibility** - Screen reader support, keyboard navigation

---

# Bonus Challenges

## Advanced Features

- [ ] **Push Notifications** - Real-time updates
- [ ] **Haptic Feedback** - Vibration on interactions
- [ ] **Voice Commands** - Speech-to-text search
- [ ] **Biometric Auth** - Fingerprint/face recognition
- [ ] **Dark Mode** - Theme switching
- [ ] **Multi-language** - Internationalization
- [ ] **Advanced Gestures** - Pinch to zoom, long press
- [ ] **Background Sync** - Sync when app is closed

---

# Getting Started

## Setup Instructions

1. **Choose your approach** - React Native Web, Flutter, or PWA
2. **Set up the project** - Create new project with mobile focus
3. **Configure PWA** - Add manifest and service worker
4. **Implement gestures** - Add swipe and touch interactions
5. **Build mobile components** - Create touch-optimized UI
6. **Add offline support** - Implement caching and sync
7. **Test on devices** - Use real devices for testing
8. **Optimize performance** - Lazy loading, image optimization

---

# Resources

## Helpful Links

- **PWA Documentation** - https://web.dev/progressive-web-apps/
- **Touch Events** - https://developer.mozilla.org/en-US/docs/Web/API/Touch_events
- **Service Workers** - https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API
- **React Native Web** - https://necolas.github.io/react-native-web/
- **Flutter Web** - https://flutter.dev/web
- **Mobile Testing** - https://web.dev/test-mobile/

---

# Let's Build!

## Ready to Start?

**This assignment will teach you:**
- Mobile-first design principles
- Touch gesture implementation
- Progressive Web App development
- Offline-first architecture
- Performance optimization for mobile
- Cross-platform development

**Start with the basic mobile layout and build up from there!**

---

# Next Steps

## After Completing This Assignment

1. **Test on real devices** - Use various phones and tablets
2. **Deploy as PWA** - Make it installable
3. **Share your code** - Create a GitHub repository
4. **Document your approach** - Write a comprehensive README
5. **Move to the next track** - Try collaborative features or advanced UI patterns next!

**Happy coding! 🚀**
