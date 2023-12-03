import React, { useState, useEffect } from 'react';
import Landing from './components/landing';
import NavBar from './components/navbar';
import Instruction from './components/instruction';
import Upload from './components/upload';
import Remaining from './components/remaining';
import Footer from './components/footer';
import Filter from './components/filter';
import './App.css';

function App() {
  const [remainingClasses, setClasses] = useState();
  const [remainingProfessors, setProfessors ] = useState();
  const [remainingRequirements, setRequirements] = useState();

  useEffect(() => {
    // This code will run every time remainingClasses is updated
   // console.log('Remaining Classes:', remainingClasses);
  }, [remainingClasses, remainingProfessors, remainingRequirements]);

  return(
    <div>
      <NavBar/>
      <Landing/>
      <div className='BlueSection'></div>
      <Instruction/>
      <div className='BlueSection'></div>
      <Upload
        setRemainingClasses={setClasses}
        setRemainingProfessors={setProfessors}
        setRemainingRequirements={setRequirements}
      />
      {console.log("HI")}
      {console.log(remainingClasses)}
      <div className='BlueSection'></div>
      <div className='BlueSection'></div>
      <Remaining
        sendRemainingClasses = {remainingClasses}
        sendRemainingProfessors = {remainingProfessors}
        sendRemainingRequirements = {remainingRequirements}
      />
      <Filter
        sendRemainingClasses = {remainingClasses}
        sendRemainingProfessors = {remainingProfessors}
        sendRemainingRequirements = {remainingRequirements}
      />
      <div className='BlueSection'></div>

      <Footer/>
    </div>
  )
}

export default App;