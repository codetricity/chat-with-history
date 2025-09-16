---
theme: gaia
_class: lead
paginate: true
backgroundColor: #fff
backgroundImage: url('https://marp.app/assets/hero-background.svg')
---

![bg left:40% 80%](https://oppkey.com/static/logo.jpg)

# **Vue.js Dashboard Assignment**
## Lightweight, Reactive Interface

**Build a modern Vue.js dashboard for FastOpp**

---

# Assignment Overview

## What You'll Build

A Vue.js application that provides a clean, lightweight interface for FastOpp, featuring:
- **Reactive data binding** - Automatic UI updates
- **Component-based architecture** - Reusable, maintainable code
- **Lightweight framework** - Fast loading and minimal bundle size
- **Composition API** - Modern Vue 3 patterns
- **TypeScript support** - Type-safe development

---

# Problem Statement

## Why Vue.js?

The current FastOpp UI, while functional, could benefit from a lighter, more reactive approach:
- **Heavy JavaScript frameworks** - Slow initial load times
- **Complex state management** - Over-engineered solutions
- **Poor developer experience** - Hard to maintain and extend
- **Limited reactivity** - Manual DOM updates
- **Bundle size** - Large JavaScript payloads

---

# Your Solution

## Vue.js-Powered Interface

Create a Vue.js application that addresses these limitations:

1. **Lightweight Framework** - Small bundle size, fast loading
2. **Reactive Data** - Automatic UI updates when data changes
3. **Simple State Management** - Pinia for clean state management
4. **Component Reusability** - Easy to maintain and extend
5. **Great DX** - Excellent developer experience with TypeScript

---

# Technical Requirements

## Tech Stack

- **Vue 3** with Composition API
- **TypeScript** for type safety
- **Pinia** for state management
- **Vue Router** for navigation
- **Axios** for HTTP requests
- **Tailwind CSS** for styling
- **Vite** for build tooling

---

# Project Structure

## Recommended Architecture

```
src/
├── main.ts
├── App.vue
├── components/
│   ├── ConversationCard.vue
│   ├── FolderTree.vue
│   ├── SearchBar.vue
│   └── ConversationList.vue
├── views/
│   ├── Dashboard.vue
│   ├── ConversationDetail.vue
│   └── Settings.vue
├── stores/
│   ├── conversation.ts
│   ├── folder.ts
│   └── auth.ts
├── services/
│   ├── api.ts
│   └── websocket.ts
├── types/
│   └── index.ts
└── composables/
    ├── useConversations.ts
    ├── useFolders.ts
    └── useSearch.ts
```

---

# Core Components

## 1. Conversation Card

```vue
<!-- components/ConversationCard.vue -->
<template>
  <div
    class="bg-white rounded-lg shadow-md p-4 hover:shadow-lg transition-shadow cursor-pointer"
    @click="handleClick"
  >
    <div class="flex items-center justify-between">
      <div class="flex-1">
        <h3 class="text-lg font-semibold text-gray-900">
          {{ conversation.title }}
        </h3>
        <p class="text-sm text-gray-500 mt-1">
          {{ formatDate(conversation.updatedAt) }}
        </p>
      </div>
      <div class="flex items-center space-x-2">
        <button
          @click.stop="handleEdit"
          class="p-2 text-gray-400 hover:text-blue-500 transition-colors"
        >
          <EditIcon class="w-4 h-4" />
        </button>
        <button
          @click.stop="handleDelete"
          class="p-2 text-gray-400 hover:text-red-500 transition-colors"
        >
          <DeleteIcon class="w-4 h-4" />
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useConversationStore } from '@/stores/conversation'
import type { Conversation } from '@/types'

interface Props {
  conversation: Conversation
}

const props = defineProps<Props>()
const router = useRouter()
const conversationStore = useConversationStore()

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString()
}

const handleClick = () => {
  router.push(`/conversations/${props.conversation.id}`)
}

const handleEdit = () => {
  conversationStore.setEditingConversation(props.conversation)
}

const handleDelete = async () => {
  if (confirm('Are you sure you want to delete this conversation?')) {
    await conversationStore.deleteConversation(props.conversation.id)
  }
}
</script>
```

---

# Core Components

## 2. Folder Tree

```vue
<!-- components/FolderTree.vue -->
<template>
  <div class="space-y-2">
    <div
      v-for="folder in folders"
      :key="folder.id"
      class="folder-item"
    >
      <div
        class="flex items-center justify-between p-2 rounded hover:bg-gray-100 cursor-pointer"
        @click="toggleFolder(folder.id)"
      >
        <div class="flex items-center space-x-2">
          <ChevronRightIcon
            :class="[
              'w-4 h-4 transition-transform',
              expandedFolders.has(folder.id) ? 'rotate-90' : ''
            ]"
          />
          <FolderIcon class="w-4 h-4 text-blue-500" />
          <span class="text-sm font-medium">{{ folder.name }}</span>
        </div>
        <div class="flex items-center space-x-1">
          <span class="text-xs text-gray-500">
            {{ getConversationCount(folder.id) }}
          </span>
          <button
            @click.stop="handleAddConversation(folder.id)"
            class="p-1 text-gray-400 hover:text-blue-500"
          >
            <PlusIcon class="w-3 h-3" />
          </button>
        </div>
      </div>
      
      <div
        v-if="expandedFolders.has(folder.id)"
        class="ml-6 space-y-1"
      >
        <ConversationCard
          v-for="conversation in getConversationsInFolder(folder.id)"
          :key="conversation.id"
          :conversation="conversation"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useConversationStore } from '@/stores/conversation'
import { useFolderStore } from '@/stores/folder'
import ConversationCard from './ConversationCard.vue'
import type { Folder } from '@/types'

const conversationStore = useConversationStore()
const folderStore = useFolderStore()

const expandedFolders = ref(new Set<string>())

const folders = computed(() => folderStore.folders)
const conversations = computed(() => conversationStore.conversations)

const toggleFolder = (folderId: string) => {
  if (expandedFolders.value.has(folderId)) {
    expandedFolders.value.delete(folderId)
  } else {
    expandedFolders.value.add(folderId)
  }
}

const getConversationCount = (folderId: string) => {
  return conversations.value.filter(c => c.folderId === folderId).length
}

const getConversationsInFolder = (folderId: string) => {
  return conversations.value.filter(c => c.folderId === folderId)
}

const handleAddConversation = (folderId: string) => {
  conversationStore.createConversation({ folderId })
}
</script>
```

---

# State Management

## Pinia Store

```typescript
// stores/conversation.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { conversationApi } from '@/services/api'
import type { Conversation, CreateConversationData } from '@/types'

export const useConversationStore = defineStore('conversation', () => {
  const conversations = ref<Conversation[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const selectedConversation = ref<Conversation | null>(null)
  const editingConversation = ref<Conversation | null>(null)

  const activeConversations = computed(() =>
    conversations.value.filter(c => c.isActive)
  )

  const getConversationById = computed(() => (id: string) =>
    conversations.value.find(c => c.id === id)
  )

  const fetchConversations = async () => {
    loading.value = true
    error.value = null
    
    try {
      const data = await conversationApi.getAll()
      conversations.value = data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch conversations'
    } finally {
      loading.value = false
    }
  }

  const createConversation = async (data: CreateConversationData) => {
    try {
      const newConversation = await conversationApi.create(data)
      conversations.value.push(newConversation)
      return newConversation
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to create conversation'
      throw err
    }
  }

  const updateConversation = async (id: string, data: Partial<Conversation>) => {
    try {
      const updatedConversation = await conversationApi.update(id, data)
      const index = conversations.value.findIndex(c => c.id === id)
      if (index !== -1) {
        conversations.value[index] = updatedConversation
      }
      return updatedConversation
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to update conversation'
      throw err
    }
  }

  const deleteConversation = async (id: string) => {
    try {
      await conversationApi.delete(id)
      conversations.value = conversations.value.filter(c => c.id !== id)
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to delete conversation'
      throw err
    }
  }

  const setSelectedConversation = (conversation: Conversation | null) => {
    selectedConversation.value = conversation
  }

  const setEditingConversation = (conversation: Conversation | null) => {
    editingConversation.value = conversation
  }

  return {
    conversations,
    loading,
    error,
    selectedConversation,
    editingConversation,
    activeConversations,
    getConversationById,
    fetchConversations,
    createConversation,
    updateConversation,
    deleteConversation,
    setSelectedConversation,
    setEditingConversation
  }
})
```

---

# Composables

## Custom Hooks

```typescript
// composables/useConversations.ts
import { computed } from 'vue'
import { useConversationStore } from '@/stores/conversation'
import { useSearchStore } from '@/stores/search'

export function useConversations() {
  const conversationStore = useConversationStore()
  const searchStore = useSearchStore()

  const filteredConversations = computed(() => {
    if (!searchStore.query) {
      return conversationStore.activeConversations
    }

    return conversationStore.activeConversations.filter(conversation =>
      conversation.title.toLowerCase().includes(searchStore.query.toLowerCase())
    )
  })

  const conversationsByFolder = computed(() => {
    const grouped: Record<string, typeof conversationStore.conversations> = {}
    
    filteredConversations.value.forEach(conversation => {
      const folderId = conversation.folderId || 'unorganized'
      if (!grouped[folderId]) {
        grouped[folderId] = []
      }
      grouped[folderId].push(conversation)
    })

    return grouped
  })

  const getConversationsInFolder = (folderId: string) => {
    return conversationsByFolder.value[folderId] || []
  }

  return {
    conversations: filteredConversations,
    conversationsByFolder,
    getConversationsInFolder,
    loading: conversationStore.loading,
    error: conversationStore.error,
    fetchConversations: conversationStore.fetchConversations,
    createConversation: conversationStore.createConversation,
    updateConversation: conversationStore.updateConversation,
    deleteConversation: conversationStore.deleteConversation
  }
}
```

---

# API Integration

## Service Layer

```typescript
// services/api.ts
import axios from 'axios'
import type { Conversation, Folder, Client, Project } from '@/types'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor for auth
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized
      localStorage.removeItem('auth_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export const conversationApi = {
  getAll: () => api.get<Conversation[]>('/api/conversations').then(res => res.data),
  getById: (id: string) => api.get<Conversation>(`/api/conversations/${id}`).then(res => res.data),
  create: (data: Partial<Conversation>) => api.post<Conversation>('/api/conversations', data).then(res => res.data),
  update: (id: string, data: Partial<Conversation>) => api.put<Conversation>(`/api/conversations/${id}`, data).then(res => res.data),
  delete: (id: string) => api.delete(`/api/conversations/${id}`)
}

export const folderApi = {
  getAll: () => api.get<Folder[]>('/api/folders').then(res => res.data),
  create: (data: Partial<Folder>) => api.post<Folder>('/api/folders', data).then(res => res.data),
  update: (id: string, data: Partial<Folder>) => api.put<Folder>(`/api/folders/${id}`, data).then(res => res.data),
  delete: (id: string) => api.delete(`/api/folders/${id}`)
}

export const searchApi = {
  search: (query: string) => api.get(`/api/search?q=${encodeURIComponent(query)}`).then(res => res.data)
}
```

---

# Search Functionality

## Real-time Search

```vue
<!-- components/SearchBar.vue -->
<template>
  <div class="relative">
    <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
      <SearchIcon class="h-5 w-5 text-gray-400" />
    </div>
    <input
      v-model="searchQuery"
      type="text"
      class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-blue-500 focus:border-blue-500"
      placeholder="Search conversations..."
      @input="handleSearch"
    />
    <div
      v-if="searchQuery"
      class="absolute inset-y-0 right-0 pr-3 flex items-center"
    >
      <button
        @click="clearSearch"
        class="text-gray-400 hover:text-gray-600"
      >
        <XIcon class="h-5 w-5" />
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useSearchStore } from '@/stores/search'
import { useDebounce } from '@/composables/useDebounce'

const searchStore = useSearchStore()
const searchQuery = ref('')

const debouncedSearchQuery = useDebounce(searchQuery, 300)

watch(debouncedSearchQuery, (newQuery) => {
  searchStore.setQuery(newQuery)
})

const handleSearch = () => {
  // Search is handled by the watcher
}

const clearSearch = () => {
  searchQuery.value = ''
  searchStore.setQuery('')
}
</script>
```

---

# Responsive Design

## Mobile-First Layout

```vue
<!-- views/Dashboard.vue -->
<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow-sm border-b">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <h1 class="text-xl font-semibold text-gray-900">
            FastOpp Dashboard
          </h1>
          <div class="flex items-center space-x-4">
            <SearchBar />
            <button
              @click="showNewConversationModal = true"
              class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors"
            >
              New Conversation
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <!-- Sidebar -->
        <aside class="lg:col-span-1">
          <div class="bg-white rounded-lg shadow-sm p-4">
            <h2 class="text-lg font-medium text-gray-900 mb-4">Folders</h2>
            <FolderTree />
          </div>
        </aside>

        <!-- Main Content -->
        <main class="lg:col-span-3">
          <div class="bg-white rounded-lg shadow-sm">
            <div class="p-4 border-b">
              <h2 class="text-lg font-medium text-gray-900">
                Conversations
                <span class="text-sm text-gray-500 ml-2">
                  ({{ conversations.length }})
                </span>
              </h2>
            </div>
            <div class="p-4">
              <ConversationList :conversations="conversations" />
            </div>
          </div>
        </main>
      </div>
    </div>

    <!-- Modals -->
    <NewConversationModal
      v-if="showNewConversationModal"
      @close="showNewConversationModal = false"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useConversations } from '@/composables/useConversations'
import SearchBar from '@/components/SearchBar.vue'
import FolderTree from '@/components/FolderTree.vue'
import ConversationList from '@/components/ConversationList.vue'
import NewConversationModal from '@/components/NewConversationModal.vue'

const { conversations, fetchConversations } = useConversations()
const showNewConversationModal = ref(false)

onMounted(() => {
  fetchConversations()
})
</script>
```

---

# Testing

## Component Tests

```typescript
// tests/components/ConversationCard.test.ts
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import ConversationCard from '@/components/ConversationCard.vue'
import type { Conversation } from '@/types'

describe('ConversationCard', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('renders conversation title', () => {
    const conversation: Conversation = {
      id: '1',
      title: 'Test Conversation',
      createdAt: '2024-01-01T00:00:00Z',
      updatedAt: '2024-01-01T00:00:00Z',
      isActive: true
    }

    const wrapper = mount(ConversationCard, {
      props: { conversation }
    })

    expect(wrapper.text()).toContain('Test Conversation')
  })

  it('emits click event when clicked', async () => {
    const conversation: Conversation = {
      id: '1',
      title: 'Test Conversation',
      createdAt: '2024-01-01T00:00:00Z',
      updatedAt: '2024-01-01T00:00:00Z',
      isActive: true
    }

    const wrapper = mount(ConversationCard, {
      props: { conversation }
    })

    await wrapper.trigger('click')
    expect(wrapper.emitted('click')).toBeTruthy()
  })
})
```

---

# Success Criteria

## Must-Have Features

- [ ] **Conversation Management** - CRUD operations for conversations
- [ ] **Folder Organization** - Hierarchical folder structure
- [ ] **Search & Filter** - Real-time search functionality
- [ ] **Responsive Design** - Works on all screen sizes
- [ ] **State Management** - Clean Pinia store implementation
- [ ] **TypeScript** - Type-safe development
- [ ] **Component Architecture** - Reusable, maintainable components
- [ ] **Error Handling** - Graceful error states

---

# Bonus Challenges

## Advanced Features

- [ ] **Real-time Updates** - WebSocket integration
- [ ] **Offline Support** - Service worker implementation
- [ ] **Dark Mode** - Theme switching
- [ ] **Keyboard Shortcuts** - Power user features
- [ ] **Bulk Operations** - Multi-select actions
- [ ] **Export/Import** - Data portability
- [ ] **PWA Features** - Installable web app
- [ ] **Performance Optimization** - Lazy loading, virtual scrolling

---

# Getting Started

## Setup Instructions

1. **Create Vue project** - `npm create vue@latest fastopp-vue`
2. **Install dependencies** - Add Pinia, Axios, Tailwind CSS
3. **Set up project structure** - Create the folder structure above
4. **Configure TypeScript** - Set up type definitions
5. **Create stores** - Implement Pinia stores
6. **Build components** - Start with basic components
7. **Add routing** - Set up Vue Router
8. **Integrate with API** - Connect to FastOpp backend

---

# Dependencies

## package.json

```json
{
  "dependencies": {
    "vue": "^3.3.4",
    "vue-router": "^4.2.4",
    "pinia": "^2.1.6",
    "axios": "^1.5.0",
    "@headlessui/vue": "^1.7.16",
    "@heroicons/vue": "^2.0.18"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^4.3.4",
    "typescript": "^5.1.6",
    "vite": "^4.4.9",
    "tailwindcss": "^3.3.3",
    "autoprefixer": "^10.4.15",
    "postcss": "^8.4.29",
    "@vue/test-utils": "^2.4.1",
    "vitest": "^0.34.3"
  }
}
```

---

# Resources

## Helpful Links

- **Vue.js Documentation** - https://vuejs.org/
- **Pinia** - https://pinia.vuejs.org/
- **Vue Router** - https://router.vuejs.org/
- **Tailwind CSS** - https://tailwindcss.com/
- **Vite** - https://vitejs.dev/
- **TypeScript** - https://www.typescriptlang.org/

---

# Let's Build!

## Ready to Start?

**This assignment will teach you:**
- Vue.js 3 with Composition API
- Modern state management with Pinia
- TypeScript integration
- Component-based architecture
- Reactive programming patterns
- Performance optimization

**Start with the basic app structure and build up from there!**

---

# Next Steps

## After Completing This Assignment

1. **Deploy your app** - Use Vercel, Netlify, or similar
2. **Test thoroughly** - Ensure all features work correctly
3. **Share your code** - Create a GitHub repository
4. **Document your approach** - Write a comprehensive README
5. **Move to the next track** - Try mobile development or collaborative features next!

**Happy coding! 🚀**
