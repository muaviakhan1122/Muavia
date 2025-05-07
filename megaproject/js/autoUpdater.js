console.log("✅ autoUpdater.js loaded");

class AutoUpdater {
  constructor(app) {
    this.app = app;
    this.updateQueue = [];
    this.appliedFeatures = new Set(); // Avoid re-adding same feature
  }

  async fetchAndApplyNewFeatures() {
    console.log("🤖 AutoUpdater running: Fetching trending AI modules...");

    const features = await this.app.ai.suggester.fetchTrendingFeatures();
    const scored = this.app.ai.suggester.scoreFeatures(features);
    const top = scored.slice(0, 3); // Only test top 3 for now

    for (const feature of top) {
      if (this.appliedFeatures.has(feature.name)) {
        console.log(`⏭️ Skipping already applied: ${feature.name}`);
        continue;
      }

      const module = await this.app.ai.generateFeatureModule(feature);
      const result = await this.app.update.testInSandbox(module.code);

      if (result.status === 'passed') {
        console.log(`✅ Passed sandbox: ${feature.name}`);
        this.app.version.applyFeatureModule(module.code, feature.description);
        this.appliedFeatures.add(feature.name);
      } else {
        console.warn(`❌ Failed sandbox: ${feature.name} → ${result.error}`);
      }
    }

    this.app.memory.set("lastAutoUpdate", new Date().toISOString());
    Orion.version.applyFeatureModule(generatedCode, "Added feature: X");
  }
}
