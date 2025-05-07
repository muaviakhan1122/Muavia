console.log("✅ aiService.js loaded");

class OrionAIService {
  constructor(app) {
    this.app = app;
    this.suggester = new FeatureSuggester();
  }

  async suggestAndAnalyze() {
    const features = await this.suggester.fetchTrendingFeatures();
    const scoredFeatures = this.suggester.scoreFeatures(features);
    const topFeatures = scoredFeatures.slice(0, 3);

    this.suggester.analyzeFeatureTrends(features);

    console.log("🌟 Top Recommended Features:", topFeatures);
    this.app.ui.showFeatureSuggestions(topFeatures);

    // Save trending analysis to memory
    this.app.memory.set('lastTrendAnalysis', {
      date: new Date().toISOString(),
      topFeatures: topFeatures
    });
  }

  async generateFeatureModule(feature) {
    const prompt = `Generate JavaScript module for: ${feature.description}\nExports: init(), run(), cleanup()`;
    return {
      code: `// ${feature.name}
(function(){
  function init() {
    console.log("${feature.name} loaded");
  }
  window.${feature.name.replace(/-/g, "_")} = { init };
})();`,
      isValid: true
    };       
  }
}

class FeatureSuggester {
  constructor() {
    this.sources = {
      github: "https://api.github.com/search/repositories?q=AI+assistant+language:javascript",
      blogs: ["https://openai.com/blog", "https://huggingface.co/blog"]
    };
  }

  async fetchTrendingFeatures() {
    try {
      const response = await fetch(this.sources.github);
      const data = await response.json();
      return data.items
        .filter(repo => 
          repo.stargazers_count > 1000 &&
          !repo.archived &&
          repo.description?.includes('AI')
        )
        .map(repo => ({
          name: repo.name,
          description: repo.description,
          stars: repo.stargazers_count,
          url: repo.html_url,
          updated_at: repo.updated_at,
          language: repo.language
        }));
    } catch (error) {
      console.error("Fetch error:", error);
      return [];
    }
  }

  analyzeFeatureTrends(features) {
    const languages = {};
    features.forEach(f => {
      languages[f.language] = (languages[f.language] || 0) + 1;
    });

    const topLang = Object.entries(languages).sort((a, b) => b[1] - a[1])[0];
    if (topLang) {
      console.log(`📊 Most trending AI language: ${topLang[0]} (${topLang[1]} projects)`);
    }
  }

  scoreFeatures(features) {
    return features
      .map(f => {
        let score = 0;
        if (f.stars) score += f.stars / 1000;   // 1 point per 1000 stars
        if (f.updated_at) {
          const daysOld = (new Date() - new Date(f.updated_at)) / (1000 * 60 * 60 * 24);
          if (daysOld < 30) score += 2;         // Bonus for recent update
        }
        if (f.description && f.description.length > 50) score += 1; // Bonus for rich description
        return {...f, score: Math.round(score * 10) / 10}; // round to 1 decimal
      })
      .sort((a, b) => b.score - a.score); // Sort highest score first
  }
}
