import './download.css';
import React, { useState } from 'react';
import html2canvas from 'html2canvas';

export default function Download() {
  
    const handleCaptureScreenshot = () => {
    const element = document.getElementById('capture'); // Replace 'capture' with the ID of the element you want to capture

    html2canvas(element).then(canvas => {
      // Convert canvas to image data URL
      const dataURL = canvas.toDataURL('image/png');

      // Create a download link
      const downloadLink = document.createElement('a');
      downloadLink.href = dataURL;
      downloadLink.download = 'my_schedule.png';
      document.body.appendChild(downloadLink);

      // Trigger the download
      downloadLink.click();

      // Clean up
      document.body.removeChild(downloadLink);
    });
  };

  return (
    <div>
      <div className="UploadSection" id="capture">
      <div className="SectionTitle">
          Download
      </div>
        {/* Content to capture */}
        <h1>Hello, this is the content to capture!</h1>
      </div>
      <div className="ButtonContainer">
        <button className="generateButton" onClick={handleCaptureScreenshot}>Download Screenshot</button>
      </div>
    </div>
  );
}