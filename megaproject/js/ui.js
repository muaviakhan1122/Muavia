console.log("✅ ui.js loaded");
class OrionUI {
  constructor(app) {
    this.app = app;
    this.initUI();
  }

  initUI() {
    this.container = document.getElementById('app-container');
    this.renderMainInterface();
    this.bindEvents();
    this.renderSettingsPanel();
  }
  
  renderMainInterface() {
    this.container.innerHTML = `
      <div class="header">
        <h1>Orion AI Assistant</h1>
        <div class="version">v${this.app.state.currentVersion}</div>
      </div>
      <div class="chat-container">
        <div class="conversation"></div>
        <div class="input-area">
          <input type="text" class="user-input" placeholder="Ask me anything...">
          <button class="send-button">Send</button>
        </div>
      </div>
      <div class="update-notification hidden"></div>
      <div id="suggestions-panel" class="hidden"></div>
    `;
  }
  // Inside OrionUI class, in the initUI() method, after rendering the main interface
  renderSettingsPanel() {
  const settingsHtml = `
    <div class="settings-panel">
      <h3>Orion Settings</h3>
      <div>
        <label for="auto-update">Auto-Update: </label>
        <input type="checkbox" id="auto-update" ${this.app.memory.get('autoSchedulerEnabled') ? 'checked' : ''}>
      </div>
      <div>
        <label for="update-interval">Update Interval: </label>
        <input type="number" id="update-interval" value="${this.app.memory.get('schedulerIntervalMinutes') || 5}" min="1" max="60">
      </div>
      <div>
        <label for="debug-mode">Debug Mode: </label>
        <input type="checkbox" id="debug-mode" ${this.app.state.userPreferences.debugMode ? 'checked' : ''}>
      </div>
      <button class="save-settings">Save Settings</button>
    </div>
  `;
  
  const settingsContainer = document.createElement('div');
  settingsContainer.innerHTML = settingsHtml;
  this.container.appendChild(settingsContainer);

  // Event bindings for settings
  this.container.querySelector('.save-settings').addEventListener('click', () => this.saveSettings());
}

saveSettings() {
  const autoUpdate = this.container.querySelector('#auto-update').checked;
  const interval = this.container.querySelector('#update-interval').value;
  const debugMode = this.container.querySelector('#debug-mode').checked;

  // Save to memory
  this.app.memory.set('autoSchedulerEnabled', autoUpdate);
  this.app.memory.set('schedulerIntervalMinutes', interval);
  this.app.state.userPreferences.debugMode = debugMode;
  
  // Optionally restart the scheduler if enabled
  if (autoUpdate) {
    this.app.scheduler.start();
  } else {
    this.app.scheduler.stop();
  }
  
  console.log("Settings saved:", { autoUpdate, interval, debugMode });
}

  bindEvents() {
    const sendBtn = this.container.querySelector('.send-button');
    const input = this.container.querySelector('.user-input');
    
    sendBtn.addEventListener('click', () => this.sendMessage(input.value));
    input.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') this.sendMessage(input.value);
    });
  }

  sendMessage(message) {
    if (!message.trim()) return;
    
    const convo = this.container.querySelector('.conversation');
    convo.innerHTML += `<div class="message user">👤 ${message}</div>`;
    
    // Reset input field
    this.container.querySelector('.user-input').value = "";

    // Fake AI reply
    setTimeout(() => {
      convo.innerHTML += `<div class="message ai">🤖 Processing your request...</div>`;
    }, 600);
  }

  showFeatureSuggestions(features) {
    const panel = document.getElementById('suggestions-panel');
    panel.classList.remove('hidden');
    panel.innerHTML = features.map(feat => {
      const previewUrl = feat.html_url || feat.url || feat.repoUrl || '#';
      
      return `
        <div class="feature-card">
          <h3>${feat.name.replace(/-/g, ' ')} ★${(feat.stars || 0).toLocaleString()}</h3>
          <p class="description">${feat.description}</p>
          <div class="meta">
            <span>Updated: ${new Date(feat.updated_at).toLocaleDateString()}</span>
            <span>Language: ${feat.language || 'N/A'}</span>
          </div>
          <button class="preview-btn" data-url="${previewUrl}">Preview</button>
          <button class="request-btn" data-name="${feat.name}">Request Integration</button>
        </div>
      `;
    }).join('');
    
    panel.querySelectorAll('.preview-btn').forEach(btn => {
      btn.addEventListener('click', () => this.previewFeature(btn.dataset.url));
    });
  
    panel.querySelectorAll('.request-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        alert(`🔧 Request to integrate "${btn.dataset.name}" received.`);
      });
    });
  }
  
  // previewFeature(url) {
  //   const modal = document.createElement('div');
  //   modal.className = 'feature-modal';
  //   modal.innerHTML = `
  //     <div class="modal-content">
  //       <h3>Feature Preview</h3>
  //       <iframe src="${url}" class="repo-preview"></iframe>
  //       <button class="close-modal">Close</button>
  //     </div>
  //   `;
    
  //   document.body.appendChild(modal);
    
  //   modal.querySelector('.close-modal').addEventListener('click', () => modal.remove());
  // }
  previewFeature(url) {
    // Opens the link in a new tab instead of an iframe
    window.open(url, '_blank');
  }
  
  showUpdatePrompt(updateInfo) {
    const notification = document.querySelector('.update-notification');
    notification.classList.remove('hidden');
    notification.innerHTML = `
      <div class="update-alert">
        <p><strong>🚀 Proposed Update:</strong> v${updateInfo.version}</p>
        <p><strong>Changes:</strong></p>
        <ul>${updateInfo.changes.map(change => `<li>🛠️ ${change}</li>`).join('')}</ul>
        <button class="approve-update">Approve</button>
        <button class="reject-update">Reject</button>
      </div>
    `;
  
    notification.querySelector('.approve-update').addEventListener('click', () => {
      console.log(`✅ Update v${updateInfo.version} approved!`);
      Orion.version.createVersion({ description: updateInfo.changes.join(', ') });
      notification.classList.add('hidden');
    });
  
    notification.querySelector('.reject-update').addEventListener('click', () => {
      console.warn(`❌ Update v${updateInfo.version} rejected.`);
      notification.classList.add('hidden');
    });
  }
   
}
