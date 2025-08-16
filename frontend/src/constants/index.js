import {
  benefitIcon1,
  benefitIcon2,
  benefitIcon3,
  benefitIcon4,
  benefitImage2,
  chromecast,
  disc02,
  discord,
  discordBlack,
  facebook,
  figma,
  file02,
  framer,
  homeSmile,
  instagram,
  notification2,
  notification3,
  notification4,
  notion,
  photoshop,
  plusSquare,
  protopie,
  raindrop,
  recording01,
  recording03,
  roadmap1,
  roadmap2,
  roadmap3,
  roadmap4,
  searchMd,
  slack,
  sliders04,
  telegram,
  twitter,
  yourlogo,
  noun1,
  noun2,
  noun3,
  noun4,
  sabarni,
  arka,
  preety,
  herohiralal,
} from "../assets";
import { links } from "../config";

export const navigation = [
  {
    id: "0",
    title: "team",
    url: "#team",
  },
  {
    id: "1",
    title: "Features",
    url: "#features",
  },
  {
    id: "2",
    title: "Technologies",
    url: "#technology",
  },
  {
    id: "3",
    title: "Demo",
    url: "#how-to-use",
  },

  {
    id: "4",
    title: "Pricing",
    url: "#pricing",
  },

  {
    id: "5",
    title: "Testimonials",
    url: "#roadmap",
  },
  {
    id: "6",
    title: "Let's Ocrify",
    url: "/input",
    onlyMobile: true,
    external: true,
    useReactRouting: true,
  },
];

export const heroIcons = [noun1, noun2, noun3, noun4];

export const notificationImages = [notification4, notification3, notification2];

export const companyLogos = [sabarni, arka, preety, herohiralal];

export const brainwaveServices = [
  "Photo generating",
  "Photo enhance",
  "Seamless Integration",
];

export const brainwaveServicesIcons = [
  recording03,
  recording01,
  disc02,
  chromecast,
  sliders04,
];

export const roadmap = [
  {
    id: "0",
    // title: "Voice recognition",
    // text: "Enable the chatbot to understand and respond to voice commands, making it easier for users to interact with the app hands-free.",
    // date: "May 2023",
    status: "progress",
    imageUrl: roadmap1,
    colorful: true,
  },
  {
    id: "1",
    // title: "Gamification",
    // text: "Add game-like elements, such as badges or leaderboards, to incentivize users to engage with the chatbot more frequently.",
    // date: "May 2023",
    status: "progress",
    imageUrl: roadmap2,
  },
  {
    id: "2",
    // title: "Chatbot customization",
    // text: "Allow users to customize the chatbot's appearance and behavior, making it more engaging and fun to interact with.",
    // date: "May 2023",
    status: "progress",
    imageUrl: roadmap3,
  },
  {
    id: "3",
    // title: "Integration with APIs",
    // text: "Allow the chatbot to access external data sources, such as weather APIs or news APIs, to provide more relevant recommendations.",
    // date: "May 2023",
    status: "progress",
    imageUrl: roadmap4,
  },
];

export const collabText =
  "Topnotch technologies used to give you a seamless experience";

export const collabContent = [
  {
    id: "0",
    title: "ReactJS",
    text: collabText,
  },
  {
    id: "1",
    title: "Flask",
  },
  {
    id: "2",
    title: "AWS",
  },
  {
    id: "3",
    title: "Github",
  },
];

export const collabApps = [
  {
    id: "0",
    title: "Figma",
    icon: figma,
    width: 26,
    height: 36,
  },
  {
    id: "1",
    title: "Notion",
    icon: notion,
    width: 34,
    height: 36,
  },
  {
    id: "2",
    title: "Discord",
    icon: discord,
    width: 36,
    height: 28,
  },
  {
    id: "3",
    title: "Slack",
    icon: slack,
    width: 34,
    height: 35,
  },
  {
    id: "4",
    title: "Photoshop",
    icon: photoshop,
    width: 34,
    height: 34,
  },
  {
    id: "5",
    title: "Protopie",
    icon: protopie,
    width: 34,
    height: 34,
  },
  {
    id: "6",
    title: "Framer",
    icon: framer,
    width: 26,
    height: 34,
  },
  {
    id: "7",
    title: "Raindrop",
    icon: raindrop,
    width: 38,
    height: 32,
  },
];

export const pricing = [
  {
    id: "0",
    title: "Basic",
    description: "Basic ocr services",
    price: "0",
    features: [
      "upload JPG, PNG, and PDF files for text extraction",
      "Support drag-and-drop functionality, as well as file selection from the device",
      "Provide easy options to export extracted text in various formats (plain text, PDF, Word)",
    ],
    premium: false,
  },
  {
    id: "1",
    title: "Premium",
    description: "Advanced features",
    price: "500",
    features: [
      "Ensure secure file uploads and downloads through encryption (SSL/HTTPS)",
      "Enable integration with cloud storage services like Google Drive or Dropbox for direct saving",
      "Priority support to solve issues quickly",
    ],
    premium: true,
  },
  {
    id: "2",
    title: "Enterprise",
    description: "Upcoming",
    price: null,
    features: [
      "Ensure secure file uploads and downloads through encryption (SSL/HTTPS)",
      "Implement auto-deletion of uploaded files after a set period to maintain privacy",
      "Allow users to email the extracted text or download it as a compressed file for multiple documents",
    ],
    premium: false,
  },
];

export const benefits = [
  {
    id: "0",
    title: "Multi-format File Upload",
    text: "Allow users to upload JPG, PNG, and PDF files for text extraction, Support drag-and-drop functionality, as well as file selection from the device.",
    backgroundUrl: "/src/assets/benefits/card-1.svg",
    iconUrl: benefitIcon1,
    imageUrl: benefitImage2,
  },
  {
    id: "1",
    title: "Advanced Text Recognition",
    text: "Utilize cutting-edge OCR algorithms to accurately recognize text from images and PDFs.",
    backgroundUrl: "/src/assets/benefits/card-2.svg",
    iconUrl: benefitIcon2,
    imageUrl: benefitImage2,
    light: true,
  },
  {
    id: "2",
    title: "Real-time Preview of Extracted Text",
    text: "Provide users with a live preview of the extracted text as the OCR process runs, Highlight errors or uncertain characters in the preview for user correction.",
    backgroundUrl: "/src/assets/benefits/card-3.svg",
    iconUrl: benefitIcon3,
    imageUrl: benefitImage2,
  },
  {
    id: "3",
    title: "Editable Output",
    text: "Allow users to edit extracted text before downloading or saving it, provide options to copy the text to clipboard or download it in TXT format.",
    backgroundUrl: "/src/assets/benefits/card-4.svg",
    iconUrl: benefitIcon4,
    imageUrl: benefitImage2,
    light: true,
  },
  {
    id: "4",
    title: "Secure File Handling",
    text: "Ensure secure file uploads and downloads through encryption (SSL/HTTPS), Implement auto-deletion of uploaded files after a set period to maintain privacy.",
    backgroundUrl: "/src/assets/benefits/card-5.svg",
    iconUrl: benefitIcon1,
    imageUrl: benefitImage2,
  },
  {
    id: "5",
    title: "Download and Export Options",
    text: "Provide easy options to export extracted text in various formats (plain text, PDF).",
    backgroundUrl: "/src/assets/benefits/card-6.svg",
    iconUrl: benefitIcon2,
    imageUrl: benefitImage2,
  },
];

export const socials = [
  {
    id: "0",
    title: "Discord",
    iconUrl: discordBlack,
    url: "#",
  },
  {
    id: "1",
    title: "Twitter",
    iconUrl: twitter,
    url: "#",
  },
  {
    id: "2",
    title: "Instagram",
    iconUrl: instagram,
    url: "#",
  },
  {
    id: "3",
    title: "Telegram",
    iconUrl: telegram,
    url: "#",
  },
  {
    id: "4",
    title: "Facebook",
    iconUrl: facebook,
    url: "#",
  },
];
