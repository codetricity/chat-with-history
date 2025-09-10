---
theme: gaia
_class: lead
paginate: true
backgroundColor: #fff
backgroundImage: url('https://marp.app/assets/hero-background.svg')
---

![bg left:40% 80%](https://oppkey.com/static/logo.jpg)

# **Flutter Web App Assignment**
## Cross-Platform Conversation Management

**Build a beautiful Flutter web app for FastOpp**

---

# Assignment Overview

## What You'll Build

A Flutter web application that provides a modern, responsive interface for FastOpp, featuring:
- **Cross-platform compatibility** - Works on web, mobile, and desktop
- **Material Design 3** - Modern, beautiful UI components
- **Smooth animations** - Delightful user interactions
- **Offline-first architecture** - Works without internet connection
- **Native performance** - Fast, responsive interface

---

# Problem Statement

## Why Flutter for Web?

The current FastOpp UI is built with traditional web technologies, which have limitations:
- **Platform-specific code** - Different codebases for web and mobile
- **Performance issues** - JavaScript can be slow for complex UIs
- **Inconsistent UX** - Different experiences across platforms
- **Limited offline support** - Requires constant internet connection
- **Complex state management** - Hard to maintain across components

---

# Your Solution

## Flutter-Powered Interface

Create a Flutter web app that addresses these limitations:

1. **Single Codebase** - One app for web, mobile, and desktop
2. **High Performance** - Compiled to native code
3. **Consistent UX** - Same experience across all platforms
4. **Offline Support** - Local storage and sync capabilities
5. **Beautiful Animations** - Smooth, native-feeling interactions

---

# Technical Requirements

## Tech Stack

- **Flutter 3.0+** with Dart 3.0+
- **State Management** - Riverpod or Bloc
- **HTTP Client** - Dio or http package
- **Local Storage** - Hive or SQLite
- **UI Framework** - Material Design 3
- **Routing** - GoRouter
- **Build Tool** - Flutter web build

---

# Project Structure

## Recommended Architecture

```
lib/
├── main.dart
├── app/
│   ├── app.dart
│   └── routes.dart
├── core/
│   ├── constants/
│   ├── errors/
│   ├── network/
│   └── utils/
├── features/
│   ├── conversations/
│   │   ├── data/
│   │   ├── domain/
│   │   └── presentation/
│   ├── folders/
│   └── search/
├── shared/
│   ├── widgets/
│   ├── services/
│   └── models/
└── theme/
    └── app_theme.dart
```

---

# Core Features

## 1. Conversation List

```dart
// features/conversations/presentation/widgets/conversation_list.dart
class ConversationList extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final conversations = ref.watch(conversationProvider);
    final isLoading = ref.watch(conversationLoadingProvider);

    if (isLoading) {
      return const Center(child: CircularProgressIndicator());
    }

    return ListView.builder(
      itemCount: conversations.length,
      itemBuilder: (context, index) {
        final conversation = conversations[index];
        return ConversationCard(conversation: conversation);
      },
    );
  }
}
```

---

# Core Features

## 2. Conversation Card

```dart
// features/conversations/presentation/widgets/conversation_card.dart
class ConversationCard extends ConsumerWidget {
  final Conversation conversation;

  const ConversationCard({Key? key, required this.conversation}) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Card(
      elevation: 2,
      child: ListTile(
        leading: CircleAvatar(
          backgroundColor: Theme.of(context).primaryColor,
          child: Text(conversation.title[0].toUpperCase()),
        ),
        title: Text(conversation.title),
        subtitle: Text(
          _formatDate(conversation.updatedAt),
          style: Theme.of(context).textTheme.bodySmall,
        ),
        trailing: PopupMenuButton(
          itemBuilder: (context) => [
            PopupMenuItem(
              value: 'edit',
              child: const Text('Edit'),
            ),
            PopupMenuItem(
              value: 'delete',
              child: const Text('Delete'),
            ),
          ],
          onSelected: (value) => _handleMenuAction(value, ref),
        ),
        onTap: () => _navigateToConversation(context, conversation.id),
      ),
    );
  }
}
```

---

# State Management

## Riverpod Setup

```dart
// features/conversations/data/providers/conversation_provider.dart
final conversationProvider = StateNotifierProvider<ConversationNotifier, List<Conversation>>(
  (ref) => ConversationNotifier(ref.read(conversationRepositoryProvider)),
);

final conversationLoadingProvider = StateProvider<bool>((ref) => false);

class ConversationNotifier extends StateNotifier<List<Conversation>> {
  final ConversationRepository _repository;

  ConversationNotifier(this._repository) : super([]) {
    loadConversations();
  }

  Future<void> loadConversations() async {
    try {
      state = await _repository.getConversations();
    } catch (e) {
      // Handle error
    }
  }

  Future<void> createConversation(Conversation conversation) async {
    final newConversation = await _repository.createConversation(conversation);
    state = [...state, newConversation];
  }

  Future<void> deleteConversation(String id) async {
    await _repository.deleteConversation(id);
    state = state.where((c) => c.id != id).toList();
  }
}
```

---

# API Integration

## Repository Pattern

```dart
// features/conversations/data/repositories/conversation_repository.dart
abstract class ConversationRepository {
  Future<List<Conversation>> getConversations();
  Future<Conversation> getConversation(String id);
  Future<Conversation> createConversation(Conversation conversation);
  Future<Conversation> updateConversation(Conversation conversation);
  Future<void> deleteConversation(String id);
}

class ConversationRepositoryImpl implements ConversationRepository {
  final ApiClient _apiClient;

  ConversationRepositoryImpl(this._apiClient);

  @override
  Future<List<Conversation>> getConversations() async {
    try {
      final response = await _apiClient.get('/api/conversations');
      return (response.data as List)
          .map((json) => Conversation.fromJson(json))
          .toList();
    } catch (e) {
      throw ServerException('Failed to load conversations');
    }
  }

  @override
  Future<Conversation> createConversation(Conversation conversation) async {
    try {
      final response = await _apiClient.post(
        '/api/conversations',
        data: conversation.toJson(),
      );
      return Conversation.fromJson(response.data);
    } catch (e) {
      throw ServerException('Failed to create conversation');
    }
  }
}
```

---

# Offline Support

## Local Storage

```dart
// core/storage/local_storage.dart
class LocalStorage {
  static const String _conversationsKey = 'conversations';
  static const String _foldersKey = 'folders';

  static Future<void> saveConversations(List<Conversation> conversations) async {
    final prefs = await SharedPreferences.getInstance();
    final jsonList = conversations.map((c) => c.toJson()).toList();
    await prefs.setString(_conversationsKey, jsonEncode(jsonList));
  }

  static Future<List<Conversation>> loadConversations() async {
    final prefs = await SharedPreferences.getInstance();
    final jsonString = prefs.getString(_conversationsKey);
    
    if (jsonString == null) return [];
    
    final jsonList = jsonDecode(jsonString) as List;
    return jsonList.map((json) => Conversation.fromJson(json)).toList();
  }

  static Future<void> syncWithServer() async {
    // Implement sync logic
    final localConversations = await loadConversations();
    final serverConversations = await _apiClient.getConversations();
    
    // Merge and resolve conflicts
    final mergedConversations = _mergeConversations(localConversations, serverConversations);
    await saveConversations(mergedConversations);
  }
}
```

---

# Search Functionality

## Real-time Search

```dart
// features/search/presentation/widgets/search_bar.dart
class SearchBar extends ConsumerStatefulWidget {
  @override
  _SearchBarState createState() => _SearchBarState();
}

class _SearchBarState extends ConsumerState<SearchBar> {
  final TextEditingController _controller = TextEditingController();
  Timer? _debounceTimer;

  @override
  void dispose() {
    _controller.dispose();
    _debounceTimer?.cancel();
    super.dispose();
  }

  void _onSearchChanged(String query) {
    _debounceTimer?.cancel();
    _debounceTimer = Timer(const Duration(milliseconds: 300), () {
      ref.read(searchQueryProvider.notifier).update((state) => query);
    });
  }

  @override
  Widget build(BuildContext context) {
    return TextField(
      controller: _controller,
      onChanged: _onSearchChanged,
      decoration: InputDecoration(
        hintText: 'Search conversations...',
        prefixIcon: const Icon(Icons.search),
        suffixIcon: _controller.text.isNotEmpty
            ? IconButton(
                icon: const Icon(Icons.clear),
                onPressed: () {
                  _controller.clear();
                  _onSearchChanged('');
                },
              )
            : null,
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
        ),
      ),
    );
  }
}
```

---

# Folder Organization

## Drag and Drop

```dart
// features/folders/presentation/widgets/folder_tree.dart
class FolderTree extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final folders = ref.watch(folderProvider);
    final conversations = ref.watch(conversationProvider);

    return ReorderableListView.builder(
      itemCount: folders.length,
      onReorder: (oldIndex, newIndex) {
        ref.read(folderProvider.notifier).reorderFolders(oldIndex, newIndex);
      },
      itemBuilder: (context, index) {
        final folder = folders[index];
        return FolderTile(
          key: ValueKey(folder.id),
          folder: folder,
          conversations: conversations.where((c) => c.folderId == folder.id).toList(),
        );
      },
    );
  }
}

class FolderTile extends StatelessWidget {
  final Folder folder;
  final List<Conversation> conversations;

  const FolderTile({
    Key? key,
    required this.folder,
    required this.conversations,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return ExpansionTile(
      title: Text(folder.name),
      subtitle: Text('${conversations.length} conversations'),
      children: conversations.map((conversation) => 
        ConversationCard(conversation: conversation)
      ).toList(),
    );
  }
}
```

---

# Responsive Design

## Adaptive Layout

```dart
// shared/widgets/responsive_layout.dart
class ResponsiveLayout extends StatelessWidget {
  final Widget mobile;
  final Widget? tablet;
  final Widget desktop;

  const ResponsiveLayout({
    Key? key,
    required this.mobile,
    this.tablet,
    required this.desktop,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        if (constraints.maxWidth < 600) {
          return mobile;
        } else if (constraints.maxWidth < 1200) {
          return tablet ?? desktop;
        } else {
          return desktop;
        }
      },
    );
  }
}

// Usage
ResponsiveLayout(
  mobile: MobileConversationView(),
  tablet: TabletConversationView(),
  desktop: DesktopConversationView(),
)
```

---

# Animations

## Smooth Transitions

```dart
// shared/widgets/animated_conversation_card.dart
class AnimatedConversationCard extends StatefulWidget {
  final Conversation conversation;
  final VoidCallback onTap;

  @override
  _AnimatedConversationCardState createState() => _AnimatedConversationCardState();
}

class _AnimatedConversationCardState extends State<AnimatedConversationCard>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _scaleAnimation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: const Duration(milliseconds: 200),
      vsync: this,
    );
    _scaleAnimation = Tween<double>(
      begin: 1.0,
      end: 0.95,
    ).animate(CurvedAnimation(
      parent: _controller,
      curve: Curves.easeInOut,
    ));
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTapDown: (_) => _controller.forward(),
      onTapUp: (_) {
        _controller.reverse();
        widget.onTap();
      },
      onTapCancel: () => _controller.reverse(),
      child: AnimatedBuilder(
        animation: _scaleAnimation,
        builder: (context, child) {
          return Transform.scale(
            scale: _scaleAnimation.value,
            child: ConversationCard(conversation: widget.conversation),
          );
        },
      ),
    );
  }
}
```

---

# Testing

## Widget Tests

```dart
// test/features/conversations/presentation/widgets/conversation_card_test.dart
void main() {
  group('ConversationCard', () {
    testWidgets('displays conversation title', (WidgetTester tester) async {
      final conversation = Conversation(
        id: '1',
        title: 'Test Conversation',
        createdAt: DateTime.now(),
        updatedAt: DateTime.now(),
        isActive: true,
      );

      await tester.pumpWidget(
        MaterialApp(
          home: ConversationCard(conversation: conversation),
        ),
      );

      expect(find.text('Test Conversation'), findsOneWidget);
    });

    testWidgets('calls onTap when tapped', (WidgetTester tester) async {
      bool wasTapped = false;
      final conversation = Conversation(
        id: '1',
        title: 'Test Conversation',
        createdAt: DateTime.now(),
        updatedAt: DateTime.now(),
        isActive: true,
      );

      await tester.pumpWidget(
        MaterialApp(
          home: ConversationCard(
            conversation: conversation,
            onTap: () => wasTapped = true,
          ),
        ),
      );

      await tester.tap(find.byType(ConversationCard));
      expect(wasTapped, isTrue);
    });
  });
}
```

---

# Success Criteria

## Must-Have Features

- [ ] **Conversation Management** - CRUD operations for conversations
- [ ] **Folder Organization** - Hierarchical folder structure
- [ ] **Search & Filter** - Real-time search functionality
- [ ] **Responsive Design** - Works on all screen sizes
- [ ] **Offline Support** - Local storage and sync
- [ ] **Authentication** - Login/logout functionality
- [ ] **Smooth Animations** - Delightful user interactions
- [ ] **Error Handling** - Graceful error states

---

# Bonus Challenges

## Advanced Features

- [ ] **Real-time Updates** - WebSocket integration
- [ ] **Push Notifications** - Browser notifications
- [ ] **PWA Features** - Installable web app
- [ ] **Dark Mode** - Theme switching
- [ ] **Keyboard Shortcuts** - Power user features
- [ ] **Bulk Operations** - Multi-select actions
- [ ] **Export/Import** - Data portability
- [ ] **Voice Search** - Speech-to-text

---

# Getting Started

## Setup Instructions

1. **Install Flutter** - Get Flutter SDK and enable web support
2. **Create new project** - `flutter create fastopp_web`
3. **Add dependencies** - Add required packages to pubspec.yaml
4. **Set up project structure** - Create the folder structure above
5. **Start with models** - Define your data models
6. **Build the UI** - Create your first screens
7. **Add state management** - Implement Riverpod providers
8. **Integrate with API** - Connect to FastOpp backend

---

# Dependencies

## pubspec.yaml

```yaml
dependencies:
  flutter:
    sdk: flutter
  cupertino_icons: ^1.0.2
  
  # State Management
  flutter_riverpod: ^2.4.9
  
  # HTTP Client
  dio: ^5.3.2
  
  # Local Storage
  shared_preferences: ^2.2.2
  hive: ^2.2.3
  hive_flutter: ^1.1.0
  
  # UI
  material_design_icons_flutter: ^7.0.7296
  
  # Utils
  intl: ^0.18.1
  uuid: ^4.2.1

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.0
  hive_generator: ^2.0.1
  build_runner: ^2.4.7
```

---

# Resources

## Helpful Links

- **Flutter Documentation** - https://flutter.dev/docs
- **Riverpod** - https://riverpod.dev/
- **Material Design 3** - https://m3.material.io/
- **Flutter Web** - https://flutter.dev/web
- **Dio HTTP** - https://pub.dev/packages/dio
- **Hive Database** - https://pub.dev/packages/hive

---

# Let's Build!

## Ready to Start?

**This assignment will teach you:**
- Flutter web development
- Cross-platform UI design
- State management with Riverpod
- Offline-first architecture
- Material Design 3 principles
- Performance optimization

**Start with the basic app structure and build up from there!**

---

# Next Steps

## After Completing This Assignment

1. **Deploy your app** - Use Firebase Hosting or similar
2. **Test on different devices** - Ensure cross-platform compatibility
3. **Share your code** - Create a GitHub repository
4. **Document your approach** - Write a comprehensive README
5. **Move to the next track** - Try Vue.js or mobile development next!

**Happy coding! 🚀**
