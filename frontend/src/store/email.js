// store/chat.js
import { defineStore } from 'pinia'
import { create_request, get_request, delete_request, update_request } from '@/store/services/request_http'

export const useEmailStore = defineStore('email', {
  state: () => ({
    emailFocus: null,
    isEditing: false,
    emails: [],
    usersEmails: []
  }),
  getters: {
    /**
     * Get scheduled emails (emails that are not yet sent).
     * 
     * @returns {Array} List of scheduled emails.
     */
    scheduledEmails: (state) => {
      return state.usersEmails.filter(userEmail => !userEmail.sent)
    },
    /**
     * Get sent emails (emails that are already sent).
     * 
     * @returns {Array} List of sent emails.
     */
    sentEmails: (state) => {
      return state.usersEmails.filter(userEmail => userEmail.sent)
    }
  },
  actions: {
    /**
     * Fetch all emails from the backend.
     * 
     * @returns {Promise<void>}
     */
    async fetchEmails() {
      try {
        const response = await get_request('emails/')
        this.emails = response
      } catch (error) {
        console.error('Failed to fetch emails:', error)
      }
    },
    /**
     * Fetch all user emails (sent and scheduled) from the backend.
     * 
     * @returns {Promise<void>}
     */
    async fetchUsersEmails() {
      try {
        const response = await get_request('users_emails/')
        this.usersEmails = response
      } catch (error) {
        console.error('Failed to fetch user emails:', error)
      }
    },
    /**
     * Create a new email.
     * 
     * @param {FormData} formData - The form data containing email details.
     * @returns {Promise<void>}
     */
    async createEmail(formData) {
      try {
        const response = await create_request('emails/', formData)
        this.emailFocus = response
      } catch (error) {
        console.error('Failed to create email:', error)
      }
    },
    /**
     * Update an existing email.
     * 
     * @param {number} id - The ID of the email to update.
     * @param {FormData} formData - The form data containing updated email details.
     * @returns {Promise<Object>} The updated email object.
     */
    async updateEmail(id, formData) {
      try {
        const response = await update_request(`emails/update/${id}/`, formData)
        this.emailFocus = response
        return response
      } catch (error) {
        console.error('Failed to update email:', error)
      }
    },
    /**
     * Delete an email.
     * 
     * @param {number} email_id - The ID of the email to delete.
     * @returns {Promise<void>}
     */
    async deleteEmail(email_id) {
      try {
        await delete_request(`emails/delete/${email_id}/`)
        this.emailFocus = ''
        this.emails = this.emails.filter(email => email.id !== email_id)
      } catch (error) {
        console.error('Failed to delete email:', error)
      }
    },
    /**
     * Send an email to selected users.
     * 
     * @param {number} emailId - The ID of the email to send.
     * @param {Array<number>} userIds - The IDs of the users to send the email to.
     * @returns {Promise<void>}
     */
    async sendEmailToUsers(emailId, userIds) {
      try {
        const response = await create_request('send_email_to_users/', {
          email_id: emailId,
          user_ids: userIds
        })
        console.log('Emails are being sent:', response)
        this.fetchUsersEmails()
      } catch (error) {
        console.error('Failed to send emails:', error)
      }
    },
    /**
     * Schedule an email to be sent at a later date.
     * 
     * @param {number} emailId - The ID of the email to schedule.
     * @param {Array<number>} userIds - The IDs of the users to send the email to.
     * @param {string} scheduledDate - The date when the email should be sent.
     * @returns {Promise<void>}
     */
    async scheduleEmail(emailId, userIds, scheduledDate) {
      try {
        const response = await create_request('schedule_email/', {
          email_id: emailId,
          user_ids: userIds,
          scheduled_date: scheduledDate
        })
        console.log('Email scheduled:', response)
        this.fetchUsersEmails()
      } catch (error) {
        console.error('Failed to schedule email:', error)
      }
    },
    /**
     * Delete a scheduled email.
     * 
     * @param {number} userEmailId - The ID of the scheduled email to delete.
     * @returns {Promise<void>}
     */
    async deleteScheduledEmail(userEmailId) {
      try {
        await delete_request(`delete_scheduled_email/${userEmailId}/`)
        this.usersEmails = this.usersEmails.filter(userEmail => userEmail.id !== userEmailId)
      } catch (error) {
        console.error('Failed to delete scheduled email:', error)
      }
    }
  },
})
