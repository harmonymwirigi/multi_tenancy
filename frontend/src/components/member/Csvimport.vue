<template>
  <div class="csv-import-container">
    <!-- Import CSV Button - Matches your existing UI -->
    <div class="import-action" @click="triggerFileUpload">
      <div class="import-icon">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
          <polyline points="14,2 14,8 20,8"/>
          <line x1="16" y1="13" x2="8" y2="13"/>
          <line x1="16" y1="17" x2="8" y2="17"/>
          <line x1="12" y1="9" x2="12" y2="13"/>
          <line x1="10" y1="11" x2="14" y2="11"/>
        </svg>
      </div>
      <p class="import-text">Import from CSV →</p>
    </div>

    <!-- Hidden File Input -->
    <input
      ref="csvFileInput"
      type="file"
      accept=".csv,.xlsx,.xls"
      @change="handleFileSelect"
      style="display: none;"
    />

    <!-- Upload Progress Modal -->
    <div v-if="showProgressModal" class="modal-overlay">
      <div class="modal-content">
        <div class="modal-header">
          <h3>{{ progressTitle }}</h3>
        </div>
        <div class="modal-body">
          <div class="progress-container">
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: uploadProgress + '%' }"></div>
            </div>
            <p class="progress-text">{{ progressMessage }}</p>
          </div>
          <div v-if="uploadProgress === 100 && !isProcessing" class="progress-actions">
            <button @click="closeProgressModal" class="btn btn-primary">Close</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Success Modal -->
    <div v-if="showSuccessModal" class="modal-overlay">
      <div class="modal-content success-modal">
        <div class="modal-header">
          <div class="success-icon">✓</div>
          <h3>Import Successful!</h3>
        </div>
        <div class="modal-body">
          <div class="import-summary">
            <p class="summary-main">{{ successMessage }}</p>
            <div v-if="importDetails && importDetails.length > 0" class="import-details">
              <h4>Import Details:</h4>
              <ul>
                <li v-for="(detail, index) in importDetails" :key="index">{{ detail }}</li>
              </ul>
            </div>
          </div>
          <div class="modal-actions">
            <button @click="closeSuccessModal" class="btn btn-primary">Close</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Error Modal -->
    <div v-if="showErrorModal" class="modal-overlay">
      <div class="modal-content error-modal">
        <div class="modal-header">
          <div class="error-icon">⚠</div>
          <h3>Import Failed</h3>
        </div>
        <div class="modal-body">
          <div class="error-summary">
            <p class="error-main">{{ errorMessage }}</p>
            <div v-if="errorDetails && errorDetails.length > 0" class="error-details">
              <h4>Error Details:</h4>
              <ul>
                <li v-for="(error, index) in errorDetails" :key="index">{{ error }}</li>
              </ul>
            </div>
          </div>
          <div class="modal-actions">
            <button @click="closeErrorModal" class="btn btn-secondary">Close</button>
            <button @click="retryImport" class="btn btn-primary">Try Again</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'CSVImport',
  data() {
    return {
      // File handling
      selectedFile: null,
      
      // Progress tracking
      showProgressModal: false,
      uploadProgress: 0,
      progressTitle: 'Importing Members',
      progressMessage: 'Preparing upload...',
      isProcessing: false,
      
      // Success handling
      showSuccessModal: false,
      successMessage: '',
      importDetails: [],
      
      // Error handling
      showErrorModal: false,
      errorMessage: '',
      errorDetails: [],
      
      // Configuration
      maxFileSize: 10 * 1024 * 1024, // 10MB
      allowedExtensions: ['.csv', '.xlsx', '.xls'],
      apiEndpoint: '/api/members/upload-csv/' // Change this to match your Django endpoint
    }
  },
  methods: {
    // Trigger file selection
    triggerFileUpload() {
      this.$refs.csvFileInput.click()
    },

    // Handle file selection
    handleFileSelect(event) {
      const file = event.target.files[0]
      
      if (!file) {
        return
      }

      // Validate file
      if (!this.validateFile(file)) {
        return
      }

      this.selectedFile = file
      this.startImport()
    },

    // Validate selected file
    validateFile(file) {
      // Check file extension
      const fileName = file.name.toLowerCase()
      const hasValidExtension = this.allowedExtensions.some(ext => fileName.endsWith(ext))
      
      if (!hasValidExtension) {
        this.showError(
          'Invalid file format',
          ['Please select a CSV or Excel file (.csv, .xlsx, .xls)']
        )
        return false
      }

      // Check file size
      if (file.size > this.maxFileSize) {
        const maxSizeMB = Math.round(this.maxFileSize / (1024 * 1024))
        this.showError(
          'File too large',
          [`File size must be less than ${maxSizeMB}MB`]
        )
        return false
      }

      return true
    },

    // Start the import process
    async startImport() {
      if (!this.selectedFile) return

      try {
        // Show progress modal
        this.showProgressModal = true
        this.uploadProgress = 0
        this.progressMessage = 'Preparing file for upload...'
        this.isProcessing = true

        // Create form data
        const formData = new FormData()
        formData.append('csv_file', this.selectedFile)
        formData.append('file_name', this.selectedFile.name)

        // Update progress
        this.updateProgress(10, 'Uploading file...')

        // Make API request
        const response = await axios.post(this.apiEndpoint, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
          onUploadProgress: (progressEvent) => {
            const percentCompleted = Math.round(
              (progressEvent.loaded * 70) / progressEvent.total
            )
            this.updateProgress(
              10 + percentCompleted,
              percentCompleted < 70 ? 'Uploading file...' : 'Processing members...'
            )
          }
        })

        // Handle successful response
        this.handleImportSuccess(response.data)

      } catch (error) {
        console.error('Import error:', error)
        this.handleImportError(error)
      } finally {
        // Reset file input
        this.$refs.csvFileInput.value = ''
        this.selectedFile = null
        this.isProcessing = false
      }
    },

    // Update progress
    updateProgress(progress, message) {
      this.uploadProgress = Math.min(progress, 100)
      this.progressMessage = message
    },

    // Handle successful import
    handleImportSuccess(data) {
      // Complete progress
      this.updateProgress(100, 'Import completed successfully!')
      
      setTimeout(() => {
        // Close progress modal
        this.showProgressModal = false
        
        // Extract data from response
        const importedCount = data.imported_count || data.success_count || 0
        const updatedCount = data.updated_count || 0
        const skippedCount = data.skipped_count || 0
        const totalProcessed = data.total_processed || importedCount + updatedCount + skippedCount

        // Prepare success message
        let message = `Successfully processed ${totalProcessed} records.`
        if (importedCount > 0) {
          message = `Successfully imported ${importedCount} members!`
        }

        // Prepare details
        const details = []
        if (importedCount > 0) details.push(`${importedCount} new members imported`)
        if (updatedCount > 0) details.push(`${updatedCount} existing members updated`)
        if (skippedCount > 0) details.push(`${skippedCount} records skipped`)
        
        // Add any additional details from backend
        if (data.details && Array.isArray(data.details)) {
          details.push(...data.details)
        }

        // Show success modal
        this.showSuccess(message, details)

        // Emit success event to parent component
        this.$emit('import-success', {
          imported_count: importedCount,
          updated_count: updatedCount,
          skipped_count: skippedCount,
          total_processed: totalProcessed,
          details: details
        })

        // Emit refresh event to reload member list
        this.$emit('refresh-members')
        
      }, 1000)
    },

    // Handle import error
    handleImportError(error) {
      // Close progress modal
      this.showProgressModal = false

      let message = 'An unexpected error occurred during import.'
      let details = []

      if (error.response) {
        // Server responded with error
        const errorData = error.response.data
        message = errorData.message || errorData.error || message
        
        if (errorData.details && Array.isArray(errorData.details)) {
          details = errorData.details
        } else if (errorData.errors && Array.isArray(errorData.errors)) {
          details = errorData.errors
        } else if (typeof errorData.details === 'string') {
          details = [errorData.details]
        }

        // Handle specific error cases
        if (error.response.status === 413) {
          message = 'File too large for server to process.'
        } else if (error.response.status === 400) {
          message = 'Invalid file format or missing required fields.'
        } else if (error.response.status === 500) {
          message = 'Server error occurred while processing the file.'
        }
      } else if (error.request) {
        // Network error
        message = 'Network error. Please check your connection and try again.'
      }

      this.showError(message, details)
    },

    // Show success modal
    showSuccess(message, details = []) {
      this.successMessage = message
      this.importDetails = details
      this.showSuccessModal = true
    },

    // Show error modal
    showError(message, details = []) {
      this.errorMessage = message
      this.errorDetails = details
      this.showErrorModal = true
    },

    // Close modals
    closeProgressModal() {
      this.showProgressModal = false
    },

    closeSuccessModal() {
      this.showSuccessModal = false
      this.successMessage = ''
      this.importDetails = []
    },

    closeErrorModal() {
      this.showErrorModal = false
      this.errorMessage = ''
      this.errorDetails = []
    },

    // Retry import
    retryImport() {
      this.closeErrorModal()
      this.triggerFileUpload()
    }
  }
}
</script>

<style scoped>
/* Import Action Button */
.csv-import-container {
  display: inline-block;
}

.import-action {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  border-radius: 8px;
  background: #fff;
  min-width: 120px;
}

.import-action:hover {
  background-color: #f8f9fa;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.import-icon {
  margin-bottom: 8px;
  color: #6c757d;
  transition: color 0.3s ease;
}

.import-action:hover .import-icon {
  color: #007bff;
}

.import-text {
  margin: 0;
  color: #007bff;
  font-size: 14px;
  font-weight: 500;
  text-decoration: none;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1050;
  backdrop-filter: blur(3px);
}

.modal-content {
  background: white;
  border-radius: 12px;
  max-width: 500px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  animation: modalFadeIn 0.3s ease;
}

@keyframes modalFadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-header {
  padding: 24px 24px 16px;
  border-bottom: 1px solid #e9ecef;
  text-align: center;
}

.modal-header h3 {
  margin: 8px 0 0;
  color: #343a40;
  font-size: 20px;
  font-weight: 600;
}

.modal-body {
  padding: 20px 24px 24px;
}

/* Progress Styles */
.progress-container {
  text-align: center;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background-color: #e9ecef;
  border-radius: 4px;
  overflow: hidden;
  margin: 16px 0;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #007bff, #0056b3);
  border-radius: 4px;
  transition: width 0.4s ease;
  position: relative;
}

.progress-fill::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  background-image: linear-gradient(
    -45deg,
    rgba(255, 255, 255, 0.2) 25%,
    transparent 25%,
    transparent 50%,
    rgba(255, 255, 255, 0.2) 50%,
    rgba(255, 255, 255, 0.2) 75%,
    transparent 75%,
    transparent
  );
  background-size: 20px 20px;
  animation: progressAnimation 1s linear infinite;
}

@keyframes progressAnimation {
  0% {
    background-position: 0 0;
  }
  100% {
    background-position: 20px 20px;
  }
}

.progress-text {
  margin: 16px 0 0;
  color: #6c757d;
  font-size: 14px;
}

.progress-actions {
  margin-top: 20px;
  text-align: center;
}

/* Success Modal */
.success-modal .modal-header {
  background: linear-gradient(135deg, #28a745, #20c997);
  color: white;
  border-radius: 12px 12px 0 0;
}

.success-icon {
  width: 48px;
  height: 48px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  font-size: 24px;
  font-weight: bold;
}

/* Error Modal */
.error-modal .modal-header {
  background: linear-gradient(135deg, #dc3545, #c82333);
  color: white;
  border-radius: 12px 12px 0 0;
}

.error-icon {
  width: 48px;
  height: 48px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  font-size: 24px;
  font-weight: bold;
}

/* Summary Sections */
.import-summary, .error-summary {
  text-align: center;
}

.summary-main, .error-main {
  font-size: 16px;
  font-weight: 500;
  color: #343a40;
  margin: 0 0 16px;
}

.import-details, .error-details {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 16px;
  margin-top: 16px;
  text-align: left;
}

.import-details h4, .error-details h4 {
  margin: 0 0 12px;
  color: #495057;
  font-size: 14px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.import-details ul, .error-details ul {
  margin: 0;
  padding: 0;
  list-style: none;
}

.import-details li, .error-details li {
  padding: 4px 0;
  color: #6c757d;
  font-size: 14px;
  position: relative;
  padding-left: 20px;
}

.import-details li::before {
  content: '✓';
  position: absolute;
  left: 0;
  color: #28a745;
  font-weight: bold;
}

.error-details li::before {
  content: '•';
  position: absolute;
  left: 0;
  color: #dc3545;
  font-weight: bold;
}

/* Buttons */
.modal-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
  margin-top: 24px;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 80px;
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn-primary:hover {
  background: #0056b3;
  transform: translateY(-1px);
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #545b62;
  transform: translateY(-1px);
}

/* Responsive Design */
@media (max-width: 768px) {
  .modal-content {
    width: 95%;
    margin: 20px;
  }
  
  .modal-header, .modal-body {
    padding: 16px 20px;
  }
  
  .modal-actions {
    flex-direction: column;
  }
  
  .btn {
    width: 100%;
  }
}
</style>