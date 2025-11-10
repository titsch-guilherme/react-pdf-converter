#!/usr/bin/env node

// Simple test runner to help debug Jest configuration issues
const { execSync } = require('child_process');
const path = require('path');

console.log('🧪 PDF OCR Converter - Test Runner');
console.log('==================================');

try {
  console.log('📋 Checking Jest configuration...');
  
  // Check if jest config exists
  const configPath = path.join(__dirname, 'jest.config.cjs');
  console.log(`Config file: ${configPath}`);
  
  // Try to run Jest with verbose output
  console.log('🚀 Running tests...');
  execSync('npx jest --config=jest.config.cjs --verbose --no-cache', {
    stdio: 'inherit',
    cwd: __dirname
  });
  
  console.log('✅ All tests passed!');
} catch (error) {
  console.error('❌ Test execution failed:');
  console.error(error.message);
  process.exit(1);
}