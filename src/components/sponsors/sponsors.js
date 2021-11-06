import * as React from "react";
import "./sponsors.scss";
import {StaticImage} from "gatsby-plugin-image";
import {CloudIcon} from "../icons";

const Sponsors = () => {
    return (
        <div className="sponsors-div" id="sponsors">
            <div className="icon-div">
                <CloudIcon />
            </div>
            <h2>Our Sponsors</h2>
            <p>Manim is proudly sponsored by the following organizations</p>
            <div className="sponsor-flex">
                <div className="sponsor">
                    <a
                        href="https://tutanota.com/"
                        rel="sponsored noreferrer noopener"
                        target="_blank"
                    >
                        <StaticImage
                            src="./tutanota-logo-red-black-font.png"
                            alt="Tutanota Logo"
                            width="300"
                            placeholder="blurred"
                        />
                        <p className="sponsor-title">Tutanota</p>
                        <p className="sponsor-textone">
                            Tutanota is the world's most secure email service,
                            easy to use and private by design.
                        </p>
                    </a>
                </div>
            </div>
        </div>
    );
};
export {Sponsors};
