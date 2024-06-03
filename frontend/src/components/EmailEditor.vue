<template>
  <div class="space-y-4">
    <h1 class="font-bold">Email Post Editor</h1>
    <div class="relative z-0">
        <input
          v-model="email.title"
          type="text" 
          id="floating_standard_title" 
          class="block py-2.5 px-0 w-full text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none focus:outline-none focus:ring-0 focus:border-blue-600 peer" 
          placeholder=" " />
        <label for="floating_standard_title" class="absolute text-sm text-gray-500 duration-300 transform -translate-y-6 scale-75 top-3 -z-10 origin-[0] peer-focus:start-0 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-6 rtl:peer-focus:translate-x-1/4 rtl:peer-focus:left-auto">
          Title
        </label>
    </div>
    <div class="relative z-0">
        <input
          v-model="email.subject"
          type="text" 
          id="floating_standard_subject" 
          class="block py-2.5 px-0 w-full text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none focus:outline-none focus:ring-0 focus:border-blue-600 peer" 
          placeholder=" " />
        <label for="floating_standard_subject" class="absolute text-sm text-gray-500 duration-300 transform -translate-y-6 scale-75 top-3 -z-10 origin-[0] peer-focus:start-0 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-6 rtl:peer-focus:translate-x-1/4 rtl:peer-focus:left-auto">
          Subject
        </label>
    </div>
    <div>
      <QuillEditor
        ref="quillEditor"
        v-model:content="email.content"
        contentType="html"
        :toolbar="toolbarOptions"
        :modules="modules"
        placeholder="Here you can write the content of your email and/or email"        
        @update:content="handleTextChange" />
    </div>
    <button
      @click="publishEmail"
      type="button" 
      class="text-white bg-gradient-to-r from-blue-500 via-blue-600 to-blue-700 hover:bg-gradient-to-br focus:ring-4 focus:outline-none focus:ring-blue-300 shadow-lg shadow-blue-500/50 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-2">
      <span v-if="props.action == 'create'">Create Email</span>
      <span v-else>Edit Email</span>
    </button>
  </div>
</template>

<script setup>
  import { onMounted, reactive, ref, watch } from 'vue';
  // QuillEditor component for rich text editing
  import { QuillEditor } from '@vueup/vue-quill';
  // Module to format images and other embeds in the Quill editor
  import BlotFormatter from 'quill-blot-formatter'; 
  // Module to handle image drag and drop/paste functionality
  import QuillImageDropAndPaste from 'quill-image-drop-and-paste';
  // Module to automatically link URLs in the Quill editor
  import MagicUrl from 'quill-magic-url';
  // Module to compress images before inserting them into the Quill editor
  import ImageCompress from 'quill-image-compress'; 
  import '@vueup/vue-quill/dist/vue-quill.snow.css';
  import { useEmailStore } from '@/store/email';

  const store = useEmailStore();

  const props = defineProps({
    action: String,
  });

  const email = reactive({
    id: '',
    title: '',
    subject: '',
    content: '',
    created_at: '',
    updated_at: ''
  });

  const quillEditor = ref(null);

  const toolbarOptions = [
    ['bold', 'italic', 'underline', 'strike'],
    ['link', 'image', 'video'],
    [{ 'header': 1 }, { 'header': 2 }],
    [{ 'list': 'ordered'}, { 'list': 'bullet' }, { 'list': 'check' }],
    [{ 'indent': '-1'}, { 'indent': '+1' }],
    [{ 'size': ['small', false, 'large', 'huge'] }],
    [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
    [{ 'color': [] }, { 'background': [] }],
    [{ 'font': [] }],
    [{ 'align': [] }],
    ['clean'],
  ];

  const modules = [
    {
      name: 'blotFormatter',
      module: BlotFormatter,
    },
    {
      name: 'imageDropAndPaste',
      module: QuillImageDropAndPaste,
      options: {
        handler: function (dataUrl, type, data) {}
      }
    },
    {
      name: 'magicUrl',
      module: MagicUrl,
      options: {}
    },
    {
      name: 'imageCompress',
      module: ImageCompress,
      options: {
        quality: 0.9,
        maxWidth: 1000,
        maxHeight: 1000,
        imageType: 'image/jpeg',
      }
    },
  ];

  /**
   * On component mount, populate email object with the focused email from the store.
   * This function is called when the component is mounted.
   */
  onMounted(() => {
    if (store.emailFocus) Object.assign(email, store.emailFocus)
  });

  /**
   * Watch for changes in the store's focused email and update the local email object accordingly.
   * This function is called whenever the emailFocus in the store changes.
   *
   * @param {Object} newValue - The new value of emailFocus from the store.
   */
  watch(() => store.emailFocus, (newValue) => {
    if (!newValue) reStartEditor()
  });

  /**
   * Watch for changes in the store's editing state and update the local email object accordingly.
   * This function is called whenever the isEditing in the store changes.
   *
   * @param {boolean} newValue - The new value of isEditing from the store.
   */
  watch(() => store.isEditing, (newValue) => {
    if (newValue) {
      Object.assign(email, store.emailFocus)
    }
  });

  /**
   * Publish the email after validating the fields.
   * This function is called when the user clicks the publish button.
   */
  const publishEmail = async () => {
    if (email.title.trim() === '') {
      alert('Title cannot be empty');
      return;
    }

    if (email.subject.trim() === '') {
      alert('Subject cannot be empty');
      return;
    }

    if (email.content === '') {
      alert('The editor content cannot be empty');
      return;
    }

    try {
      if (props.action == 'create') Object.assign(email, await store.createEmail(setFormData()))
      if (props.action == 'update') Object.assign(email, await store.updateEmail(email.id, setFormData()))

      reStartEditor() 
      await store.fetchEmails()

      alert('Email published successfully');  
      console.log('Email published')
    } catch (error) {
      console.error('Failed to publish email:', error)
    }
  }

  /**
   * Set form data for the email.
   * This function formats the form data before sending it to the backend.
   *
   * @returns {FormData} - The formatted form data.
   */
  const setFormData = () => {
    const formData = new FormData()
    formData.append('title', email.title)
    formData.append('subject', email.subject)
    formData.append('content', email.content)

    const currentDate = new Date();
    const formattedDate = currentDate.toISOString(); // Format 'YYYY-MM-DDTHH:MM:SS.mmmZ'
    formData.append('updated_at', formattedDate);

    return formData;
  };

  /**
   * Handle text changes in the Quill editor.
   * This function is called whenever the content in the editor changes.
   */
  const handleTextChange = () => {
    //console.log(content.value);
  };

  /**
   * Reset the editor to its initial state.
   * This function clears the email object and the Quill editor content.
   */
  const reStartEditor = () => {
    email.id = ''
    email.title = ''
    email.subject = ''
    email.content = ''
    email.created_at = ''
    email.updated_at = ''

    quillEditor.value.setContents([])
    store.isEditing = false
  };
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
