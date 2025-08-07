#!/usr/bin/env node

import fs from 'fs/promises'
import path from 'path'
import { glob } from 'glob'

class ContentManager {
  constructor(docsPath = './docs') {
    this.docsPath = docsPath
  }

  // Tự động tạo sidebar từ cấu trúc file
  async generateSidebar() {
    const mdFiles = await glob(`${this.docsPath}/**/*.md`)
    const sidebar = {}
    
    for (const file of mdFiles) {
      const relativePath = path.relative(this.docsPath, file)
      const content = await fs.readFile(file, 'utf-8')
      const title = this.extractTitle(content)
      
      // Build sidebar structure
      const pathParts = relativePath.split('/')
      let current = sidebar
      
      for (let i = 0; i < pathParts.length - 1; i++) {
        const part = pathParts[i]
        if (!current[part]) current[part] = {}
        current = current[part]
      }
      
      current[path.basename(file, '.md')] = {
        title,
        path: `/${relativePath.replace('.md', '')}`
      }
    }
    
    return sidebar
  }

  // Extract title from markdown frontmatter or first h1
  extractTitle(content) {
    const frontmatterMatch = content.match(/^---\s*\ntitle:\s*["'](.+)["']\s*\n/m)
    if (frontmatterMatch) return frontmatterMatch[1]
    
    const h1Match = content.match(/^#\s+(.+)$/m)
    if (h1Match) return h1Match[1]
    
    return 'Untitled'
  }

  // Validate all internal links
  async validateLinks() {
    const mdFiles = await glob(`${this.docsPath}/**/*.md`)
    const errors = []
    
    for (const file of mdFiles) {
      const content = await fs.readFile(file, 'utf-8')
      const links = content.match(/\[.*?\]\(\.\/.*?\)/g) || []
      
      for (const link of links) {
        const linkPath = link.match(/\((.+)\)/)[1]
        const fullPath = path.resolve(path.dirname(file), linkPath)
        
        try {
          await fs.access(fullPath)
        } catch {
          errors.push(`Broken link in ${file}: ${link}`)
        }
      }
    }
    
    return errors
  }

  // Auto-format markdown files
  async formatMarkdown() {
    const mdFiles = await glob(`${this.docsPath}/**/*.md`)
    
    for (const file of mdFiles) {
      let content = await fs.readFile(file, 'utf-8')
      
      // Standardize frontmatter
      if (!content.startsWith('---')) {
        const title = this.extractTitle(content)
        content = `---\ntitle: "${title}"\n---\n\n${content}`
      }
      
      // Fix common formatting issues
      content = content
        .replace(/\n{3,}/g, '\n\n') // Remove excessive newlines
        .replace(/\s+$/gm, '') // Remove trailing spaces
        .replace(/^\s*#\s+/gm, '# ') // Standardize headers
      
      await fs.writeFile(file, content)
    }
  }
}

// CLI usage
const manager = new ContentManager()

const command = process.argv[2]
switch (command) {
  case 'sidebar':
    manager.generateSidebar().then(console.log)
    break
  case 'validate':
    manager.validateLinks().then(errors => {
      if (errors.length) {
        console.error('Link validation errors:')
        errors.forEach(err => console.error(err))
        process.exit(1)
      }
      console.log('All links valid!')
    })
    break
  case 'format':
    manager.formatMarkdown().then(() => console.log('Formatting complete!'))
    break
  default:
    console.log('Usage: node content-manager.js [sidebar|validate|format]')
}
