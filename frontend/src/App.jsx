import React from "react";

import { Routes, Route, Link } from "react-router-dom";
import ButtonGradient from "./assets/svg/ButtonGradient";
import Benefits from "./components/Benefits";
import Collaboration from "./components/Collaboration";
import Footer from "./components/Footer";
import Header from "./components/Header";
import Hero from "./components/Hero";
import Pricing from "./components/Pricing";
import Roadmap from "./components/Roadmap";
import Services from "./components/Services";
import InputPage from "./components/InputPage.jsx";
import OutputPage from "./components/OutputPage.jsx";


const LandingPage = () => <Hero />;

const App = () => {
  return (
    <div>
      <div className="bg-n-8/90 backdrop-blur-sm text-white p-4 `fixed top-0 left-0 w-full z-50 border-b  border-n-6 lg:bg-n-8/90 lg:bg-blur-sm">
        <div className="flex items-center h-[30px] px-5 lg:px-7.5 xl:px-10 max-lg:py-4">
          <Link to="/" className="block w-[12rem] xl:mr-8" href="#hero">
            <p className="text-3xl">RxVision</p>
          </Link>
          <nav className=" text-white p-4">
            <ul className="flex space-x-4">
              <li>
                <Link to="/input" className="hover:text-gray-300">
                  OCR Input
                </Link>
              </li>
            </ul>
          </nav>
        </div>
      </div>

      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/input" element={<InputPage />} />
        <Route path="/output" element={<OutputPage />} />
      </Routes>
    </div>
  );
};

export default App;
