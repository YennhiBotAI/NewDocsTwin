#!/usr/bin/env node

import chokidar from 'chokidar'
import { exec } from 'child_process'
import path from 'path'

class DocWatcher {
  constructor() {
    this.watcher = null
    this.debounceTimeout = null
  }

  start() {
    console.log('🔍 Watching for documentation changes...')
    
    this.watcher = chokidar.watch([
      'docs/**/*.md',
      'docs/**/*.json',
      'docs/.vitepress/config.*'
    ], {
      ignored: /node_modules/,
      persistent: true
    })

    this.watcher
      .on('add', this.handleChange.bind(this))
      .on('change', this.handleChange.bind(this))
      .on('unlink', this.handleChange.bind(this))

    console.log('✅ Watcher started. Press Ctrl+C to stop.')
  }

  handleChange(filePath) {
    clearTimeout(this.debounceTimeout)
    
    this.debounceTimeout = setTimeout(() => {
      console.log(`📝 File changed: ${path.relative(process.cwd(), filePath)}`)
      
      if (filePath.includes('config.')) {
        console.log('🔄 Config changed, restarting dev server...')
        this.restartDevServer()
      } else {
        console.log('✨ Content updated, hot reload active')
        this.validateContent(filePath)
      }
    }, 500)
  }

  async validateContent(filePath) {
    // Quick validation
    if (filePath.endsWith('.md')) {
      exec(`node scripts/content-manager.js validate`, (error, stdout, stderr) => {
        if (error) {
          console.error('❌ Validation failed:', stderr)
        } else {
          console.log('✅ Content validation passed')
        }
      })
    }
  }

  restartDevServer() {
    exec('pkill -f "vitepress dev" && npm run docs:dev', (error) => {
      if (error) {
        console.error('Failed to restart server:', error)
      } else {
        console.log('🚀 Dev server restarted')
      }
    })
  }

  stop() {
    if (this.watcher) {
      this.watcher.close()
      console.log('👋 Watcher stopped')
    }
  }
}

const watcher = new DocWatcher()
watcher.start()

// Graceful shutdown
process.on('SIGINT', () => {
  watcher.stop()
  process.exit(0)
})
