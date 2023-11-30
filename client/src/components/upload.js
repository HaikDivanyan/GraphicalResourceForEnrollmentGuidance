import React from "react";
import './upload.css';
import {useDropzone} from 'react-dropzone'

export default function Upload() {
    const {acceptedFiles, getRootProps, getInputProps} = useDropzone({
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