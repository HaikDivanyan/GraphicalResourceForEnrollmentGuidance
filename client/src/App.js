import React, { useState, useEffect } from 'react';
import Landing from './components/landing';
import NavBar from './components/navbar';
import Instruction from './components/instruction';
import Upload from './components/upload';
import Remaining from './components/remaining';
import Footer from './components/footer';
import Filter from './components/filter';
<<<<<<< HEAD
<<<<<<< HEAD
import Download from './components/download';
=======
import Schedule from './components/schedule';
import Demo from './components/demo';
>>>>>>> dcf004b (DISPLAY SCHEDULES BASED ON SAMPLE DATA)
=======
import Schedule from './components/schedule';
import Demo from './components/demo';
=======
import Download from './components/download';
>>>>>>> 28eecf5 (Download rough draft)
>>>>>>> e58ac87 (Download rough with main)
import './App.css';

function App() {
  const [remainingClasses, setClasses] = useState();
  const [remainingProfessors, setProfessors ] = useState();
  const [remainingRequirements, setRequirements] = useState();
  const [file, setFile] = useState();

  useEffect(() => {
    // This code will run every time remainingClasses is updated
   // console.log('Remaining Classes:', remainingClasses);
  }, [remainingClasses, remainingProfessors, remainingRequirements, file]);

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
        setDarsFile = {setFile}
      />
      {console.log("Dars file given")}
      {console.log(file)}
      <div className='BlueSection'></div>
      <Remaining
        sendRemainingClasses = {remainingClasses}
        sendRemainingProfessors = {remainingProfessors}
        sendRemainingRequirements = {remainingRequirements}
      />
      <div className='BlueSection'></div>
      <Filter
        sendRemainingClasses = {remainingClasses}
        sendRemainingProfessors = {remainingProfessors}
        sendRemainingRequirements = {remainingRequirements}
        sendFileBack = {file}
      />
      <div className='BlueSection'></div>
<<<<<<< HEAD
      <Download/>
      <div className='BlueSection'></div>
=======
<<<<<<< HEAD
>>>>>>> e58ac87 (Download rough with main)
      <Schedule/>
      <Demo/>
=======
      <Download/>
      <div className='BlueSection'></div>
>>>>>>> 28eecf5 (Download rough draft)
      <Footer/>
    </div>
  )
}

export default App;