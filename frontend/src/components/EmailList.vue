<template>
  <div class="flex space-x-12">
    <div class="w-1/2">
      <div v-if="store.emails.length">
        <h1 class="font-bold pb-6">Email Posts</h1>
        <div v-for="email in store.emails" :key="email.id" class="email-post space-y-2">
          <div class="flex justify-between">
            <button
              @click="selectEmail(email)"
              class="pr-24 text-blue-600 hover:text-blue-800 focus:outline-none">
              <span class="font-bold">Title: </span>{{ email.title }}
            </button>
          </div>
          <h1><span class="font-bold">Subject: </span>{{ email.subject }}</h1>
          <div>
            <p>Published on: {{ formatDate(email.created_at) }}</p>
            <p>Last updated on: {{ formatDate(email.updated_at) }}</p>
          </div>
          <div class="space-x-2">
            <button
              @click="sendEmail(email)"
              :disabled="!userStore.userChecked.length"
              :class="['text-white bg-gradient-to-r from-purple-500 via-purple-600 to-purple-700 hover:bg-gradient-to-br focus:ring-4 focus:outline-none focus:ring-purple-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center mb-2', { 'opacity-50 cursor-not-allowed': !userStore.userChecked.length }]"
            >
              Send Email
            </button>
            <button
              @click="showScheduleEmailModal(email)"
              :disabled="!userStore.userChecked.length"
              :class="['text-white bg-gradient-to-r from-green-500 via-green-600 to-green-700 hover:bg-gradient-to-br focus:ring-4 focus:outline-none focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center mb-2', { 'opacity-50 cursor-not-allowed': !userStore.userChecked.length }]"
            >
              Schedule Email
            </button>
            <button
              v-if="!store.isEditing"
              @click="editEmail(email)"
              type="button"
              class="text-white bg-gradient-to-r from-cyan-400 via-cyan-500 to-cyan-600 hover:bg-gradient-to-br focus:ring-4 focus:outline-none focus:ring-cyan-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center mb-2"
            >
              Edit email
            </button>
            <button
              @click="deleteEmail(email.id)"
              type="button"
              class="text-white bg-gradient-to-r from-red-400 via-red-500 to-red-600 hover:bg-gradient-to-br focus:ring-4 focus:outline-none focus:ring-red-300 shadow-lg shadow-red-500/50 font-medium rounded-lg text-sm px-5 py-2.5 text-center mb-2"
            >
              Delete
            </button>
          </div>
        </div>
      </div>
      <div v-else>
        <p>No email posts available.</p>
      </div>
    </div>

    <div class="w-1/2">
      <h2 class="font-bold">Users</h2>
      <div v-if="userStore.users.length">
        <div>
          <input type="checkbox" @change="selectAllUsers($event)" /> Select All
        </div>
        <div v-for="user in userStore.users" :key="user.id" class="user-item space-y-2 space-x-2">
          <input type="checkbox" :value="user.id" v-model="userStore.userChecked" />
          <span>{{ user.first_name }} {{ user.last_name }} (<span class="font-bold">{{ user.email }}</span>)</span>
        </div>
      </div>
      <div v-else>
        <p>No users available.</p>
      </div>
    </div>

    <!-- Modal to schedule email -->
    <div v-if="showScheduleEmail" class="modal fixed w-full h-full top-0 left-0 flex items-center justify-center">
      <div class="modal-overlay absolute w-full h-full bg-gray-900 opacity-50"></div>
      <div class="modal-container bg-white w-1/3 mx-auto rounded shadow-lg z-50 overflow-y-auto">
        <div class="modal-content py-4 text-left px-6">
          <div class="flex justify-between items-center pb-3">
            <p class="text-2xl font-bold">Schedule Email</p>
            <div class="modal-close cursor-pointer z-50" @click="closeScheduleEmailModal">✕</div>
          </div>
          <div>
            <label for="scheduledDate" class="block font-bold mb-2">Schedule Date:</label>
            <input type="date" v-model="scheduledDate" class="w-full p-2 border border-gray-300 rounded" />
          </div>
          <div class="flex justify-end pt-4">
            <button 
              @click="scheduleEmail" 
              class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
              Schedule
            </button>
            <button 
              @click="closeScheduleEmailModal" 
              class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded ml-2">
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { ref } from 'vue'
  import { watchEffect } from 'vue'
  import { useEmailStore } from '@/store/email'
  import { useUserStore } from '@/store/user'

  const store = useEmailStore()
  const userStore = useUserStore()
  const emit = defineEmits(['select-email'])

  const showScheduleEmail = ref(false)
  const scheduledDate = ref('')
  const selectedEmail = ref(null)

  // Fetch emails and users when the component is mounted
  watchEffect(async () => {
    await store.fetchEmails()
    await userStore.fetchUsers()
  })

  /**
   * Select an email to view or edit.
   * This function is called when the user clicks on an email title.
   *
   * @param {Object} email - The email object to select.
   */
  const selectEmail = (email) => {
    store.emailFocus = email
    emit('select-email')
  }

  /**
   * Send an email to selected users.
   * This function is called when the user clicks the "Send Email" button.
   *
   * @param {Object} email - The email object to send.
   */
  const sendEmail = async (email) => {
    if (userStore.userChecked.length) {
      await store.sendEmailToUsers(email.id, userStore.userChecked)
      alert('Emails are being sent');
    }
  }

  /**
   * Show the modal to schedule an email.
   * This function is called when the user clicks the "Schedule Email" button.
   *
   * @param {Object} email - The email object to schedule.
   */
  const showScheduleEmailModal = (email) => {
    selectedEmail.value = email
    showScheduleEmail.value = true
  }

  /**
   * Close the modal to schedule an email.
   * This function is called when the user clicks the "Cancel" button in the modal.
   */
  const closeScheduleEmailModal = () => {
    showScheduleEmail.value = false
    scheduledDate.value = ''
  }

  /**
   * Schedule an email to be sent at a later date.
   * This function is called when the user clicks the "Schedule" button in the modal.
   */
  const scheduleEmail = async () => {
    if (userStore.userChecked.length && scheduledDate.value) {
      await store.scheduleEmail(selectedEmail.value.id, userStore.userChecked, scheduledDate.value)
      alert('Email scheduled')
      closeScheduleEmailModal()
    }
  }

  /**
   * Edit an email.
   * This function is called when the user clicks the "Edit Email" button.
   *
   * @param {Object} email - The email object to edit.
   */
  const editEmail = (email) => {
    store.emailFocus = email
    emit('edit-email')
  }

  /**
   * Delete an email.
   * This function is called when the user clicks the "Delete" button.
   *
   * @param {number} id - The ID of the email to delete.
   */
  const deleteEmail = async (id) => {
    if (confirm('Are you sure you want to delete this email?')) {
      await store.deleteEmail(id)
    }
  }

  /**
   * Format a date string into a more readable format.
   * This function is called to format the created_at and updated_at dates.
   *
   * @param {string} dateString - The date string to format.
   * @returns {string} - The formatted date string.
   */
  const formatDate = (dateString) => {
    const options = { year: 'numeric', month: 'long', day: 'numeric' }
    return new Date(dateString).toLocaleDateString(undefined, options)
  }

  /**
   * Select or deselect all users.
   * This function is called when the user clicks the "Select All" checkbox.
   *
   * @param {Event} event - The event object from the checkbox change.
   */
  const selectAllUsers = (event) => {
    if (event.target.checked) {
      userStore.userChecked = userStore.users.map(user => user.id)
    } else {
      userStore.userChecked = []
    }
  }
</script>

<style scoped>
  .email-post {
    margin-bottom: 2rem;
    padding: 1rem;
    border: 1px solid #ddd;
    border-radius: 5px;
  }

  .email-post h2 {
    margin: 0;
    font-size: 1.5rem;
  }

  .email-post p {
    font-size: 0.9rem;
    color: #666;
  }

  .user-item {
    margin-bottom: 1rem;
    padding: 0.5rem;
    border: 1px solid #ddd;
    border-radius: 5px;
  }

  .modal {
    transition: opacity 0.25s ease;
  }
</style>
