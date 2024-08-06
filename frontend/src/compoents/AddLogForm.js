import React, { useState } from 'react';
import axios from 'axios';

const AddLogForm = () => {
    const [type, setType] = useState('phishing_url'); // Default type
    const [content, setContent] = useState('');
    const [timestamp, setTimestamp] = useState('');
    const [statusMessage, setStatusMessage] = useState('');

    const handleSubmit = (event) => {
        event.preventDefault();
        const newLog = {
            type,
            content,
            timestamp
        };

        axios.post('http://127.0.0.1:5000/api/logs', newLog)
            .then(response => {
                console.log('Log added:', response.data);
                setType('phishing_url'); // Reset to default
                setContent('');
                setTimestamp('');
                setStatusMessage(response.data.is_phishing ? 'This content is identified as phishing.' : 'This content is safe.');
            })
            .catch(error => {
                console.error('There was an error adding the log!', error);
                setStatusMessage('There was an error adding the log.');
            });
    };

    return (
        <div className="add-log-form">
            <h2>Add New Log</h2>
            <form onSubmit={handleSubmit}>
                <label>
                    Content Type:
                    <select value={type} onChange={(e) => setType(e.target.value)} required>
                        <option value="phishing_url">URL</option>
                        <option value="phishing_email">Email</option>
                    </select>
                </label>
                <br />
                <label>
                    Content:
                    <input 
                        type={type === 'phishing_email' ? 'email' : 'text'} 
                        value={content} 
                        onChange={(e) => setContent(e.target.value)} 
                        placeholder={type === 'phishing_url' ? 'Enter URL' : 'Enter Email'} 
                        required 
                    />
                </label>
                <br />
                <label>
                    Timestamp:
                    <input 
                        type="datetime-local" 
                        value={timestamp} 
                        onChange={(e) => setTimestamp(e.target.value)} 
                        required 
                    />
                </label>
                <br />
                <button type="submit">Add Log</button>
                {statusMessage && <p>Status: {statusMessage}</p>}
            </form>
        </div>
    );
};

export default AddLogForm;
