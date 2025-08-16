import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Gradient } from "./design/Services";
import { grid } from "../assets";
import { BentoGrid, BentoGridItem } from "./bento-grid";
import { IconClipboardCopy, IconFileBroken } from "@tabler/icons-react";
import { FileUpload } from "./file-upload";
import HyperText from "./hyper-text";

const Skeleton = () => (
  <div className="flex flex-1 w-full h-full min-h-[6rem] rounded-xl dark:bg-dot-white/[0.2] bg-dot-black/[0.2] [mask-image:radial-gradient(ellipse_at_center,white,transparent)] border border-transparent dark:border-white/[0.2] bg-neutral-100 dark:bg-black"></div>
);

const FileUploadComponent = ({ handleFileUpload }) => (
  <div className="rounded-lg">
    <FileUpload onChange={handleFileUpload} accept=".txt, .jpg, .jpeg, .png" />{" "}
    {/* Adjusted to accept image files */}
  </div>
);

const ButtonComponent = ({ disabled }) => (
  <button
    type="submit"
    className={`relative inline-flex h-12 overflow-hidden rounded-full p-[3px] focus:outline-none focus:ring-2 focus:ring-slate-400 focus:ring-offset-2 focus:ring-offset-slate-50 ${
      disabled ? "opacity-50 cursor-not-allowed" : ""
    }`}
    disabled={disabled}
  >
    <span className="absolute inset-[-1000%] animate-[spin_2s_linear_infinite] bg-[conic-gradient(from_90deg_at_50%_50%,#E2CBFF_0%,#393BB2_50%,#E2CBFF_100%)]" />
    <span className="inline-flex h-full w-full items-center justify-center rounded-full bg-slate-950 px-3 py-1 text-sm font-medium text-white backdrop-blur-3xl">
      Process File
    </span>
  </button>
);

const InputPage = () => {
  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);
  const [file, setFile] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const navigate = useNavigate();

  const handleFileUpload = (uploadedFile) => {
    setFile(uploadedFile);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (file) {
      setIsProcessing(true);
      try {
        const formData = new FormData();
        formData.append("file", file);

        const response = await fetch("/api/imageupload", {
          method: "POST",
          body: formData,
        });

        if (!response.ok) {
          throw new Error("File processing failed");
        }

        const result = await response.json();
        navigate("/output", {
          state: {
            text: result.text,
            annotatedImageFilename: result.annotated_image,
          },
        });
      } catch (error) {
        console.error("Error processing file:", error);
        alert("An error occurred while processing the file. Please try again.");
      } finally {
        setIsProcessing(false);
      }
    }
  };

  const items = [
    {
      title: "Upload File",
      description: "Upload an image file (.jpg, .jpeg, .png).",
      className: "md:col-span-3",
      component: <FileUploadComponent handleFileUpload={handleFileUpload} />,
      icon: <IconClipboardCopy className="h-4 w-4 text-neutral-500" />,
    },
    {
      header: <Skeleton />,
      className: "md:col-span-1 ",
    },
    {
      title: "Process File",
      description: "Click to process the uploaded file.",
      className: "md:col-span-1",
      component: <ButtonComponent disabled={!file || isProcessing} />,
      icon: <IconFileBroken className="h-4 w-4 text-neutral-500" />,
    },
    {
      header: <Skeleton />,
      className: "md:col-span-1",
    },
  ];

  return (
    <div className="container mx-auto mt-10 p-4">
      {/* <h1 className="text-3xl font-bold mb-6">Image File Input</h1> */}
      <HyperText
        className="text-4xl font-bold text-black  dark:text-white"
        text="OCR Input"
      />
      <div className="md:flex even:md:translate-y-[7rem] p-0.25 rounded-[2.5rem] bg-conic-gradient">
        <div className="relative w-full p-8 bg-n-8 rounded-[2.4375rem] overflow-hidden xl:p-15">
          <div className="absolute top-0 left-0 max-w-full">
            <img
              className="w-full pointer-events-none select-none"
              src={grid}
              width={550}
              height={550}
              alt="Grid"
            />
          </div>
          <div className="relative z-1">
            <div className="">
              <div className="relative flex h-auto w-auto flex-col items-center justify-center overflow-hidden bg-background md:shadow-xl">
                <form onSubmit={handleSubmit}>
                  <BentoGrid className="max-w-4xl mx-auto md:auto-rows-[20rem]">
                    {items.map((item, i) => (
                      <BentoGridItem
                        key={i}
                        title={item.title}
                        description={item.description}
                        header={item.header}
                        className={item.className}
                        icon={item.icon}
                        component={item.component}
                      />
                    ))}
                  </BentoGrid>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
      <Gradient />
    </div>
  );
};

export default InputPage;
