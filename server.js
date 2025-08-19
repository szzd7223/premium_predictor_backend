const express = require('express');
const cors = require('cors');
const { spawn } = require('child_process');
const app = express();

app.use(cors());
app.use(express.json());

// Route to handle prediction requests
app.post('/api/predict', async (req, res) => {
    try {
        // Launch Python script as a separate process
        const pythonProcess = spawn('python', ['predict.py']);
        
        let prediction = '';
        let error = '';

        // Send data to Python script
        pythonProcess.stdin.write(JSON.stringify(req.body));
        pythonProcess.stdin.end();

        // Collect data from Python script
        pythonProcess.stdout.on('data', (data) => {
            prediction += data.toString();
        });

        pythonProcess.stderr.on('data', (data) => {
            error += data.toString();
        });

        // Handle completion
        pythonProcess.on('close', (code) => {
            if (code !== 0) {
                return res.status(500).json({
                    status: 'error',
                    error: error || 'Failed to get prediction'
                });
            }
            
            try {
                const result = JSON.parse(prediction);
                res.json({
                    status: 'success',
                    predicted_price: result.predicted_price
                });
            } catch (e) {
                res.status(500).json({
                    status: 'error',
                    error: 'Invalid prediction format'
                });
            }
        });

    } catch (error) {
        res.status(500).json({
            status: 'error',
            error: error.message
        });
    }
});

// Health check endpoint
app.get('/api/health', (req, res) => {
    res.json({ status: 'healthy' });
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
    console.log(`Express server running on port ${PORT}`);
});
