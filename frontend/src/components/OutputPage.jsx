import React, { useEffect, useState } from "react";
import { Gradient } from "./design/Services";
import HyperText from "./hyper-text";

const OutputPage = () => {
  const [text, setText] = useState(null);
  const [annotatedImageFilename, setAnnotatedImageFilename] = useState(null);

  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  useEffect(() => {
    const fetchText = async () => {
      try {
        // const response = await fetch('/static/results/result.txt');
        const response = await fetch(
          "http://localhost:8080/results/result.txt"
        );

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const textContent = await response.text();
        setText(textContent.split("\n")); // Assuming you want to split the text by lines
      } catch (error) {
        console.error("Failed to fetch text file:", error);
      }
    };

    fetchText();
  }, []);
  const handleCopy = () => {
    if (text) {
      navigator.clipboard.writeText(text.join("\n"));
      alert("Text copied to clipboard!");
    }
  };

  const handleDownload = () => {
    if (text) {
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
      {/* <h1 className="text-3xl font-bold mb-6 text-center">OCR Output</h1> */}

      <HyperText
        className="text-4xl font-bold text-black  dark:text-white"
        text="OCR Output"
      />
      <div className=" bg-black border-solid border-purple-700 border-4 shadow-md rounded-lg px-8 pt-6 pb-8 mb-4 ">
        <div className="mb-4">
          <h2 className="text-xl font-semibold mb-2 pb-5">Extracted Text:</h2>
          <div className="bg-black border-solid border-purple-700 border-4 p-4 rounded">
            {text ? (
              <pre className="whitespace-pre-wrap">{text.join("\n")}</pre>
            ) : (
              <p>
                No text available. Please ensure the text file is accessible.
              </p>
            )}
          </div>
        </div>
        {annotatedImageFilename && (
          <div className="mb-4">
            <h2 className="text-xl font-semibold mb-2">Annotated Image:</h2>
            <img
              //src={`/static/results/${annotatedImageFilename}`}
              src={`http://localhost:8080/static/results/annotated_${annotatedImageFilename}`}
              alt="Annotated Image"
              className="max-w-full h-auto"
            />
          </div>
        )}{" "}
        <div className="flex justify-end space-x-4">
          {/* <button
            onClick={handleCopy}
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
            disabled={!text}
          >
            Copy Text
          </button> */}
          <button
            onClick={handleCopy}
            className="p-[3px] relative "
            disabled={!text}
          >
            <div className="absolute inset-0 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-lg" />
            <div className="px-8 py-2  bg-black rounded-[6px]  relative group transition duration-200 text-white hover:bg-transparent">
              Copy Text
            </div>
          </button>
          {/* <button
            onClick={handleDownload}
            className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
            disabled={!text}
          >
            Download Text
          </button> */}
          <button
            onClick={handleDownload}
            className="p-[3px] relative"
            disabled={!text}
          >
            <div className="absolute inset-0 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-lg" />
            <div className="px-8 py-2  bg-black rounded-[6px]  relative group transition duration-200 text-white hover:bg-transparent">
              Download Button
            </div>
          </button>
        </div>
      </div>
      <Gradient />
    </div>
  );
};

export default OutputPage;
