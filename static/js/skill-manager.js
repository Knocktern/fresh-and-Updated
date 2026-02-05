// Skill Management Component
class SkillManager {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        this.selectedSkills = new Set(options.selectedSkills || []);
        this.onSkillChange = options.onSkillChange || (() => {});
        this.hiddenInputName = options.hiddenInputName || 'skills';
        this.allowAddNew = options.allowAddNew !== false; // Default to true
        this.searchEndpoint = '/api/skills/search';
        this.createEndpoint = '/api/skills/create';
        this.categoriesEndpoint = '/api/skills/categories';
        
        this.init();
    }

    async init() {
        await this.createUI();
        this.attachEventListeners();
        this.updateHiddenInputs();
    }

    async createUI() {
        const categories = await this.fetchCategories();
        
        this.container.innerHTML = `
            <div class="skill-manager">
                <!-- Search and Add Section -->
                <div class="mb-6 bg-gray-50 rounded-xl p-4 border border-gray-200">
                    <div class="flex flex-col md:flex-row gap-4">
                        <div class="flex-1">
                            <label class="block text-sm font-semibold text-gray-700 mb-2">Search Skills</label>
                            <div class="relative">
                                <input type="text" 
                                       id="skill-search" 
                                       placeholder="Search skills by name, category, or description..."
                                       class="w-full p-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500">
                                <div class="absolute inset-y-0 right-0 flex items-center pr-3">
                                    <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                                    </svg>
                                </div>
                            </div>
                            <!-- Search Results -->
                            <div id="search-results" class="mt-2 bg-white border border-gray-200 rounded-lg shadow-lg hidden max-h-60 overflow-y-auto">
                            </div>
                        </div>
                        
                        ${this.allowAddNew ? `
                        <div class="md:w-72">
                            <label class="block text-sm font-semibold text-gray-700 mb-2">Add New Skill</label>
                            <button type="button" 
                                    id="add-skill-btn" 
                                    class="w-full p-3 bg-gradient-to-r from-green-500 to-emerald-600 text-white font-semibold rounded-lg hover:opacity-90 transition flex items-center justify-center space-x-2">
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
                                </svg>
                                <span>Add Custom Skill</span>
                            </button>
                        </div>
                        ` : ''}
                    </div>
                </div>

                <!-- Selected Skills Display -->
                <div id="selected-skills" class="mb-6">
                    <h3 class="text-sm font-semibold text-gray-700 mb-3 flex items-center">
                        <svg class="w-4 h-4 mr-2 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                        </svg>
                        Selected Skills (<span id="selected-count">0</span>)
                    </h3>
                    <div id="selected-skills-list" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-2">
                        <!-- Selected skills will appear here -->
                    </div>
                    <div id="no-skills-message" class="text-gray-500 text-sm italic">No skills selected yet</div>
                </div>

                <!-- Category-based Skill Browser -->
                <div class="space-y-4">
                    <h3 class="text-sm font-semibold text-gray-700 mb-3 flex items-center">
                        <svg class="w-4 h-4 mr-2 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"></path>
                        </svg>
                        Browse by Category
                    </h3>
                    <div id="category-browser">
                        <!-- Categories will be loaded here -->
                    </div>
                </div>

                <!-- Hidden inputs for form submission -->
                <div id="hidden-inputs"></div>
            </div>

            <!-- Add Skill Modal -->
            ${this.allowAddNew ? `
            <div id="add-skill-modal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 hidden">
                <div class="bg-white rounded-2xl p-6 w-full max-w-md mx-4 max-h-screen overflow-y-auto">
                    <div class="flex justify-between items-center mb-4">
                        <h3 class="text-lg font-bold text-gray-900">Add New Skill</h3>
                        <button id="close-modal" class="text-gray-400 hover:text-gray-600">
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                            </svg>
                        </button>
                    </div>
                    
                    <form id="add-skill-form" class="space-y-4">
                        <div>
                            <label class="block text-sm font-semibold text-gray-700 mb-2">Skill Name *</label>
                            <input type="text" 
                                   id="new-skill-name" 
                                   placeholder="e.g. Quantum Computing"
                                   class="w-full p-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                                   required>
                        </div>
                        
                        <div>
                            <label class="block text-sm font-semibold text-gray-700 mb-2">Category *</label>
                            <select id="new-skill-category" 
                                    class="w-full p-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                                    required>
                                <option value="">Select or type new category</option>
                                ${categories.map(cat => `<option value="${cat}">${cat}</option>`).join('')}
                            </select>
                            <input type="text" 
                                   id="new-skill-category-custom" 
                                   placeholder="Or enter new category"
                                   class="w-full p-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 mt-2 hidden">
                        </div>
                        
                        <div>
                            <label class="block text-sm font-semibold text-gray-700 mb-2">Description</label>
                            <textarea id="new-skill-description" 
                                     placeholder="Brief description of the skill..."
                                     rows="3"
                                     class="w-full p-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"></textarea>
                        </div>
                        
                        <div class="flex justify-end space-x-3 pt-4">
                            <button type="button" 
                                    id="cancel-add-skill" 
                                    class="px-4 py-2 border border-gray-200 text-gray-700 rounded-lg hover:bg-gray-50">
                                Cancel
                            </button>
                            <button type="submit" 
                                    class="px-4 py-2 bg-gradient-to-r from-green-500 to-emerald-600 text-white rounded-lg hover:opacity-90 flex items-center space-x-2">
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
                                </svg>
                                <span>Add Skill</span>
                            </button>
                        </div>
                    </form>
                </div>
            </div>
            ` : ''}
        `;
    }

    attachEventListeners() {
        // Search functionality
        const searchInput = document.getElementById('skill-search');
        const searchResults = document.getElementById('search-results');
        let searchTimeout;

        searchInput.addEventListener('input', (e) => {
            clearTimeout(searchTimeout);
            const query = e.target.value.trim();
            
            if (query.length < 2) {
                searchResults.classList.add('hidden');
                return;
            }

            searchTimeout = setTimeout(() => this.performSearch(query), 300);
        });

        // Click outside to close search results
        document.addEventListener('click', (e) => {
            if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
                searchResults.classList.add('hidden');
            }
        });

        // Add skill modal functionality
        if (this.allowAddNew) {
            const addSkillBtn = document.getElementById('add-skill-btn');
            const modal = document.getElementById('add-skill-modal');
            const closeModal = document.getElementById('close-modal');
            const cancelBtn = document.getElementById('cancel-add-skill');
            const form = document.getElementById('add-skill-form');
            const categorySelect = document.getElementById('new-skill-category');
            const categoryCustom = document.getElementById('new-skill-category-custom');

            addSkillBtn.addEventListener('click', () => modal.classList.remove('hidden'));
            closeModal.addEventListener('click', () => modal.classList.add('hidden'));
            cancelBtn.addEventListener('click', () => modal.classList.add('hidden'));

            // Custom category handling
            categorySelect.addEventListener('change', (e) => {
                if (e.target.value === '') {
                    categoryCustom.classList.remove('hidden');
                    categoryCustom.required = true;
                } else {
                    categoryCustom.classList.add('hidden');
                    categoryCustom.required = false;
                }
            });

            form.addEventListener('submit', (e) => this.handleAddSkill(e));
        }

        this.loadCategorizedSkills();
    }

    async performSearch(query) {
        try {
            const response = await fetch(`${this.searchEndpoint}?q=${encodeURIComponent(query)}&limit=10`);
            const skills = await response.json();
            
            const searchResults = document.getElementById('search-results');
            
            if (skills.length === 0) {
                searchResults.innerHTML = `
                    <div class="p-3 text-gray-500 text-sm text-center">
                        No skills found matching "${query}"
                    </div>
                `;
            } else {
                searchResults.innerHTML = skills.map(skill => `
                    <div class="p-3 border-b border-gray-100 hover:bg-gray-50 cursor-pointer skill-search-item" 
                         data-skill-id="${skill.id}"
                         data-skill-name="${skill.skill_name}"
                         data-skill-category="${skill.category}">
                        <div class="flex items-center justify-between">
                            <div>
                                <div class="font-medium text-gray-900">${skill.skill_name}</div>
                                <div class="text-sm text-gray-500">${skill.category}</div>
                            </div>
                            <div class="text-xs ${this.selectedSkills.has(skill.id) ? 'text-green-600' : 'text-indigo-600'}">
                                ${this.selectedSkills.has(skill.id) ? 'Selected' : 'Click to add'}
                            </div>
                        </div>
                    </div>
                `).join('');

                // Add click handlers for search results
                searchResults.querySelectorAll('.skill-search-item').forEach(item => {
                    item.addEventListener('click', () => {
                        const skillId = parseInt(item.dataset.skillId);
                        const skillName = item.dataset.skillName;
                        const skillCategory = item.dataset.skillCategory;
                        
                        this.toggleSkill(skillId, skillName, skillCategory);
                        this.performSearch(document.getElementById('skill-search').value); // Refresh results
                    });
                });
            }
            
            searchResults.classList.remove('hidden');
        } catch (error) {
            console.error('Search failed:', error);
        }
    }

    async handleAddSkill(e) {
        e.preventDefault();
        
        const skillName = document.getElementById('new-skill-name').value.trim();
        const categorySelect = document.getElementById('new-skill-category');
        const categoryCustom = document.getElementById('new-skill-category-custom');
        const description = document.getElementById('new-skill-description').value.trim();
        
        const category = categorySelect.value || categoryCustom.value.trim();
        
        if (!skillName || !category) {
            alert('Please fill in all required fields');
            return;
        }

        try {
            const response = await fetch(this.createEndpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    skill_name: skillName,
                    category: category,
                    description: description
                })
            });

            const result = await response.json();

            if (response.status === 201) {
                // Success - new skill created
                alert(result.message);
                this.addSkill(result.skill.id, result.skill.skill_name, result.skill.category);
                document.getElementById('add-skill-modal').classList.add('hidden');
                document.getElementById('add-skill-form').reset();
                categoryCustom.classList.add('hidden');
                
                // Refresh the category browser to show the new skill
                await this.loadCategorizedSkills();
            } else if (response.status === 409) {
                // Skill already exists
                alert(`Skill "${skillName}" already exists. Adding it to your selection.`);
                this.addSkill(result.skill.id, result.skill.skill_name, result.skill.category);
                document.getElementById('add-skill-modal').classList.add('hidden');
                document.getElementById('add-skill-form').reset();
                categoryCustom.classList.add('hidden');
            } else {
                alert(result.error || 'Failed to create skill');
            }
        } catch (error) {
            console.error('Failed to create skill:', error);
            alert('Failed to create skill. Please try again.');
        }
    }

    async fetchCategories() {
        try {
            const response = await fetch(this.categoriesEndpoint);
            return await response.json();
        } catch (error) {
            console.error('Failed to fetch categories:', error);
            return [];
        }
    }

    async loadCategorizedSkills() {
        try {
            const response = await fetch(`${this.searchEndpoint}?limit=1000`);
            const skills = await response.json();
            
            // Group skills by category
            const skillsByCategory = skills.reduce((acc, skill) => {
                const category = skill.category || 'Other';
                if (!acc[category]) acc[category] = [];
                acc[category].push(skill);
                return acc;
            }, {});

            const categoryBrowser = document.getElementById('category-browser');
            categoryBrowser.innerHTML = Object.entries(skillsByCategory)
                .map(([category, skills]) => `
                    <div class="border border-gray-200 rounded-lg mb-4">
                        <button type="button" 
                                class="w-full p-4 text-left font-semibold text-gray-700 hover:bg-gray-50 flex items-center justify-between category-toggle"
                                data-category="${category}">
                            <span class="flex items-center">
                                <svg class="w-4 h-4 mr-2 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"></path>
                                </svg>
                                ${category}
                                <span class="ml-2 text-xs font-normal text-gray-500">(${skills.length} skills)</span>
                            </span>
                            <svg class="w-5 h-5 text-gray-400 category-chevron transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                            </svg>
                        </button>
                        <div class="category-skills p-4 border-t border-gray-200 hidden">
                            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                                ${skills.map(skill => `
                                    <label class="relative cursor-pointer skill-checkbox-item" data-skill-id="${skill.id}">
                                        <input type="checkbox" 
                                               class="sr-only peer skill-checkbox" 
                                               data-skill-id="${skill.id}"
                                               data-skill-name="${skill.skill_name}"
                                               data-skill-category="${skill.category}"
                                               ${this.selectedSkills.has(skill.id) ? 'checked' : ''}>
                                        <div class="p-3 border-2 rounded-xl peer-checked:border-purple-600 peer-checked:bg-purple-50 transition hover:border-gray-300 hover:bg-gray-50 ${this.selectedSkills.has(skill.id) ? 'border-purple-600 bg-purple-50' : 'border-gray-200'}">
                                            <div class="flex items-center justify-between">
                                                <span class="font-medium text-gray-700 text-sm">${skill.skill_name}</span>
                                                <svg class="w-5 h-5 text-purple-600 ${this.selectedSkills.has(skill.id) ? '' : 'hidden'} skill-check-icon" fill="currentColor" viewBox="0 0 20 20">
                                                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                                                </svg>
                                            </div>
                                        </div>
                                    </label>
                                `).join('')}
                            </div>
                        </div>
                    </div>
                `).join('');

            // Add event listeners for category toggles and skill checkboxes
            categoryBrowser.querySelectorAll('.category-toggle').forEach((toggle, index) => {
                toggle.addEventListener('click', () => {
                    const skillsContainer = toggle.nextElementSibling;
                    const chevron = toggle.querySelector('.category-chevron');
                    
                    skillsContainer.classList.toggle('hidden');
                    chevron.style.transform = skillsContainer.classList.contains('hidden') ? 'rotate(0deg)' : 'rotate(180deg)';
                });
                
                // Expand the first 3 categories by default
                if (index < 3) {
                    const skillsContainer = toggle.nextElementSibling;
                    const chevron = toggle.querySelector('.category-chevron');
                    skillsContainer.classList.remove('hidden');
                    chevron.style.transform = 'rotate(180deg)';
                }
            });

            categoryBrowser.querySelectorAll('.skill-checkbox').forEach(checkbox => {
                checkbox.addEventListener('change', (e) => {
                    const skillId = parseInt(e.target.dataset.skillId);
                    const skillName = e.target.dataset.skillName;
                    const skillCategory = e.target.dataset.skillCategory;
                    const checkIcon = e.target.closest('.skill-checkbox-item').querySelector('.skill-check-icon');
                    const skillDiv = e.target.nextElementSibling;
                    
                    if (e.target.checked) {
                        this.addSkill(skillId, skillName, skillCategory);
                        checkIcon.classList.remove('hidden');
                        skillDiv.classList.add('border-purple-600', 'bg-purple-50');
                        skillDiv.classList.remove('border-gray-200');
                    } else {
                        this.removeSkill(skillId);
                        checkIcon.classList.add('hidden');
                        skillDiv.classList.remove('border-purple-600', 'bg-purple-50');
                        skillDiv.classList.add('border-gray-200');
                    }
                });
            });

        } catch (error) {
            console.error('Failed to load categorized skills:', error);
        }
    }

    toggleSkill(skillId, skillName, skillCategory) {
        if (this.selectedSkills.has(skillId)) {
            this.removeSkill(skillId);
        } else {
            this.addSkill(skillId, skillName, skillCategory);
        }
    }

    addSkill(skillId, skillName, skillCategory) {
        this.selectedSkills.add(skillId);
        this.updateSelectedSkillsDisplay();
        this.updateHiddenInputs();
        this.updateCheckboxState(skillId, true);
        this.onSkillChange(Array.from(this.selectedSkills));
    }

    removeSkill(skillId) {
        this.selectedSkills.delete(skillId);
        this.updateSelectedSkillsDisplay();
        this.updateHiddenInputs();
        this.updateCheckboxState(skillId, false);
        this.onSkillChange(Array.from(this.selectedSkills));
    }

    updateCheckboxState(skillId, isSelected) {
        // Update checkbox in category browser if it exists
        const checkbox = document.querySelector(`.skill-checkbox[data-skill-id="${skillId}"]`);
        if (checkbox) {
            checkbox.checked = isSelected;
            
            const checkIcon = checkbox.closest('.skill-checkbox-item').querySelector('.skill-check-icon');
            const skillDiv = checkbox.nextElementSibling;
            
            if (isSelected) {
                checkIcon.classList.remove('hidden');
                skillDiv.classList.add('border-purple-600', 'bg-purple-50');
                skillDiv.classList.remove('border-gray-200');
            } else {
                checkIcon.classList.add('hidden');
                skillDiv.classList.remove('border-purple-600', 'bg-purple-50');
                skillDiv.classList.add('border-gray-200');
            }
        }
    }

    updateSelectedSkillsDisplay() {
        const selectedSkillsList = document.getElementById('selected-skills-list');
        const selectedCount = document.getElementById('selected-count');
        const noSkillsMessage = document.getElementById('no-skills-message');
        
        selectedCount.textContent = this.selectedSkills.size;
        
        if (this.selectedSkills.size === 0) {
            noSkillsMessage.classList.remove('hidden');
            selectedSkillsList.innerHTML = '';
        } else {
            noSkillsMessage.classList.add('hidden');
            // For now, just show skill IDs. In a real implementation, you'd fetch skill details
            this.fetchSelectedSkillDetails();
        }
    }

    async fetchSelectedSkillDetails() {
        if (this.selectedSkills.size === 0) return;
        
        try {
            const skillIds = Array.from(this.selectedSkills);
            const response = await fetch(`/api/skills/bulk?${skillIds.map(id => `ids=${id}`).join('&')}`);
            const skills = await response.json();
            
            const selectedSkillsList = document.getElementById('selected-skills-list');
            selectedSkillsList.innerHTML = skills.map(skill => `
                <div class="flex items-center justify-between p-3 bg-indigo-50 border border-indigo-200 rounded-lg">
                    <div>
                        <div class="font-medium text-indigo-900">${skill.skill_name}</div>
                        <div class="text-xs text-indigo-600">${skill.category}</div>
                    </div>
                    <button type="button" 
                            class="text-indigo-400 hover:text-indigo-600 remove-skill"
                            data-skill-id="${skill.id}">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                        </svg>
                    </button>
                </div>
            `).join('');
            
            // Add remove handlers
            selectedSkillsList.querySelectorAll('.remove-skill').forEach(btn => {
                btn.addEventListener('click', () => {
                    const skillId = parseInt(btn.dataset.skillId);
                    this.removeSkill(skillId);
                });
            });
            
        } catch (error) {
            console.error('Failed to fetch selected skill details:', error);
        }
    }

    updateHiddenInputs() {
        const hiddenInputsContainer = document.getElementById('hidden-inputs');
        hiddenInputsContainer.innerHTML = Array.from(this.selectedSkills).map(skillId => 
            `<input type="hidden" name="${this.hiddenInputName}" value="${skillId}">`
        ).join('');
    }

    // Public methods for external use
    getSelectedSkills() {
        return Array.from(this.selectedSkills);
    }

    setSelectedSkills(skillIds) {
        this.selectedSkills = new Set(skillIds);
        this.updateSelectedSkillsDisplay();
        this.updateHiddenInputs();
        
        // Update all checkboxes to reflect current state
        skillIds.forEach(skillId => this.updateCheckboxState(skillId, true));
        
        // Also uncheck any previously selected skills not in the new list
        document.querySelectorAll('.skill-checkbox').forEach(checkbox => {
            const skillId = parseInt(checkbox.dataset.skillId);
            if (!skillIds.includes(skillId) && checkbox.checked) {
                this.updateCheckboxState(skillId, false);
            }
        });
        
        this.onSkillChange(Array.from(this.selectedSkills));
    }

    clearAllSkills() {
        // Update all checkboxes to unchecked
        this.selectedSkills.forEach(skillId => {
            this.updateCheckboxState(skillId, false);
        });
        
        this.selectedSkills.clear();
        this.updateSelectedSkillsDisplay();
        this.updateHiddenInputs();
        this.onSkillChange([]);
    }
}