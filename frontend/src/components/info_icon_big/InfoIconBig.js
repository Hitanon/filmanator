import React from "react";
import './style.css';


const InfoIconBig = ({icon, text, color, height, fontSize}) => {
    return ( 
        <div className="icon-big" style={{ height}}>
            {icon && <img src = {icon} alt = {text}/>}
            <p style = {{color: color, fontSize: fontSize}}>{text}</p>
        </div>
     );
}
    
export default InfoIconBig;