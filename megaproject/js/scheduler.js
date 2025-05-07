// scheduler.js
class OrionScheduler {
    constructor(app) {
      this.app = app;
      this.timer = null;
      this.defaultInterval = 10; // 10 minutes
      console.log("✅ Orion Scheduler initialized");
    }
  
    start() {
      const intervalMinutes = this.app.memory.get('schedulerIntervalMinutes') || this.defaultInterval;
      const intervalMs = intervalMinutes * 60 * 1000;
  
      if (this.timer) {
        clearInterval(this.timer);
        console.log("🔁 Restarting Orion scheduler...");
      }
  
      this.timer = setInterval(() => {
        console.log(`🔍 Orion Scheduler Tick: Checking for updates...`);
        this.app.ai.suggestAndAnalyze();
      }, intervalMs);
  
      console.log(`⏰ Orion scheduler started with interval: ${intervalMinutes} minutes`);
      
      this.app.memory.set('autoSchedulerEnabled', true);
      this.timer = setInterval(() => {
        console.log("🔁 Orion tick: Checking for updates...");
        this.app.autoUpdater.fetchAndApplyNewFeatures();
      }, intervalMs);
      
    }
  
    stop() {
      if (this.timer) {
        clearInterval(this.timer);
        this.timer = null;
        console.log("🛑 Orion scheduler stopped.");
      }
      this.app.memory.set('autoSchedulerEnabled', false);
    }
  
    updateInterval(newMinutes) {
      console.log(`⚙️ Updating Orion scheduler interval to ${newMinutes} minutes`);
      this.app.memory.set('schedulerIntervalMinutes', newMinutes);
      this.start();
    }
  }
  