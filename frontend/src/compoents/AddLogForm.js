import React, { useState } from 'react';
import axios from 'axios';

const AddLogForm = () => {
    const [type, setType] = useState('type'); // Default type
    const [content, setContent] = useState('');
    const [timestamp, setTimestamp] = useState('');
    const [statusMessage, setStatusMessage] = useState('');
    const [prediction, setPrediction] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (event) => {
        event.preventDefault();
        setLoading(true);

        // Basic validation
        if (!content || !timestamp) {
            setStatusMessage('Content and Timestamp are required.');
            setLoading(false);
            return;
        }

        const newLog = {
            contentType: type,
            content,
            timestamp: new Date(timestamp).toISOString() // Convert timestamp to ISO 8601 format
        };

        try {
            const response = await axios.post('http://127.0.0.1:5000/api/logs', newLog);
            setStatusMessage('Log added successfully.');
            const isPhishing = parseInt(response.data.is_phishing) === 1 ? 'not safe' : 'safe';
            setPrediction(`The ${type === 'phishing_email' ? 'email' : 'URL'} is ${isPhishing}.`);
            // Clear form inputs after submission
            setType('phishing_url');
            setContent('');
            setTimestamp('');
        } catch (error) {
            console.error('There was an error adding the log!', error);
            setStatusMessage('There was an error adding the log.');
            setPrediction('');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="add-log-form">
            <h2>Add New Log</h2>
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label htmlFor="contentType">Content Type:</label>
                    <select 
                        id="contentType"
                        value={type} 
                        onChange={(e) => setType(e.target.value)} 
                        required
                        disabled={loading}
                    >
                        <option value="phishing_url">URL</option>
                        <option value="phishing_email">Email</option>
                    </select>
                </div>
                <div className="form-group">
                    <label htmlFor="content">Content:</label>
                    <input 
                        id="content"
                        type={type === 'phishing_email' ? 'email' : 'text'} 
                        value={content} 
                        onChange={(e) => setContent(e.target.value)} 
                        placeholder={type === 'phishing_url' ? 'Enter URL' : 'Enter Email'} 
                        required 
                        disabled={loading}
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="timestamp">Timestamp:</label>
                    <input 
                        id="timestamp"
                        type="datetime-local" 
                        value={timestamp} 
                        onChange={(e) => setTimestamp(e.target.value)} 
                        required 
                        disabled={loading}
                    />
                </div>
                <div className="button-group">
                    <button type="submit" disabled={loading}>
                        {loading ? 'Adding...' : 'Add Log'}
                    </button>
                </div>
                {statusMessage && <p className="status-message">{statusMessage}</p>}
                {prediction && <p className="prediction">{prediction}</p>}
            </form>
        </div>
    );
};

export default AddLogForm;
