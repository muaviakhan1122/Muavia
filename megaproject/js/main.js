console.log("✅ main.js loaded");
class OrionApp {
    constructor() {
        console.log("Initializing Orion AI Assistant");
        this.state = {
            currentVersion: '1.0.0',
            userPreferences: {},
            conversationHistory: []
        };
        this.init();
    }

    init() {
        this.memory   = new OrionMemory(this);   // 1) Create memory right away
        this.ui       = new OrionUI(this);       // 2) Then UI can safely call memory.get()
        this.ai       = new OrionAIService(this);
        this.version  = new VersionControl(this);
        this.update   = new UpdateSystem(this);
        this.scheduler= new OrionScheduler(this);
        
        this.loadState();
        this.startSchedulerIfNeeded();
        this.autoUpdater = new AutoUpdater(this); 
      }

    startSchedulerIfNeeded() {
        const autoStart = this.memory.get('autoSchedulerEnabled');
        if (autoStart) {
          this.scheduler.start();
        } else {
          console.log("🛌 Orion scheduler is disabled (manual start needed).");
        }
      }

    saveState() {
        localStorage.setItem('orionState', JSON.stringify(this.state));
    }

    loadState() {
        const saved = localStorage.getItem('orionState');
        if (saved) this.state = {...this.state, ...JSON.parse(saved)};
        this.learnFromPastVersions();
    }
    learnFromPastVersions() {
        const versions = this.version.getVersionHistory();
        if (!versions || versions.length < 2) return;
    
        const lastVersion = versions[versions.length - 1];
        const previousVersion = versions[versions.length - 2];
    
        // Safely check for description before calling .includes
        const lastDesc = lastVersion && lastVersion.description;
        const prevDesc = previousVersion && previousVersion.description;
    
        if (
          typeof lastDesc === 'string' &&
          typeof prevDesc === 'string' &&
          lastDesc.includes("bug") &&
          prevDesc.includes("bug")
        ) {
            console.warn("🚨 Repeated bugs detected in recent versions.");
            this.state.userPreferences.debugMode = true;
            this.saveState();
        } else {
            console.log("🧠 Learned from past versions: No recurring bugs detected.");
        }
    }     
}
// Global instance
console.log("✅ Instantiating OrionApp...");
window.Orion = new OrionApp();
console.log("✅ Orion created:", window.Orion);  
