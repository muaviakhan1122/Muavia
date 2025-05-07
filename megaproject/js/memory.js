// memory.js
class OrionMemory {
    constructor(app) {
      this.app = app;
      this.prefix = 'orionMemory_'; // Safe prefix for localStorage keys
      console.log("✅ Orion Memory module initialized");
    }
  
    set(key, value) {
      try {
        localStorage.setItem(this.prefix + key, JSON.stringify(value));
        console.log(`📝 Memory set: ${key}`, value);
      } catch (e) {
        console.error("❌ Failed to save to memory:", e);
      }
    }
  
    get(key) {
      try {
        const value = localStorage.getItem(this.prefix + key);
        console.log(`📥 Memory get: ${key}`, value);
        return value ? JSON.parse(value) : null;
      } catch (e) {
        console.error("❌ Failed to load from memory:", e);
        return null;
      }
    }
  
    remove(key) {
      try {
        localStorage.removeItem(this.prefix + key);
        console.log(`🗑️ Memory removed: ${key}`);
      } catch (e) {
        console.error("❌ Failed to remove from memory:", e);
      }
    }
  
    clearAll() {
      try {
        Object.keys(localStorage)
          .filter(k => k.startsWith(this.prefix))
          .forEach(k => localStorage.removeItem(k));
        console.log("🧹 All Orion memory cleared");
      } catch (e) {
        console.error("❌ Failed to clear memory:", e);
      }
    }
  }
  