<template>
  <div class="email space-y-4">
    <h1><span class="font-bold">Title: </span>{{ email.title }}</h1>
    <h1><span class="font-bold">Subject: </span>{{ email.subject }}</h1>
    <h2><span class="font-bold">Content editor: </span></h2>
    <div v-html="email.content"></div>
    <p>Published on: {{ formatDate(email.created_at) }}</p>
    <button
      @click="$emit('back-to-list')"
      type="button"
      class="text-white bg-gradient-to-r from-cyan-400 via-green-500 to-green-600 hover:bg-gradient-to-br focus:ring-4 focus:outline-none focus:ring-green-300 shadow-lg shadow-green-500/50 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-2">
      Create new email
    </button>
    <button
      v-if="(!store.isEditing)"
      @click="$emit('edit-email')"
      type="button" 
      class="text-white bg-gradient-to-r from-cyan-400 via-cyan-500 to-cyan-600 hover:bg-gradient-to-br focus:ring-4 focus:outline-none focus:ring-cyan-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-2">
      Edit email
    </button>
    <button
      @click="deleteEmail(email.id)"
      type="button" 
      class="text-white bg-gradient-to-r from-red-400 via-red-500 to-red-600 hover:bg-gradient-to-br focus:ring-4 focus:outline-none focus:ring-red-300 shadow-lg shadow-red-500/50 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-2">
      Delete
    </button>
    <button
      @click="$emit('back-to-list')"
      type="button" 
      class="text-white bg-gradient-to-r from-pink-400 via-pink-500 to-pink-600 hover:bg-gradient-to-br focus:ring-4 focus:outline-none focus:ring-pink-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-2">
      Back to Email List
    </button>
  </div>
</template>

<script setup>
  import { onMounted, reactive, watch } from 'vue'
  import { useEmailStore } from '@/store/email'

  const store = useEmailStore()
  const email = reactive({})

  /**
   * On component mount, populate email object with the focused email from the store.
   * This function is called when the component is mounted.
   */
  onMounted(() => {
    Object.assign(email, store.emailFocus)
  })

  /**
   * Watch for changes in the store's focused email and update the local email object accordingly.
   * This function is called whenever the emailFocus in the store changes.
   *
   * @param {Object} newValue - The new value of emailFocus from the store.
   */
  watch(() => store.emailFocus, (newValue) => {
    Object.assign(email, newValue)
  })

  /**
   * Delete an email after confirming the action with the user.
   * This function is called when the user clicks the delete button.
   *
   * @param {number} id - The ID of the email to delete.
   */
  const deleteEmail = async (id) => {
    if (confirm('Are you sure you want to delete this email?')) {
      await store.deleteemail(id)
    }
  }

  /**
   * Format date strings into a more readable format.
   * This function converts a date string into a localized date string.
   *
   * @param {string} dateString - The date string to format.
   * @returns {string} - The formatted date string.
   */
  const formatDate = (dateString) => {
    const options = { year: 'numeric', month: 'long', day: 'numeric' }
    return new Date(dateString).toLocaleDateString(undefined, options)
  }
</script>
  
<style scoped>
  ::v-deep ol {
    list-style-type: decimal;
  }

  .email {
    padding: 2rem;
  }

  .email h1 {
    margin-bottom: 1rem;
  }

  .email p {
    font-size: 0.9rem;
    color: #666;
  }

  button {
    margin-top: 2rem;
    padding: 0.5rem 1rem;
    cursor: pointer;
  }
</style>
