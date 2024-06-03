<template>
  <div class="flex space-x-12">
    <div class="w-1/2">
      <h2 class="font-bold pb-6">Sent Emails</h2>
      <div v-if="sentEmails.length">
        <div
          v-for="userEmail in sentEmails"
          :key="userEmail.id"
          class="email-post space-y-2"
        >
          <h1>
            <span class="font-bold">Title: </span>{{ userEmail.email.title }}
          </h1>
          <h1>
            <span class="font-bold">Subject: </span
            >{{ userEmail.email.subject }}
          </h1>
          <div>
            <p>Sent on: {{ formatDate(userEmail.sent_date) }}</p>
          </div>
        </div>
      </div>
      <div v-else>
        <p>No sent emails available.</p>
      </div>
    </div>

    <div class="w-1/2">
      <h2 class="font-bold pb-6">Scheduled Emails</h2>
      <div v-if="scheduledEmails.length">
        <div
          v-for="userEmail in scheduledEmails"
          :key="userEmail.id"
          class="email-post space-y-2"
        >
          <h1>
            <span class="font-bold">Title: </span>{{ userEmail.email.title }}
          </h1>
          <h1>
            <span class="font-bold">Subject: </span
            >{{ userEmail.email.subject }}
          </h1>
          <div>
            <p>Scheduled for: {{ formatDate(userEmail.scheduled_date) }}</p>
          </div>
          <button
            @click="deleteScheduledEmail(userEmail.id)"
            class="text-white bg-gradient-to-r from-red-400 via-red-500 to-red-600 hover:bg-gradient-to-br focus:ring-4 focus:outline-none focus:ring-red-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center mb-2"
          >
            Delete
          </button>
        </div>
      </div>
      <div v-else>
        <p>No scheduled emails available.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { ref, watch } from "vue";
  import { useEmailStore } from "@/store/email";

  const store = useEmailStore();
  const scheduledEmails = ref([]);
  const sentEmails = ref([]);

  /**
   * Watch for changes in the store's usersEmails and update local references for scheduled and sent emails.
   * This function is called immediately and whenever the store's usersEmails changes.
   */
  watch(
    () => store.usersEmails,
    async (newValue) => {
      if (!newValue.length) await store.fetchUsersEmails();
      scheduledEmails.value = store.scheduledEmails;
      sentEmails.value = store.sentEmails;
    },
    { immediate: true }
  );

  /**
   * Delete a scheduled email.
   * This function is called when the user clicks the "Delete" button for a scheduled email.
   *
   * @param {number} userEmailId - The ID of the scheduled email to delete.
   */
  const deleteScheduledEmail = async (userEmailId) => {
    if (confirm("Are you sure you want to delete this scheduled email?")) {
      await store.deleteScheduledEmail(userEmailId);
    }
  };

  /**
   * Format a date string into a more readable format.
   * This function is called to format the sent_date and scheduled_date.
   *
   * @param {string} dateString - The date string to format.
   * @returns {string} - The formatted date string.
   */
  const formatDate = (dateString) => {
    const options = { year: "numeric", month: "long", day: "numeric" };
    return new Date(dateString).toLocaleDateString(undefined, options);
  };
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
</style>
