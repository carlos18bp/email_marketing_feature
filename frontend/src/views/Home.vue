<template>
  <div class="flex space-x-24 m-4">
    <div class="w-2/5 space-y-8">
      <EmailEditor :action="action" />
      <ScheduledEmails />
    </div>
    <div class="w-3/5">
      <div v-show="!store.emailFocus">
        <EmailList @select-email="showEmail" @edit-email="editEmail" />
      </div>
      <div v-if="store.emailFocus">
        <Email @back-to-list="showEmailList" @edit-email="editEmail" />
      </div>
    </div>
  </div>
</template>

<script setup>
  import { ref } from 'vue'
  import EmailEditor from '@/components/EmailEditor.vue'
  import EmailList from '@/components/EmailList.vue'
  import Email from '@/components/Email.vue'
  import ScheduledEmails from '@/components/ScheduledEmails.vue'
  import { useEmailStore } from '@/store/email'

  const store = useEmailStore()

  const action = ref('create')

  /**
   * Show the email details and switch action to 'update'.
   * This function is called when an email is selected from the email list.
   */
  const showEmail = () => {
    action.value = 'update'
  }

  /**
   * Set the store's isEditing state to true and switch action to 'update'.
   * This function is called when the edit email button is clicked.
   */
  const editEmail = () => {
    store.isEditing = true
    action.value = 'update'
  }

  /**
   * Show the email list and reset the action to 'create'.
   * This function is called when the back to list button is clicked.
   */
  const showEmailList = () => {
    store.emailFocus = null
    action.value = 'create'
  }
</script>

<style scoped>
</style>
