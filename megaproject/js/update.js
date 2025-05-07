console.log("✅ update.js loaded");
class UpdateSystem {
    constructor(app) {
        this.app = app;
    }

    async testInSandbox(code) {
        return new Promise(resolve => {
            const sandbox = document.createElement('iframe');
            sandbox.style.display = 'none';
            sandbox.srcdoc = `
                <script>
                    try {
                        ${code}
                        parent.postMessage({ status: 'passed' }, '*');
                    } catch(e) {
                        parent.postMessage({ status: 'failed', error: e.message }, '*');
                    }
                <\/script>
            `;
            document.body.appendChild(sandbox);

            const handler = (e) => {
                if (e.data.status) {
                    resolve(e.data);
                    window.removeEventListener('message', handler);
                    sandbox.remove();
                }
            };

            window.addEventListener('message', handler);
        });
    }

    async proposeUpdate(feature) {
        const module = await this.app.ai.generateFeatureModule(feature);
        const testResult = await this.testInSandbox(module.code);

        if (testResult.status === 'passed') {
            this.app.ui.showUpdatePrompt({
                version: this.app.version.incrementVersion(this.app.state.currentVersion),
                changes: [feature.description],
                code: module.code
            });
        }
    }
} 
