const fs = require('fs');
const path = require('path');

console.log('🚀 Setting up Krishi Drishti Frontend...\n');

// 1. Create public directory structure
const dirs = [
    'public',
    'public/icons',
    'src',
    'src/components',
    'src/components/Auth',
    'src/components/Dashboard',
    'src/components/Onboarding',
    'src/components/shared',
    'src/services',
    'src/hooks',
    'src/i18n',
    'src/i18n/translations'
];

dirs.forEach(dir => {
    const dirPath = path.join(__dirname, dir);
    if (!fs.existsSync(dirPath)) {
        fs.mkdirSync(dirPath, { recursive: true });
        console.log(`✅ Created: ${dir}`);
    }
});

// 2. Create index.html if missing
const indexHtmlPath = path.join(__dirname, 'public', 'index.html');
if (!fs.existsSync(indexHtmlPath)) {
    const indexHtmlContent = `<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#10b981" />
    <meta name="description" content="Krishi Drishti - Smart Farming Solutions" />
    <title>Krishi Drishti</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>`;
    
    fs.writeFileSync(indexHtmlPath, indexHtmlContent);
    console.log('✅ Created: public/index.html');
}

// 3. Create manifest.json if missing
const manifestPath = path.join(__dirname, 'public', 'manifest.json');
if (!fs.existsSync(manifestPath)) {
    const manifestContent = {
        "short_name": "Krishi Drishti",
        "name": "Krishi Drishti - Smart Farming",
        "icons": [
            {
                "src": "favicon.ico",
                "sizes": "64x64 32x32 24x24 16x16",
                "type": "image/x-icon"
            }
        ],
        "start_url": ".",
        "display": "standalone",
        "theme_color": "#10b981",
        "background_color": "#ffffff"
    };
    
    fs.writeFileSync(manifestPath, JSON.stringify(manifestContent, null, 2));
    console.log('✅ Created: public/manifest.json');
}

// 4. Create robots.txt
const robotsPath = path.join(__dirname, 'public', 'robots.txt');
if (!fs.existsSync(robotsPath)) {
    fs.writeFileSync(robotsPath, 'User-agent: *\nDisallow:');
    console.log('✅ Created: public/robots.txt');
}

// 5. Create .env if missing
const envPath = path.join(__dirname, '.env');
if (!fs.existsSync(envPath)) {
    const envContent = `REACT_APP_API_URL=http://localhost:8000
REACT_APP_ENVIRONMENT=development`;
    fs.writeFileSync(envPath, envContent);
    console.log('✅ Created: .env');
}

console.log('\n🎉 Frontend setup completed!');
console.log('\n📝 Next steps:');
console.log('   1. Add icon images to public/icons/');
console.log('   2. Run: npm install');
console.log('   3. Run: npm start');
