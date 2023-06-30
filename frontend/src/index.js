import React, { createContext } from 'react';
import ReactDOM from 'react-dom/client';

import App from './App';

import './index.css'

const root = ReactDOM.createRoot(document.getElementById('root'));
const Context = createContext(null);

root.render(
  <Context.Provider value={{
  }}>
    <App />
  </Context.Provider>
);


export { Context };