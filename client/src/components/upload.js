import React from "react";
import './upload.css';
import {useDropzone} from 'react-dropzone'

export default function Upload( {setRemainingClasses, setRemainingProfessors, setRemainingRequirements}) {
   
    const url = "http://127.0.0.1:8000/dars/";

    const onDrop = (files) => {
      sendHTML(files)
    }

    const sendHTML = async(inputfile) => {
      try {
      let formData = new FormData()
      formData.append('file', inputfile[0])
      console.log(inputfile[0])
      const response = await fetch(`${url}`, { 
        method: 'POST',
        body: formData

      })
      const data = await response.json()
      console.log(data)
      const updated = data
      console.log(updated.classes)
      setRemainingClasses(updated.classes)
      setRemainingProfessors(updated.professors)
      setRemainingRequirements(updated.requirements)

    }
    catch(e) {
      console.log(e)
    }
      //const {id} = data //HOW we use get the data
    }

    const {acceptedFiles, getRootProps, getInputProps} = useDropzone({
      onDrop,
      accept: {
          'text/html': ['.html']
      }
  });

    const files = acceptedFiles.map(file => (
      <li key={file.path}>
        {file.path} - {file.size} bytes
      </li>
    ));

    return (
    <div className="UploadSection" id="upload">
      <div className="SectionTitle">
          Upload DARS
      </div>
        <div className="Upload">
          <section className="container">
              <div {...getRootProps({className: 'dropzone'})}>
                  <input {...getInputProps()} />
                  <p>Add file or drop file here</p>
              </div>
              <aside>
                  <h4>Files</h4>
                  <ul>{files}</ul>
              </aside>
          </section>
        </div>
    </div>
    );
  }