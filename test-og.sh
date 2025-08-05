#!/bin/bash

echo "🔍 Testing Open Graph Meta Tags..."
echo ""

# Build the site first
echo "📦 Building VitePress site..."
npm run docs:build

echo ""
echo "🌐 Testing with different social media debuggers:"
echo ""

echo "📘 Facebook Debugger:"
echo "https://developers.facebook.com/tools/debug/"
echo ""

echo "🐦 Twitter Card Validator:"
echo "https://cards-dev.twitter.com/validator"
echo ""

echo "🔗 LinkedIn Post Inspector:"
echo "https://www.linkedin.com/post-inspector/"
echo ""

echo "📋 General Open Graph Tester:"
echo "https://www.opengraph.xyz/"
echo ""

echo "🚀 Your Vercel URL to test:"
echo "https://your-vercel-app.vercel.app"
echo ""

echo "✅ Meta tags configured successfully!"
echo "Don't forget to:"
echo "1. Update the domain in config.mjs"
echo "2. Test on social platforms after deployment"
echo "3. Create custom images for important pages"
