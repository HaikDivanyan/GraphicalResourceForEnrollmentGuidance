import React from "react";
import './landing.css';

export default function Landing() {
    const colors = ['#005587', '#8BB8E8', '#FFB81C', '#FFD100'];
    const colors2 = ['#005587', '#8BB8E8', '#000000', '#FFB81C', '#FFD100'];
    const smallTitle = 'Graphical Resources for Enrollment Guidance';

    return (
      <div className="Container">
            <div className="Text">
                <div className="BigTitle">
                    {['G', 'R', 'E', 'G'].map((letter, index) => (
                         <span key={index} style={{ color: colors[index], letterSpacing: '15px' }}>{letter}</span>
                    ))}
                </div>
                <div className="SmallTitle">
                    {smallTitle.split(' ').map((word, index) => (
                        <span key={index} style={{ color: colors2[index] }}>{word} </span>
                    ))}
                </div>
                <div className="Slogan">
                    "For a schedule that's prime, go with GREG every time."
                </div>
                <div className="Buttons">
                        <button className="button1" onClick={()=> {
                            const target = document.getElementById("how-to-use");
                            if (target) {
                                target.scrollIntoView({
                                    behavior: 'smooth',
                                    block: 'center',
                                    inline: 'center'
                                })
                            }
                        }}>How to Use</button>
                        <button className="button2" onClick={()=> {
                            const target = document.getElementById("upload");
                            if (target) {
                                target.scrollIntoView({
                                    behavior: 'smooth',
                                    block: 'center',
                                    inline: 'center'
                                })
                            }
                        }}>Get Started</button>
                </div>
            </div> 
      </div>
    );
  }