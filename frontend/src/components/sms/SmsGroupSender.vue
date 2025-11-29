<template>
  <div class="container mt-4">
    <h3 class="mb-4 font-weight-bold">Church Communication Center</h3>
    
    <!-- Loading Overlay -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="spinner-border text-primary" role="status">
        <span class="sr-only">Loading...</span>
      </div>
      <p>{{ loadingMessage }}</p>
    </div>
    
    <ul class="nav nav-tabs mb-3" role="tablist">
      <li class="nav-item">
        <a class="nav-link" :class="{ active: activeTab === 'compose' }" @click="activeTab = 'compose'">Compose Message</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" :class="{ active: activeTab === 'recipients' }" @click="activeTab = 'recipients'">Select Recipients</a>
      </li>
    </ul>

    <div class="tab-content">
      <!-- Compose Message Tab -->
      <div class="tab-pane fade show" :class="{ 'active': activeTab === 'compose' }">
        <div class="card mb-3">
          <div class="card-body">
            <h5 class="card-title">Message Content</h5>
            <textarea 
              class="form-control mb-2" 
              rows="5" 
              v-model="message" 
              placeholder="Enter message..."
              :disabled="isLoading"
            ></textarea>
            <small class="text-muted">
              You can use placeholders like <code>[name]</code>, <code>[amount]</code>, <code>[date]</code>
            </small>
            <div class="mt-2">
              <small class="text-info">Characters: {{ message.length }}</small>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="card-body">
            <h5 class="card-title">App & Website Info</h5>
            <div class="form-group">
              <label for="app">App</label>
              <input 
                type="text" 
                class="form-control" 
                v-model="app" 
                placeholder="e.g., admin"
                :disabled="isLoading"
              />
            </div>
            <div class="form-group">
              <label>Send to Website?</label>
              <select v-model="website" class="form-control" :disabled="isLoading">
                <option :value="true">Yes</option>
                <option :value="false">No</option>
              </select>
            </div>
            <button 
              class="btn btn-success mt-3" 
              @click="sendSms"
              :disabled="isLoading || !canSendMessage"
            >
              <span v-if="isLoading" class="spinner-border spinner-border-sm mr-2"></span>
              Send SMS
            </button>
            <div v-if="!canSendMessage" class="mt-2">
              <small class="text-warning">Please enter a message and select recipients</small>
            </div>
          </div>
        </div>
      </div>

      <!-- Select Recipients Tab -->
      <div class="tab-pane fade show" :class="{ 'active': activeTab === 'recipients' }">
        <div class="card mb-3">
          <div class="card-body">
            <h5 class="card-title">Select Groups</h5>
            <div v-if="groupsLoading" class="text-center">
              <div class="spinner-border spinner-border-sm mr-2"></div>
              Loading groups...
            </div>
            <div v-else-if="groupsError" class="alert alert-danger">
              {{ groupsError }}
              <button class="btn btn-sm btn-outline-danger ml-2" @click="fetchGroups">Retry</button>
            </div>
            <div v-else-if="groups.length === 0" class="text-muted">
              No groups found
            </div>
            <div v-else>
              <div class="mb-2">
                <button class="btn btn-sm btn-outline-primary" @click="selectAllGroups">
                  {{ selectedGroupIds.length === groups.length ? 'Deselect All' : 'Select All' }}
                </button>
              </div>
              <div v-for="group in groups" :key="group.id" class="form-check">
                <input 
                  class="form-check-input" 
                  type="checkbox" 
                  :id="'group-' + group.id" 
                  :value="group.id" 
                  v-model="selectedGroupIds"
                  :disabled="isLoading"
                >
                <label class="form-check-label" :for="'group-' + group.id">
                  {{ group.name }}
                </label>
              </div>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="card-body">
            <h5 class="card-title">Select Members</h5>
            <div v-if="membersLoading" class="text-center">
              <div class="spinner-border spinner-border-sm mr-2"></div>
              Loading members...
            </div>
            <div v-else-if="membersError" class="alert alert-danger">
              {{ membersError }}
              <button class="btn btn-sm btn-outline-danger ml-2" @click="fetchMembers">Retry</button>
            </div>
            <div v-else-if="members.length === 0" class="text-muted">
              No members found
            </div>
            <div v-else>
              <div class="mb-2">
                <button class="btn btn-sm btn-outline-primary" @click="selectAllMembers">
                  {{ selectedMemberIds.length === members.length ? 'Deselect All' : 'Select All' }}
                </button>
                <span class="ml-2 badge badge-info">{{ selectedMemberIds.length }} selected</span>
              </div>
              <div class="member-list">
                <div v-for="member in members" :key="member.id" class="form-check">
                  <input 
                    class="form-check-input" 
                    type="checkbox" 
                    :id="'member-' + member.id" 
                    :value="member.id" 
                    v-model="selectedMemberIds"
                    :disabled="isLoading"
                  >
                  <label class="form-check-label" :for="'member-' + member.id">
                    {{ member.member.first_name }} {{ member.member.last_name }}
                    <span class="text-muted">({{ member.phone_number }})</span>
                  </label>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Success/Error Messages -->
    <div v-if="successMessage" class="alert alert-success mt-3">
      {{ successMessage }}
    </div>
    <div v-if="errorMessage" class="alert alert-danger mt-3">
      {{ errorMessage }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'SmsGroupSender',
  data() {
    return {
      activeTab: 'compose',
      app: 'admin',
      website: true,
      message: '',
      selectedGroupIds: [],
      selectedMemberIds: [],
      groups: [],
      members: [],
      sending_member_id: localStorage.getItem('user_id'),
      
      // Loading states
      isLoading: false,
      loadingMessage: '',
      groupsLoading: false,
      membersLoading: false,
      
      // Error states
      groupsError: null,
      membersError: null,
      errorMessage: null,
      successMessage: null,
    }
  },
  computed: {
    canSendMessage() {
      return this.message.trim() && 
             (this.selectedMemberIds.length > 0 || this.selectedGroupIds.length > 0);
    }
  },
  mounted() {
    this.fetchGroups();
    this.fetchMembers();
  },
  methods: {
    async fetchGroups() {
      this.groupsLoading = true;
      this.groupsError = null;
      
      try {
        const response = await this.$http.get(this.$BASE_URL + '/api/groups/church-group-list/');
        this.groups = response.data;
      } catch (error) {
        this.groupsError = 'Failed to fetch church groups. Please try again.';
        console.error('Error fetching groups:', error);
      } finally {
        this.groupsLoading = false;
      }
    },
    
    async fetchMembers() {
      this.membersLoading = true;
      this.membersError = null;
      
      try {
        const response = await this.$http.get(this.$BASE_URL + '/api/members/member-list/');
        this.members = response.data;
      } catch (error) {
        this.membersError = 'Failed to fetch members. Please try again.';
        console.error('Error fetching members:', error);
      } finally {
        this.membersLoading = false;
      }
    },
    
    async sendSms() {
      if (!this.canSendMessage) {
        this.errorMessage = 'Please enter a message and select recipients.';
        return;
      }
      
      this.isLoading = true;
      this.loadingMessage = 'Sending SMS...';
      this.errorMessage = null;
      this.successMessage = null;
      
      const payload = {
        sending_member_id: this.sending_member_id,
        app: this.app,
        message: this.message,
        website: this.website,
        recipient_member_ids: this.selectedMemberIds,
        recipient_group_ids: this.selectedGroupIds, // Add this if your backend supports groups
      };
      
      try {
        await this.$http.post(this.$BASE_URL + '/api/sms/add-custom-sms/', payload);
        this.successMessage = `SMS sent successfully to ${this.selectedMemberIds.length} members!`;
        this.resetForm();
      } catch (error) {
        this.errorMessage = 'Failed to send SMS. Please try again.';
        console.error('Error sending SMS:', error);
      } finally {
        this.isLoading = false;
        this.loadingMessage = '';
      }
    },
    
    resetForm() {
      this.message = '';
      this.selectedMemberIds = [];
      this.selectedGroupIds = [];
    },
    
    selectAllGroups() {
      if (this.selectedGroupIds.length === this.groups.length) {
        this.selectedGroupIds = [];
      } else {
        this.selectedGroupIds = this.groups.map(group => group.id);
      }
    },
    
    selectAllMembers() {
      if (this.selectedMemberIds.length === this.members.length) {
        this.selectedMemberIds = [];
      } else {
        this.selectedMemberIds = this.members.map(member => member.id);
      }
    },
    
    // Auto-clear messages after some time
    clearMessages() {
      setTimeout(() => {
        this.successMessage = null;
        this.errorMessage = null;
      }, 5000);
    }
  },
  
  watch: {
    successMessage(newVal) {
      if (newVal) this.clearMessages();
    },
    errorMessage(newVal) {
      if (newVal) this.clearMessages();
    }
  }
}
</script>

<style scoped>
.container {
  max-width: 600px;
}

.card {
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.nav-tabs .nav-link.active {
  font-weight: bold;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.9);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.member-list {
  max-height: 300px;
  overflow-y: auto;
}

.form-check {
  margin-bottom: 0.5rem;
}

.form-check-label {
  margin-left: 0.25rem;
}

.spinner-border-sm {
  width: 1rem;
  height: 1rem;
}
</style>