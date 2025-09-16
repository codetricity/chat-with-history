---
theme: gaia
_class: lead
paginate: true
backgroundColor: #fff
backgroundImage: url('https://marp.app/assets/hero-background.svg')
---

![bg left:40% 80%](https://oppkey.com/static/logo.jpg)

# **React Modern UI Assignment**
## Component-Based Conversation Management

**Build a sophisticated React interface for FastOpp**

---

# Assignment Overview

## What You'll Build

A modern React application that provides an alternative to the default FastOpp UI, focusing on:
- **Component-based architecture** with reusable UI elements
- **Advanced state management** using Redux or Zustand
- **Real-time updates** with WebSocket integration
- **Drag-and-drop organization** using React DnD
- **Advanced filtering and search** with instant results

---

# Problem Statement

## Current UI Limitations

The existing FastOpp UI, while functional, has some limitations:
- **Monolithic structure** - Hard to customize individual components
- **Limited real-time features** - No live updates
- **Basic drag-and-drop** - Limited organization options
- **Static filtering** - No instant search results
- **Desktop-focused** - Not optimized for mobile workflows

---

# Your Solution

## React-Powered Interface

Create a React application that addresses these limitations:

1. **Modular Components** - Reusable conversation cards, folder trees, search bars
2. **Real-time Updates** - Live conversation updates and collaboration
3. **Advanced Organization** - Nested drag-and-drop with visual feedback
4. **Instant Search** - Real-time filtering as you type
5. **Mobile-First Design** - Touch-optimized for all devices

---

# Technical Requirements

## Tech Stack

- **React 18+** with TypeScript
- **State Management** - Redux Toolkit or Zustand
- **UI Library** - Material-UI, Chakra UI, or Tailwind CSS
- **Drag & Drop** - React DnD or @dnd-kit
- **HTTP Client** - Axios or React Query
- **Routing** - React Router v6
- **Build Tool** - Vite or Create React App

---

# Project Structure

## Recommended Architecture

```
src/
├── components/
│   ├── ConversationCard/
│   ├── FolderTree/
│   ├── SearchBar/
│   ├── FilterPanel/
│   └── ConversationList/
├── hooks/
│   ├── useConversations.ts
│   ├── useFolders.ts
│   └── useSearch.ts
├── services/
│   ├── api.ts
│   └── websocket.ts
├── store/
│   ├── conversationSlice.ts
│   └── folderSlice.ts
└── types/
    └── index.ts
```

---

# Core Components

## 1. ConversationCard Component

```typescript
interface ConversationCardProps {
  conversation: Conversation;
  onEdit: (id: string) => void;
  onDelete: (id: string) => void;
  onMove: (id: string, folderId: string) => void;
  isSelected: boolean;
  onSelect: (id: string) => void;
}

const ConversationCard: React.FC<ConversationCardProps> = ({
  conversation,
  onEdit,
  onDelete,
  onMove,
  isSelected,
  onSelect
}) => {
  // Component implementation
};
```

---

# Core Components

## 2. FolderTree Component

```typescript
interface FolderTreeProps {
  folders: Folder[];
  onFolderSelect: (folderId: string) => void;
  onFolderCreate: (parentId?: string) => void;
  onFolderEdit: (folderId: string) => void;
  onFolderDelete: (folderId: string) => void;
  selectedFolderId?: string;
}

const FolderTree: React.FC<FolderTreeProps> = ({
  folders,
  onFolderSelect,
  onFolderCreate,
  onFolderEdit,
  onFolderDelete,
  selectedFolderId
}) => {
  // Hierarchical folder display with drag-and-drop
};
```

---

# State Management

## Redux Toolkit Setup

```typescript
// store/conversationSlice.ts
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

interface ConversationState {
  conversations: Conversation[];
  loading: boolean;
  error: string | null;
  selectedConversation: string | null;
  filters: ConversationFilters;
}

const conversationSlice = createSlice({
  name: 'conversations',
  initialState,
  reducers: {
    setSelectedConversation: (state, action) => {
      state.selectedConversation = action.payload;
    },
    updateFilters: (state, action) => {
      state.filters = { ...state.filters, ...action.payload };
    }
  },
  extraReducers: (builder) => {
    // Async thunks for API calls
  }
});
```

---

# API Integration

## Custom Hooks

```typescript
// hooks/useConversations.ts
export const useConversations = () => {
  const dispatch = useAppDispatch();
  const { conversations, loading, error } = useAppSelector(
    (state) => state.conversations
  );

  const fetchConversations = useCallback(async () => {
    try {
      dispatch(fetchConversationsStart());
      const data = await conversationAPI.getAll();
      dispatch(fetchConversationsSuccess(data));
    } catch (err) {
      dispatch(fetchConversationsFailure(err.message));
    }
  }, [dispatch]);

  return {
    conversations,
    loading,
    error,
    fetchConversations
  };
};
```

---

# Real-time Features

## WebSocket Integration

```typescript
// services/websocket.ts
class ConversationWebSocket {
  private ws: WebSocket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;

  connect(token: string) {
    this.ws = new WebSocket(`ws://localhost:8000/ws?token=${token}`);
    
    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      this.handleMessage(data);
    };
  }

  private handleMessage(data: any) {
    switch (data.type) {
      case 'conversation_updated':
        // Update conversation in store
        break;
      case 'conversation_created':
        // Add new conversation to store
        break;
      case 'conversation_deleted':
        // Remove conversation from store
        break;
    }
  }
}
```

---

# Advanced Search

## Real-time Filtering

```typescript
// components/SearchBar.tsx
const SearchBar: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [debouncedSearchTerm] = useDebounce(searchTerm, 300);
  const { conversations, setFilteredConversations } = useConversations();

  useEffect(() => {
    if (debouncedSearchTerm) {
      const filtered = conversations.filter(conversation =>
        conversation.title.toLowerCase().includes(debouncedSearchTerm.toLowerCase())
      );
      setFilteredConversations(filtered);
    } else {
      setFilteredConversations(conversations);
    }
  }, [debouncedSearchTerm, conversations]);

  return (
    <input
      type="text"
      value={searchTerm}
      onChange={(e) => setSearchTerm(e.target.value)}
      placeholder="Search conversations..."
      className="w-full p-3 border rounded-lg"
    />
  );
};
```

---

# Drag and Drop

## React DnD Implementation

```typescript
// components/DraggableConversationCard.tsx
import { useDrag, useDrop } from 'react-dnd';

const DraggableConversationCard: React.FC<Props> = ({ conversation, onMove }) => {
  const [{ isDragging }, drag] = useDrag({
    type: 'conversation',
    item: { id: conversation.id, type: 'conversation' },
    collect: (monitor) => ({
      isDragging: monitor.isDragging()
    })
  });

  const [{ isOver }, drop] = useDrop({
    accept: 'conversation',
    drop: (item: any) => {
      if (item.id !== conversation.id) {
        onMove(item.id, conversation.folder_id);
      }
    },
    collect: (monitor) => ({
      isOver: monitor.isOver()
    })
  });

  return (
    <div
      ref={(node) => drag(drop(node))}
      className={`p-4 border rounded-lg ${
        isDragging ? 'opacity-50' : ''
      } ${isOver ? 'bg-blue-50' : ''}`}
    >
      {/* Card content */}
    </div>
  );
};
```

---

# Mobile Optimization

## Responsive Design

```typescript
// components/ConversationList.tsx
const ConversationList: React.FC = () => {
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 768);
    };
    
    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  return (
    <div className={`${isMobile ? 'grid-cols-1' : 'grid-cols-3'} grid gap-4`}>
      {conversations.map(conversation => (
        <ConversationCard
          key={conversation.id}
          conversation={conversation}
          isMobile={isMobile}
        />
      ))}
    </div>
  );
};
```

---

# Performance Optimization

## React.memo and useMemo

```typescript
// components/ConversationCard.tsx
const ConversationCard = React.memo<ConversationCardProps>(({
  conversation,
  onEdit,
  onDelete,
  onMove,
  isSelected,
  onSelect
}) => {
  const handleEdit = useCallback(() => {
    onEdit(conversation.id);
  }, [conversation.id, onEdit]);

  const handleDelete = useCallback(() => {
    onDelete(conversation.id);
  }, [conversation.id, onDelete]);

  const handleMove = useCallback((folderId: string) => {
    onMove(conversation.id, folderId);
  }, [conversation.id, onMove]);

  return (
    <div className={`conversation-card ${isSelected ? 'selected' : ''}`}>
      {/* Card content */}
    </div>
  );
});
```

---

# Testing Strategy

## Component Testing

```typescript
// __tests__/ConversationCard.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { ConversationCard } from '../ConversationCard';

describe('ConversationCard', () => {
  const mockConversation = {
    id: '1',
    title: 'Test Conversation',
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-01T00:00:00Z',
    is_active: true
  };

  it('renders conversation title', () => {
    render(
      <ConversationCard
        conversation={mockConversation}
        onEdit={jest.fn()}
        onDelete={jest.fn()}
        onMove={jest.fn()}
        isSelected={false}
        onSelect={jest.fn()}
      />
    );
    
    expect(screen.getByText('Test Conversation')).toBeInTheDocument();
  });

  it('calls onEdit when edit button is clicked', () => {
    const mockOnEdit = jest.fn();
    render(
      <ConversationCard
        conversation={mockConversation}
        onEdit={mockOnEdit}
        onDelete={jest.fn()}
        onMove={jest.fn()}
        isSelected={false}
        onSelect={jest.fn()}
      />
    );
    
    fireEvent.click(screen.getByRole('button', { name: /edit/i }));
    expect(mockOnEdit).toHaveBeenCalledWith('1');
  });
});
```

---

# Success Criteria

## Must-Have Features

- [ ] **Conversation List** - Display all conversations with proper pagination
- [ ] **Folder Organization** - Hierarchical folder structure with drag-and-drop
- [ ] **Search & Filter** - Real-time search with multiple filter options
- [ ] **CRUD Operations** - Create, read, update, delete conversations
- [ ] **Responsive Design** - Works on desktop, tablet, and mobile
- [ ] **Authentication** - Proper login/logout functionality
- [ ] **Error Handling** - Graceful error states and loading indicators

---

# Bonus Challenges

## Advanced Features

- [ ] **Real-time Collaboration** - Live updates when others make changes
- [ ] **Keyboard Shortcuts** - Power user keyboard navigation
- [ ] **Bulk Operations** - Select multiple conversations for batch actions
- [ ] **Export/Import** - Export conversations to various formats
- [ ] **Dark Mode** - Theme switching capability
- [ ] **Offline Support** - PWA with offline functionality
- [ ] **Voice Search** - Speech-to-text search functionality

---

# Getting Started

## Setup Instructions

1. **Clone the repository** and explore the API
2. **Create a new React app** with TypeScript
3. **Install required dependencies** (Redux Toolkit, React DnD, etc.)
4. **Set up the project structure** as outlined above
5. **Start with the ConversationCard component** - build the foundation
6. **Add state management** - implement Redux slices
7. **Integrate with the API** - create custom hooks
8. **Add advanced features** - search, drag-and-drop, real-time updates

---

# Resources

## Helpful Links

- **React Documentation** - https://react.dev/
- **Redux Toolkit** - https://redux-toolkit.js.org/
- **React DnD** - https://react-dnd.github.io/react-dnd/
- **Material-UI** - https://mui.com/
- **Chakra UI** - https://chakra-ui.com/
- **React Query** - https://tanstack.com/query/latest

---

# Let's Build!

## Ready to Start?

**This assignment will teach you:**
- Modern React patterns and best practices
- Advanced state management techniques
- Real-time application development
- Performance optimization strategies
- Mobile-first responsive design

**Start with the ConversationCard component and build up from there!**

---

# Next Steps

## After Completing This Assignment

1. **Share your code** - Create a GitHub repository
2. **Document your approach** - Write a README explaining your decisions
3. **Deploy your app** - Use Vercel, Netlify, or similar
4. **Get feedback** - Share with the community
5. **Move to the next track** - Try Flutter or Vue.js next!

**Happy coding! 🚀**
