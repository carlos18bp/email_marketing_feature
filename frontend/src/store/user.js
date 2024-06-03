import { defineStore } from 'pinia'
import { get_request } from '@/store/services/request_http'

export const useUserStore = defineStore('user', {
  state: () => ({
    users: [],
    userChecked: []
  }),
  actions: {
    /**
     * Fetch all users from the backend.
     * 
     * This function sends a GET request to the backend to retrieve the list of users and updates
     * the `users` state with the response.
     * 
     * @returns {Promise<void>}
     */
    async fetchUsers() {
      try {
        const response = await get_request('users/')
        this.users = response
      } catch (error) {
        console.error('Failed to fetch users:', error)
      }
    }
  }
})
