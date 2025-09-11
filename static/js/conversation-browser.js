// Global function to handle conversation moves from Sortable.js
function handleConversationMove(evt) {
    const conversationElement = evt.item;
    const conversationId = conversationElement.getAttribute('data-conversation-id');
    const targetElement = evt.to;
    
    if (!conversationId) {
        console.error('No conversation ID found on moved element');
        return;
    }
    
    // Determine the target folder ID
    let targetFolderId = null;
    
    if (targetElement.id === 'root-conversations') {
        // Moving to root
        targetFolderId = null;
    } else if (targetElement.id.startsWith('folder-')) {
        // Moving to a specific folder
        targetFolderId = targetElement.id.replace('folder-', '');
    }
    
    console.log('Moving conversation', conversationId, 'to folder', targetFolderId);
    
    // Get the Alpine.js component instance and call moveConversation
    const alpineComponent = Alpine.$data(conversationElement.closest('[x-data]'));
    if (alpineComponent && alpineComponent.moveConversation) {
        alpineComponent.moveConversation(conversationId, targetFolderId);
    } else {
        console.error('Could not find Alpine.js component or moveConversation method');
    }
}

// Alpine.js Data Function for Conversation Browser
function conversationBrowser() {
    return {
        loading: true,
        error: null,
        folders: [],
        rootConversations: [],
        clients: [],
        projects: [],
        users: [],
        contentTemplates: [],
        statusCounts: {
            draft: 0,
            review: 0,
            approved: 0,
            rejected: 0,
            published: 0
        },
        statusFilter: '',
        showCreateFolderModal: false,
        showEditFolderModal: false,
        showCreateClientModal: false,
        showCreateProjectModal: false,
        showContentTemplatesModal: false,
        showStatusUpdateModal: false,
        showContentStatusModal: false,
        editingContentStatus: {
            id: null,
            conversation_id: null,
            project_id: '',
            status: 'draft',
            content_type: 'blog_post',
            assigned_to: '',
            review_notes: '',
            due_date: '',
            published_at: ''
        },
        filters: {
            clientId: '',
            projectId: '',
            contentType: '',
            status: '',
            startDate: '',
            endDate: ''
        },
        newFolder: {
            name: '',
            description: '',
            project_id: ''
        },
        editingFolder: {
            id: null,
            name: '',
            description: '',
            project_id: ''
        },
        newClient: {
            name: '',
            company: '',
            email: '',
            phone: '',
            industry: '',
            notes: ''
        },
        newProject: {
            client_id: '',
            name: '',
            description: '',
            project_type: 'content_creation',
            start_date: '',
            end_date: '',
            budget: ''
        },
        statusUpdate: {
            conversation_id: null,
            project_id: null,
            status: 'draft',
            content_type: '',
            review_notes: '',
            assigned_to: ''
        },
        expandedFolders: {},
        searchResults: [],

        // Computed properties for organizing folders
        get projectsWithFolders() {
            const projectFolders = {};
            
            // Group folders by project
            this.folders.forEach(folder => {
                if (folder.project_id) {
                    if (!projectFolders[folder.project_id]) {
                        projectFolders[folder.project_id] = [];
                    }
                    projectFolders[folder.project_id].push(folder);
                }
            });
            
            // Convert to array with project info
            return Object.keys(projectFolders).map(projectId => {
                const project = this.projects.find(p => p.id === projectId);
                return {
                    id: projectId,
                    name: project ? project.name : 'Unknown Project',
                    folders: projectFolders[projectId]
                };
            });
        },

        get generalFolders() {
            return this.folders.filter(folder => !folder.project_id);
        },

        // Folder management methods
        toggleFolder(folderId) {
            this.expandedFolders[folderId] = !this.expandedFolders[folderId];
        },

        async init() {
            console.log('Alpine.js init() called');
            
            // Initialize modal states
            this.showCreateClientModal = false;
            this.showCreateProjectModal = false;
            console.log('Modal states initialized:', {
                showCreateClientModal: this.showCreateClientModal,
                showCreateProjectModal: this.showCreateProjectModal
            });
            
            await this.loadData();
        },

        async loadData() {
            try {
                this.loading = true;
                this.error = null;
                
                // Load all data in parallel
                await Promise.all([
                    this.loadFolders(),
                    this.loadMarketingData()
                ]);
                
                this.loading = false;
            } catch (error) {
                console.error('Error loading data:', error);
                this.error = 'Failed to load data';
                this.loading = false;
            }
        },

        async loadFolders() {
            try {
                const response = await fetch('/api/folders/hierarchy');
                if (response.ok) {
                    const data = await response.json();
                    this.folders = data.folders || [];
                    this.rootConversations = data.root_conversations || [];
                    console.log('Loaded folders:', this.folders.length);
                    console.log('Loaded root conversations:', this.rootConversations.length);
                    console.log('Sample conversation data:', this.rootConversations[0]);
                }
            } catch (error) {
                console.error('Error loading folders:', error);
            }
        },

        async loadConversations() {
            try {
                // Build query parameters for filtering
                const params = new URLSearchParams();
                
                if (this.filters.clientId) {
                    params.append('client_id', this.filters.clientId);
                }
                if (this.filters.projectId) {
                    params.append('project_id', this.filters.projectId);
                }
                if (this.filters.contentType) {
                    params.append('content_type', this.filters.contentType);
                }
                if (this.filters.status) {
                    params.append('status', this.filters.status);
                }
                if (this.filters.startDate) {
                    params.append('start_date', this.filters.startDate);
                }
                if (this.filters.endDate) {
                    params.append('end_date', this.filters.endDate);
                }
                
                // Use the search API to get conversations with all the metadata
                const response = await fetch(`/api/search/conversations?${params.toString()}`);
                if (response.ok) {
                    const conversations = await response.json();
                    
                    // Map the search results to our conversation format
                    this.rootConversations = conversations.map(conv => ({
                        id: conv.id,
                        title: conv.title,
                        created_at: conv.created_at,
                        updated_at: conv.updated_at,
                        message_count: conv.message_count || 0, // Use actual message count from API
                        client_id: conv.client_id,
                        client_name: conv.client_name,
                        project_id: conv.project_id,
                        project_name: conv.project_name,
                        content_type: conv.content_type,
                        status: conv.status,
                        folder_name: conv.folder_name
                    }));
                    
                    console.log('Loaded conversations:', this.rootConversations.length);
                    console.log('Conversation statuses:', this.rootConversations.map(c => ({ title: c.title, status: c.status })));
                } else {
                    console.error('Failed to load conversations');
                }
            } catch (error) {
                console.error('Error loading conversations:', error);
            }
        },

        async applyConversationFilters() {
            console.log('Applying conversation filters:', this.filters);
            await this.loadConversations();
        },

        clearConversationFilters() {
            this.filters = {
                clientId: '',
                projectId: '',
                contentType: '',
                status: '',
                startDate: '',
                endDate: ''
            };
            this.loadConversations();
        },

        async loadMarketingData() {
            try {
                // Load clients
                const clientsResponse = await fetch('/api/clients');
                if (clientsResponse.ok) {
                    this.clients = await clientsResponse.json();
                }

                // Load projects
                const projectsResponse = await fetch('/api/projects');
                if (projectsResponse.ok) {
                    this.projects = await projectsResponse.json();
                }

                // Load content templates
                const templatesResponse = await fetch('/api/content-templates');
                if (templatesResponse.ok) {
                    this.contentTemplates = await templatesResponse.json();
                }

                // Load users
                const usersResponse = await fetch('/api/users');
                if (usersResponse.ok) {
                    this.users = await usersResponse.json();
                }

                // Load status counts
                await this.loadStatusCounts();
            } catch (error) {
                console.error('Error loading marketing data:', error);
            }
        },

        async loadStatusCounts() {
            try {
                const statusResponse = await fetch('/api/content-status/summary');
                if (statusResponse.ok) {
                    this.statusCounts = await statusResponse.json();
                    console.log('Status counts updated:', this.statusCounts);
                    console.log('Review count:', this.statusCounts.review);
                }
            } catch (error) {
                console.error('Error loading status counts:', error);
            }
        },

        async createClient() {
            try {
                const response = await fetch('/api/clients', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(this.newClient)
                });
                
                if (response.ok) {
                    this.showCreateClientModal = false;
                    this.newClient = { name: '', company: '', email: '', phone: '', industry: '', notes: '' };
                    // Just refresh the clients list instead of all marketing data
                    const clientsResponse = await fetch('/api/clients');
                    if (clientsResponse.ok) {
                        this.clients = await clientsResponse.json();
                    }
                } else {
                    const errorData = await response.json();
                    console.error('Client creation failed:', response.status, errorData);
                    this.error = `Failed to create client: ${errorData.detail || 'Unknown error'}`;
                }
            } catch (error) {
                this.error = 'Failed to create client';
                console.error('Error creating client:', error);
            }
        },

        async createProject() {
            try {
                console.log('Creating project with data:', this.newProject);
                console.log('Available clients:', this.clients);
                console.log('Selected client_id:', this.newProject.client_id);
                console.log('Client_id type:', typeof this.newProject.client_id);
                
                // Prepare project data, converting empty strings to null for optional fields
                const projectData = {
                    client_id: this.newProject.client_id,
                    name: this.newProject.name,
                    description: this.newProject.description || null,
                    project_type: this.newProject.project_type,
                    start_date: this.newProject.start_date || null,
                    end_date: this.newProject.end_date || null,
                    budget: this.newProject.budget ? parseFloat(this.newProject.budget) : null
                };
                
                console.log('Sending project data:', projectData);
                
                const response = await fetch('/api/projects', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(projectData)
                });
                
                if (response.ok) {
                    this.showCreateProjectModal = false;
                    this.newProject = { client_id: '', name: '', description: '', project_type: 'content_creation', start_date: '', end_date: '', budget: '' };
                    // Just refresh the projects list instead of all marketing data
                    const projectsResponse = await fetch('/api/projects');
                    if (projectsResponse.ok) {
                        this.projects = await projectsResponse.json();
                    }
                } else {
                    const errorData = await response.json();
                    console.error('Project creation failed:', response.status, errorData);
                    console.error('Error details:', errorData.detail);
                    this.error = `Failed to create project: ${errorData.detail || 'Unknown error'}`;
                }
            } catch (error) {
                this.error = 'Failed to create project';
                console.error('Error creating project:', error);
            }
        },

        viewConversation(conversationId) {
            // Redirect to the main chat page with the conversation ID
            console.log('Viewing conversation with ID:', conversationId);
            console.log('Redirecting to:', `/?conversation_id=${conversationId}`);
            window.location.href = `/?conversation_id=${conversationId}`;
        },

        updateContentStatus(conversationId) {
            this.statusUpdate.conversation_id = conversationId;
            this.showStatusUpdateModal = true;
        },

        async deleteConversation(conversationId) {
            if (!confirm('Are you sure you want to delete this conversation? This action cannot be undone.')) {
                return;
            }
            
            try {
                const response = await fetch(`/api/conversations/${conversationId}`, {
                    method: 'DELETE'
                });
                
                if (response.ok) {
                    // Remove from local arrays
                    this.rootConversations = this.rootConversations.filter(c => c.id !== conversationId);
                    // Also remove from folder conversations
                    this.folders.forEach(folder => {
                        if (folder.conversations) {
                            folder.conversations = folder.conversations.filter(c => c.id !== conversationId);
                        }
                    });
                    console.log('Conversation deleted successfully');
                } else {
                    const errorData = await response.json();
                    console.error('Failed to delete conversation:', errorData);
                    this.error = `Failed to delete conversation: ${errorData.detail || 'Unknown error'}`;
                }
            } catch (error) {
                console.error('Error deleting conversation:', error);
                this.error = 'Failed to delete conversation';
            }
        },

        editFolder(folder) {
            this.editingFolder = {
                id: folder.id,
                name: folder.name,
                description: folder.description || '',
                project_id: folder.project_id || ''
            };
            this.showEditFolderModal = true;
        },

        editContentStatus(conversation) {
            console.log('Editing content status for conversation:', conversation);
            // Get existing content status for this conversation
            const existingStatus = conversation.content_status || {};
            console.log('Existing content status:', existingStatus);
            
            this.editingContentStatus = {
                id: existingStatus.id || null,
                conversation_id: conversation.id,
                project_id: existingStatus.project_id || conversation.project_id || '',
                status: existingStatus.status || conversation.status || 'draft',
                content_type: existingStatus.content_type || conversation.content_type || 'blog_post',
                assigned_to: existingStatus.assigned_to || '',
                review_notes: existingStatus.review_notes || '',
                due_date: existingStatus.due_date ? new Date(existingStatus.due_date).toISOString().slice(0, 16) : '',
                published_at: existingStatus.published_at || ''
            };
            console.log('Editing content status data:', this.editingContentStatus);
            this.showContentStatusModal = true;
        },

        async updateContentStatus() {
            try {
                const statusData = {
                    conversation_id: this.editingContentStatus.conversation_id,
                    project_id: this.editingContentStatus.project_id || null,
                    status: this.editingContentStatus.status,
                    content_type: this.editingContentStatus.content_type,
                    assigned_to: this.editingContentStatus.assigned_to || null,
                    review_notes: this.editingContentStatus.review_notes || null,
                    due_date: this.editingContentStatus.due_date ? new Date(this.editingContentStatus.due_date).toISOString() : null,
                    published_at: this.editingContentStatus.published_at ? new Date(this.editingContentStatus.published_at).toISOString() : null
                };

                let response;
                if (this.editingContentStatus.id) {
                    // Update existing content status
                    response = await fetch(`/api/content-status/${this.editingContentStatus.id}`, {
                        method: 'PUT',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(statusData)
                    });
                } else {
                    // Create new content status
                    response = await fetch('/api/content-status', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(statusData)
                    });
                }

                if (!response.ok) {
                    throw new Error('Failed to update content status');
                }

                console.log('Content status updated successfully');
                this.showContentStatusModal = false;
                this.editingContentStatus = {
                    id: null,
                    conversation_id: null,
                    project_id: '',
                    status: 'draft',
                    content_type: 'blog_post',
                    assigned_to: '',
                    review_notes: '',
                    due_date: '',
                    published_at: ''
                };
                
                // Refresh status counts and conversation data
                await Promise.all([
                    this.loadStatusCounts(),
                    this.loadFolders(),
                    this.loadConversations()
                ]);
            } catch (error) {
                this.error = 'Failed to update content status';
                console.error('Error updating content status:', error);
            }
        },

        getStatusClass(status) {
            const statusClasses = {
                'draft': 'status-draft',
                'review': 'status-review',
                'approved': 'status-approved',
                'rejected': 'status-rejected',
                'published': 'status-published'
            };
            return statusClasses[status] || 'status-draft';
        },

        filterByStatus(status) {
            console.log('Filtering by status:', status);
            this.filters.status = status;
            this.applyConversationFilters();
        },

        clearStatusFilter() {
            console.log('Clearing status filter');
            this.filters.status = '';
            this.applyConversationFilters();
        },

        hasActiveFilters() {
            return this.filters.clientId || 
                   this.filters.projectId || 
                   this.filters.contentType || 
                   this.filters.status || 
                   this.filters.startDate || 
                   this.filters.endDate;
        },

        getFilteredConversationCount() {
            return this.rootConversations.length;
        },

        getConversationFilterLabel(key, value) {
            if (!value) return '';
            
            const labels = {
                'clientId': 'Client',
                'projectId': 'Project', 
                'contentType': 'Type',
                'status': 'Status',
                'startDate': 'From',
                'endDate': 'To'
            };
            
            const label = labels[key] || key;
            
            // Try to find the display name for the value
            if (key === 'clientId') {
                const client = this.clients.find(c => c.id === value);
                return `${label}: ${client ? client.name : value}`;
            } else if (key === 'projectId') {
                const project = this.projects.find(p => p.id === value);
                return `${label}: ${project ? project.name : value}`;
            } else {
                return `${label}: ${value}`;
            }
        },

        hasActiveFilters() {
            return !!(this.filters.clientId || this.filters.projectId || this.filters.contentType || 
                     this.filters.status || this.filters.startDate || this.filters.endDate);
        },

        getFilteredConversationCount() {
            // If we have search results, use that count
            if (this.searchResults && this.searchResults.length > 0) {
                return this.searchResults.length;
            }
            
            // If filters are applied, only count rootConversations (which are filtered)
            if (this.hasActiveFilters()) {
                return this.rootConversations ? this.rootConversations.length : 0;
            }
            
            // Otherwise, count all conversations from root and folders
            let count = this.rootConversations ? this.rootConversations.length : 0;
            this.folders.forEach(folder => {
                count += folder.conversations ? folder.conversations.length : 0;
            });
            return count;
        },

        getFilterLabel(key, value) {
            if (!value) return '';
            
            const labels = {
                clientId: () => {
                    const client = this.clients.find(c => c.id === value);
                    return `Client: ${client ? client.name : value}`;
                },
                projectId: () => {
                    const project = this.projects.find(p => p.id === value);
                    return `Project: ${project ? project.name : value}`;
                },
                contentType: () => `Type: ${value.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}`,
                status: () => `Status: ${value.charAt(0).toUpperCase() + value.slice(1)}`,
                startDate: () => `From: ${value}`,
                endDate: () => `To: ${value}`
            };
            return labels[key] ? labels[key]() : `${key}: ${value}`;
        },

        async moveConversation(conversationId, folderId) {
            try {
                const response = await fetch(`/api/conversations/${conversationId}/move`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ folder_id: folderId })
                });
                
                if (response.ok) {
                    // Reload the data to reflect the changes
                    await this.loadFolders();
                    console.log('Conversation moved successfully');
                } else {
                    const errorData = await response.json();
                    console.error('Failed to move conversation:', errorData);
                    this.error = `Failed to move conversation: ${errorData.error || 'Unknown error'}`;
                }
            } catch (error) {
                console.error('Error moving conversation:', error);
                this.error = 'Failed to move conversation';
            }
        },

        async createFolder() {
            try {
                const response = await fetch('/api/folders', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(this.newFolder)
                });
                
                if (!response.ok) {
                    throw new Error('Failed to create folder');
                }
                
                this.showCreateFolderModal = false;
                this.newFolder = { name: '', description: '', project_id: '' };
                await this.loadData();
            } catch (error) {
                this.error = 'Failed to create folder';
                console.error('Error creating folder:', error);
            }
        },

        async updateFolder() {
            try {
                const response = await fetch(`/api/folders/${this.editingFolder.id}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        name: this.editingFolder.name,
                        description: this.editingFolder.description,
                        project_id: this.editingFolder.project_id
                    })
                });
                
                if (!response.ok) {
                    throw new Error('Failed to update folder');
                }
                
                this.showEditFolderModal = false;
                this.editingFolder = { id: null, name: '', description: '', project_id: '' };
                await this.loadData();
            } catch (error) {
                this.error = 'Failed to update folder';
                console.error('Error updating folder:', error);
            }
        },

        async deleteFolder(folderId) {
            if (!confirm('Are you sure you want to delete this folder? This action cannot be undone.')) {
                return;
            }
            
            try {
                const response = await fetch(`/api/folders/${folderId}`, {
                    method: 'DELETE'
                });
                
                if (response.ok) {
                    await this.loadData();
                    console.log('Folder deleted successfully');
                } else {
                    const errorData = await response.json();
                    console.error('Failed to delete folder:', errorData);
                    this.error = `Failed to delete folder: ${errorData.detail || 'Unknown error'}`;
                }
            } catch (error) {
                console.error('Error deleting folder:', error);
                this.error = 'Failed to delete folder';
            }
        },

        openLearningGoals() {
            // Open learning goals in a popup window
            const popup = window.open(
                '/conversation-learning-goals',
                'learning-goals',
                'width=1200,height=800,scrollbars=yes,resizable=yes,menubar=no,toolbar=no,location=no,status=no'
            );
            
            // Focus the popup window
            if (popup) {
                popup.focus();
            }
        }
    }
}
