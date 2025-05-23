import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

import { QueryClientProvider } from '@tanstack/react-query';
import queryClient from './queryClient';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      {/* AuthProvider is disabled for now */}
      <App />
    </QueryClientProvider>
  </React.StrictMode>
);
