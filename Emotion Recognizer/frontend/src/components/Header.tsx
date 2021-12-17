

import React from "react";

type IHeaderProps={

}

export const Header: React.FC<IHeaderProps> = () => {
return(
    // <div> <h2> Emotion Recognizer </h2> </div>
    <div className="header">
    <a href="#default" className="logo"><h1> Emotion Recognizer </h1> </a> </div>
)
}
