import React from 'react';
import LogList from '../compoents/LogList';
import AddLogForm from '../compoents/AddLogForm';

const HomePage = () => {
    return (
        <div>
            <h1>Phishing Detection System</h1>
            <AddLogForm />
            <LogList />
        </div>
    );
};

export default HomePage;
