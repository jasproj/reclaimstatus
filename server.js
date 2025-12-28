/**
 * Treasury Package Generator - Backend Server
 * Express API for document generation
 */

const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');
const archiver = require('archiver');
const crypto = require('crypto-js');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// Security middleware
app.use(helmet());
app.use(cors({
  origin: process.env.ALLOWED_ORIGINS?.split(',') || '*',
  methods: ['GET', 'POST'],
}));

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 10, // 10 requests per window
  message: { error: 'Too many requests, please try again later.' }
});
app.use('/api/generate', limiter);

// Body parsing
app.use(express.json({ limit: '1mb' }));

// Serve static files
app.use(express.static(path.join(__dirname, '../frontend')));

// Health check
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Generate package endpoint
app.post('/api/generate-package', async (req, res) => {
  const startTime = Date.now();
  const sessionId = crypto.lib.WordArray.random(16).toString();
  
  console.log(`[${sessionId}] Starting package generation...`);
  
  try {
    const customerData = req.body;
    
    // Validate required fields
    const required = ['firstName', 'lastName', 'ssn', 'birthDate', 'streetAddress', 
                      'city', 'state', 'zipCode', 'uccFilingNumber'];
    const missing = required.filter(f => !customerData[f]);
    
    if (missing.length > 0) {
      return res.status(400).json({ 
        error: 'Missing required fields', 
        fields: missing 
      });
    }
    
    // Create temporary output directory
    const outputDir = path.join(__dirname, '../temp', sessionId);
    fs.mkdirSync(outputDir, { recursive: true });
    
    // Write customer data to temp file
    const dataPath = path.join(outputDir, 'customer_data.json');
    fs.writeFileSync(dataPath, JSON.stringify(customerData, null, 2));
    
    // Call Python generator
    const pythonProcess = spawn('python3', [
      path.join(__dirname, 'generator.py'),
      '--data', dataPath,
      '--output', outputDir,
      '--templates', process.env.TEMPLATE_DIR || '../templates'
    ]);
    
    let stdout = '';
    let stderr = '';
    
    pythonProcess.stdout.on('data', (data) => {
      stdout += data.toString();
      console.log(`[${sessionId}] ${data.toString().trim()}`);
    });
    
    pythonProcess.stderr.on('data', (data) => {
      stderr += data.toString();
      console.error(`[${sessionId}] ERROR: ${data.toString().trim()}`);
    });
    
    pythonProcess.on('close', async (code) => {
      if (code !== 0) {
        console.error(`[${sessionId}] Generator exited with code ${code}`);
        cleanup(outputDir);
        return res.status(500).json({ error: 'Generation failed', details: stderr });
      }
      
      // Find generated files
      const files = fs.readdirSync(outputDir);
      const mergedPdf = files.find(f => f.includes('COMPLETE.pdf'));
      const zipFile = files.find(f => f.endsWith('.zip'));
      
      if (mergedPdf) {
        // Send merged PDF
        const pdfPath = path.join(outputDir, mergedPdf);
        res.setHeader('Content-Type', 'application/pdf');
        res.setHeader('Content-Disposition', `attachment; filename="${mergedPdf}"`);
        
        const stream = fs.createReadStream(pdfPath);
        stream.pipe(res);
        
        stream.on('end', () => {
          const duration = Date.now() - startTime;
          console.log(`[${sessionId}] Completed in ${duration}ms`);
          
          // Cleanup after 5 seconds
          setTimeout(() => cleanup(outputDir), 5000);
        });
      } else if (zipFile) {
        // Fallback to ZIP
        const zipPath = path.join(outputDir, zipFile);
        res.setHeader('Content-Type', 'application/zip');
        res.setHeader('Content-Disposition', `attachment; filename="${zipFile}"`);
        
        const stream = fs.createReadStream(zipPath);
        stream.pipe(res);
        
        stream.on('end', () => {
          setTimeout(() => cleanup(outputDir), 5000);
        });
      } else {
        cleanup(outputDir);
        res.status(500).json({ error: 'No output files generated' });
      }
    });
    
  } catch (error) {
    console.error(`Generation error:`, error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Download JSON data (for testing)
app.post('/api/export-data', (req, res) => {
  const customerData = req.body;
  const filename = `treasury_data_${customerData.lastName || 'customer'}_${Date.now()}.json`;
  
  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Content-Disposition', `attachment; filename="${filename}"`);
  res.json(customerData);
});

// Cleanup function
function cleanup(dir) {
  try {
    fs.rmSync(dir, { recursive: true, force: true });
    console.log(`Cleaned up: ${dir}`);
  } catch (e) {
    console.error(`Cleanup failed for ${dir}:`, e.message);
  }
}

// Error handling
app.use((err, req, res, next) => {
  console.error('Unhandled error:', err);
  res.status(500).json({ error: 'Internal server error' });
});

// Start server
app.listen(PORT, () => {
  console.log(`
╔════════════════════════════════════════════════════════╗
║     Treasury Package Generator Server                  ║
║     Running on http://localhost:${PORT}                    ║
╚════════════════════════════════════════════════════════╝
  `);
});

module.exports = app;
