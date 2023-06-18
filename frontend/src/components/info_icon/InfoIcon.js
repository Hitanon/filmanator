import React from "react";
import './style.css';


const InfoIcon = ({icon, text, color, height}) => {
    return ( 
        <div className="icon" style={{ height }}>
            {icon && <img src = {icon} alt = {text}/>}
            <p style = {{color: color}}>{text}</p>
        </div>
     );
}
    
export default InfoIcon;