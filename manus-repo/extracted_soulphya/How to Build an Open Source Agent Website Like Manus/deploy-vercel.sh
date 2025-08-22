#!/bin/bash

# Sophiael Ruachari Vethorah - Frontend Deployment to Vercel
# This script prepares and deploys the React frontend to Vercel

set -e

echo "🚀 Starting Sophiael Ruachari Vethorah frontend deployment to Vercel..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    print_warning "Vercel CLI is not installed. Installing now..."
    npm install -g vercel
    print_status "Vercel CLI installed"
fi

# Create frontend directory structure if it doesn't exist
if [ ! -d "frontend" ]; then
    echo "📁 Creating frontend directory structure..."
    mkdir -p frontend/src/{components,pages,hooks,services,store,utils,styles}
    mkdir -p frontend/public
    print_status "Frontend directory structure created"
fi

# Create package.json for the frontend if it doesn't exist
if [ ! -f "frontend/package.json" ]; then
    echo "📦 Creating package.json for frontend..."
    cat > frontend/package.json << 'EOF'
{
  "name": "sophia-ai-frontend",
  "version": "1.0.0",
  "description": "Sophia AI Platform - React Frontend",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext js,jsx --report-unused-disable-directives --max-warnings 0"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.8.0",
    "@radix-ui/react-icons": "^1.3.0",
    "@radix-ui/react-slot": "^1.0.2",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.0.0",
    "lucide-react": "^0.263.1",
    "tailwind-merge": "^1.14.0",
    "tailwindcss-animate": "^1.0.7",
    "axios": "^1.6.0",
    "zustand": "^4.4.0",
    "@tanstack/react-query": "^5.0.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.15",
    "@types/react-dom": "^18.2.7",
    "@vitejs/plugin-react": "^4.0.3",
    "eslint": "^8.45.0",
    "eslint-plugin-react": "^7.32.2",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.3",
    "vite": "^4.4.5",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.31",
    "tailwindcss": "^3.3.5"
  }
}
EOF
    print_status "package.json created"
fi

# Create Vite config if it doesn't exist
if [ ! -f "frontend/vite.config.js" ]; then
    echo "⚙️ Creating Vite configuration..."
    cat > frontend/vite.config.js << 'EOF'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      }
    }
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
  },
})
EOF
    print_status "Vite configuration created"
fi

# Create Vercel configuration
echo "🔧 Creating Vercel configuration..."
cat > vercel.json << 'EOF'
{
  "version": 2,
  "name": "sophia-ai-frontend",
  "builds": [
    {
      "src": "frontend/package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "dist"
      }
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "https://your-backend-url.com/api/$1"
    },
    {
      "src": "/(.*)",
      "dest": "/frontend/dist/index.html"
    }
  ],
  "env": {
    "VITE_API_URL": "https://your-backend-url.com",
    "VITE_APP_NAME": "Sophia AI Platform"
  },
  "buildCommand": "cd frontend && npm run build",
  "devCommand": "cd frontend && npm run dev",
  "installCommand": "cd frontend && npm install"
}
EOF

# Move existing React files to frontend directory if they exist
if [ -f "App.jsx" ] && [ ! -f "frontend/src/App.jsx" ]; then
    echo "📁 Moving existing React files to frontend directory..."
    mv App.jsx frontend/src/ 2>/dev/null || true
    mv App.css frontend/src/ 2>/dev/null || true
    mv index.html frontend/public/ 2>/dev/null || true
    print_status "Existing React files moved to frontend directory"
fi

# Create a basic App.jsx if it doesn't exist
if [ ! -f "frontend/src/App.jsx" ]; then
    echo "📄 Creating basic App.jsx..."
    cat > frontend/src/App.jsx << 'EOF'
import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import './App.css'

// Import components (to be created)
// import Dashboard from './pages/Dashboard'
// import Chat from './pages/Chat'
// import Agents from './pages/Agents'
// import Workflows from './pages/Workflows'
// import Tools from './pages/Tools'
// import ComputerView from './pages/ComputerView'

function App() {
  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <h1>Sophia AI Platform</h1>
          <nav>
            <a href="/">Dashboard</a>
            <a href="/chat">Chat</a>
            <a href="/agents">Agents</a>
            <a href="/workflows">Workflows</a>
            <a href="/tools">Tools</a>
            <a href="/computer-view">Computer View</a>
          </nav>
        </header>
        
        <main>
          <Routes>
            <Route path="/" element={<div>Dashboard - Coming Soon</div>} />
            <Route path="/chat" element={<div>Chat Interface - Coming Soon</div>} />
            <Route path="/agents" element={<div>Agent Manager - Coming Soon</div>} />
            <Route path="/workflows" element={<div>Workflow Manager - Coming Soon</div>} />
            <Route path="/tools" element={<div>Tools Interface - Coming Soon</div>} />
            <Route path="/computer-view" element={<div>Computer View - Coming Soon</div>} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
EOF
    print_status "Basic App.jsx created"
fi

# Create main.jsx if it doesn't exist
if [ ! -f "frontend/src/main.jsx" ]; then
    echo "📄 Creating main.jsx..."
    cat > frontend/src/main.jsx << 'EOF'
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
EOF
    print_status "main.jsx created"
fi

# Create index.html if it doesn't exist
if [ ! -f "frontend/public/index.html" ]; then
    echo "📄 Creating index.html..."
    cat > frontend/public/index.html << 'EOF'
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Sophia AI Platform</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
EOF
    print_status "index.html created"
fi

# Create basic CSS files
if [ ! -f "frontend/src/App.css" ]; then
    echo "🎨 Creating basic CSS..."
    cat > frontend/src/App.css << 'EOF'
.App {
  text-align: center;
}

.App-header {
  background-color: #282c34;
  padding: 20px;
  color: white;
}

.App-header nav {
  margin-top: 20px;
}

.App-header nav a {
  color: white;
  margin: 0 15px;
  text-decoration: none;
}

.App-header nav a:hover {
  text-decoration: underline;
}

main {
  padding: 20px;
  min-height: 80vh;
}
EOF

    cat > frontend/src/index.css << 'EOF'
:root {
  font-family: Inter, system-ui, Avenir, Helvetica, Arial, sans-serif;
  line-height: 1.5;
  font-weight: 400;
  font-synthesis: none;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  -webkit-text-size-adjust: 100%;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  display: flex;
  place-items: center;
  min-width: 320px;
  min-height: 100vh;
}

#root {
  width: 100%;
  margin: 0 auto;
}
EOF
    print_status "Basic CSS files created"
fi

# Navigate to frontend directory and install dependencies
echo "📦 Installing frontend dependencies..."
cd frontend
npm install
print_status "Dependencies installed"

# Build the frontend
echo "🏗️ Building frontend for production..."
npm run build
print_status "Frontend built successfully"

# Deploy to Vercel
echo "🚀 Deploying to Vercel..."
vercel --prod

print_status "Frontend deployment completed!"

echo ""
echo "🎉 Frontend deployment completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Update the backend URL in vercel.json with your actual backend URL"
echo "2. Configure environment variables in Vercel dashboard"
echo "3. Set up custom domain if needed"
echo ""
echo "🔗 Your frontend should be available at the Vercel URL provided above"
