import React from 'react';
import Landing from './components/landing';
import NavBar from './components/navbar';
import './App.css';

function App() {
  return(
    <div>
      <NavBar/>
      <Landing/>
      <div className='BlueSection'></div>
    </div>
  )
}

export default App;