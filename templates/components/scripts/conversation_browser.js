// Alpine.js Data Function for Conversation Browser
function conversationBrowser() {
    return {
        loading: true,
        error: null,
        folders: [],
        rootConversations: [],
        clients: [],
        projects: [],
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
        searchQuery: '',
        searchResults: [],
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
            description: ''
        },
        editingFolder: {
            id: null,
            name: '',
            description: ''
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
                    this.loadConversations(),
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
                    this.folders = await response.json();
                }
            } catch (error) {
                console.error('Error loading folders:', error);
            }
        },

        async loadConversations() {
            try {
                const response = await fetch('/api/conversations');
                if (response.ok) {
                    this.rootConversations = await response.json();
                }
            } catch (error) {
                console.error('Error loading conversations:', error);
            }
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

                // Load status counts
                const statusResponse = await fetch('/api/content-status/summary');
                if (statusResponse.ok) {
                    this.statusCounts = await statusResponse.json();
                }
            } catch (error) {
                console.error('Error loading marketing data:', error);
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

        updateContentStatus(conversationId) {
            this.statusUpdate.conversation_id = conversationId;
            this.showStatusUpdateModal = true;
        },

        async searchConversations() {
            if (!this.searchQuery.trim()) {
                this.searchResults = [];
                return;
            }

            try {
                const response = await fetch(`/api/search/conversations?q=${encodeURIComponent(this.searchQuery)}`);
                if (response.ok) {
                    this.searchResults = await response.json();
                }
            } catch (error) {
                console.error('Search error:', error);
                this.searchResults = [];
            }
        },

        applyFilters() {
            // This would implement the advanced filtering logic
            console.log('Applying filters:', this.filters);
        },

        clearFilters() {
            this.filters = {
                clientId: '',
                projectId: '',
                contentType: '',
                status: '',
                startDate: '',
                endDate: ''
            };
            this.applyFilters();
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
        }
    }
}
