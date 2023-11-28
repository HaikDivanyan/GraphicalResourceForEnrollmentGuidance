import React from 'react';
import Landing from './components/landing';
import NavBar from './components/navbar';
import Instruction from './components/instruction';
import Upload from './components/upload';
import Remaining from './components/remaining';
import './App.css';

function App() {
  return(
    <div>
      <NavBar/>
      <Landing/>
      <div className='BlueSection'></div>
      <Instruction/>
      <div className='BlueSection'></div>
      <Upload/>
      <div className='BlueSection'></div>
      <Remaining/>
    </div>
  )
}

export default App;