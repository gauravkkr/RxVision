
import React from "react";
import { useLocation } from "react-router-dom";
import { Gradient } from "./design/Services";
import HyperText from "./hyper-text";


const OutputPage = () => {
  const location = useLocation();
  const text = location.state?.text || [];
  const annotatedImageFilename = location.state?.annotatedImageFilename || null;
  const guessedMedicines = location.state?.guessed_medicines || [];

  // Debug logging
  console.log("[DEBUG OutputPage] Full location.state:", location.state);
  console.log("[DEBUG OutputPage] text:", text);
  console.log("[DEBUG OutputPage] guessedMedicines:", guessedMedicines);

  const handleCopy = () => {
    if (text && text.length > 0) {
      navigator.clipboard.writeText(text.join("\n"));
      alert("Text copied to clipboard!");
    }
  };

  const handleDownload = () => {
    if (text && text.length > 0) {
      const element = document.createElement("a");
      const file = new Blob([text.join("\n")], { type: "text/plain" });
      element.href = URL.createObjectURL(file);
      element.download = "processed_text.txt";
      document.body.appendChild(element);
      element.click();
      document.body.removeChild(element);
    }
  };

  return (
    <div className="container mx-auto mt-10 p-4">
      <HyperText
        className="text-4xl font-bold text-black  dark:text-white"
        text="OCR Output"
      />
      <div className=" bg-black border-solid border-purple-700 border-4 shadow-md rounded-lg px-8 pt-6 pb-8 mb-4 ">
        {/* Guessed Medicines Section - Show match method and medicine name */}
        <div className="mb-4">
          <h2 className="text-2xl font-bold mb-4 text-green-500">Detected Medicine Name(s):</h2>
          <div className="bg-black border-solid border-green-700 border-4 p-6 rounded flex flex-col items-center">
            {guessedMedicines && guessedMedicines.length > 0 ? (
              guessedMedicines.map((item, idx) => (
                <div key={idx} className="text-green-300 text-3xl font-extrabold mb-2">
                  {item.guess} (from: "{item.input}" - {item.method})
                </div>
              ))
            ) : (
              <p className="text-white">No medicine detected. Please check your input.</p>
            )}
          </div>
        </div>
        
        {/* Extracted Text Section for debugging */}
        <div className="mb-4">
          <h2 className="text-2xl font-bold mb-4 text-blue-500">Extracted Text:</h2>
          <div className="bg-black border-solid border-blue-700 border-4 p-6 rounded">
            {text && text.length > 0 ? (
              text.map((line, idx) => (
                <div key={idx} className="text-blue-300 text-lg mb-1">
                  "{line}"
                </div>
              ))
            ) : (
              <p className="text-white">No text extracted.</p>
            )}
          </div>
        </div>
        {annotatedImageFilename && (
          <div className="mb-4">
            <h2 className="text-xl font-semibold mb-2">Annotated Image:</h2>
            <img
              src={`http://localhost:8080/static/results/annotated_${annotatedImageFilename}`}
              alt="Annotated Image"
              className="max-w-full h-auto"
            />
          </div>
        )}
  {/* Removed extracted text copy/download buttons. Only medicine name output and annotated image are shown. */}
      </div>
      <Gradient />
    </div>
  );
};

export default OutputPage;
